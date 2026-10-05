Python 3.14.2 (v3.14.2:df793163d58, Dec  5 2025, 12:18:06) [Clang 16.0.0 (clang-1600.0.26.6)] on darwin
Enter "help" below or click "Help" above for more information.
a
# This is simple basic project for Trading portfolio
# Ask user for monry
# Ask user for stock/crypto symbol like AAPL, TSLA, BTC-USD, ETH-USD
# Download the latest market
# Calculate current price, 5-day moving average, 20-day moving average and trends
# Let user buy, sell, view portfolio, view profit or loss
# keep running until user exits


import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf




def get_market_data(symbol, period="1mo", interval="1d"):
   """
   Download market data for the given symbol.
   """
   try:
       data = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False)
       if data.empty:
           return None
       return data
   except Exception as e:
       print(f"Error downloading data: {e}")
       return None




def get_current_price(data):
   """
   Safely get the latest closing price.
   """
   close_series = data["Close"].squeeze()
   return float(close_series.iloc[-1])




def calculate_moving_averages(data):
   """
   Add moving average columns.
   """
   data = data.copy()
   close_series = data["Close"].squeeze()
   data["MA5"] = close_series.rolling(window=5).mean()
   data["MA20"] = close_series.rolling(window=20).mean()
   return data




def get_trend(data):
   """
   Simple trend logic using MA5 and MA20.
   """
   ma5 = data["MA5"].iloc[-1]
   ma20 = data["MA20"].iloc[-1]


   if pd.isna(ma5) or pd.isna(ma20):
       return "Not enough data"
   if ma5 > ma20:
       return "Uptrend"
   elif ma5 < ma20:
       return "Downtrend"
   else:
       return "Sideways"




def show_market_summary(symbol, data):
   """
   Print market summary.
   """
   current_price = get_current_price(data)
   ma5 = data["MA5"].iloc[-1]
   ma20 = data["MA20"].iloc[-1]
   trend = get_trend(data)


   print("\n--- Market Summary ---")
   print(f"Symbol: {symbol}")
   print(f"Current Price: ${current_price:.2f}")


   if pd.notna(ma5):
       print(f"5-Day Moving Average: ${ma5:.2f}")
   else:
       print("5-Day Moving Average: Not enough data")


   if pd.notna(ma20):
       print(f"20-Day Moving Average: ${ma20:.2f}")
   else:
       print("20-Day Moving Average: Not enough data")


   print(f"Trend: {trend}")




def plot_line_chart(symbol, data):
   """
   Plot close price with moving averages.
   """
   close_series = data["Close"].squeeze()


   plt.figure(figsize=(10, 5))
   plt.plot(data.index, close_series, label="Close Price")
   plt.plot(data.index, data["MA5"], label="MA5")
   plt.plot(data.index, data["MA20"], label="MA20")
   plt.title(f"{symbol} Price Chart")
   plt.xlabel("Date")
   plt.ylabel("Price")
   plt.legend()
   plt.xticks(rotation=45)
   plt.tight_layout()
   plt.show()




def plot_candlestick_chart(symbol):
   candle_data = yf.download(
       symbol,
       period="5d",
       interval="15m",
       auto_adjust=False,
       progress=False
   )


   if candle_data is None or candle_data.empty:
       print("Could not fetch candlestick data.")
       return


   # If columns are multi-level, flatten them
   if isinstance(candle_data.columns, pd.MultiIndex):
       candle_data.columns = candle_data.columns.get_level_values(0)


   # Keep only needed columns
   needed_cols = ["Open", "High", "Low", "Close", "Volume"]
   candle_data = candle_data[needed_cols].copy()


   # Convert each column one by one to numeric
   for col in needed_cols:
       candle_data[col] = pd.to_numeric(candle_data[col], errors="coerce")


   # Remove bad rows
   candle_data.dropna(subset=needed_cols, inplace=True)


   # Make sure index is datetime
   candle_data.index = pd.to_datetime(candle_data.index)


   # Final safety check
   if candle_data.empty:
       print("Candlestick data became empty after cleaning.")
       return


   print("\nCandlestick data types:")
   print(candle_data.dtypes)


   mpf.plot(
       candle_data,
       type="candle",
       style="charles",
       title=f"{symbol} Candlestick Chart",
       mav=(5, 10),
       volume=True
   )


