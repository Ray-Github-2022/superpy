from datetime import datetime, timedelta
from rich import print
import argparse
import csv
import os

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
def main():
     pass

INVENTORY_FILE = 'INVENTORY_new.csv'
SALES_LOG_FILE = 'sales_log.csv'
DATE_FILE = 'date.txt'
# report.md

def main():
    parser = argparse.ArgumentParser(description="Supermarket Inventory Management CLI => "
                                                 "Please type your command in the CLI..",
                                     epilog="Good luck and have fun: Keeping track of the Supermarket's Inventory!")
    
    # Print the help message (print this help message standard/programmatically)
    parser.print_help() # Leaving/Commenting OUT: parser.print_help() 

    parser.add_argument("command", choices=["add", "remove", "update", "list", "calculate", "sales", "buy", "sell"], help="Command to perform")
    parser.add_argument("--id", help="Product ID")
    parser.add_argument("--name", help="Product name")
    parser.add_argument("--buy_price", type=float, help="Product buy price")
    parser.add_argument("--sell_price", type=float, help="Product sell price")
    parser.add_argument("--quantity", type=int, help="Product quantity")
    parser.add_argument("--buy_date", help="Product buy date")
    parser.add_argument("--expiration_date", help="Product expiration date")
    parser.add_argument("--sell_date", help="Product sell date")
    parser.add_argument('--advance-date', type=int, help='Number of days to advance the date')

    args = parser.parse_args()
    initialize_inventory(INVENTORY_FILE)
    initialize_sales_log(SALES_LOG_FILE)
    # execute_command(args)

    ##################################
    print("Info regarding the date..")
    today = datetime.today()  # Only showing today's date
    print(f"Today's date is {today.strftime('%Y-%m-%d')}")
    ######################################################

    # Using arguments in script
    if args.advance_date is not None:
        advance_date(args.advance_date)
    else:
        initialize_inventory(INVENTORY_FILE)
        execute_command(args)

def initialize_inventory(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'buy_price', 'sell_price', 'quantity', 'buy_date'])

def initialize_sales_log(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'quantity', 'sell_date', 'sell_price'])

def read_inventory(file_path):
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            # next(reader) # Skip the header line => No skipping because of dictionary.
            # print(f"Stock & Current volume:") NOT NEEDED.. See: def list_products():
            return list(reader)
    except FileNotFoundError:
        print(f"Inventory file not found at {file_path}. Returning empty list.")
        return []   

def write_inventory(products, file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'name', 'buy_price', 'sell_price', 'quantity', 'buy_date', 'expiration_date', 'sell_date'])
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def read_sales_log(file_path):
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"Sales log file not found at {file_path}. Returning empty list.")
        return []  

# Update the write_sales_log function to remove unnecessary print statements
def write_sales_log(sales, file_path):
    try:
        # Open the file in append mode ('a')
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'quantity', 'sell_date', 'sell_price'])
            # Check if the file is empty and write the header only once
            if file.tell() == 0: # Check for empty file (file.tell() returns position)
                writer.writeheader()
                writer.writerows(sales) # Write all sales data in the list
            # print(f"Sales data to write: {sales}")
    except Exception as e:
        print(f"Error writing to sales log: {e}")

def add_product(name, buy_price, buy_date, sell_price, quantity, expiration_date):
    products = read_inventory(INVENTORY_FILE)
    product_id = 1 if not products else max(int(product['id']) for product in products) + 1
    new_product = {
        'id': product_id, 
        'name': name, 
        'buy_price': buy_price, 
        'sell_price': sell_price, 
        'quantity': quantity, 
        'buy_date': buy_date, 
        'expiration_date': expiration_date, 
        'sell_date': ''}
    products.append(new_product)
    write_inventory(products, INVENTORY_FILE)
    print("Product added successfully.")

def remove_product(product_id):
    products = read_inventory(INVENTORY_FILE)
    products = [product for product in products if product['id'] != product_id]
    write_inventory(products, INVENTORY_FILE)
    print("Product removed successfully.")

def update_product(product_id, name, buy_price, sell_price, quantity):
    products = read_inventory(INVENTORY_FILE)
    for product in products:
        if product['id'] == product_id:
            product.update({'name': name, 'buy_price': buy_price, 'sell_price': sell_price, 'quantity': quantity})
            break
    write_inventory(products, INVENTORY_FILE)
    print("Product updated successfully.")

def sell_product(product_id, quantity, sell_date):
    products = read_inventory(INVENTORY_FILE)
    sales = read_sales_log(SALES_LOG_FILE)
    product_found = False
    for product in products:
        if int(product['id']) == int(product_id):
            product_found = True
            if int(product['quantity']) >= quantity:
                product['quantity'] = int(product['quantity']) - quantity
                product['sell_date'] = sell_date  # Update the sell_date field
                new_sale = {'id': product_id, 'name': product['name'], 'quantity': quantity, 'sell_date': sell_date, 'sell_price': product['sell_price']}
                sales.append(new_sale) # Append the sale to the sales list
                write_inventory(products, INVENTORY_FILE)
                write_sales_log(sales, SALES_LOG_FILE) # Write all sales data to the log
                write_sales_log([new_sale], SALES_LOG_FILE) # Write new sale data to the log
                print("Product sold successfully.")
            else:
                print("Error: Not enough quantity in stock.")
            break
    if not product_found:
        print("Error: Product ID not found.")
        print(f"Sales data before writing: {sales}") # Debugging output
    
