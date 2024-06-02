import mysql.connector

# Add parameters if necessary.
# Be verbose: Display all necessary data to explicitly state what's being done. Check food_establishment.py for reference.

# Create Food Item
def create_food_item(connection, item_name, price, establishment_id):
    try:
        print("\nCreating Food Item...")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO foodItem (food_name, food_price, food_foodestablishmentid) VALUES (%s, %s, %s);",
            (item_name, price, establishment_id)
        )
        connection.commit()
        
        print("\nFood Item '{}' created successfully!\n".format(item_name))
        
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to create Food Item.\n")

# Read All Food Items
def read_all_food_items(connection):
    print("\nReading all food items...")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM foodItem;")
        items = cursor.fetchall()
        
        if items:
            print("\n")
            for item in items:
                print(item)
            print("\n")
        else:
            print("\nNo Food Items found.\n")
            
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch Food Items.\n")


# Read Certain Item/s
def read_certain_food_items(connection, item_name):
    print('\nReading all Food Items with Name: "' + item_name + '"...')
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM foodItem WHERE food_name = %s;", (item_name,))
        items = cursor.fetchall()
        
        if items:
            print("\n")
            for item in items:
                print(item)
            print("\n")
        else:
            print("\nNo Food Items found with the name '{}'.\n".format(item_name))
            
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch Food Items.\n")

# Update Food Item
def update_food_item(connection, item_id, new_name, new_price):
    try:
        print("\nUpdating food item...")
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE foodItem SET food_name = %s, food_price = %s WHERE food_id = %s;",
            (new_name, new_price, item_id)
        )
        connection.commit()
        
        print("\nFood Item with ID {} updated successfully!\n".format(item_id))
        
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to update Food Item.\n")

# Delete Food Item 
def delete_food_item(connection, item_id):
    try:
        print("\nDeleting food item...")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM foodItem WHERE food_id = %s;", (item_id,))
        connection.commit()
        
        print("\nFood Item with ID {} deleted successfully!\n".format(item_id))
        
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to delete Food Item.\n")