def buy_asset(portfolio, symbol, price, quantity):
   """
   Buy an asset if user has enough cash.
   """
   if quantity <= 0:
       print("Quantity must be greater than 0.")
       return


   cost = price * quantity


   if portfolio["cash"] < cost:
       print("Not enough cash to complete this purchase.")
       return


   portfolio["cash"] -= cost


   if symbol in portfolio["holdings"]:
       old_qty = portfolio["holdings"][symbol]["quantity"]
       old_avg = portfolio["holdings"][symbol]["avg_price"]


       new_qty = old_qty + quantity
       new_avg = ((old_qty * old_avg) + (quantity * price)) / new_qty


       portfolio["holdings"][symbol]["quantity"] = new_qty
       portfolio["holdings"][symbol]["avg_price"] = new_avg
   else:
       portfolio["holdings"][symbol] = {
           "quantity": quantity,
           "avg_price": price
       }


   print(f"\nBought {quantity} of {symbol} at ${price:.2f}")
   print(f"Total cost: ${cost:.2f}")
   print(f"Remaining cash: ${portfolio['cash']:.2f}")




def sell_asset(portfolio, symbol, price, quantity):
   """
   Sell an asset if enough quantity is owned.
   """
   if quantity <= 0:
       print("Quantity must be greater than 0.")
       return


   if symbol not in portfolio["holdings"]:
       print("You do not own this asset.")
       return


   owned_qty = portfolio["holdings"][symbol]["quantity"]
   avg_price = portfolio["holdings"][symbol]["avg_price"]


   if quantity > owned_qty:
       print("You do not have enough quantity to sell.")
       return


   revenue = price * quantity
   profit = (price - avg_price) * quantity


   portfolio["cash"] += revenue
   portfolio["holdings"][symbol]["quantity"] -= quantity


   if portfolio["holdings"][symbol]["quantity"] == 0:
       del portfolio["holdings"][symbol]


   print(f"\nSold {quantity} of {symbol} at ${price:.2f}")
   print(f"Revenue: ${revenue:.2f}")
   print(f"Profit/Loss on this sale: ${profit:.2f}")
   print(f"Updated cash: ${portfolio['cash']:.2f}")




def show_portfolio(portfolio):
   """
   Show current portfolio.
   """
   print("\n--- Portfolio Summary ---")
   print(f"Cash Balance: ${portfolio['cash']:.2f}")


   if not portfolio["holdings"]:
       print("No holdings yet.")
       return


   print("\nHoldings:")
   for symbol, info in portfolio["holdings"].items():
       print(f"{symbol} -> Quantity: {info['quantity']}, Average Buy Price: ${info['avg_price']:.2f}")




def show_total_portfolio_value(portfolio):
   """
   Show full portfolio value using current market prices.
   """
   total_value = portfolio["cash"]


   print("\n--- Total Portfolio Value ---")
   print(f"Cash: ${portfolio['cash']:.2f}")


   if not portfolio["holdings"]:
       print(f"Total Portfolio Value: ${total_value:.2f}")
       return


   for symbol, info in portfolio["holdings"].items():
       data = get_market_data(symbol)
       if data is None:
           print(f"\nCould not fetch data for {symbol}")
           continue


       current_price = get_current_price(data)
       market_value = current_price * info["quantity"]
       profit_loss = (current_price - info["avg_price"]) * info["quantity"]
       total_value += market_value


       print(f"\n{symbol}")
       print(f"Quantity: {info['quantity']}")
       print(f"Average Buy Price: ${info['avg_price']:.2f}")
       print(f"Current Price: ${current_price:.2f}")
       print(f"Market Value: ${market_value:.2f}")
       print(f"Profit/Loss: ${profit_loss:.2f}")


   print(f"\nTotal Portfolio Value: ${total_value:.2f}")




