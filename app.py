from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# Replace with your Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = 'your_alpha_vantage_api_key'

def get_stock_price(symbol):
    """Fetch real-time stock price using Alpha Vantage API."""
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'Global Quote' in data:
        return data['Global Quote']['05. price']
    return None

def get_financial_news():
    """Fetch financial news using Alpha Vantage API."""
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={ALPHA_VANTAGE_API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'feed' in data:
        return data['feed'][:5]  # Return top 5 news articles
    return None

@app.route('/')
def index():
    """Render the dashboard."""
    return render_template('index.html')

@socketio.on('request_update')
def handle_update_request():
    """Handle real-time updates for stock prices and news."""
    stock_symbols = ['AAPL', 'GOOGL', 'MSFT']  # Example stock symbols
    stock_prices = {symbol: get_stock_price(symbol) for symbol in stock_symbols}
    news = get_financial_news()
    socketio.emit('update_data', {'stock_prices': stock_prices, 'news': news})

if __name__ == '__main__':
    socketio.run(app, debug=True)
