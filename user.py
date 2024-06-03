import mysql.connector
import project

# Add parameters if necessary.
# Be verbose: Display all necessary data to explicitly state what's being done. Check food_establishment.py for reference.

# Create User
def create_user(connection, user_username, user_password):
    try:
        print("\nCreating user...")
        cursor = connection.cursor()
        # Input username and password: 
        cursor.execute("INSERT INTO user (user_username, user_password) VALUES (%s, %s);",
                       (user_username, user_password))
        connection.commit() 
        print("\nUser '{}' created successfully!\n".format(user_username))

    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to create User.\n")

# Read All Users
def read_all_users(connection):
    print("\nReading all users...")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user;")
        users = cursor.fetchall()
        
        # Check if there are users:
        if users:
            print("\n")
            for user in users:
                print(user)
            print("\n")
        
        # No users:
        else:
            print("\nNo users found.\n")
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch users.\n")

# Read Certain User
def read_certain_user(connection, user_username):
    print('\nReading all Users with username: "' + user_username + '"...')
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user WHERE user_username = %s;", (user_username,))
        users = cursor.fetchall()
        
        # If user exists:
        if users:
            print("\n")
            for user in users:
                print(user)
            print("\n")
        
        # If user in selected query is not found:
        else:
            print("\nNo user found with the username '{}'.\n".format(user_username))
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch user.")

# Update User
def update_user(connection, input_attribute, user_username, input_username):
    print("\nUpdating user...")
    try:
        cursor = connection.cursor()

        # First, we validate if the user exists to ensure that we are not updating nothing.
        cursor.execute("SELECT user_username FROM user WHERE user_username = %s;", (user_username,))
        if cursor.fetchone() is None:
            print("\nUser '{}' does not exist.\n".format(user_username))
            return # Return if user is non-existent.
        
        cursor.execute("UPDATE user SET {} = %s WHERE user_username = %s;".format(
            input_attribute # Attribute to be set
        ), (
        input_username, # Value to be set
        user_username)) # Username of the user to be updated

        project.update_average_rating(connection)
        connection.commit() # Ensure that the update is saved

        # Print update details:
        print("\nUser user_username updated from '{}' to '{}' successfully!\n".format(user_username, input_username))

    except mysql.connector.Error as err:
        print("\nError: ", err)
        print("Failed to update user.")

# Delete User 
def delete_user(connection, user_username):
    print("\nDeleting user...")
    try:
        cursor=connection.cursor()

        # Validate if user exists
        cursor.execute("SELECT user_username FROM user WHERE user_username = %s;", (user_username,))
        if cursor.fetchone() is None:
            print("\nUser '{}' does not exist.\n".format(user_username))
            return
        
        # Delete statement
        cursor.execute("DELETE from user WHERE user_username= %s;", (user_username,))
        rows_affected = cursor.rowcount  # Get the number of rows affected by the delete operation
        project.update_average_rating(connection)
        connection.commit()

        # Status message to show whether user has been deleted successfully.
        if rows_affected > 0:
            print(f"\nUser '{user_username}' successfully deleted!")
        else:
            print(f"\nUser '{user_username}' does not exist or has already been deleted.")
    except mysql.connector.Error as err:
        print("\nError: ", err)
        print("Failed to update user.")