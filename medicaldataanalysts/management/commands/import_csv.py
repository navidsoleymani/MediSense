"""
🧩 Management Command: import_csv_to_mongo

This custom Django management command is designed to import two CSV files (`long.csv` and `cross.csv`)
into their corresponding MongoDB collections (`long_data` and `cross_data`). The command renames the columns
in the CSV files to match the field names of the MongoDB collections, deletes existing data in the collections,
and inserts the new data.

### Features:
- **CSV Column Renaming**: Automatically renames CSV columns to match the MongoEngine schema field names.
- **Data Deletion**: Clears the previous data in the MongoDB collections before inserting new data.
- **Environment-Specific MongoDB Connection**: Uses MongoDB connection parameters defined in the environment (`.env`) file.
- **Usage**: Callable via the Django command line tool:
    - `python manage.py import_csv --data-dir=./data`
- **Dependencies**: pandas, pymongo, python-dotenv

### Data Handling:
- **CSV Columns Mapping**: The columns in the CSV files are mapped to MongoDB collection field names.
- **Empty Row Removal**: Empty rows are dropped before data insertion into MongoDB.
- **Collection Overwrite**: Each CSV file overwrites the existing data in its corresponding collection.

### Example usage:
    python manage.py import_csv --data-dir=./data

"""

import os
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from django.core.management.base import BaseCommand, CommandError

# Load environment variables from .env file
load_dotenv()

# MongoDB connection parameters from .env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB_NAME", "medisense_db")


def rename_columns(df: pd.DataFrame, collection_name: str) -> pd.DataFrame:
    """
    Rename incoming CSV columns to match MongoEngine model field names.

    Args:
        df (pd.DataFrame): The raw loaded DataFrame from CSV.
        collection_name (str): Either 'long_data' or 'cross_data'.

    Returns:
        pd.DataFrame: DataFrame with renamed columns if applicable.
    """
    if collection_name == 'cross_data':
        return df.rename(columns={
            "ID": "patient_id",
            "M/F": "gender",
            "Educ": "educ",
            "Delay": "delay"
        })
    elif collection_name == 'long_data':
        return df.rename(columns={
            "Subject ID": "subject_id",
            "MRI ID": "mri_id",
            "Group": "group",
            "Visit": "visit",
            "MR Delay": "mr_delay",
            "M/F": "gender",
            "EDUC": "educ"
        })
    return df


def import_csv_to_mongo(csv_path: str, collection_name: str):
    """
    Import a single CSV file into a specified MongoDB collection.

    Steps:
    - Read CSV with pandas
    - Rename columns for MongoEngine compatibility
    - Drop empty rows
    - Replace all existing data in the collection

    Args:
        csv_path (str): Path to the CSV file.
        collection_name (str): MongoDB collection to import into.
    """
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[collection_name]

    # Load CSV into DataFrame
    df = pd.read_csv(csv_path)
    print(f"[INFO] Loaded {csv_path} with {df.shape[0]} rows")

    # Rename columns if needed
    df = rename_columns(df, collection_name)

    # Drop fully empty rows and convert to dict
    records = df.dropna(how="all").to_dict(orient='records')

    # Overwrite the existing MongoDB collection
    collection.delete_many({})
    collection.insert_many(records)

    print(f"[✓] Imported {len(records)} records into '{collection_name}' collection.")


class Command(BaseCommand):
    """
    Django BaseCommand to import medical CSV datasets into MongoDB.

    Example usage:
        python manage.py import_csv --data-dir=./data

    Requirements:
    - The directory must contain `long.csv` and `cross.csv` files
    - Environment variables for MongoDB must be set in .env
    """
    help = "Import long.csv and cross.csv into MongoDB from a given directory."

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            required=True,
            help='Absolute or relative path to the directory containing long.csv and cross.csv'
        )

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        long_csv = os.path.join(data_dir, 'long.csv')
        cross_csv = os.path.join(data_dir, 'cross.csv')

        # Ensure files exist before importing
        if not os.path.exists(long_csv):
            raise CommandError(f"'long.csv' not found in {data_dir}")
        if not os.path.exists(cross_csv):
            raise CommandError(f"'cross.csv' not found in {data_dir}")

        # Import each file into MongoDB
        import_csv_to_mongo(long_csv, 'long_data')
        import_csv_to_mongo(cross_csv, 'cross_data')

        self.stdout.write(self.style.SUCCESS(
            f"✅ Successfully imported data from '{data_dir}' to MongoDB."
        ))
