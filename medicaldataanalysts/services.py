"""
🧠 Model Training Service — MediSense

This module is responsible for loading, preprocessing, and training a machine learning model
on longitudinal medical records from MongoDB. The process involves the following steps:
- Loading data from MongoDB's 'long_data' collection
- Data cleaning and preprocessing (handling missing values, encoding features)
- Splitting the dataset into training and validation sets
- Training an XGBoost classifier using sklearn's pipeline
- Generating and returning model evaluation metrics and predicted probabilities

The core functions in this module are designed to be reusable for different views or CLI commands.

### Features:
- **Data Loading**: Efficiently loads longitudinal medical data stored in MongoDB into a pandas DataFrame.
- **Preprocessing**: Handles missing data, scales numerical features, and applies one-hot encoding for categorical features.
- **Model Training**: Trains an XGBoost model for classification and outputs evaluation metrics.
- **Output**: Provides classification reports and predicted probabilities for further analysis.

"""

import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

from medicaldataanalysts.documents import LongData


def load_longdata_as_dataframe() -> pd.DataFrame:
    """
    Loads longitudinal medical data from the MongoDB 'long_data' collection into a Pandas DataFrame.

    This function queries the MongoDB collection, converts the data to a pandas DataFrame,
    and cleans up the DataFrame by removing MongoDB's internal '_id' field.

    Returns:
        pd.DataFrame: Cleaned dataframe without the '_id' field from MongoDB
    """
    df = pd.DataFrame(LongData.objects().as_pymongo())
    df.drop(columns=["_id"], inplace=True, errors="ignore")
    return df


def preprocess_and_train() -> dict:
    """
    Full pipeline for preprocessing and training an XGBoost classifier on the longitudinal dataset.

    Steps:
    1. Load and clean the data
    2. Handle missing values by filling with the mode of each column
    3. Split the data into features and target variables
    4. Perform feature scaling and one-hot encoding
    5. Train an XGBoost classifier using sklearn's Pipeline
    6. Evaluate the model and return performance metrics

    Returns:
        dict: {
            'rf_result': classification report (dict),
            'y_prob': list of predicted probabilities,
            'classes': list of original class labels
        }

    Raises:
        ValueError: if the required 'group' column is missing in the dataset
    """
    data = load_longdata_as_dataframe()

    # Ensure that the 'group' column exists for model training
    if "group" not in data.columns:
        raise ValueError("❌ The required 'group' column is missing from the dataset.")

    # Clean the data by dropping empty rows and filling missing values with the mode
    data.dropna(how="all", inplace=True)
    for col in data.columns:
        if data[col].isnull().any():
            mode = data[col].mode()
            if not mode.empty:
                data[col] = data[col].fillna(mode[0])

    # Separate the target variable and features
    y = data["group"]
    X = data.drop(columns=["group", "subject_id", "mri_id"], errors="ignore")

    # Define columns for scaling and one-hot encoding
    scale_cols = ['age', 'educ', 'ses', 'mmse', 'cdr', 'etiv', 'nwbv', 'asf']
    ohe_cols = ['gender', 'hand']

    # Ensure only the existing columns are selected for preprocessing
    scale_cols = [col for col in scale_cols if col in X.columns]
    ohe_cols = [col for col in ohe_cols if col in X.columns]

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Define preprocessing steps: scaling for numerical columns, encoding for categorical columns
    preprocessor = ColumnTransformer([
        ('scale', StandardScaler(), scale_cols),
        ('ohe', OneHotEncoder(), ohe_cols)
    ])

    # Encode the target labels (group column)
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_val_encoded = label_encoder.transform(y_val)

    # Create a pipeline that combines preprocessing and the XGBoost classifier
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', XGBClassifier(n_jobs=-1, random_state=42))
    ])

    # Train the model on the training data
    pipeline.fit(X_train, y_train_encoded)

    # Predict on the validation data and calculate predicted probabilities
    y_pred = pipeline.predict(X_val)
    y_prob = pipeline.predict_proba(X_val)

    # Generate a classification report (performance metrics)
    report = classification_report(y_val_encoded, y_pred, output_dict=True)

    # Return the classification report, predicted probabilities, and class labels
    return {
        "rf_result": report,
        "y_prob": y_prob.tolist(),
        "classes": label_encoder.classes_.tolist()
    }
