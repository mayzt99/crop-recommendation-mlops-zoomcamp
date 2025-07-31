import pandas as pd
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, accuracy_score
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
import pickle
import os
from datetime import datetime
from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner


@task(name="Load Data", retries=2, retry_delay_seconds=60)
def load_data():
    """Load the crop recommendation dataset."""
    df = pd.read_csv("data/Crop_recommendation.csv")
    return df


@task(name="Prepare Dataset")
def prepare_dataset(df):
    """Prepare the dataset for model training."""
    X = df.drop("label", axis=1)
    y = df["label"]

    df_train, df_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    train_dicts = df_train.to_dict(orient="records")
    test_dicts = df_test.to_dict(orient="records")

    dv = DictVectorizer(sparse=False)
    X_train = dv.fit_transform(train_dicts)
    X_test = dv.transform(test_dicts)

    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)

    with open("models/dv.pkl", "wb") as f:
        pickle.dump(dv, f)

    return X_train, X_test, y_train, y_test


@task(name="Train Model")
def train_model(X_train, X_test, y_train, y_test, num_trials=10):
    """Train a Random Forest model with hyperparameter optimization and MLflow tracking."""

    def objective(params):
        with mlflow.start_run(nested=True):
            # Log parameters
            mlflow.log_param("n_estimators", int(params["n_estimators"]))
            mlflow.log_param("max_depth", int(params["max_depth"]))
            mlflow.log_param("min_samples_split", params["min_samples_split"])
            mlflow.log_param("min_samples_leaf", int(params["min_samples_leaf"]))
            mlflow.log_param("random_state", 42)

            # Train model
            model = RandomForestClassifier(
                n_estimators=int(params["n_estimators"]),
                max_depth=int(params["max_depth"]),
                min_samples_split=params["min_samples_split"],
                min_samples_leaf=int(params["min_samples_leaf"]),
                random_state=42,
            )
            model.fit(X_train, y_train)

            # Make predictions and calculate metrics
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average="macro")
            recall = recall_score(y_test, y_pred, average="macro")

            # Log metrics
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)

            # Log model
            mlflow.sklearn.log_model(model, "model")

            return {"loss": -accuracy, "status": STATUS_OK, "model": model}

    search_space = {
        "n_estimators": hp.randint("n_estimators", 50, 100),
        "max_depth": hp.randint("max_depth", 5, 10),
        "min_samples_split": hp.uniform("min_samples_split", 0.1, 0.5),
        "min_samples_leaf": hp.randint("min_samples_leaf", 1, 10),
    }

    best_params = fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        trials=Trials(),
        max_evals=num_trials,
    )

    return best_params


@task(name="Register Best Model")
def register_best_model():
    """Register the best performing model in MLflow Model Registry"""

    client = MlflowClient()
    experiment = client.get_experiment_by_name("crop-recommendation")
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["metrics.accuracy DESC"],
        max_results=1,
    )

    if runs:
        best_run = runs[0]
        model_uri = f"runs:/{best_run.info.run_id}/model"

        # Create models directory if it doesn't exist
        os.makedirs("models", exist_ok=True)

        # Download the model from MLflow and save it locally
        model = mlflow.sklearn.load_model(model_uri)
        with open("models/random_forest_model.pkl", "wb") as model_file:
            pickle.dump(model, model_file)

        try:
            client.create_registered_model("crop-recommendation-model")
        except:
            pass

        model_version = client.create_model_version(
            name="crop-recommendation-model",
            source=model_uri,
            run_id=best_run.info.run_id,
        )

        accuracy = best_run.data.metrics["accuracy"]
        return f"Model registered with accuracy: {accuracy:.4f}, version: {model_version.version}"

    return "No runs found"


@flow(name="Crop Recommendation Training Pipeline", task_runner=SequentialTaskRunner())
def training_pipeline(num_trials=10):
    """Main training pipeline flow"""

    # Set up MLflow tracking
    mlflow.set_tracking_uri("http://localhost:5000")

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_name = "crop-recommendation"

    with mlflow.start_run(run_name=f"prefect_pipeline_{run_id}") as run:
        mlflow.set_experiment(experiment_name)

        # Log pipeline parameters
        mlflow.log_param("num_trials", num_trials)
        mlflow.log_param("pipeline_type", "prefect")

        # Execute pipeline tasks
        df = load_data()
        X_train, X_test, y_train, y_test = prepare_dataset(df)
        best_params = train_model(X_train, X_test, y_train, y_test, num_trials)

        # Log best parameters from hyperparameter optimization
        for param_name, param_value in best_params.items():
            mlflow.log_param(f"best_{param_name}", param_value)

        # Register the best model
        registration_result = register_best_model()

        return {
            "status": "success",
            "best_params": best_params,
            "registration_result": registration_result,
        }


if __name__ == "__main__":
    # Run the Prefect flow and capture the return value
    result = training_pipeline()

    # Print the results in a formatted way
    print("\n" + "=" * 50)
    print("PIPELINE EXECUTION RESULTS")
    print("=" * 50)
    print(f"Status: {result['status']}")
    print("\nBest Parameters:")
    for param, value in result["best_params"].items():
        print(f"  {param}: {value}")
    print(f"\nModel Registration: {result['registration_result']}")
    print("=" * 50)
