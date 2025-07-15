"""
🧪 Unit Tests — preprocess_and_train()

This test suite verifies the end-to-end logic of the
`preprocess_and_train` function which performs:

- Data loading from MongoDB (mocked)
- Preprocessing steps
- Model training (XGBoost)
- Evaluation report generation
- Class probability prediction

All tests use synthetic pandas DataFrames (no database dependency).
"""

import pytest
import pandas as pd
from unittest.mock import patch

from medicaldataanalysts.services import preprocess_and_train


@pytest.fixture
def mock_longdata():
    """
    Provides a sample longitudinal dataset with multiple class labels
    to ensure train_test_split and classification can proceed.
    """
    return pd.DataFrame({
        "subject_id": ["id1", "id2", "id3", "id4", "id5"],
        "mri_id": ["mr1", "mr2", "mr3", "mr4", "mr5"],
        "group": ["Nondemented", "Demented", "Converted", "Nondemented", "Demented"],
        "age": [88, 74, 65, 80, 79],
        "educ": [14, 16, 12, 10, 13],
        "ses": [2, 3, 2, 1, 3],
        "mmse": [30, 29, 26, 28, 27],
        "cdr": [0, 1, 0.5, 0, 0.5],
        "etiv": [2004, 1500, 1800, 1600, 1700],
        "nwbv": [0.681, 0.700, 0.695, 0.688, 0.689],
        "asf": [0.876, 0.900, 0.870, 0.880, 0.879],
        "gender": ["M", "F", "F", "M", "F"],
        "hand": ["R", "L", "R", "R", "L"]
    })


@patch("medicaldataanalysts.services.load_longdata_as_dataframe")
def test_preprocess_and_train(mock_loader, mock_longdata):
    """
    ✅ End-to-end test for:
    - Validating output format of preprocess_and_train()
    - Ensuring model returns classification report, y_prob, and classes
    """
    mock_loader.return_value = mock_longdata

    result = preprocess_and_train()

    # Classification report structure
    assert "rf_result" in result, "Missing 'rf_result' in output"
    assert "accuracy" in result["rf_result"], "'accuracy' not present in report"

    # Predicted probabilities
    assert isinstance(result["y_prob"], list), "y_prob must be a list"
    assert all(isinstance(row, list) for row in result["y_prob"]), "Each y_prob entry must be a list"

    # Class label encoding
    assert isinstance(result["classes"], list), "classes must be a list"
    assert sorted(result["classes"]) == ["Converted", "Demented", "Nondemented"], "Unexpected classes returned"
