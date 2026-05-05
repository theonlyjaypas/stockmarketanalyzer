# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Add Stock ---")
        symbol = input("Enter Stock Symbol: ").strip().upper()
        name = input("Enter Stock Name: ").strip()
        try:
            shares = float(input("Enter Number of Shares: ").strip())
        except ValueError:
            print("*** Invalid number of shares. Try again. ***")
            input("Press Enter to Continue")
            continue
        new_stock = Stock(symbol, name, shares)
        stock_list.append(new_stock)
        print(f"Stock {symbol} added.")
        option = input("Enter 0 to exit or any other key to add another stock: ").strip()

# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Stock")
        print("2 - Sell Stock")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Buy Stock")
            print("2 - Sell Stock")
            print("0 - Exit Update Shares")
            option = input("Enter Menu Option: ")
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print("Stock List: [", end="")
    print(", ".join(s.symbol for s in stock_list), end="")
    print("]")
    symbol = input("Enter Stock Symbol: ").strip().upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                shares = float(input(f"Enter number of shares to buy: ").strip())
                stock.buy(shares)
                print(f"Purchased {shares} shares of {symbol}. Total shares: {stock.shares}")
            except ValueError:
                print("*** Invalid number of shares. ***")
            input("Press Enter to Continue")
            return
    print(f"*** Stock {symbol} not found. ***")
    input("Press Enter to Continue")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    print("Stock List: [", end="")
    print(", ".join(s.symbol for s in stock_list), end="")
    print("]")
    symbol = input("Enter Stock Symbol: ").strip().upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                shares = float(input(f"Enter number of shares to sell: ").strip())
                stock.sell(shares)
                print(f"Sold {shares} shares of {symbol}. Total shares: {stock.shares}")
            except ValueError:
                print("*** Invalid number of shares. ***")
            input("Press Enter to Continue")
            return
    print(f"*** Stock {symbol} not found. ***")
    input("Press Enter to Continue")

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    print("Stock List: [", end="")
    print(", ".join(s.symbol for s in stock_list), end="")
    print("]")
    symbol = input("Enter Stock Symbol to Delete: ").strip().upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            confirm = input(f"Are you sure you want to delete {symbol}? (y/n): ").strip().lower()
            if confirm == "y":
                stock_list.remove(stock)
                print(f"Stock {symbol} deleted.")
            else:
                print("Delete cancelled.")
            input("Press Enter to Continue")
            return
    print(f"*** Stock {symbol} not found. ***")
    input("Press Enter to Continue")


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("Stock List ---")
    if not stock_list:
        print("No stocks being tracked.")
    else:
        print(f"{'Symbol':<10} {'Name':<30} {'Shares':>10}")
        print("-" * 52)
        for stock in stock_list:
            print(f"{stock.symbol:<10} {stock.name:<30} {stock.shares:>10.2f}")
    input("Press Enter to Continue")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ---")
    print("Stock List: [", end="")
    print(", ".join(s.symbol for s in stock_list), end="")
    print("]")
    symbol = input("Enter Stock Symbol: ").strip().upper()
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                date_str = input("Enter Date (MM/DD/YY): ").strip()
                date = datetime.strptime(date_str, "%m/%d/%y")
                close = float(input("Enter Closing Price: ").strip())
                volume = float(input("Enter Volume: ").strip())
                daily_data = DailyData(date, close, volume)
                stock.add_data(daily_data)
                print(f"Data added for {symbol} on {date_str}.")
            except ValueError as e:
                print(f"*** Invalid input: {e} ***")
            input("Press Enter to Continue")
            return
    print(f"*** Stock {symbol} not found. ***")
    input("Press Enter to Continue")

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    for stock in stock_data:
        print(f"\n{stock.symbol} - {stock.name}")
        print("=" * 40)
        print(f"Shares Owned : {stock.shares}")
        if len(stock.DataList) > 0:
            prices = [d.close for d in stock.DataList]
            latest = stock.DataList[-1].close
            high = max(prices)
            low = min(prices)
            avg = sum(prices) / len(prices)
            value = latest * stock.shares
            print(f"Latest Price : ${latest:,.2f}")
            print(f"Highest Price: ${high:,.2f}")
            print(f"Lowest Price : ${low:,.2f}")
            print(f"Average Price: ${avg:,.2f}")
            print(f"Total Value  : ${value:,.2f}")
            print(f"Records      : {len(stock.DataList)}")
        else:
            print("No daily data available.")
    input("\nPress Enter to Continue")





# Display Chart
def display_chart(stock_list):
    clear_screen()
    print("Display Chart ---")
    print("Stock List: [", end="")
    print(", ".join(s.symbol for s in stock_list), end="")
    print("]")
    symbol = input("Enter Stock Symbol: ").strip().upper()
    display_stock_chart(stock_list, symbol)

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data")
        print("2 - Load Data")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Save Data")
            print("2 - Load Data")
            print("3 - Retrieve Data from Web")
            print("4 - Import from CSV File")
            print("0 - Exit Manage Data")
            option = input("Enter Menu Option: ")
        if option == "1":
            clear_screen()
            stock_data.save_stock_data(stock_list)
            print("Data Saved.")
            input("Press Enter to Continue")
        elif option == "2":
            clear_screen()
            stock_data.load_stock_data(stock_list)
            print("Data Loaded.")
            input("Press Enter to Continue")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)


# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieving Stock Data from Yahoo! Finance ---")
    dateFrom = input("Enter Start Date (MM/DD/YY): ").strip()
    dateTo = input("Enter End Date (MM/DD/YY): ").strip()
    try:
        count = stock_data.retrieve_stock_web(dateFrom, dateTo, stock_list)
        print(f"Records Retrieved: {count}")
    except Exception as e:
        print(f"*** Error retrieving data: {e} ***")
    input("Press Enter to Continue")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV file from Yahoo! Finance---")
    print("Stock List: [", end="")
    print(", ".join(s.symbol for s in stock_list), end="")
    print("]")
    print("Which stock do you want to use?")
    symbol = input("Enter Stock Symbol: ").strip().upper()
    filename = input("Enter filename: ").strip()
    try:
        count = stock_data.import_stock_web_csv(stock_list, symbol, filename)
        print(f"CSV File Imported - {count} records added.")
    except Exception as e:
        print(f"*** Error importing CSV: {e} ***")
    input("Press Enter to Continue")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()
