# Summary: This module contains the functions used by both console and GUI programs to manage stock data.


import csv
import sqlite3
import time
import requests
from datetime import datetime

from stock_class import DailyData, Stock
from utilities import clear_screen, sortDailyData

# Create the SQLite database
def create_database():
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    createStockTableCmd = """CREATE TABLE IF NOT EXISTS stocks (
                            symbol TEXT NOT NULL PRIMARY KEY,
                            name TEXT,
                            shares REAL
                        );"""
    createDailyDataTableCmd = """CREATE TABLE IF NOT EXISTS dailyData (
                                symbol TEXT NOT NULL,
                                date TEXT NOT NULL,
                                price REAL NOT NULL,
                                volume REAL NOT NULL,
                                PRIMARY KEY (symbol, date)
                        );"""   
    cur.execute(createStockTableCmd)
    cur.execute(createDailyDataTableCmd)
    conn.commit()
    conn.close()

# Save stocks and daily data into database
def save_stock_data(stock_list):
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    insertStockCmd = """INSERT INTO stocks
                            (symbol, name, shares)
                            VALUES
                            (?, ?, ?); """
    insertDailyDataCmd = """INSERT INTO dailyData
                                    (symbol, date, price, volume)
                                    VALUES
                                    (?, ?, ?, ?);"""
    for stock in stock_list:
        insertValues = (stock.symbol, stock.name, stock.shares)
        try:
            cur.execute(insertStockCmd, insertValues)
            cur.execute("COMMIT;")
        except:
            pass
        for daily_data in stock.DataList: 
            insertValues = (stock.symbol,daily_data.date.strftime("%m/%d/%y"),daily_data.close,daily_data.volume)
            try:
                cur.execute(insertDailyDataCmd, insertValues)
                cur.execute("COMMIT;")
            except:
                pass
    
# Load stocks and daily data from database
def load_stock_data(stock_list):
    stock_list.clear()
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    stockCur = conn.cursor()
    stockSelectCmd = """SELECT symbol, name, shares
                    FROM stocks; """
    stockCur.execute(stockSelectCmd)
    stockRows = stockCur.fetchall()
    for row in stockRows:
        new_stock = Stock(row[0],row[1],row[2])
        dailyDataCur = conn.cursor()
        dailyDataCmd = """SELECT date, price, volume
                        FROM dailyData
                        WHERE symbol=?; """
        selectValue = (new_stock.symbol)
        dailyDataCur.execute(dailyDataCmd,(selectValue,))
        dailyDataRows = dailyDataCur.fetchall()
        for dailyRow in dailyDataRows:
            daily_data = DailyData(datetime.strptime(dailyRow[0],"%m/%d/%y"),float(dailyRow[1]),float(dailyRow[2]))
            new_stock.add_data(daily_data)
        stock_list.append(new_stock)
    sortDailyData(stock_list)

# Get stock price history from Yahoo Finance using their chart API
def retrieve_stock_web(dateStart, dateEnd, stock_list):
    period1 = int(time.mktime(datetime.strptime(dateStart, "%m/%d/%y").timetuple()))
    period2 = int(time.mktime(datetime.strptime(dateEnd, "%m/%d/%y").timetuple()))
    headers = {"User-Agent": "Mozilla/5.0"}
    recordCount = 0
    for stock in stock_list:
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{stock.symbol}"
               f"?period1={period1}&period2={period2}&interval=1d&events=history")
        response = requests.get(url, headers=headers)
        data = response.json()
        result = data["chart"]["result"][0]
        timestamps = result["timestamp"]
        closes = result["indicators"]["quote"][0]["close"]
        volumes = result["indicators"]["quote"][0]["volume"]
        for ts, close, volume in zip(timestamps, closes, volumes):
            if close is None or volume is None:
                continue
            daily_data = DailyData(datetime.fromtimestamp(ts), float(close), float(volume))
            stock.add_data(daily_data)
            recordCount += 1
    return recordCount

# Get price and volume history from Yahoo! Finance using CSV import.
def import_stock_web_csv(stock_list,symbol,filename):
    for stock in stock_list:
        if stock.symbol == symbol:
            count = 0
            with open(filename, newline='') as stockdata:
                datareader = csv.reader(stockdata, delimiter=',')
                next(datareader)
                for row in datareader:
                    try:
                        daily_data = DailyData(datetime.strptime(row[0], "%Y-%m-%d"), float(row[4]), float(row[6]))
                        stock.add_data(daily_data)
                        count += 1
                    except (ValueError, IndexError):
                        continue
            sortDailyData(stock_list)
            return count
    raise ValueError(f"Stock symbol {symbol} not found in stock list.")

def main():
    clear_screen()
    print("This module will handle data storage and retrieval.")

if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()