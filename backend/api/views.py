from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer,UserProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import DailyTicker, DailyPrediction, UserProfile, PreviousPrediction
from .utils import select_daily_ticker
from datetime import date

# view for creating a new user
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # create a new user profile for every user
    def perform_create(self, serializer):
        user = serializer.save()
        # Create the user profile with score = 0
        UserProfile.objects.create(user=user)
        # Create a previous prediction with no ticker
        PreviousPrediction.objects.create(user=user)

# get today's ticker
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_today_ticker(request):
    ticker = DailyTicker.objects.first()
    return Response({"symbol": ticker.symbol}) if ticker else Response({"symbol": "Fetching you a stock..."})

# submit a preditction
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_prediction(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    prediction = request.data.get("prediction")
    symbol = DailyTicker.objects.first().symbol

    # check if user already predicted
    if user_profile.predicted:
        return Response({"error": "You already predicted today!"}, status=400)
    
    # create a prediction
    DailyPrediction.objects.create(user=user, symbol=symbol, prediction=prediction)

    # update the user's profile to mark "predicted" as True
    user_profile.predicted = True
    user_profile.save() 
    return Response({"message": "Prediction submitted!"})

# get the user profile
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    return Response({
        "username": profile.user.username,
        "score": profile.score,
        "predicted": profile.predicted
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_profiles(request):
    profiles = UserProfile.objects.all()
    serializer = UserProfileSerializer(profiles, many=True)
    return Response(serializer.data)

# get the user's last prediction
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_prev_prediction(request):
    user = request.user
    prev_prediction = PreviousPrediction.objects.get(user=user)
    print(prev_prediction.user, prev_prediction.ticker, prev_prediction.correct)
    print(prev_prediction)
    return Response({
        "last": prev_prediction.__str__()
    })