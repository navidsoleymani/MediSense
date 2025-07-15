# Import required libraries
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, auc
from xgboost import XGBClassifier

# Set the path to the CSV file
main_path = os.path.join(os.getcwd(), "your_csv_file_path")

# Load cross-sectional data
data_cross = pd.read_csv(os.path.join(main_path,'cross.csv'))

# Load longitudinal data
data_long = pd.read_csv(os.path.join(main_path,'long.csv'))

# Merge the two dataframes into a single dataframe
data = pd.concat([data_cross, data_long])

# Display the first few rows of the data
data.head()

# Fill missing values (NaN) in each column with the mode of that column
for column in data.columns:
    mode_value = data[column].mode()[0]
    data[column].fillna(mode_value, inplace=True)

# Check for missing values after filling
missing_values_after_filling = data.isnull().sum()

# Remove unnecessary columns from the data and define features (X) and labels (y)
X = data.drop(['Group', 'ID', 'Delay', 'Subject ID', 'MRI ID', 'Visit', 'MR Delay'], axis=1)
y = data['Group']

# Define columns that require standardization and one-hot encoding
scale = ['Age', 'EDUC', 'SES', 'MMSE', 'CDR', 'eTIV','nWBV', 'ASF']
ohe = ['M/F', 'Hand']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the preprocessor to apply transformations to the columns
preprocessor = ColumnTransformer(
    transformers=[
        ('scale', StandardScaler(), scale),  # Standardize numerical features
        ('ohe', OneHotEncoder(), ohe)        # Convert categorical features to one-hot
    ])

# Define a pipeline consisting of the preprocessor and a RandomForest classifier
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
])

# Encode the target variable (for use in models)
label = LabelEncoder()
y_train_label = label.fit_transform(y_train)
y_test_label = label.transform(y_val)

# Train the RandomForest model
pipeline.fit(X_train, y_train_label)

# Evaluate the model's accuracy on the validation data
accuracy = pipeline.score(X_val, y_test_label)

# Redefine the pipeline using XGBoost instead of RandomForest
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(random_state=42, n_jobs=-1))
])

# Train the XGBoost model
pipeline.fit(X_train, y_train_label)

# Calculate the accuracy of the XGBoost model
accuracy = pipeline.score(X_val, y_test_label)

# Generate a classification report for the XGBoost model
rf_rsult = classification_report(y_test_label, pipeline.predict(X_val))

# Predict classification probabilities for the validation data
y_prob = pipeline.predict_proba(X_val)