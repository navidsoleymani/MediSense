"""
🎯 medicaldataanalysts.views

This module defines secured API endpoints (JWT-authenticated) for managing and interacting with
medical data analytics in the app. The views are implemented as class-based views using Django REST Framework
and require authentication via JWT for all requests.

### Available Endpoints:

1. **Classification Report (RFResultView)**
   - 📊 **GET**: /api/v1/medicaldataanalysts/result/rf/
   - Returns the classification report of a trained model (Random Forest or XGBoost).

2. **Predicted Probabilities (YProbView)**
   - 📈 **GET**: /api/v1/medicaldataanalysts/result/y/
   - Returns the predicted class probabilities from the model.

3. **Cleaned Dataset (DataView)**
   - 📂 **GET**: /api/v1/medicaldataanalysts/data/
   - Returns the cleaned and merged dataset used for model training in JSON format.

4. **Model Training (TrainModelView)**
   - 🚀 **POST**: /api/v1/medicaldataanalysts/train/
   - Triggers model training on the current MongoDB dataset and returns the model evaluation results.

5. **Save Model Result (SaveModelResultView)**
   - 💾 **POST**: /api/v1/medicaldataanalysts/result/add/
   - Trains the model and persists the results (classification report, predicted probabilities, and class labels) in the `model_results` MongoDB collection.

6. **Model Results Listing (ResultListView)**
   - 📜 **GET**: /api/v1/medicaldataanalysts/results/
   - Returns a list of all stored model results, with metadata summary (e.g., accuracy, creation time, and class labels).

7. **Model Result Detail (ResultDetailView)**
   - 🔍 **GET**: /api/v1/medicaldataanalysts/results/<str:pk>/
   - Retrieves detailed information about a specific model result by its ID.

### Permissions:
- All views require the user to be authenticated via JWT.
- The permission class used for all views is `IsAuthenticated`.

"""

import numpy as np
import pandas as pd

from mongoengine.errors import DoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from medicaldataanalysts.documents import LongData, ModelResult
from medicaldataanalysts.services import preprocess_and_train


class RFResultView(APIView):
    """
    📊 **GET** /api/v1/medicaldataanalysts/result/rf/
    Returns the classification report (Random Forest or XGBoost) from the trained model.

    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = preprocess_and_train()
        return Response(result["rf_result"], status=status.HTTP_200_OK)


class YProbView(APIView):
    """
    📈 **GET** /api/v1/medicaldataanalysts/result/y/
    Returns the predicted class probabilities from the trained model.

    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = preprocess_and_train()
        return Response({"y_prob": result["y_prob"]}, status=status.HTTP_200_OK)


class DataView(APIView):
    """
    📂 **GET** /api/v1/medicaldataanalysts/data/
    Returns the cleaned and merged dataset used for model training as JSON.

    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        df = pd.DataFrame(LongData.objects().as_pymongo())
        df.drop(columns=["_id"], inplace=True, errors="ignore")

        # Convert NaN and infinities to None for JSON serialization
        df = df.replace({np.nan: None, np.inf: None, -np.inf: None})

        data = df.to_dict(orient="records")
        return Response(data, status=status.HTTP_200_OK)


class TrainModelView(APIView):
    """
    🚀 **POST** /api/v1/medicaldataanalysts/train/
    Triggers model training on the current MongoDB dataset and returns results.

    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            result = preprocess_and_train()
            return Response({
                "rf_result": result["rf_result"],
                "y_prob": result["y_prob"],
                "classes": result["classes"]
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaveModelResultView(APIView):
    """
    💾 **POST** /api/v1/medicaldataanalysts/result/add/
    Trains the model and persists the results in MongoDB (model_results collection).

    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            result = preprocess_and_train()

            model_result = ModelResult(
                rf_result=result["rf_result"],
                y_prob=result["y_prob"],
                classes=result["classes"]
            )
            model_result.save()

            return Response({"message": "Model result saved successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResultListView(APIView):
    """
    📜 **GET** /api/v1/medicaldataanalysts/results/
    Returns a list of all stored model results with metadata summary, such as accuracy and creation time.

    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        results = ModelResult.objects.order_by('-created_at')
        output = []

        for r in results:
            output.append({
                "id": str(r.id),
                "created_at": r.created_at.isoformat(),
                "accuracy": round(r.accuracy, 3),
                "classes": r.classes,
            })

        return Response(output, status=status.HTTP_200_OK)


class ResultDetailView(APIView):
    """
    🔍 **GET** /api/v1/medicaldataanalysts/results/<str:pk>/
    Returns detailed information of a specific saved model result by ID.

    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            result = ModelResult.objects.get(id=pk)

            return Response({
                "id": str(result.id),
                "created_at": result.created_at.isoformat(),
                "rf_result": result.rf_result,
                "y_prob": result.y_prob,
                "classes": result.classes
            }, status=status.HTTP_200_OK)

        except DoesNotExist:
            return Response({"error": "Result not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
