import mysql.connector
import project

# Create Food Establishment
def create_food_establishment(connection, establishment_name):
    try:
        print("\nCreating Food Establishment...") 
        cursor = connection.cursor()
        # Random tip: The comma after (establishment_name,) is necessary for creating a single-element tuple in Python.
        cursor.execute("INSERT INTO foodEstablishment (establishment_name) VALUES (%s);",
                       (establishment_name,))
        connection.commit() 
        
        print("\nFood Establishment '{}' created successfully!\n".format(establishment_name))
        
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to create Food Establishment.\n")

# Read All Food Establishments  
def read_all_food_establishments(connection):
    print("\nReading all Food Establishments...")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM foodEstablishment;")
        establishments = cursor.fetchall()
        
        # If there are instances...
        if establishments:
            print("\n")
            for establishment in establishments:
                print(establishment)
            print("\n")
        
        # Else, empty set...
        else:
            print("\nNo Food Establishments found.\n")
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch Food Establishments.\n")
        
# Read Certain Food Establishment/s  
def read_certain_food_establishments(connection, establishment_name):
    print('\nReading all Food Establishments with Establishment Name: "' + establishment_name + '"...')
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM foodEstablishment WHERE establishment_name = %s;", (establishment_name,))
        establishments = cursor.fetchall()
        
        # If there are instances...
        if establishments:
            print("\n")
            for establishment in establishments:
                print(establishment)
            print("\n")
        
        # Else, empty set...
        else:
            print("\nNo Food Establishments found with the name '{}'.\n".format(establishment_name))
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch Food Establishments.\n")

# Update Food Establishment  
def update_food_establishment(connection, input_attribute, input_value, establishment_name):
    print("\nUpdating Food Establishment...")
    try:
        cursor = connection.cursor()
        
        # Fetch the old value before updating
        cursor.execute("SELECT {} FROM foodEstablishment WHERE establishment_name = %s;".format(input_attribute), (establishment_name,))
                        
        old_value_result = cursor.fetchone()
        
        if old_value_result is None:
            print("Food Establishment Name '{}' does not exist.\n".format(establishment_name))
            return # Return if food establishment is non-existent.
        
        old_value = old_value_result[0] # If old_value exists, proceed the subscript and gets the old_value
        
        # Perform the update
        query = "UPDATE foodEstablishment SET {} = %s WHERE establishment_name = %s;".format(input_attribute)
        cursor.execute(query, (input_value, establishment_name))
        project.update_average_rating(connection)
        connection.commit() 
        
        # Print the update details
        # print("\nFood Establishment '{}' '{}' updated from '{}' to '{}' successfully!\n".format(establishment_name, input_attribute, old_value, input_value))
        
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to update Food Establishment.\n")

# Delete Food Establishment
def delete_food_establishment(connection, establishment_name):
    print("\nDeleting Food Establishment...") 
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM foodEstablishment WHERE establishment_name = %s;", (establishment_name,))
        if cursor.rowcount == 0:
            print("Food Establishment Name '{}' does not exist.\n".format(establishment_name))
            return # Return if food establishment is non-existent.
        project.update_average_rating(connection)
        connection.commit() 
        
        print("\nFood Establishment '{}' deleted successfully!\n".format(establishment_name))
        
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to delete Food Establishment.\n")