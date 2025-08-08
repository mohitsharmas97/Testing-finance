import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("bot.log"),
                              logging.StreamHandler()])

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """
        Initializes the Binance client with API keys and connects to the testnet.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        
        if self.testnet:
            self.client = Client(self.api_key, self.api_secret, tld='com', testnet=True)
            logging.info("Connected to Binance Futures Testnet.")
        else:
            self.client = Client(self.api_key, self.api_secret)
            logging.info("Connected to Binance Futures Live.")

    def _validate_order_params(self, symbol, side, quantity, order_type, price=None):
        """
        Validates the parameters for an order.
        """
        if side not in ['BUY', 'SELL']:
            logging.error(f"Invalid side: {side}")
            return False
        
        if order_type not in ['MARKET', 'LIMIT']:
            logging.error(f"Invalid order type: {order_type}")
            return False

        if order_type == 'LIMIT' and price is None:
            logging.error("Price is required for LIMIT orders.")
            return False
        
        if quantity <= 0:
            logging.error("Quantity must be a positive number.")
            return False
            
        return True

    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Places a market or limit order on the Binance Futures Testnet.
        :param symbol: The trading pair (e.g., 'BTCUSDT').
        :param side: 'BUY' or 'SELL'.
        :param order_type: 'MARKET' or 'LIMIT'.
        :param quantity: The amount of the base asset to trade.
        :param price: The price for a limit order (optional).
        """
        if not self._validate_order_params(symbol, side, quantity, order_type, price):
            return None

        try:
            if order_type == 'MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='LIMIT',
                    timeInForce='GTC',  # Good Till Cancel
                    quantity=quantity,
                    price=price
                )
            
            logging.info(f"Order placed successfully: {order}")
            print("\nOrder Details:")
            print(f"  - Order ID: {order['orderId']}")
            print(f"  - Symbol: {order['symbol']}")
            print(f"  - Side: {order['side']}")
            print(f"  - Type: {order['type']}")
            print(f"  - Status: {order['status']}")
            print(f"  - Quantity: {order['origQty']}")
            if 'price' in order:
                print(f"  - Price: {order['price']}")

            return order

        except BinanceAPIException as e:
            logging.error(f"Binance API Error: {e}")
            print(f"An error occurred: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            print(f"An unexpected error occurred: {e}")
            return None