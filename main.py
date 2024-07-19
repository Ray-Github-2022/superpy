from datetime import datetime, timedelta
import argparse
import csv
import os
from rich.console import Console
from rich.table import Table
from tabulate import tabulate

console = Console()

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

INVENTORY_FILE = 'INVENTORY.csv'
SALES_LOG_FILE = 'sales_log.csv'
DATE_FILE = 'date.txt'

def main():
    parser = argparse.ArgumentParser(description="Supermarket Inventory Management CLI",
                                     epilog="Good luck and have fun managing the supermarket's inventory!")
    
    # print help message (standard/programmatically)
    parser.print_help() # Extra..

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    parser_add = subparsers.add_parser("add", help="Add a new product to the inventory")
    parser_add.add_argument("--name", required=True, help="Product name")
    parser_add.add_argument("--buy_price", required=True, type=float, help="Product buy price")
    parser_add.add_argument("--sell_price", required=True, type=float, help="Product sell price")
    parser_add.add_argument("--quantity", required=True, type=int, help="Product quantity")
    parser_add.add_argument("--buy_date", required=True, help="Product buy date (YYYY-MM-DD)")
    parser_add.add_argument("--expiration_date", required=True, help="Product expiration date (YYYY-MM-DD)")

    parser_remove = subparsers.add_parser("remove", help="Remove a product from the inventory")
    parser_remove.add_argument("--id", required=True, type=int, help="Product ID")

    parser_buy = subparsers.add_parser("buy", help="Record the purchase of new stock")
    parser_buy.add_argument("--name", required=True, help="Product name")
    parser_buy.add_argument("--buy_price", required=True, type=float, help="Product buy price")
    parser_buy.add_argument("--quantity", required=True, type=int, help="Quantity purchased")
    parser_buy.add_argument("--buy_date", required=True, help="Purchase date (YYYY-MM-DD)")
    parser_buy.add_argument("--expiration_date", required=True, help="Expiration date (YYYY-MM-DD)")

    parser_sell = subparsers.add_parser("sell", help="Record the sale of a product")
    parser_sell.add_argument("--id", required=True, type=int, help="Product ID")
    parser_sell.add_argument("--quantity", required=True, type=int, help="Quantity sold")
    parser_sell.add_argument("--sell_date", required=True, help="Sale date (YYYY-MM-DD)")

    subparsers.add_parser("list", help="List all products in the inventory")

    subparsers.add_parser("sales", help="List all sales records")

    subparsers.add_parser("calculate", help="Calculate total sales, cost, and profit")

    subparsers.add_parser("report", help="Generate a report of the current inventory")

    subparsers.add_parser("usage", help="Show the usage guide")

    parser_revenue = subparsers.add_parser("revenue", help="Calculate total revenue from sales")
    parser_revenue.add_argument("--start_date", required=True, help="Start date for the report (YYYY-MM-DD)")
    parser_revenue.add_argument("--end_date", required=True, help="End date for the report (YYYY-MM-DD)")

    parser_profit = subparsers.add_parser("profit", help="Calculate total profit from sales")
    parser_profit.add_argument("--start_date", required=True, help="Start date for the report (YYYY-MM-DD)")
    parser_profit.add_argument("--end_date", required=True, help="End date for the report (YYYY-MM-DD)")

    parser_set_date = subparsers.add_parser("set-date", help="Set the current date")
    parser_set_date.add_argument("--date", required=True, help="Date to set (YYYY-MM-DD)")

    parser_advance_date = subparsers.add_parser("advance-date", help="Advance the current date by a number of days")
    parser_advance_date.add_argument("--days", required=True, type=int, help="Number of days to advance")

    args = parser.parse_args()
    initialize_inventory(INVENTORY_FILE)
    initialize_sales_log(SALES_LOG_FILE)

    # print("Info regarding the date..")
    today = datetime.today()  # Only showing today's date
    print(f"Today's date is {today.strftime('%Y-%m-%d')}")

    if args.command == "usage":
        show_usage_guide()
    if args.command == "advance-date":
        advance_date(args.days)
    elif args.command == "set-date":
        set_date(args.date)
    else:
        execute_command(args)

