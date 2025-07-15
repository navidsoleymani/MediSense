# Task Name:

Development and Implementation of a Medical Data Analysis System using MongoDB, JWT, and Django.

## Task Description:

You need to develop a web-based system that reads, stores, processes, and provides medical data through APIs. The
project steps are as follows:

### Step 1: Reading and Storing Data in MongoDB

- Read two attached CSV files named `long.csv` and `cross.csv`.
- Import each CSV file as a separate Collection in MongoDB.

### Step 2: Merging Data in Django ORM Layer

- Create two Django models with appropriate structures for `long` and `cross` data.
- Use Django ORM to retrieve both tables and merge them into a comprehensive dataframe named `data`.

### Step 3: Data Analysis

- Implement the code provided in the attached Python file (.py) using an appropriate Design Pattern, including:
    - Data cleaning (removing missing values).
    - Data preprocessing and training machine learning models with Scikit-learn.
- Calculate the following outputs:
    - Model classification report (`rf_result`).
    - Model classification probability (`y_prob`).

### Step 4: Developing Async APIs with DRF

- Create three APIs to retrieve outputs:
    - Display model classification report: `GET /api/rf_result/`.
    - Display model classification probability: `GET /api/y_result/`.
    - Display final dataframe of data: `GET /api/data/`.
- Implement these APIs as `async def` (if possible using asgiref or FastAPI-style views).

### Step 5: JWT Authentication

- Create a special Admin User for JWT authentication without modifying Django Admin.
- Implement JWT-based authentication system using SimpleJWT:
    - Token obtain: `POST /api/token/`.
    - Token refresh: `POST /api/token/refresh/`.
- Protect all Step 4 APIs so that only authenticated users can access them.

### Step 6: Documentation and Additional APIs

- Document all APIs in Postman Collection format and place the JSON file in the project's `/docs` folder.
- Create an additional POST API to store results (`rf_result`, `y_result`, `data`) in MongoDB as JSON.

## Expected Technologies:

- Django REST Framework
- MongoDB
- JWT Authentication
- Scikit-learn, XGBoost
- Pandas, Numpy
- (Optional) Async DRF views
- Postman
- Follow Clean Coding principles

## Additional Notes:

- The prepared files must be placed in Git and the link should be submitted.
- Use of AI Assistant (e.g., Grok, ChatGPT, etc.) is mandatory. Screenshots of permissions must be included in the
  project.
- For any questions, contact the relevant team via email.
