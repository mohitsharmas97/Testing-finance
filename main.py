from BasicBot import BasicBot
import os
import logging
from dotenv import load_dotenv

# Re-configure logging for the main script as well
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("bot.log"),
                              logging.StreamHandler()])

def get_user_input():
    """
    Prompts the user for order details and validates input.
    """
    symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
    side = input("Enter order side (BUY or SELL): ").upper()
    order_type = input("Enter order type (MARKET or LIMIT): ").upper()
    
    while True:
        try:
            quantity = float(input("Enter quantity: "))
            if quantity <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid quantity. Please enter a positive number.")

    price = None
    if order_type == 'LIMIT':
        while True:
            try:
                price = float(input("Enter price: "))
                if price <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Invalid price. Please enter a positive number.")

    return symbol, side, order_type, quantity, price

if __name__ == '__main__':
    load_dotenv()
    # It is a best practice to store API keys as environment variables
    api_key = os.environ.get('BINANCE_API_KEY')
    api_secret = os.environ.get('BINANCE_API_SECRET')

    if not api_key or not api_secret:
        print("API keys not found. Please set them as environment variables.")
    else:
        bot = BasicBot(api_key=api_key, api_secret=api_secret)

        print("Welcome to the Simplified Trading Bot!")
        while True:
            symbol, side, order_type, quantity, price = get_user_input()
            bot.place_order(symbol, side, order_type, quantity, price)

            another_order = input("\nPlace another order? (yes/no): ").lower()
            if another_order != 'yes':
                break
        
        logging.info("Bot session ended.")