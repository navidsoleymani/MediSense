"""
🔗 URL Configuration — medicaldataanalysts

This module defines the URL patterns for the medical data analytics app.
It maps the various REST API endpoints for handling tasks related to:
- Training machine learning models
- Returning model evaluation metrics (classification report, predicted probabilities)
- Fetching and saving data from/to MongoDB
- Storing and retrieving model results

Each URL pattern corresponds to a specific API view, which is implemented as a class-based view
using Django REST Framework.

### Endpoints:
1. **Model Training:**
   - Trigger model training on the MongoDB dataset.

2. **Classification Results:**
   - Retrieve the classification report (RFResultView).
   - Fetch predicted class probabilities (YProbView).

3. **Data Access:**
   - Fetch the final dataset used for model training (DataView).

4. **Model Result Persistence:**
   - Save the model results to MongoDB (SaveModelResultView).
   - List all saved model results (ResultListView).
   - Retrieve specific model result by its ID (ResultDetailView).

The views are designed to perform their tasks efficiently, using Django REST Framework's class-based views
and making it easy to extend or modify functionality.

"""

from django.urls import path
from .views import (
    RFResultView,               # View for returning classification report (Random Forest)
    YProbView,                  # View for returning predicted class probabilities
    DataView,                   # View for fetching the final merged dataset used in training
    TrainModelView,             # View for triggering model training on MongoDB data
    SaveModelResultView,        # View for saving trained model results to MongoDB
    ResultListView,             # View for listing all stored model results
    ResultDetailView,           # View for retrieving a specific model result by ID
)

urlpatterns = [
    # 📊 GET: Classification report (Random Forest)
    path("result/rf/", RFResultView.as_view(), name="rf_result"),

    # 📈 GET: Predicted class probabilities
    path("result/y/", YProbView.as_view(), name="y_result"),

    # 📂 GET: Final merged dataset used in training
    path("data/", DataView.as_view(), name="data_view"),

    # 🚀 POST: Trigger model training on MongoDB data
    path("train/", TrainModelView.as_view(), name="train_model"),

    # 💾 POST: Save model result to MongoDB
    path("result/add/", SaveModelResultView.as_view(), name="save_model_result"),

    # 📚 GET: List all saved model results
    path("results/", ResultListView.as_view(), name="result_list"),

    # 🔍 GET: Retrieve a single model result by its ID
    path("results/<str:pk>/", ResultDetailView.as_view(), name="result_detail"),
]
