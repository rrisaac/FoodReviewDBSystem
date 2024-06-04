import mysql.connector
import project

# Add parameters if necessary.
# Be verbose: Display all necessary data to explicitly state what's being done. Check food_establishment.py for reference.

# Create Food Item
def create_food_item(connection, establishment_name, food_name, food_type, price):
    try:
        # Convert price to a float and validate the range
        
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
            return (query % (food_name, food_type, price, establishment_name))
        connection.commit()
        
        print("\nFood Item '{}' created successfully!\n".format(food_name))
        return (query % (food_name, food_type, price, establishment_name))
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
        query = "SELECT * FROM foodItem;"
        cursor.execute(query)

        items = cursor.fetchall()
        
        if items:
            print("\n")
            for item in items:
                print(item)
            print("\n")
        else:
            print("\nNo Food Items found.\n")
            return (query, [])
        return(query, items)
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch Food Items.\n")


# Read Certain Item/s
def read_certain_food_items(connection, food_name):
    print('\nReading all Food Items with Name: "' + food_name + '"...')
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM foodItem WHERE food_name = %s;"
        cursor.execute(query, (food_name,))

        items = cursor.fetchall()
        
        if items:
            print("\n")
            for item in items:
                print(item)
            print("\n")
        else:
            print("\nNo Food Items found with the name '{}'.\n".format(food_name))
            return (query % (food_name,), [])
            
        return (query % (food_name,), items)
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch Food Items.\n")

# Update Food Item
def update_food_item(connection, food_name, input_attribute, input_value):
    try:
        cursor = connection.cursor()

        # First, we validate if the food exists to ensure that we are not updating nothing.
        query = "SELECT food_name FROM fooditem WHERE food_name = %s;"
        cursor.execute(query, (food_name,))
        old_value_result = cursor.fetchone()
        
        if old_value_result is None:
            print("\nFood item '{}' does not exist.\n".format(food_name))
            return (query % (food_name,)) # Return if food item is non-existent.
        
        old_value = old_value_result[0] # If old_value exists, proceed to get the old_value
        
        query = "UPDATE fooditem SET {} = %s WHERE food_name = %s;".format(input_attribute)
        cursor.execute(query, (input_value, food_name))
        project.update_average_rating(connection)
        connection.commit() # Ensure that the update is saved

        # Print update details:
        print("\nFood {} updated from '{}' to '{}' successfully!\n".format(input_attribute, food_name, input_value))
        return (query % (input_value, food_name))
    except mysql.connector.Error as err:
        print("\nError: ", err)


# Delete Food Item 
def delete_food_item(connection, food_name):
    try:
        print("\nDeleting food item...")
        cursor = connection.cursor()
        query = "DELETE FROM foodItem WHERE food_name = %s;"
        cursor.execute(query, (food_name,))

        project.update_average_rating(connection)
        connection.commit()
        
        print("\nFood Item with name {} deleted successfully!\n".format(food_name))
        return(query %(food_name,))
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to delete Food Item.\n")
