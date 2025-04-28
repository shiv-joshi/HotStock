import random
from datetime import date, timedelta
from .models import DailyTicker, DailyPrediction, UserProfile, PreviousPrediction
import yfinance as yf
import pandas as pd
from django.contrib.auth.models import User
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    df = tables[0]
    tickers = df['Symbol'].tolist()
    # Fix symbols with "." (e.g., BRK.B → BRK-B for yfinance)
    tickers = [ticker.replace('.', '-') for ticker in tickers]
    return tickers

# Tickers to choose random stock from
TICKERS = get_sp500_tickers()


def select_daily_ticker():
    today = date.today()
    dt = DailyTicker.objects.first()
    
    if dt:
        # move today's ticker to prev_symbol field
        dt.prev_symbol = dt.symbol
        dt.symbol = random.choice(TICKERS)
        print(dt.symbol)
        dt.save()
    else:
        # pick and create a new Daily Ticker object
        symbol = random.choice(TICKERS)
        DailyTicker.objects.create(date=today, symbol=symbol)
    
    # change every user's profile "predicted" to false
    all_users = User.objects.all()
    for user in all_users:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.predicted = False
        user_profile.save()
    

# calculate user's score based on previous ticker, and show what their guess was 
def calculate_scores():
    # Get all the predictions for this ticker
    symbol = DailyTicker.objects.first().prev_symbol
    predictions = DailyPrediction.objects.filter(symbol=symbol)

    # Check correctness
    for prediction in predictions:
        try:
            # get user and their profile
            user = prediction.user
            user_profile = UserProfile.objects.get(user=user)
            prev_prediction = PreviousPrediction.objects.get(user=user)

            # Get stock data
            stock = yf.Ticker(symbol)
            historical_data = stock.history(period="1d")
            open_price = historical_data["Open"].iloc[0]
            close_price = historical_data["Close"].iloc[0]

            # Determine if the stock went up or down AND if they predicted right
            went_up = close_price > open_price
            user_predicted_rise = prediction.prediction.upper() == "RISE"

            # If the prediction is correct, increase the score
            correct = (went_up == user_predicted_rise)
            if correct:
                user_profile.score += 1
                user_profile.save()

            # update last prediction of user
            print(f"checking for {symbol} it was {correct}")
            prev_prediction.ticker = symbol
            prev_prediction.correct = correct
            prev_prediction.save()
        except Exception as e:
            print(f"Error processing prediction for {symbol}: {e}")


    # After processing all predictions for this ticker, delete them
    DailyPrediction.objects.filter(symbol=symbol).delete()

# apscheduler
def start_scheduler():
    scheduler = BackgroundScheduler()

    # get daily ticker at 9am
    # scheduler.add_job(select_daily_ticker, 'interval', minutes=1) 
    scheduler.add_job(select_daily_ticker, trigger='cron', hour=9)
    
    # check user predictions at 4pm for previous ticker
    # scheduler.add_job(calculate_scores, 'interval', minutes=1) 
    scheduler.add_job(calculate_scores, trigger='cron', hour=16)
    scheduler.start()

    print("Scheduler started and job scheduled.")