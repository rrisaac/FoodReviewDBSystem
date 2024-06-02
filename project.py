# CMSC 127 - S5L (Borja_Capule_Isaac)
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os
import food_establishment
import user
import food_item
import food_review
import summary_report

def execute_sql_file(filename, connection):
    with open(filename, 'r') as sql_file:
        sql_commands = sql_file.read().split(';')
        cursor = connection.cursor()
        for command in sql_commands:
            if command.strip() != '':
                cursor.execute(command)
        connection.commit()

# This function displays the menu in a given format 
def display_menu(menu_title, menu_items):
    max_length = max(len(item) for item in menu_items)
    box_width = max_length + 6

    print("+" + "-" * (box_width + 2) + "+")
    print("| {:^{width}} |".format(menu_title, width=box_width))
    print("+" + "-" * (box_width + 2) + "+")
    for index, item in enumerate(menu_items, start=1):
        if index>=10:
            print("| [{}] {:<{width}} |".format(index, item, width=max_length+1))
        else:
            print("| [{}] {:<{width}} |".format(index, item, width=max_length+2))
    print("+" + "-" * (box_width + 2) + "+")

# This function houses the options in main menu
def display_main_menu():
    menu_title = "MAIN MENU"
    menu_items = [
        "Food Establishment CRUD",
        "Food Item CRUD",
        "Food Review CRUD",
        "User CRUD",
        "Summary Reports",
        "Exit"
    ]
    display_menu(menu_title, menu_items)

# This function houses the options in food establishment submenu
def display_food_establishment_menu():
    menu_title = "MAIN MENU > FOOD ESTABLISHMENT CRUD"
    menu_items = [
        "Create Food Establishment",
        "Read All Food Establishments",
        "Read Certain Food Establishment",
        "Update Food Establishment",
        "Delete Food Establishment",
        "Back"
    ]
    display_menu(menu_title, menu_items)

# This function houses the options in food item submenu
def display_food_item_menu():
    menu_title = "MAIN MENU > FOOD ITEM CRUD"
    menu_items = [
        "Create Food Item",
        "Read All Food Items",
        "Read Certain Item",
        "Update Food Item",
        "Delete Food Item",
        "Back"
    ]
    display_menu(menu_title, menu_items)

# This function houses the options in food review submenu
def display_food_review_menu():
    menu_title = "MAIN MENU > FOOD REVIEW CRUD"
    menu_items = [
        "Create Food Review",
        "Read All Food Reviews",
        "Read Certain Food Review",
        "Update Food Review",
        "Delete Food Review",
        "Back"
    ]
    display_menu(menu_title, menu_items)


# This function houses the options in user submenu
def display_user_menu():
    menu_title = "MAIN MENU > USER CRUD"
    menu_items = [
        "Create User",
        "Read All Users",
        "Read Certain User",
        "Update User",
        "Delete User",
        "Back"
    ]
    display_menu(menu_title, menu_items)

# This function houses the options in generating reports submenu
def display_summary_reports_menu():
    menu_title = "MAIN MENU > Summary Reports"
    menu_items = [
        "View all food establishments",
        "View all food reviews for an establishment",
        "View all food reviews for a food item",
        "View all food items from an establishment",
        "View all food items from an establishment that belong to a food type",
        "View all reviews made within a month for an establishment",
        "View all reviews made within a month for an food item",
        "View all establishments with a high average rating",
        "View all food items from an establishment arranged according to price",
        "Search food items from any establishment based on a given price range",
        "Search food items from establishment based on a given food type",
        "Search food items from any establishment based on a given price range AND food type",
        "Back"
    ]
    display_menu(menu_title, menu_items)