def show_popular_asset_prices():
   """
   Show current prices for some popular stocks and crypto.
   """
   symbols = ["AAPL", "TSLA", "MSFT", "NVDA", "BTC-USD", "ETH-USD"]


   print("\n--- Popular Asset Prices ---")
   for symbol in symbols:
       data = get_market_data(symbol, period="5d", interval="1d")
       if data is not None:
           price = get_current_price(data)
           print(f"{symbol}: ${price:.2f}")
       else:
           print(f"{symbol}: Data not available")




def main():
   print("=== Simple Trading Portfolio Tracker ===")


   while True:
       try:
           starting_cash = float(input("Enter your starting cash amount: $"))
           if starting_cash > 0:
               break
           print("Please enter a number greater than 0.")
       except ValueError:
           print("Please enter a valid number.")


   portfolio = {
       "cash": starting_cash,
       "holdings": {}
   }


   while True:
       print("\n========== MENU ==========")
       print("1. Check Market Data")
       print("2. Buy Asset")
       print("3. Sell Asset")
       print("4. View Portfolio")
       print("5. View Total Portfolio Value")
       print("6. Show Popular Asset Prices")
       print("7. Exit")


       choice = input("Enter your choice (1-7): ")


       if choice == "1":
           symbol = input("Enter symbol (example: AAPL, TSLA, BTC-USD, ETH-USD): ").upper()
           data = get_market_data(symbol)


           if data is None:
               print("Could not fetch market data for this symbol.")
               continue


           data = calculate_moving_averages(data)
           show_market_summary(symbol, data)


           line_chart = input("Do you want to see the line chart? (yes/no): ").strip().lower()
           if line_chart == "yes":
               plot_line_chart(symbol, data)


           candle_chart = input("Do you want to see the candlestick chart? (yes/no): ").strip().lower()
           if candle_chart == "yes":
...                plot_candlestick_chart(symbol)
... 
... 
...        elif choice == "2":
...            symbol = input("Enter symbol to buy: ").upper()
...            data = get_market_data(symbol)
... 
... 
...            if data is None:
...                print("Could not fetch market data for this symbol.")
...                continue
... 
... 
...            price = get_current_price(data)
...            print(f"Current price of {symbol}: ${price:.2f}")
... 
... 
...            try:
...                quantity = float(input("Enter quantity to buy: "))
...                buy_asset(portfolio, symbol, price, quantity)
...            except ValueError:
...                print("Please enter a proper number for quantity.")
... 
... 
...        elif choice == "3":
...            symbol = input("Enter symbol to sell: ").upper()
...            data = get_market_data(symbol)
... 
... 
...            if data is None:
...                print("Could not fetch market data for this symbol.")
...                continue
... 
... 
...            price = get_current_price(data)
...            print(f"Current price of {symbol}: ${price:.2f}")
... 
... 
...            try:
...                quantity = float(input("Enter quantity to sell: "))
...                sell_asset(portfolio, symbol, price, quantity)
...            except ValueError:
...                print("Please enter a proper number for quantity.")
... 
... 
...        elif choice == "4":
...            show_portfolio(portfolio)
... 
... 
...        elif choice == "5":
...            show_total_portfolio_value(portfolio)
... 
... 
...        elif choice == "6":
...            show_popular_asset_prices()
... 
... 
...        elif choice == "7":
...            print("Exiting program. Goodbye!")
...            break
... 
... 
...        else:
...            print("Invalid choice. Please enter a number from 1 to 7.")
... 
... 
... 
... 
... if __name__ == "__main__":
...    main()
... 
