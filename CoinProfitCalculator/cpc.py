#!/usr/bin/python

import csv
import time
import argparse
import datetime

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

class CoinProfit():

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    product_name = ""

    row_list = {"bought":[], "sold":[]}
    profit_list = {}

    def __init__(self, product_name_inp):
        self.product_name = product_name_inp
        #with open('./eth_fills.csv', 'rb') as csvfile:
        #    reading = csv.DictReader(csvfile, delimiter=',')
        #    counter = 0
        #    for item in reading:
        #        #Sort cells into "bought" and "sold" lists =======================
        #        if item["side"] == "BUY":
        #            self.row_list["bought"].append(item)
        #            counter += 1
        #        elif item["side"] == "SELL":
        #            self.row_list["sold"].append(item)
        #            counter += 1
        #        #Sort cells into "bought" and "sold" lists -----------------------
            
    def __str__(self):
        return str(self.row_list["bought"])

    def date_to_seconds(self, date_object, current_date):
        return time.mktime(date_object.timetuple())

    def sell(self, sell_quantity, coin_price, transaction_date):
        """
        Calculate the profit when selling a number of coins at a given price
        """
        quantity = sell_quantity
        profit = 0

        #current_date = datetime.datetime.now().strftime("%Y/%m/%d")
        #created_date = ""

        stock_quantity = 0.0
        for item in self.row_list["bought"]: #Get stock quantity
            #Compare date times of the bought coin with the sold coin to avoid selling coins that haven't been bought yet
            if datetime.datetime.strptime(item["created at"], DATE_FORMAT) < datetime.datetime.strptime(transaction_date, DATE_FORMAT):
                stock_quantity += float(item["size"])

        if sell_quantity > stock_quantity: #Check if selling quantity exceeds inventory
            #print("DESCREPENCY: The inputed sell quantity exceeds inventory quantity")
            return  transaction_date, 0, self.product_name, False

        else:
            for item in self.row_list["bought"]:
                if quantity > 0:
                    bought_value = 0
                    sold_value = 0
                    quantity_dif = float(item["size"]) - quantity #Get the difference between the selling quantity and the coin quantity
                    
                    if quantity_dif < 0:
                        item["size"] = "0" #Subtract sold coin quantity from row 
                        bought_value += (float(item["size"]) * float(item["price"]))
                        sold_value += (float(item["size"]) * coin_price)
                        profit += sold_value - bought_value
                        quantity += -float(item["size"])

                    else:
                        item["size"] = str(float(item["size"])-quantity) #Subtract sold coin quantity from row 
                        bought_value += (quantity * float(item["price"]))
                        sold_value += (quantity * coin_price)
                        profit += sold_value - bought_value
                        quantity = 0

                else: #Exit loop when the selling quantity is depleated
                    break

        #Add profit to profit list
        if transaction_date in self.profit_list:
            self.profit_list[transaction_date] += profit
        else: 
            self.profit_list[transaction_date] = profit

        return  transaction_date, profit, self.product_name, True

    def get_profit_sum(self):
        """
        Get the sum of all profits
        """
        profit_sums = 0
        for key in self.profit_list:
            profit_sums += self.profit_list[key]

        return profit_sums

    def print_assets(self):
        for item in self.row_list["bought"]:
            date_object = datetime.datetime.strptime(item["created at"], self.DATE_FORMAT)
            thing = ""
            thing = "price: %s, date: %s" % (item["price"], str(self.date_to_seconds(date_object)))

def main():
    global product_list
    product_list = []

    #=== Get arguments ===
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required = True, help = "The file path to the csv file")
    ap.add_argument("-st", "--show_transactions", required = False, help = "Print actions")
    ap.add_argument("-s", "--summary", required = False, help = "Print actions")
    ap.add_argument("-hr", "--header", required = False, help = "Display transactions header")
    
    args = vars(ap.parse_args())
    #--- Get arguments ---

    with open(args["input"], 'rb') as csvfile:
        reading = csv.DictReader(csvfile, delimiter=',')
        counter = 0
        current_product_class = None
        for item in reading:
            #=== Get if product exists in product_list ===
            has_product = False
            for product in product_list:
                if product.product_name == item["product"]:
                    has_product = True

            if not has_product:
                current_product_class = CoinProfit(item["product"])
                product_list.append(current_product_class) #Add products to product list
            #--- Get if product exists in product_list ---

            # === Get product class ===
            for product in product_list:
                if product.product_name == item["product"]:
                    current_product_class = product
            # --- Get product class ---
            
            #=== Sort cells into "bought" and "sold" lists ===
            if item["side"] == "BUY":
                current_product_class.row_list["bought"].append(item)
                counter += 1
            elif item["side"] == "SELL":
                current_product_class.row_list["sold"].append(item)
                counter += 1
            #--- Sort cells into "bought" and "sold" lists ---

    over_draw_qty = 0
    profit_sum = 0
    if args.has_key("header"):
        pass
    elif args.has_key("show_transactions"):
        print("Date:                     Profit:   Product Name:")
    for item in current_product_class.row_list["sold"]:
        date, profit, product_name, cb = current_product_class.sell(float(item["size"]), float(item["price"]), str(item["created at"]))
        profit_sum += profit
        item["size"] = 0
        if args.has_key("show_transactions"):
            print(str(date) + ", " + str(round(profit, 2)) + ",    " + str(product_name))
            
        if cb == False:
            over_draw_qty += profit

    if args.has_key("summary"):
        print("Transaction summary: " + str(profit_sum))
        
    current_product_class.get_profit_sum()

if __name__ == "__main__":
    main()

#test_class.print_assets()