# Bijgevoegde Usage Guide:
def show_usage_guide():
    usage_guide_path = "usage_guide.txt"
    if os.path.exists(usage_guide_path):
        with open(usage_guide_path, 'r') as file:
            print(file.read())
    else:
        print(f"Usage guide file not found at {usage_guide_path}.")

# Gecomment = Niet van toepassing = Usage Guide Is Only READ
# Sla guide op als usage_guide.txt / Maak inzichtelijk voor app & gebruikers..
#    with open('usage_guide.txt', 'w') as file:
#         file.write(usage_guide_content)               

def initialize_inventory(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'buy_price', 'sell_price', 'quantity', 'buy_date', 'expiration_date', 'sell_date'])

def initialize_sales_log(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'quantity', 'sell_date', 'sell_price'])

def read_inventory(file_path):
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        console.print(f"[bold red]Inventory file not found at {file_path}. Returning empty list.[/bold red]")
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
        console.print(f"[bold red]Sales log file not found at {file_path}. Returning empty list.[/bold red]")
        return []

def write_sales_log(sales, file_path):
    try:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'quantity', 'sell_date', 'sell_price'])
            if file.tell() == 0:
                writer.writeheader()
            for sale in sales:
                # Valideer en verwijder gegevens vooraf ingave
                if not isinstance(sale.get('sell_price', ''), (int, float)):
                    sale['sell_price'] = '0.0'
                if not isinstance(sale.get('quantity', ''), int):
                    sale['quantity'] = '0'
                writer.writerow(sale)
    except Exception as e:
        console.print(f"[bold red]Error writing to sales log: {e}[/bold red]")

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
        'sell_date': ''
    }
    products.append(new_product)
    write_inventory(products, INVENTORY_FILE)
    console.print("[bold green]Product added successfully.[/bold green]")

def remove_product(product_id):
    products = read_inventory(INVENTORY_FILE)
    products = [product for product in products if int(product['id']) != product_id]
    write_inventory(products, INVENTORY_FILE)
    console.print("[bold green]Product removed successfully.[/bold green]")

def update_product(product_id, name, buy_price, sell_price, quantity):
    products = read_inventory(INVENTORY_FILE)
    for product in products:
        if int(product['id']) == product_id:
            product.update({'name': name, 'buy_price': buy_price, 'sell_price': sell_price, 'quantity': quantity})
            write_inventory(products, INVENTORY_FILE)
            console.print("[bold green]Product updated successfully.[/bold green]")
            return
    console.print("[bold red]Error: Product ID not found.[/bold red]")

def sell_product(product_id, quantity, sell_date):
    products = read_inventory(INVENTORY_FILE)
    sales = read_sales_log(SALES_LOG_FILE)
    product_found = False
    for product in products:
        if int(product['id']) == product_id:
            product_found = True
            if int(product['quantity']) >= quantity:
                product['quantity'] = int(product['quantity']) - quantity
                new_sale = {'id': product_id, 'name': product['name'], 'quantity': quantity, 'sell_date': sell_date, 'sell_price': product['sell_price']}
                sales.append(new_sale)
                write_inventory(products, INVENTORY_FILE)
                write_sales_log([new_sale], SALES_LOG_FILE)
                console.print("[bold green]Product sold successfully.[/bold green]")
            else:
                console.print("[bold red]Error: Not enough quantity in stock.[/bold red]")
            return
    if not product_found:
        console.print("[bold red]Error: Product ID not found.[/bold red]")

def list_products():
    products = read_inventory(INVENTORY_FILE)
    if not products:
        console.print("[bold red]No products found in inventory.[/bold red]")
    else:
        table = Table(title="Product List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Buy Price", style="green")
        table.add_column("Sell Price", style="yellow")
        table.add_column("Quantity", style="blue")
        table.add_column("Buy Date", style="red")
        table.add_column("Expiration Date", style="purple")

        for p in products:
            table.add_row(p['id'], p['name'], p['buy_price'], p['sell_price'], p['quantity'], p['buy_date'], p['expiration_date'])
        
        console.print(table)

