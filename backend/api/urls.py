from django.urls import path
from .views import get_today_ticker,submit_prediction,get_user_profile,get_prev_prediction,get_all_profiles
from . import views

urlpatterns = [
    path("ticker/", get_today_ticker),
    path("predict/", submit_prediction),
    path("profile/", get_user_profile),
    path("profiles/", get_all_profiles),
    path("prev-prediction/", get_prev_prediction)
]