# Main function initializes the display of menu
def main():
    # Connect to MySQL database
    load_dotenv() # Load .env file
    try:
        DB_HOST = os.getenv("DB_HOST")
        DB_USERNAME = os.getenv("DB_USERNAME")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD
        )

        # Execute SQL file
        execute_sql_file("dummydata.sql", connection)
    
        # Menu Program
        while True:
            display_main_menu()
            choice = input("Select an option: ")
            print("\n")

            if choice == '1':
                while True:
                    display_food_establishment_menu()
                    sub_choice = input("Select an option: ")
                    
                    # Create Food Establishment   
                    if sub_choice == '1':
                        input_establishment_name = input("Input establishment name to create: ")
                        food_establishment.create_food_establishment(connection, input_establishment_name)
                    
                    # Read All Food Establishments 
                    elif sub_choice == '2':
                        food_establishment.read_all_food_establishments(connection)
                    
                    # Read Certain Food Establishment/s                                
                    elif sub_choice == '3':
                        input_establishment_name = input("Input establishment name to read: ")
                        food_establishment.read_certain_food_establishments(connection, input_establishment_name)
                    
                    # Update Food Establishment
                    elif sub_choice == '4':
                        input_establishment_name = input("Input establishment name to change: ")
                        input_attribute = input("Input attribute of "+ input_establishment_name +" to be updated: ")
                        input_value = input("Input new "+ input_attribute +" value of " + input_establishment_name +": ")
                        food_establishment.update_food_establishment(connection, input_attribute, input_value, input_establishment_name)
                    
                    # Delete Food Establishment 
                    elif sub_choice == '5':
                        input_establishment_name = input("Input establishment name to delete: ")
                        food_establishment.delete_food_establishment(connection, input_establishment_name)
                    
                    # Back
                    elif sub_choice == '6':
                        break
                    else:
                        print("Invalid option. Please select again.")
                        
            elif choice == '2':
                while True:
                    display_food_item_menu()
                    sub_choice = input("Select an option: ")
                    
                    # Create Food Item 
                    if sub_choice == '1':
                        # Insert necessary input parameter statement here...
                        
                        food_item.create_food_item(connection)
                        
                    # Read All Food Items
                    elif sub_choice == '2':
                        # Insert necessary input parameter statement here...
                        
                        food_item.read_all_food_items(connection)
                        
                    # Read Certain Item
                    elif sub_choice == '3':
                        # Insert necessary input parameter statement here...
                        
                        food_item.read_certain_food_items(connection)
                        
                    # Update Food Item
                    elif sub_choice == '4':
                        # Insert necessary input parameter statement here...
                        
                        food_item.update_food_item(connection)
                        
                    # Delete Food Item
                    elif sub_choice == '5':
                        # Insert necessary input parameter statement here...
                        
                        food_item.delete_food_item(connection)
                        
                    # Break
                    elif sub_choice == '6':
                        break
                    else:
                        print("Invalid option. Please select again.")
                        
            elif choice == '3':
                while True:
                    display_food_review_menu()
                    sub_choice = input("Select an option: ")
                    
                    if sub_choice == '1':

                        review_type = input("Input review type: ")
                        review_message = input("Input review message: ")
                        review_date = input("Input review date (YYYY-MM-DD): ")
                        review_rating = input("Input review rating (1.00-5): ")
                        food_name = input("Input food name: ")
                        establishment_name = input("Input establishment name: ")
                        user_username = input("Input user username: ")
                        food_review.create_food_review(connection, review_type, review_message, review_date, review_rating, food_name, establishment_name, user_username)
                    
                    # Read All Food Reviews 
                    elif sub_choice == '2':
                     
                        food_review.read_all_food_reviews(connection)
                        
                    # Read Certain Food Review 
                    elif sub_choice == '3':
                        food_name = input("Input food name (leave blank if none): ")
                        establishment_name = input("Input food establishment (leave blank if none): ")
                        user_username = input("Input username (leave blank if none): ")
                        review_date = input("Input review date (leave blank if none): ")
                        food_review.read_certain_food_reviews(connection, food_name, user_username, establishment_name, review_date)
                        
                    # Update Food Review 
                    elif sub_choice == '4':
                        # Insert necessary input parameter statement here...
                        food_name = input("Input food name: ")
                        user_username = input("Input username: ")
                        establishment_name = input("Input establishment name: ")
                        review_date = input("Input review date: ")
                        input_attribute = input("Input attribute to change: ")
                        input_value = input("Input new value: ") 


                        food_review.update_food_review(connection, food_name, user_username, establishment_name, review_date, input_attribute, input_value)
                        
                    # Delete Food Review 
                    elif sub_choice == '5':
                        # Insert necessary input parameter statement here...
                        print("Delete Food Review: ")
                        user_username = input("Enter the username of the user who made the review (leave blank if none): ")
                        review_date = input("Enter review date (leave blank if none): ")
                        establishment_name = input("Enter establishment name (leave blank if none): ")
                        food_name = input("Enter food name (leave blank if none): ")
                        food_review.delete_food_review(connection, user_username, review_date, establishment_name, food_name)
                    
                    # Break 
                    elif sub_choice == '6':
                        break
                    else:
                        print("Invalid option. Please select again.")
            elif choice == '4':
                while True:
                    display_user_menu()
                    sub_choice = input("Select an option: ")
                    
                    # Create User 
                    if sub_choice == '1':
                        # Insert necessary input parameter statement here...
                        user_username = input("Input username: ")
                        user_password = input("Input password: ")
                        user.create_user(connection, user_username, user_password)
                        
                    # Read All Users
                    elif sub_choice == '2':
                        # Insert necessary input parameter statement here...
                        
                        user.read_all_users(connection)
                        
                    # Read Certain User
                    elif sub_choice == '3':
                        user_username = input("Input username of the user to be read: ")
                        # Insert necessary input parameter statement here...
                        
                        user.read_certain_user(connection, user_username)
                        
                    # Update User
                    elif sub_choice == '4':
                        # Insert necessary input parameter statement here...
                        input_attribute = input("Input attribute to be changed: ")
                        user_username = input("Input username of the user to be updated: ")
                        input_username = input(f"Input new {input_attribute} value of {user_username}: ")
                        user.update_user(connection, input_attribute, user_username, input_username)
                        
                    # Delete User
                    elif sub_choice == '5':
                        # Insert necessary input parameter statement here...
                        user_username = input("Input username: ")
                        review_date = input("Input review date:  ")
                        establishment_name = input("Input establishment name: ")
                        food_name = input("Input food name: ")

                        user.delete_user(connection, user_username, review_date, establishment_name, food_name)
                    
                    # Break    
                    elif sub_choice == '6':
                        break
                    else:
                        print("Invalid option. Please select again.")
            elif choice == '5':
                while True:
                    display_summary_reports_menu()
                    sub_choice = input("Select an option: ")
                    
                    # View all food establishments
                    if sub_choice == '1':
                        # Insert necessary input parameter statement here...
                        
                        summary_report.read_all_food_establishments(connection)
                    
                    # View all food reviews for an establishment
                    elif sub_choice == '2':
                        # Insert necessary input parameter statement here...
                        
                        summary_report.read_all_food_reviews_establishment(connection)
                        
                    # View all food reviews for a food item
                    elif sub_choice == '3':
                        # Insert necessary input parameter statement here...
                        
                        summary_report.read_all_food_reviews_item(connection)
                        
                    # View all food items from an establishment  
                    elif sub_choice == '4':
                        # Insert necessary input parameter statement here...
                        
                        summary_report.read_all_food_establishments(connection)
                        
                    # View all food items from an establishment that belong to a food type
                    elif sub_choice == '5':
                        
                        input_establishment_name = input("Input food establishment: ")
                        input_food_type = input(f"Input food type to search in {input_establishment_name}: ")
                        summary_report.read_all_food_items_establishment_foodtype(connection, input_establishment_name, input_food_type)
                        
                    # View all reviews made within a month for an establishment
                    elif sub_choice == '6':
                                                
                        input_establishment_name = input("Input food establishment: ")
                        input_month = input(f"Input month of reviews to search in {input_establishment_name}: ")
                        summary_report.read_all_food_reviews_establishment_month(connection, input_establishment_name, input_month)
                        
                    # View all reviews made within a month for an food item
                    elif sub_choice == '7':
                                                
                        input_food_item = input("Input food item: ")
                        input_month = input(f"Input month of reviews about {input_food_item}: ")
                        summary_report.read_all_food_reviews_establishment_month(connection, input_food_item, input_month)
                        
                    # View all establishments with a high average rating
                    elif sub_choice == '8':
                        # Insert necessary input parameter statement here...
                        
                        summary_report.read_all_food_establishments_highrating(connection)
                        
                    # View all food items from an establishment arranged according to price
                    elif sub_choice == '9':
                        # Insert necessary input parameter statement here...
                        
                        summary_report.read_all_food_items_establishment_orderprice(connection)
                        
                    # Search food items from any establishment based on a given price range
                    elif sub_choice == '10':
                        # Insert necessary input parameter statement here...
                        
                        summary_report.read_all_food_items_any_establishment_pricerange(connection)
                        
                    # Search food items from establishment based on a given food type
                    elif sub_choice == '11':
                        # Insert necessary input parameter statement here...
                        
                        summary_report.read_all_food_items_any_establishment_foodtype(connection)
                        
                    # Search food items from any establishment based on a given price range AND food type
                    elif sub_choice == '12':
                        # Insert necessary input parameter statement here...
                        
                        summary_report.read_all_food_items_any_establishment_pricerange_foodtype(connection)
                        
                    # Break 
                    elif sub_choice == '13':
                        break
                    else:
                        print("Invalid option. Please select again.")
            elif choice == '6':
                print("Exiting...")
                break
            else:
                print("Invalid option. Please select again.")
    
    except mysql.connector.Error as err:
        print("Error:", str(err))
        if err.errno == errorcode.CR_AUTH_PLUGIN_CANNOT_LOAD or err.errno == 1045: 
            print("Ensure you are using valid credentials.")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
