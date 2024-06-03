import mysql.connector
import project

# Add parameters if necessary.
# Be verbose: Display all necessary data to explicitly state what's being done. Check food_establishment.py for reference.

# Create Food Item
def create_food_item(connection, establishment_name, food_name, food_type, price):
    try:
        # Convert price to a float and validate the range
        if not (-9999.99 <= price <= 9999.99):
            raise ValueError("Price out of valid range")
        
        query = """INSERT INTO foodItem (food_name, food_type, food_price, food_foodestablishmentid) VALUES (
        %s,
        %s,
        %s,
        (SELECT establishment_id from foodestablishment WHERE establishment_name = %s)
        );"""

        print("\nCreating Food Item...")
        cursor = connection.cursor()
        cursor.execute(
            query,
            (food_name, food_type, price, establishment_name)
        )
        if cursor.rowcount == 0:
            print("No changes have occurred.")
            return
        connection.commit()
        
        print("\nFood Item '{}' created successfully!\n".format(food_name))
        
    except ValueError as ve:
        print("\nError:", ve)
        print("Failed to create Food Item due to invalid price.\n")
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
def read_certain_food_items(connection, food_name):
    print('\nReading all Food Items with Name: "' + food_name + '"...')
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM foodItem WHERE food_name = %s;", (food_name,))
        items = cursor.fetchall()
        
        if items:
            print("\n")
            for item in items:
                print(item)
            print("\n")
        else:
            print("\nNo Food Items found with the name '{}'.\n".format(food_name))
            
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch Food Items.\n")

# Update Food Item
def update_food_item(connection, food_name, input_attribute, input_value):
    try:
        cursor = connection.cursor()

        # First, we validate if the food exists to ensure that we are not updating nothing.
        cursor.execute("SELECT food_name FROM fooditem WHERE food_name = %s;", (food_name,))
        if cursor.fetchone() is None:
            print("\nUser '{}' does not exist.\n".format(food_name))
            return # Return if user is non-existent.
        
        cursor.execute("UPDATE fooditem SET {} = %s WHERE food_name = %s;".format(
            input_attribute # Attribute to be set
        ), (
        input_value, # Value to be set
        food_name)) # Food name of the food to be updated
        project.update_average_rating(connection)
        connection.commit() # Ensure that the update is saved

        # Print update details:
        print("\nFood {} updated from '{}' to '{}' successfully!\n".format(input_attribute, food_name, input_value))

    except mysql.connector.Error as err:
        print("\nError: ", err)


# Delete Food Item 
def delete_food_item(connection, food_name):
    try:
        print("\nDeleting food item...")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM foodItem WHERE food_name = %s;", (food_name,))
        project.update_average_rating(connection)
        connection.commit()
        
        print("\nFood Item with name {} deleted successfully!\n".format(food_name))
        
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to delete Food Item.\n")