def list_sales():
    sales = read_sales_log(SALES_LOG_FILE)
    if not sales:
        console.print("[bold red]No sales recorded.[/bold red]")
    else:
        table = Table(title="Sales List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")
        table.add_column("Quantity", style="green")
        table.add_column("Sell Date", style="yellow")
        table.add_column("Sell Price", style="blue")

        for s in sales:
            table.add_row(s['id'], s['name'], s['quantity'], s['sell_date'], s['sell_price'])
        
        console.print(table)

def calculate_sales():
    products = read_inventory(INVENTORY_FILE)
    total_sales = 0.0
    total_cost = 0.0
    for product in products:
        if product['sell_date']:
            try:
                sell_price = float(product['sell_price']) if product['sell_price'] else 0.0
                buy_price = float(product['buy_price']) if product['buy_price'] else 0.0
                quantity = int(product['quantity'])
                total_sales += sell_price * quantity
                total_cost += buy_price * quantity
            except ValueError:
                console.print(f"[bold red]Error: Invalid price or quantity for product ID {product['id']}[/bold red]")
    total_profit = total_sales - total_cost
    console.print(f"[bold green]Total Sales: ${total_sales:.2f}[/bold green]")
    console.print(f"[bold green]Total Cost: ${total_cost:.2f}[/bold green]")
    console.print(f"[bold green]Total Profit: ${total_profit:.2f}[/bold green]")

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
    console.print("[bold green]Product bought successfully.[/bold green]")

def advance_date(days):
    current_date = datetime.today().strftime('%Y-%m-%d')
    new_date = (datetime.strptime(current_date, '%Y-%m-%d') + timedelta(days=days)).strftime('%Y-%m-%d')
    with open(DATE_FILE, 'w') as file:
        file.write(new_date)
    console.print(f"[bold green]Last known date is {current_date}[/bold green]")
    console.print(f"[bold green]New date advanced by {days} days: {new_date}[/bold green]")

def set_date(new_date):
    try:
        datetime.strptime(new_date, '%Y-%m-%d')
        with open(DATE_FILE, 'w') as file:
            file.write(new_date)
        console.print(f"[bold green]Date set to {new_date}[/bold green]")
    except ValueError:
        console.print("[bold red]Error: Invalid date format. Please use YYYY-MM-DD.[/bold red]")

def report_inventory():
    products = read_inventory(INVENTORY_FILE)
    if not products:
        console.print("[bold red]No products found in inventory.[/bold red]")
    else:
        # Creeer Rich Table
        table = Table(title="Current Inventory Report", show_header=True, header_style="bold blue")
        
        table.add_column("ID", style="dim", width=6)
        table.add_column("Name")
        table.add_column("Buy Price", justify="right")
        table.add_column("Sell Price", justify="right")
        table.add_column("Quantity", justify="right")
        table.add_column("Buy Date")
        table.add_column("Expiration Date")
        table.add_column("Sell Date")

        # Converteer price naar float
        def safe_convert_to_float(value):
            try:
                return f"${float(value):.2f}"
            except ValueError:
                return "$0.00"

        for p in products:
            table.add_row(
                str(p['id']),
                p['name'],
                safe_convert_to_float(p['buy_price']),
                safe_convert_to_float(p['sell_price']),
                str(p['quantity']),
                p['buy_date'],
                p['expiration_date'],
                p['sell_date'] if p['sell_date'] else "N/A"
            )

        # Print Rich
        console.print(table)

def calculate_revenue(start_date, end_date):
    sales = read_sales_log(SALES_LOG_FILE)
    total_revenue = 0.0
    
    for sale in sales:
        try:
            sale_date = datetime.strptime(sale['sell_date'], '%Y-%m-%d')
            if start_date <= sale_date <= end_date:
                try:
                    sell_price = float(sale['sell_price'])
                except ValueError:
                    console.print(f"[bold red]Error: Invalid sell_price in sales record for product ID {sale['id']}. Value: {sale['sell_price']}[/bold red]")
                    continue
                
                try:
                    quantity = int(sale['quantity'])
                except ValueError:
                    console.print(f"[bold red]Error: Invalid quantity in sales record for product ID {sale['id']}. Value: {sale['quantity']}[/bold red]")
                    continue
                
                total_revenue += sell_price * quantity
        
        except ValueError as e:
            console.print(f"[bold red]Error: Invalid data in sales record for product ID {sale['id']}. Details: {e}[/bold red]")
            continue
    
    console.print(f"[bold green]Total revenue from {start_date.date()} to {end_date.date()}: ${total_revenue:.2f}[/bold green]")

