"""
🧬 MongoEngine Document Models — MediSense

This module defines MongoDB collections using MongoEngine documents
for storing medical data and machine learning model outputs.

Collections defined in this module:
- LongData:     Longitudinal patient data (multiple visits per subject)
- CrossData:    Cross-sectional patient data (single snapshot per patient)
- ModelResult:  Machine learning model output (e.g. classification metrics and probabilities)

### Collections:

1. **LongData**:
   - Stores longitudinal medical records of patients, containing data from multiple visits.
   - Used to track disease progression over time, with features such as:
     - MRI session data (mri_id)
     - Group (e.g., Nondemented, Demented)
     - Socioeconomic status, mental health scores, brain volume metrics, etc.

2. **CrossData**:
   - Stores cross-sectional data of patients, containing a snapshot from a single point in time.
   - Suitable for models that don't require time-series data, including:
     - Patient demographics (e.g., age, gender, handedness)
     - Clinical metrics (e.g., MMSE, CDR, etiv, nwbv)

3. **ModelResult**:
   - Stores the output of machine learning models (e.g., RandomForest, XGBoost).
   - Contains classification metrics, predicted class probabilities, and model execution timestamp.

### Usage:

These models are designed for easy integration with MongoEngine to store, query, and process medical data for disease progression analysis and machine learning model evaluation.

"""

from datetime import datetime
import mongoengine as documents


class LongData(documents.Document):
    """
    📘 Longitudinal Data Document

    Represents medical records of a patient over time (multiple MRI visits).
    The data is used to analyze disease progression across different sessions.

    Fields:
        - subject_id (str): Unique identifier for the subject.
        - mri_id (str): MRI session identifier.
        - group (str): Diagnostic group (e.g., Nondemented, Demented).
        - visit (int): Visit number.
        - mr_delay (int): Delay in days since the baseline MRI.
        - gender (str): Gender of the patient (M/F).
        - hand (str): Handedness (R/L).
        - age (float): Age of the patient in years.
        - educ (int): Years of education.
        - ses (float): Socioeconomic status.
        - mmse (float): Mini-Mental State Examination score.
        - cdr (float): Clinical Dementia Rating score.
        - etiv (float): Estimated Total Intracranial Volume.
        - nwbv (float): Normalized Whole Brain Volume.
        - asf (float): Atlas Scaling Factor.
    """
    subject_id = documents.StringField(required=True)
    mri_id = documents.StringField()
    group = documents.StringField()
    visit = documents.IntField()
    mr_delay = documents.IntField()
    gender = documents.StringField()
    hand = documents.StringField(db_field="Hand")
    age = documents.FloatField(db_field="Age")
    educ = documents.IntField()
    ses = documents.FloatField(db_field="SES")
    mmse = documents.FloatField(db_field="MMSE")
    cdr = documents.FloatField(db_field="CDR")
    etiv = documents.FloatField(db_field="eTIV")
    nwbv = documents.FloatField(db_field="nWBV")
    asf = documents.FloatField(db_field="ASF")

    meta = {'collection': 'long_data'}


class CrossData(documents.Document):
    """
    📗 Cross-Sectional Data Document

    Represents a single snapshot of patient medical data.
    Useful for classification models that don’t rely on time-series data.

    Fields:
        - patient_id (str): Unique identifier for the patient.
        - gender (str): Gender of the patient.
        - hand (str): Handedness (R/L).
        - age (float): Age in years.
        - educ (int): Years of education.
        - ses (float): Socioeconomic status.
        - mmse (float): Mini-Mental State Examination score.
        - cdr (float): Clinical Dementia Rating score.
        - etiv (float): Estimated Total Intracranial Volume.
        - nwbv (float): Normalized Whole Brain Volume.
        - asf (float): Atlas Scaling Factor.
        - delay (float): MRI delay from baseline (can contain NaN values).
    """
    patient_id = documents.StringField(required=True)
    gender = documents.StringField()
    hand = documents.StringField(db_field="Hand")
    age = documents.FloatField(db_field="Age")
    educ = documents.IntField()
    ses = documents.FloatField(db_field="SES")
    mmse = documents.FloatField(db_field="MMSE")
    cdr = documents.FloatField(db_field="CDR")
    etiv = documents.FloatField(db_field="eTIV")
    nwbv = documents.FloatField(db_field="nWBV")
    asf = documents.FloatField(db_field="ASF")
    delay = documents.FloatField()  # Contains missing values (NaN)

    meta = {'collection': 'cross_data'}


class ModelResult(documents.Document):
    """
    📊 Machine Learning Result Document

    Stores output from trained models (e.g., RandomForest, XGBoost), including:
    - Classification metrics (e.g., precision, recall, F1-score)
    - Predicted class probabilities for each sample

    Fields:
        - rf_result (dict): Classification report containing metrics (precision, recall, F1-score).
        - y_prob (list): List of predicted class probabilities.
        - classes (list): List of original class labels.
        - created_at (datetime): Timestamp of when the model was run.

    Property:
        - accuracy: Returns the accuracy score from the classification report or falls back to the weighted F1-score if accuracy is missing.
    """
    rf_result = documents.DictField()
    y_prob = documents.ListField()
    classes = documents.ListField()
    created_at = documents.DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'model_results'}

    @property
    def accuracy(self):
        """
        Returns the overall accuracy from the classification report,
        falling back to the weighted F1-score if the accuracy key is missing.
        """
        return self.rf_result.get("accuracy") or self.rf_result.get("weighted avg", {}).get("f1-score", 0)
