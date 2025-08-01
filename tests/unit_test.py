import pytest
import pandas as pd
from training_pipeline.prefect_training_pipeline import load_data


def validate_data_columns(df):
    """Utility function to validate required columns exist"""
    required_columns = [
        "N",
        "P",
        "K",
        "temperature",
        "humidity",
        "ph",
        "rainfall",
        "label",
    ]
    return all(col in df.columns for col in required_columns)


def calculate_feature_stats(df):
    """Calculate basic statistics for numerical features"""
    numerical_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    return df[numerical_cols].describe()


class TestUtils:

    @pytest.fixture
    def sample_data(self):
        """Load data for testing"""
        data = pd.read_csv("../data/Crop_recommendation.csv")
        return data

    def test_validate_data_columns(self, sample_data):
        """Test column validation function"""
        assert validate_data_columns(sample_data) == True

        # Test with missing column
        incomplete_data = sample_data.drop("label", axis=1)
        assert validate_data_columns(incomplete_data) == False

    def test_calculate_feature_stats(self, sample_data):
        """Test feature statistics calculation"""
        stats = calculate_feature_stats(sample_data)

        assert stats.shape[0] == 8  # count, mean, std, min, 25%, 50%, 75%, max
        assert stats.shape[1] == 7  # 7 numerical columns
        assert "N" in stats.columns

    def test_no_missing_values(self, sample_data):
        """Test that dataset has no missing values."""
        
        assert not sample_data.isnull().any().any()
        assert sample_data.shape[0] > 0
        assert sample_data.shape[1] == 8


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