def list_products():
    products = read_inventory(INVENTORY_FILE)
    if not products:
        print("No products found in inventory.")
    else:
        print("Inventory/Stock & Current volume:")
        for product in products:
            print(product)

def list_sales():
    sales = read_sales_log(SALES_LOG_FILE)
    if not sales:
        print("No sales recorded.")
    else:
        print("Sales Log:")
        for sale in sales:
            print(sale)            

# Function to calculate sales / Checks if sell_price and buy_price are non-empty before converting them to floats. If they are empty, it defaults to 0.0.
# Handles any potential ValueError exceptions by printing an error message and continuing with the next product..
def calculate_sales():
    products = read_inventory(INVENTORY_FILE)
    total_sales = 0.0
    total_cost = 0.0
    for product in products:
        if product['sell_date'] and product['sell_date'] != "Expired":
            try:
                sell_price = float(product['sell_price']) if product['sell_price'] else 0.0
                buy_price = float(product['buy_price']) if product['buy_price'] else 0.0
                quantity = int(product['quantity'])
                total_sales += sell_price * quantity
                total_cost += buy_price * quantity
            except ValueError:
                print(f"Error: Invalid price for product ID {product['id']}")
                continue
    total_profit = total_sales - total_cost
    print(f"Total sales revenue: ${total_sales:.2f}")
    print(f"Total cost: ${total_cost:.2f}")
    print(f"Total profit: ${total_profit:.2f}")

# Function to handle buying products
def buy_product(name, buy_price, quantity, buy_date, expiration_date):
    products = read_inventory(INVENTORY_FILE)
    product_id = 1 if not products else max(int(product['id']) for product in products) + 1
    new_product = {
        'id': product_id,
        'name': name,
        'buy_price': buy_price,
        'sell_price': '',
        'quantity': quantity,
        'buy_date': buy_date,
        'expiration_date': expiration_date,
        'sell_date': ''
    }
    products.append(new_product)
    write_inventory(products, INVENTORY_FILE)
    print("Product bought successfully.")             

# Function to advance the date
def advance_date(days):
    current_date = datetime.today().strftime('%Y-%m-%d')
    new_date = (datetime.strptime(current_date, '%Y-%m-%d') + timedelta(days=days)).strftime('%Y-%m-%d')
    # Write the new date to date.txt file
    with open(DATE_FILE, 'w') as file:
        file.write(new_date)
    # Print the new OR unchanged current date
    print(f"Last known date is {current_date}")
    print(f"New date advanced by {days} days: {new_date}")
 
def execute_command(args):
    if args.command == "add":
        if args.name is None or args.buy_price is None or args.sell_price is None or args.quantity is None:
            print("Error: name, quantity, buy_date, buy_price, sell_price are required to add a product.")
        else:
            add_product(args.name, args.buy_price, args.buy_date, args.sell_price, args.quantity, args.expiration_date)
    elif args.command == "remove":
        if args.id is None:
            print("Error: id is required to remove a product.")
        else:
            remove_product(args.id)
    elif args.command == "update":
        if args.id is None or args.name is None or args.buy_price is None or args.sell_price is None or args.quantity is None:
            print("Error: id, name, buy_price, sell_price, and quantity are required to update a product.")
        else:
            update_product(args.id, args.name, args.buy_price, args.sell_price, args.quantity)
    elif args.command == "buy":
        if args.name is None or args.buy_price is None or args.quantity is None or args.buy_date is None or args.expiration_date is None:
            print("Error: name, buy_price, quantity, buy_date, and expiration_date are required to buy a product.")
        else:
            buy_product(args.name, args.buy_price, args.quantity, args.buy_date, args.expiration_date)  
    elif args.command == "list":
        list_products()
    elif args.command == "sales":
        calculate_sales()

    # Update the execute_command function to call sell_product with the correct arguments
    elif args.command == "sell":
        if args.id is None or args.quantity is None or args.sell_date is None:
            print("Error: id, quantity, and sell_date are required to sell a product.")
        else:
            sell_product(args.id, args.quantity, args.sell_date)

if __name__ == "__main__":
    main()

# Commands:             Testing several functionalities.. (All tested on 2024-05-28 and functional)
# Buy product:          python main.py buy --name Milk --buy_price 2.50 --quantity 100 --buy_date 2024-05-28 --expiration_date 2025-05-30
# Add product:          python main.py add --name Wine --buy_price 10.50 --buy_date 2024-05-24 --sell_price 15.99 --quantity 100 --expiration_date 2030-05-30 
# Update product:       python main.py update --id 26 --name Wine --buy_price 12.99 --sell_price 18.50 --quantity 150
# Sell product:         python main.py sell --id 26 --quantity 5 --sell_date 2024-05-28
# List products:        python main.py list 
# Remove product:       python main.py remove --id 26
# Show report:          python main.py report revenue --yesterday
# Calculate sales:      python main.py sales
# Advance the date:     python main.py --advance-date 2 list 
# Reduce the date:      python main.py --advance-date -2 list
 
# See help message:     python main.py --help (= Output in CLI) // Running the script with the -h OR --help flag in the terminal