# importing libraries
from tabulate import tabulate


class Shoe:

    def __init__(self):
        self.country = ""
        self.code = ""
        self.product = ""
        self.cost = 0
        self.quantity = 0
        self.value = 0

    shoe_inventory = []

    # method to read data from file and create object
    def read_data(self):
        try:
            with open('inventory.txt') as file:
                for index, line in enumerate(file):
                    if index > 0:
                        info = line.strip().split(",")
                        shoe = Shoe()
                        shoe.country = info[0]
                        shoe.code = info[1]
                        shoe.product = info[2]
                        shoe.cost = int(info[3])
                        shoe.quantity = int(info[4])
                        shoe.value = shoe.cost * shoe.quantity
                        self.shoe_inventory.append(shoe)
        # if file not found
        except FileNotFoundError:
            print("File not found. Please save inventory file to folder.")

    # formatted string of object attributes
    def __str__(self):
        return f'''
        Country: {self.country}
        Code: {self.code}
        Product: {self.product}
        Cost: {self.cost}
        Quantity: {self.quantity}
        Value: {self.value}'''

    def find_shoe(self):
        code = input("Enter code: ")
        shoe_found = False
        # looking for shoe object with code inputted by user
        for shoe in self.shoe_inventory:
            if shoe.code == code:
                shoe_found = True
                print(shoe)
        if not shoe_found:
            print("No product found for this code.")

    def item_to_restock(self):
        position = 0
        # finding shoe with the lowest quantity
        for index in range(1, len(self.shoe_inventory)):
            if self.shoe_inventory[index].quantity < self.shoe_inventory[position].quantity:
                position = index
        shoe = self.shoe_inventory[position]
        print("Product Found:\n", shoe)
        # requesting amount to restock with and validating the input using trey-except and while loop
        while True:
            try:
                add_stock = int(input("Enter quantity to restock item: "))
                break
            except ValueError:
                print("Please enter a number.")
        shoe.quantity += add_stock
        shoe.value = shoe.cost * shoe.quantity
        print("\nProduct restocked.", shoe)
        # updating the file with the new quantity
        shoe.update_file()

    # function updating the file with the new attribute values
    def update_file(self):
        new_lines = []
        with open('inventory.txt') as read_file:
            for line in read_file:
                info = line.strip().split(',')
                if info[1] == self.code:
                    info[4] = str(self.quantity)
                    if len(info) > 5:
                        info[5] = str(self.cost * self.quantity)
                info = ",".join(info)
                new_lines.append(info)

        with open('inventory.txt', 'w') as write_file:
            for line in new_lines:
                write_file.write(line + "\n")

    def highest_quantity_on_sale(self):
        position = 0
        # finding shoe with highest quantity
        for index in range(1, len(self.shoe_inventory)):
            if self.shoe_inventory[index].quantity > self.shoe_inventory[position].quantity:
                position = index
        shoe = self.shoe_inventory[position]
        print(shoe)
        # asking user if tey want to mark as on sale
        choice = input("Enter 1 to mark as On Sale\n(any other key to exit): ")
        if choice == '1':
            # if already marked on sale
            if shoe.product[0] == "*":
                print("Already marked on sale.")
            else:
                # else mark on sale
                shoe.product = "*" + shoe.product
                print("\nMarked as on sale.\n")
        else:
            show_options()

    def value_per_item(self):
        new_lines = []
        with open('inventory.txt') as read_file:
            for index, line in enumerate(read_file):
                info = line.strip().split(',')
                if len(info) > 5:
                    print("Value column already added.")
                    return
                if index > 0:
                    # calculating value for shoe
                    cost = int(info[3])
                    quantity = int(info[4])
                    value = cost * quantity
                    # adding it to the end of the line for this shoe
                    info.insert(5, str(value))
                else:
                    # adding value column heading
                    info.insert(5, "Value")
                # adding lines with value amount to new_lines[]
                new_lines.append(",".join(info))
        # writing to the file with value column added
        # by printing from new_lines[]
        with open('inventory.txt', 'w') as write_file:
            for line in new_lines:
                write_file.write(line + "\n")
        print("Value column added.")

    def show_table(self):
        table = []
        # creating list of lists to store shoe values
        for shoe in self.shoe_inventory:
            info = [shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity, shoe.value]
            table.append(info)
        print("\nInventory Table\n")
        # using tabulate to create table with headings and inofrmation from the shoes
        print(tabulate(table, headers=["Country", "Code", "Product\n(*on sale)", "Cost", "Quantity", "Value"],
                       tablefmt="grid") + "\n")


# reading in the data and creating the shoe objects
Shoe().read_data()


# menu for the user
def show_options():
    print('''Inventory\n___________________________\nOptions:
    s - search for product by code
    rs - show items that need to be restocked
    hq - find item with highest quantity (mark as on sale)
    sv - show value
    st - show inventory table    
    so - show options
    e - exit
    ''')


show_options()
while True:
    option = input("Enter option (so - show options): ").lower()

    if option == 's':
        Shoe().find_shoe()
    elif option == 'rs':
        Shoe().item_to_restock()
    elif option == 'hq':
        Shoe().highest_quantity_on_sale()
    elif option == 'sv':
        Shoe().value_per_item()
    elif option == 'st':
        Shoe().show_table()
    elif option == 'so':
        show_options()
    elif option == 'e':
        print("Closing application...")
        exit()
    else:
        print("Incorrect input. Try again.")
