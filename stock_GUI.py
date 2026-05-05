# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import stock_data
from stock_class import Stock
from utilities import display_stock_chart, sortStocks

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

        # Create Window
        self.root = Tk()
        self.root.title("Stock Manager")
        self.root.geometry("950x620")

        # Add Menubar
        self.menubar = Menu(self.root)

        # Add File Menu
        self.fileMenu = Menu(self.menubar, tearoff=0)
        self.fileMenu.add_command(label="Load Data", command=self.load)
        self.fileMenu.add_command(label="Save Data", command=self.save)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

        # Add Web Menu
        self.webMenu = Menu(self.menubar, tearoff=0)
        self.webMenu.add_command(label="Scrape Data from Yahoo! Finance", command=self.scrape_web_data)
        self.webMenu.add_command(label="Import CSV From Yahoo! Finance", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web", menu=self.webMenu)

        # Add Chart Menu
        self.chartMenu = Menu(self.menubar, tearoff=0)
        self.chartMenu.add_command(label="Display Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=self.chartMenu)

        # Add menus to window
        self.root.config(menu=self.menubar)

        # Main frame
        mainFrame = Frame(self.root)
        mainFrame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Left frame - stock list and forms
        leftFrame = Frame(mainFrame, width=240)
        leftFrame.pack(side=LEFT, fill=Y, padx=5)
        leftFrame.pack_propagate(False)

        # Stock list
        Label(leftFrame, text="Stocks", font=("Arial", 11, "bold")).pack()
        listFrame = Frame(leftFrame)
        listFrame.pack(fill=BOTH, expand=True)
        scrollbar = Scrollbar(listFrame)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.stockList = Listbox(listFrame, yscrollcommand=scrollbar.set, height=10, exportselection=False)
        self.stockList.pack(fill=BOTH, expand=True)
        self.stockList.bind("<<ListboxSelect>>", self.update_data)
        scrollbar.config(command=self.stockList.yview)

        # Add Stock form
        addFrame = LabelFrame(leftFrame, text="Add Stock", padx=5, pady=5)
        addFrame.pack(fill=X, pady=4)
        Label(addFrame, text="Symbol:").grid(row=0, column=0, sticky=W)
        self.addSymbolEntry = Entry(addFrame, width=12)
        self.addSymbolEntry.grid(row=0, column=1, sticky=W, pady=1)
        Label(addFrame, text="Name:").grid(row=1, column=0, sticky=W)
        self.addNameEntry = Entry(addFrame, width=12)
        self.addNameEntry.grid(row=1, column=1, sticky=W, pady=1)
        Label(addFrame, text="Shares:").grid(row=2, column=0, sticky=W)
        self.addSharesEntry = Entry(addFrame, width=12)
        self.addSharesEntry.grid(row=2, column=1, sticky=W, pady=1)
        Button(addFrame, text="Add Stock", command=self.add_stock).grid(row=3, columnspan=2, pady=4)

        # Update shares form
        updateFrame = LabelFrame(leftFrame, text="Update Shares", padx=5, pady=5)
        updateFrame.pack(fill=X, pady=4)
        Label(updateFrame, text="Shares:").grid(row=0, column=0, sticky=W)
        self.updateSharesEntry = Entry(updateFrame, width=12)
        self.updateSharesEntry.grid(row=0, column=1, sticky=W, pady=1)
        btnRow = Frame(updateFrame)
        btnRow.grid(row=1, columnspan=2, pady=4)
        Button(btnRow, text="Buy", command=self.buy_shares, width=6).pack(side=LEFT, padx=3)
        Button(btnRow, text="Sell", command=self.sell_shares, width=6).pack(side=LEFT, padx=3)

        # Delete stock button
        Button(leftFrame, text="Delete Stock", command=self.delete_stock, fg="red").pack(pady=4)

        # Right frame - heading + tabs
        rightFrame = Frame(mainFrame)
        rightFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        # Add heading information
        self.headingLabel = Label(rightFrame, text="Select a Stock", font=("Arial", 13, "bold"))
        self.headingLabel.pack(pady=6)

        # Add Tabs
        self.notebook = ttk.Notebook(rightFrame)
        self.notebook.pack(fill=BOTH, expand=True)

        # Setup History Tab
        historyFrame = Frame(self.notebook)
        self.notebook.add(historyFrame, text="History")
        histScroll = Scrollbar(historyFrame)
        histScroll.pack(side=RIGHT, fill=Y)
        self.dailyDataList = Text(historyFrame, yscrollcommand=histScroll.set, font=("Courier", 10))
        self.dailyDataList.pack(fill=BOTH, expand=True)
        histScroll.config(command=self.dailyDataList.yview)

        # Setup Report Tab
        reportFrame = Frame(self.notebook)
        self.notebook.add(reportFrame, text="Report")
        reportScroll = Scrollbar(reportFrame)
        reportScroll.pack(side=RIGHT, fill=Y)
        self.stockReport = Text(reportFrame, yscrollcommand=reportScroll.set, font=("Courier", 10))
        self.stockReport.pack(fill=BOTH, expand=True)
        reportScroll.config(command=self.stockReport.yview)

        ## Call MainLoop
        self.root.mainloop()

# This section provides the functionality

    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0, END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)
        messagebox.showinfo("Load Data", "Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data", "Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        if not self.stockList.curselection():
            return
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0", END)
                self.stockReport.delete("1.0", END)
                self.dailyDataList.insert(END, "- Date -   - Close -    - Volume -\n")
                self.dailyDataList.insert(END, "==================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " + '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END, row)

                # display report
                if len(stock.DataList) > 0:
                    prices = [d.close for d in stock.DataList]
                    latest = stock.DataList[-1].close
                    high = max(prices)
                    low = min(prices)
                    avg = sum(prices) / len(prices)
                    value = latest * stock.shares
                    self.stockReport.insert(END, f"Stock Report: {stock.symbol} - {stock.name}\n")
                    self.stockReport.insert(END, "=" * 40 + "\n")
                    self.stockReport.insert(END, f"Shares Owned : {stock.shares}\n")
                    self.stockReport.insert(END, f"Latest Price : ${latest:,.2f}\n")
                    self.stockReport.insert(END, f"Highest Price: ${high:,.2f}\n")
                    self.stockReport.insert(END, f"Lowest Price : ${low:,.2f}\n")
                    self.stockReport.insert(END, f"Average Price: ${avg:,.2f}\n")
                    self.stockReport.insert(END, f"Total Value  : ${value:,.2f}\n")
                    self.stockReport.insert(END, f"Records      : {len(stock.DataList)}\n")

    # Add new stock to track.
    def add_stock(self):
        symbol = self.addSymbolEntry.get().strip().upper()
        name = self.addNameEntry.get().strip()
        shares_text = self.addSharesEntry.get().strip()
        if not symbol or not name or not shares_text:
            messagebox.showwarning("Missing Info", "Please fill in Symbol, Name, and Shares.")
            return
        try:
            shares = float(shares_text)
        except ValueError:
            messagebox.showwarning("Invalid Shares", "Shares must be a number.")
            return
        new_stock = Stock(symbol, name, shares)
        self.stock_list.append(new_stock)
        self.stockList.insert(END, symbol)
        self.addSymbolEntry.delete(0, END)
        self.addNameEntry.delete(0, END)
        self.addSharesEntry.delete(0, END)

    # Buy shares of stock.
    def buy_shares(self):
        if not self.stockList.curselection():
            messagebox.showwarning("No Stock Selected", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                try:
                    stock.buy(float(self.updateSharesEntry.get()))
                    self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                except ValueError:
                    messagebox.showwarning("Invalid Input", "Shares must be a number.")
                    return
        messagebox.showinfo("Buy Shares", "Shares Purchased")
        self.updateSharesEntry.delete(0, END)

    # Sell shares of stock.
    def sell_shares(self):
        if not self.stockList.curselection():
            messagebox.showwarning("No Stock Selected", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                try:
                    stock.sell(float(self.updateSharesEntry.get()))
                    self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                except ValueError:
                    messagebox.showwarning("Invalid Input", "Shares must be a number.")
                    return
        messagebox.showinfo("Sell Shares", "Shares Sold")
        self.updateSharesEntry.delete(0, END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
        if not self.stockList.curselection():
            messagebox.showwarning("No Stock Selected", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        confirm = messagebox.askyesno("Delete Stock", f"Delete {symbol} and all its history?")
        if confirm:
            self.stock_list[:] = [s for s in self.stock_list if s.symbol != symbol]
            idx = self.stockList.curselection()[0]
            self.stockList.delete(idx)
            self.headingLabel['text'] = "Select a Stock"
            self.dailyDataList.delete("1.0", END)
            self.stockReport.delete("1.0", END)

    # Get data from web scraping.
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date", "Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date", "Enter Ending Date (m/d/yy)")
        try:
            stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
        except:
            messagebox.showerror("Cannot Get Data from Web", "Check Path for Chrome Driver")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web", "Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        if not self.stockList.curselection():
            messagebox.showwarning("No Stock Selected", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import", filetypes=[('Yahoo Finance! CSV', '*.csv')])
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list, symbol, filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete", symbol + " Import Complete")

    # Display stock price chart.
    def display_chart(self):
        if not self.stockList.curselection():
            messagebox.showwarning("No Stock Selected", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list, symbol)


def main():
        app = StockApp()


if __name__ == "__main__":
    # execute only if run as a script
    main()