def calculate_profit(start_date, end_date):
    sales = read_sales_log(SALES_LOG_FILE)
    total_revenue = 0.0
    total_cost = 0.0
    products = read_inventory(INVENTORY_FILE)
    
    for sale in sales:
        try:
            sale_date = datetime.strptime(sale['sell_date'], '%Y-%m-%d')
            if start_date <= sale_date <= end_date:
                try:
                    sell_price = float(sale['sell_price'])
                except ValueError:
                    console.print(f"[bold red]Error: Invalid sell_price in sales record for product ID {sale['id']}. Value: {sale['sell_price']}[/bold red]")
                    continue
                
                try:
                    quantity = int(sale['quantity'])
                except ValueError:
                    console.print(f"[bold red]Error: Invalid quantity in sales record for product ID {sale['id']}. Value: {sale['quantity']}[/bold red]")
                    continue
                
                total_revenue += sell_price * quantity
                
                for product in products:
                    if int(product['id']) == int(sale['id']):
                        try:
                            buy_price = float(product['buy_price'])
                            total_cost += buy_price * quantity
                        except ValueError:
                            console.print(f"[bold red]Error: Invalid buy_price for product ID {product['id']}. Value: {product['buy_price']}[/bold red]")
                        break
        
        except ValueError as e:
            console.print(f"[bold red]Error: Invalid data in sales record for product ID {sale['id']}. Details: {e}[/bold red]")
            continue
    
    total_profit = total_revenue - total_cost
    console.print(f"[bold green]Total profit from {start_date.date()} to {end_date.date()}: ${total_profit:.2f}[/bold green]")

def clean_sales_log(file_path):
    cleaned_sales = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row['sell_price'] = float(row['sell_price'])
                row['quantity'] = int(row['quantity'])
                cleaned_sales.append(row)
            except ValueError:
                console.print(f"[bold red]Error cleaning sales record: {row}[/bold red]")
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'name', 'quantity', 'sell_date', 'sell_price'])
        writer.writeheader()
        writer.writerows(cleaned_sales)

def clean_inventory(file_path):
    cleaned_products = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row['buy_price'] = float(row['buy_price'])
                row['sell_price'] = float(row['sell_price']) if row['sell_price'] else 0.0
                row['quantity'] = int(row['quantity'])
                cleaned_products.append(row)
            except ValueError:
                console.print(f"[bold red]Error cleaning inventory record: {row}[/bold red]")
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'name', 'buy_price', 'sell_price', 'quantity', 'buy_date', 'expiration_date', 'sell_date'])
        writer.writeheader()
        writer.writerows(cleaned_products)

def execute_command(args):
    if args.command == "add":
        add_product(args.name, args.buy_price, args.buy_date, args.sell_price, args.quantity, args.expiration_date)
    elif args.command == "remove":
        remove_product(args.id)
    elif args.command == "buy":
        buy_product(args.name, args.buy_price, args.quantity, args.buy_date, args.expiration_date)
    elif args.command == "list":
        list_products()
    elif args.command == "sales":
        list_sales()
    elif args.command == "calculate":
        calculate_sales()
    elif args.command == "sell":
        sell_product(args.id, args.quantity, args.sell_date)
    elif args.command == "report":
        report_inventory()
    elif args.command == "revenue":
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
        calculate_revenue(start_date, end_date)
    elif args.command == "profit":
        start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(args.end_date, '%Y-%m-%d')
        calculate_profit(start_date, end_date)

if __name__ == "__main__":
    main()

# Commands in usage_guide:  Testing several functionalities.. (All tested on 2024-07-19 and functional)
# See help message:         python main.py - h OR --help (= Output in CLI) // with the -h OR --help flag in the terminal