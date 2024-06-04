import sys
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import tkinter
import tkinter.messagebox
from tkinter import filedialog, messagebox
import customtkinter
from CTkTable import *
import food_establishment
import user
import food_item
import food_review
import summary_report
import datetime
import tkinter as tk
from tkinter import ttk


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def update_average_rating(connection):
        try:
            cursor = connection.cursor()

            # Calculate average rating for each establishment
            cursor.execute("""
                SELECT review_foodestablishmentid, AVG(review_rating) AS avg_rating
                FROM foodReview
                WHERE review_type = 0
                GROUP BY review_foodestablishmentid
            """)
            establishment_ratings = cursor.fetchall()

            # Update average rating for each establishment
            for establishment_id, avg_rating in establishment_ratings:
                cursor.execute("""
                    UPDATE foodEstablishment
                    SET establishment_averagerating = %s
                    WHERE establishment_id = %s
                """, (avg_rating, establishment_id))

            cursor.execute("""
                SELECT review_fooditemid, AVG(review_rating) AS avg_rating
                FROM foodReview
                WHERE review_type = 1
                GROUP BY review_fooditemid
            """)
            fooditem_ratings = cursor.fetchall()

            # Update average rating for each food item
            for food_id, avg_rating in fooditem_ratings:
                cursor.execute("""
                    UPDATE foodItem
                    SET food_averagerating = %s
                    WHERE food_id = %s
                """, (avg_rating, food_id))

            print("Average ratings updated successfully!")

        except mysql.connector.Error as err:
            connection.rollback()
            print("Error updating average ratings:", err)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Load .env file
        load_dotenv()

        # Database connection setup
        try:
            DB_HOST = os.getenv("DB_HOST")
            DB_USERNAME = os.getenv("DB_USERNAME")
            DB_PASSWORD = os.getenv("DB_PASSWORD")
            self.connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USERNAME,
                password=DB_PASSWORD
            )
            
            if self.connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

        # configure window
        self.title("FoodReviewDBSystem")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="FoodRevPH", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="About")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="Refresh Ratings")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, fg_color="#b30000", hover_color="#800303",command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Source SQL File")
        self.entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text= "Upload SQL Dummy Data", command=self.upload_sql_file)
        self.main_button_1.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250,  height=100, font=customtkinter.CTkFont(size=12, weight="bold"))
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=500, height=100)
        self.tabview.grid(row=0, column=(2), padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Food Establishment")
        self.tabview.add("Food Item")
        self.tabview.add("Food Review")
        self.tabview.add("User")
        self.tabview.add("Summary Report")
        
        self.tabview.tab("Food Establishment").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Food Item").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Food Review").grid_columnconfigure(0, weight=1)
        self.tabview.tab("User").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Summary Report").grid_columnconfigure(0, weight=1)

        # Options in Food Establishment Dropdown
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Food Establishment"), dynamic_resizing=False, width=280,
                                                        values=["Create Food Establishment", "Read All Food Establishments", "Read Certain Food Establishment/s", "Update Food Establishment", "Delete Food Establishment",])
        self.optionmenu_1.grid(row=0, column=0, padx=30, pady=(20, 10))
        # Input Button Food Establishment
        self.string_input_button_1 = customtkinter.CTkButton(self.tabview.tab("Food Establishment"), text="Execute",
                                                           command=self.dynamic_command_food_establishment)
        self.string_input_button_1.grid(row=0, column=1, padx=30, pady=(20, 10))
        
        # Options in Food Items Dropdown
        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.tabview.tab("Food Item"), dynamic_resizing=False, width=280,
                                                        values=["Create Food Item", "Read All Food Items", "Read Certain Food Item/s", "Update Food Item", "Delete Food Item",])
        self.optionmenu_2.grid(row=0, column=0, padx=30, pady=(20, 10))
        # Input Button Food Items
        self.string_input_button_2 = customtkinter.CTkButton(self.tabview.tab("Food Item"), text="Execute",
                                                           command=self.dynamic_command_food_item)
        self.string_input_button_2.grid(row=0, column=1, padx=30, pady=(20, 10))
        
        # Options in Food Reviews Dropdown
        self.optionmenu_3 = customtkinter.CTkOptionMenu(self.tabview.tab("Food Review"), dynamic_resizing=False, width=280,
                                                        values=["Create Food Review", "Read All Food Reviews", "Read Certain Food Review/s", "Update Food Review", "Delete Food Review",])
        self.optionmenu_3.grid(row=0, column=0, padx=30, pady=(20, 10))
        # Input Button Food Reviews
        self.string_input_button_3 = customtkinter.CTkButton(self.tabview.tab("Food Review"), text="Execute",
                                                           command=self.dynamic_command_food_review)
        self.string_input_button_3.grid(row=0, column=1, padx=30, pady=(20, 10))
        
        # Options in Users Dropdown
        self.optionmenu_4 = customtkinter.CTkOptionMenu(self.tabview.tab("User"), dynamic_resizing=False, width=280,
                                                        values=["Create User", "Read All Users", "Read Certain User/s", "Update User", "Delete User",])
        self.optionmenu_4.grid(row=0, column=0, padx=30, pady=(20, 10))
        # Input Button Users
        self.string_input_button_4 = customtkinter.CTkButton(self.tabview.tab("User"), text="Execute",
                                                           command=self.dynamic_command_user)
        self.string_input_button_4.grid(row=0, column=1, padx=30, pady=(20, 10))
        
        # Options in Summary Reports Dropdown
        self.optionmenu_5 = customtkinter.CTkOptionMenu(self.tabview.tab("Summary Report"), dynamic_resizing=False, width=280,
                                                        values=["View all food establishments",
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
                                                                "Search food items from any establishment based on a given price range AND food type",])
        self.optionmenu_5.grid(row=0, column=0, padx=30, pady=(20, 10))
        # Input Summary Reports
        self.string_input_button_5 = customtkinter.CTkButton(self.tabview.tab("Summary Report"), text="Execute",
                                                           command=self.dynamic_command_summary_report)
        self.string_input_button_5.grid(row=0, column=1, padx=30, pady=(20, 10))
        
        self.table_frame = ttk.Frame(self)
        self.table_frame.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(0, 0), sticky="nsew")
        # Create a canvas inside the frame
        self.canvas = tk.Canvas(self.table_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Add a scrollbar to the canvas
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # Create another frame inside the canvas
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        # Make the inner frame expand with the canvas
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        # Create the table inside the inner frame
        # self.table = CTkTable(self.inner_frame, row=30, column=5, width=250, hover=True)
        # self.table.grid(row=0, column=0, padx=(20, 20), pady=(0, 0), sticky="nsew")
        # Assuming self.inner_frame is already defined and is a valid Frame
        

        # Setting the column headings
        # self.table.heading("Column1", text="Lexeme")
        # self.table.heading("Column2", text="Classification")
        # self.table.heading("Column3", text="Lexeme")
        # self.table.heading("Column4", text="Classification")
        # self.table.heading("Column5", text="Lexeme")
        # self.table.heading("Column6", text="Classification")
        # self.table.heading("Column7", text="Lexeme")
        # self.table.heading("Column8", text="Classification")

        #
        
        
        # # create table
        # self.table = CTkTable(self, row=10, column=5, width=250, hover=True)
        # self.table.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(0, 0), sticky="nsew")
                

        query = f"""
        SELECT * FROM foodItem
        WHERE (food_type LIKE '%meat%')
        AND (food_foodestablishmentid = (
            SELECT establishment_id FROM foodEstablishment
            WHERE establishment_name = “Pizza Hut”
        ));
        """
    
        # set default values
        self.sidebar_button_3.configure(text="Reset")
        # self.appearance_mode_optionemenu.set("Dark")
        # self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("Create Food Establishment")
        self.textbox.insert("0.0", "SQL Query\n" + query + "\n\n")
       
        
    def dynamic_command_food_establishment(self):
        selected_value = self.optionmenu_1.get()
        if selected_value == "Create Food Establishment":
            self.create_food_establishment_input_dialog_event()
        elif selected_value == "Read All Food Establishments":
            self.read_all_food_establishments_input_dialog_event()
        elif selected_value == "Read Certain Food Establishment/s":
            self.read_certain_food_establishment_input_dialog_event()
        elif selected_value == "Update Food Establishment":
            self.update_food_establishment_input_dialog_event()
        elif selected_value == "Delete Food Establishment":
            self.delete_food_establishment_input_dialog_event()
            
    def dynamic_command_food_item(self):
        selected_value = self.optionmenu_2.get()
        if selected_value == "Create Food Item":
            self.create_food_item_input_dialog_event()
        elif selected_value == "Read All Food Items":
            self.read_all_food_items_input_dialog_event()
        elif selected_value == "Read Certain Food Item/s":
            self.read_certain_food_establishment_input_dialog_event()
        elif selected_value == "Update Food Item":
            self.update_food_establishment_input_dialog_event()
        elif selected_value == "Delete Food Item":
            self.delete_food_establishment_input_dialog_event()
        
    def dynamic_command_food_review(self):
        selected_value = self.optionmenu_3.get()
        if selected_value == "Create Food Review":
            self.create_food_review_input_dialog_event()
        elif selected_value == "Read All Food Reviews":
            self.read_all_food_reviews_input_dialog_event()
        elif selected_value == "Read Certain Food Review/s":
            self.read_certain_food_review_input_dialog_event()
        elif selected_value == "Update Food Review":
            self.update_food_review_input_dialog_event()
        elif selected_value == "Delete Food Review":
            self.delete_food_review_input_dialog_event()
        
    def dynamic_command_user(self):
        selected_value = self.optionmenu_4.get()
        if selected_value == "Create User":
            self.create_user_input_dialog_event()
        elif selected_value == "Read All Users":
            self.read_all_users_input_dialog_event()
        elif selected_value == "Read Certain User/s":
            self.read_certain_user_input_dialog_event()
        elif selected_value == "Update User":
            self.update_user_input_dialog_event()
        elif selected_value == "Delete User":
            self.delete_user_input_dialog_event()
            
    def dynamic_command_summary_report(self):
        selected_value = self.optionmenu_5.get()
        if selected_value == "View all food establishments":
            self.read_all_food_establishments_input_dialog_event_2()
        elif selected_value == "View all food reviews for an establishment":
            self.read_all_food_reviews_establishment_input_dialog_event()
        elif selected_value == "View all food reviews for a food item":
            self.read_all_food_reviews_item_input_dialog_event()
        elif selected_value == "View all food items from an establishment":
            self.read_all_food_items_establishment_input_dialog_event()
        elif selected_value == "View all food items from an establishment that belong to a food type":
            self.read_all_food_items_establishment_foodtype_input_dialog_event()
        elif selected_value == "View all reviews made within a month for an establishment":
            self.read_all_food_reviews_establishment_month_input_dialog_event()
        elif selected_value == "View all reviews made within a month for an food item":
            self.read_all_food_reviews_item_month_input_dialog_event()
        elif selected_value == "View all establishments with a high average rating":
            self.read_all_food_establishments_highrating_input_dialog_event()
        elif selected_value == "View all food items from an establishment arranged according to price":
            self.read_all_food_items_establishment_orderprice_input_dialog_event()
        elif selected_value == "Search food items from any establishment based on a given price range":
            self.read_all_food_items_any_establishment_pricerange_input_dialog_event()
        elif selected_value == "Search food items from establishment based on a given food type":
            self.read_all_food_items_any_establishment_foodtype_input_dialog_event()
        elif selected_value == "Search food items from any establishment based on a given price range AND food type":
            self.read_all_food_items_any_establishment_pricerange_foodtype_input_dialog_event()

    # Date Validation
    def validate_date(date_str):
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    

    # Food Establishment Inputs
    def create_food_establishment_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name to create:", title="Create Food Establishment")
        establishment_name = establishment_name_dialog.get_input()
        
        if establishment_name:
            print(f"Establishment Name: {establishment_name}")
            # Insert process here
        else:
            print("Establishment name input was canceled")
        
    def read_all_food_establishments_input_dialog_event(self):
        # Insert process here
        tabledata = food_establishment.read_all_food_establishments(self.connection)
        print(tabledata)
        
        # Create the Treeview table
        self.table = ttk.Treeview(self.inner_frame, columns=("Column1", "Column2", "Column3"), show="headings")
        
        # Define the headings for each column
        self.table.heading("Column1", text="Establishment ID")
        self.table.heading("Column2", text="Establishment Name")
        self.table.heading("Column3", text="Establishment Average Rating")
        
        # Insert the fetched data into the table
        for row in tabledata:
            self.table.insert("", "end", values=row)
        
        # Pack the table into the inner_frame
        self.table.pack(expand=True, fill='both')
        
        self.stretch_table()
        
    
    def read_certain_food_establishment_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name to read:", title="Create Food Establishment")
        establishment_name = establishment_name_dialog.get_input()
        
        if establishment_name:
            print(f"Establishment Name: {establishment_name}")
            # Insert process here
        else:
            print("Establishment name input was canceled")
        
    def update_food_establishment_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name to read:", title="Update Food Establishment") 
        establishment_name = establishment_name_dialog.get_input()
        
        if establishment_name:
            attribute_dialog = customtkinter.CTkInputDialog(text="Input attribute to update:", title="Update Food Establishment")         
            attribute = attribute_dialog.get_input()
            
            if attribute:
                value_dialog = customtkinter.CTkInputDialog(text="Input attribute to update:", title="Update Food Establishment")         
                value = value_dialog.get_input()
                    
                if value: 
                    print(f"Establishment Name: {establishment_name}")
                    print(f"Attribute: {attribute}")
                    print(f"Value: {value}")
                    # Insert process here
                else:
                    print("Value input was canceled")
            else:
                print("Attribute input was canceled")
        else:
            print("Establishment name input was canceled")
    
    def delete_food_establishment_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name to delete:", title="Delete Food Establishment")
        establishment_name = establishment_name_dialog.get_input()
        
        if establishment_name:
            print(f"Establishment Name: {establishment_name}")
            # Insert process here
        else:
            print("Establishment name input was canceled")
        
    # Food Item Inputs
    def create_food_item_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name of food item:", title="Create Food Item")
        establishment_name = establishment_name_dialog.get_input()
        
        if establishment_name:
            food_name_dialog = customtkinter.CTkInputDialog(text="Input food name:", title="Create Food Item ")
            food_name = food_name_dialog.get_input()
            
            if food_name:
                food_type_dialog = customtkinter.CTkInputDialog(text="Input food type (if possible, separate types through commas ','):", title="Create Food Item ")
                food_type = food_type_dialog.get_input()
                
                if food_type:
                    price_dialog = customtkinter.CTkInputDialog(text="Input price:", title="Create Food Item ")
                    price = price_dialog.get_input()
                    
                    if price:
                        print(f"Establishment Name: {establishment_name}")
                        print(f"Food name: {food_name}")
                        print(f"Food type: {food_type}")
                        print(f"Price: {price}")
                        
                        # Insert process here
                    else:
                        print("Price input was canceled")
                else:
                    print("Food type input was canceled")   
            else:
                print("Food name input was canceled")
        else:
            print("Establishment name input was canceled")
        
    def read_all_food_items_input_dialog_event(self):
        # Insert process here
        food_establishment.read_all_food_establishments(self.connection)
    
    def read_certain_food_items_input_dialog_event(self):
        food_name_dialog = customtkinter.CTkInputDialog(text="Input food name:", title="Read Certain Food Item/s")
        food_name = food_name_dialog.get_input()
        
        if food_name:
            food_name_dialog = customtkinter.CTkInputDialog(text="Input food name:", title="Read Certain Food Item/s")
            food_name = food_name_dialog.get_input()
            print(f"Food name: {food_name}")
            
            # Insert process here
        else:
            print("Food name input was canceled")
            
    def update_food_item_input_dialog_event(self):
        food_name_dialog = customtkinter.CTkInputDialog(text="Input food name:", title="Update Food Item")
        food_name = food_name_dialog.get_input()
            
        if food_name:
            attribute_dialog = customtkinter.CTkInputDialog(text="Input attribute to update:", title="Update Food Item")
            attribute = attribute_dialog.get_input()
            
            if attribute:
                value_dialog = customtkinter.CTkInputDialog(text="Input attribute to update:", title="Update Food Item")         
                value = value_dialog.get_input()
                    
                if value: 
                    print(f"Establishment Name: {food_name}")
                    print(f"Attribute: {attribute}")
                    print(f"Value: {value}")
                    # Insert process here
                else:
                    print("Value input was canceled")
            else:
                print("Attribute input was canceled")
        else:
            print("Food name input was canceled")        
                
    def delete_food_item_input_dialog_event(self):
        food_name_dialog = customtkinter.CTkInputDialog(text="Input food name:", title="Delete Food Item")
        food_name = food_name_dialog.get_input()
        
        if food_name:
            food_name_dialog = customtkinter.CTkInputDialog(text="Input food name:", title="Delete Food Item")
            food_name = food_name_dialog.get_input()
            print(f"Food name: {food_name}")
            
            
        else:
            print("Food name input was canceled")
    
    # Food Review Inputs
    def create_food_review_input_dialog_event(self):
        user_username_dialog = customtkinter.CTkInputDialog(text="Input user name:", title="Create Food Review")
        user_username = user_username_dialog.get_input()
        if user_username:
            establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name:", title="Create Food Review")
            establishment_name = establishment_name_dialog.get_input()
            if establishment_name:
                food_name_dialog = customtkinter.CTkInputDialog(text="Input food name (leave blank if none):", title="Create Food Review")
                food_name = food_name_dialog.get_input()
                if food_name or food_name.strip() == "":
                    rating_dialog = customtkinter.CTkInputDialog(text="Input rating (between 1.00 and 5.00):", title="Create Food Review")
                    rating = rating_dialog.get_input()
                    while True:
                        try:
                            rating_float = float(rating)
                            if rating_float >= 1.00 and rating_float <= 5.00:
                                break
                            else:
                                rating_dialog = customtkinter.CTkInputDialog(text="Invalid rating. Please enter a number between 1.00 and 5.00.", title="Create Food Review")
                                rating = rating_dialog.get_input()
                                continue
                        except ValueError:
                            rating_dialog = customtkinter.CTkInputDialog(text="Invalid rating. Please enter a number between 1.00 and 5.00.", title="Create Food Review")
                            rating = rating_dialog.get_input()
                            continue
                    comment_dialog = customtkinter.CTkInputDialog(text="Input comment:", title="Create Food Review")
                    comment = comment_dialog.get_input()
                    if comment:
                        date_dialog = customtkinter.CTkInputDialog(text="Input date (yyyy-mm-dd):", title="Create Food Review")
                        review_date = date_dialog.get_input()
                        while True:
                            if review_date.strip() == "" or review_date is None:
                                break
                            elif not App.validate_date(review_date):
                                review_date = customtkinter.CTkInputDialog(text="Invalid date format. Please enter in YYYY-MM-DD format.", title="Create Food Review").get_input()
                                continue
                            else:
                                break
                        print(f"User Name: {user_username}")
                        print(f"Establishment Name: {establishment_name}")
                        print(f"Food name: {food_name}")
                        print(f"Rating: {rating}")
                        print(f"Comment: {comment}")
                        print(f"Date: {review_date}")
                        # Insert the thing here
                        food_review.create_food_review(self.connection, comment, review_date, rating, food_name, establishment_name, user_username)

                    else:
                        print("Comment input was canceled")
                else:
                    print("Food name input was canceled")
            else:
                print("Establishment name input was canceled")
        else:
            print("User name input was canceled")




        
    def read_all_food_reviews_input_dialog_event(self):
        # Insert process here
        food_review.read_all_food_reviews(self.connection)
    
    def read_certain_food_review_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name to read:", title="Read Certain Food Review/s")
        establishment_name = establishment_name_dialog.get_input()
        if establishment_name:
            food_name_dialog = customtkinter.CTkInputDialog(text="Input food name to read:", title="Read Certain Food Review/s")
            food_name = food_name_dialog.get_input()
            if food_name:
                username_dialog = customtkinter.CTkInputDialog(text="Input username to read:", title="Read Certain Food Review/s")
                username = username_dialog.get_input()
                if username:
                    date_dialog = customtkinter.CTkInputDialog(text="Input date to read (yyyy-mm-dd):", title="Read Certain Food Review/s")
                    review_date = date_dialog.get_input()
                    while True:
                        if review_date.strip() == "" or review_date is None:
                            break
                        elif not App.validate_date(review_date):
                            review_date = customtkinter.CTkInputDialog(text="Invalid date format. Please enter in YYYY-MM-DD format.", title="Read Certain Food Review/s").get_input()
                            continue
                        else:
                            break
                    print(f"Establishment Name: {establishment_name}")
                    print(f"Food name: {food_name}")
                    print(f"User Name: {username}")
                    print(f"Date: {review_date}")
                    # Insert the thing here
                    food_review.read_certain_food_reviews(self.connection, food_name, username, establishment_name, review_date)
                    
                else:
                    print("Username input was canceled")
            else:
                print("Food name input was canceled")
        else:
            print("Establishment name input was canceled")

    
    def update_food_review_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name to update:", title="Update Food Review")
        establishment_name = establishment_name_dialog.get_input()
        if establishment_name:
            food_name_dialog = customtkinter.CTkInputDialog(text="Input food name to update (leave blank if none):", title="Update Food Review")
            food_name = food_name_dialog.get_input()
            if food_name or food_name == "":
                username_dialog = customtkinter.CTkInputDialog(text="Input username to update:", title="Update Food Review")
                username = username_dialog.get_input()
                if username:
                    date_dialog = customtkinter.CTkInputDialog(text="Input review date (YYYY-MM-DD):", title="Update Food Review")
                    date_str = date_dialog.get_input()
                    while True:
                        if date_str.strip() == "" or date_str is None:
                            break
                        elif not App.validate_date(date_str):
                            date_str = customtkinter.CTkInputDialog(text="Invalid date format. Please enter in YYYY-MM-DD format.", title="Update Food Review").get_input()
                            continue
                        else:
                            break
                    input_attribute_dialog = customtkinter.CTkInputDialog(text="Input attribute to change:", title="Update Food Review")
                    input_attribute = input_attribute_dialog.get_input()
                    if input_attribute:
                        input_value_dialog = customtkinter.CTkInputDialog(text="Input new value:", title="Update Food Review")
                        input_value = input_value_dialog.get_input()
                        if input_value:
                            food_review.update_food_review(self.connection, food_name, username, establishment_name, date_str, input_attribute, input_value)
                            print("Food review updated successfully.")
                        else:
                            print("Input value input was canceled")
                    else:
                        print("Input attribute input was canceled")
                else:
                    print("Username input was canceled")
            else:
                print("Food name input was canceled")
        else:
            print("Establishment name input was canceled")



    
    def delete_food_review_input_dialog_event(self):
        user_username_dialog = customtkinter.CTkInputDialog(text="Enter the username of the user who made the review (leave blank if none):", title="Delete Food Review")
        user_username = user_username_dialog.get_input()
        while True:
            review_date_dialog = customtkinter.CTkInputDialog(text="Input review date (YYYY-MM-DD; leave blank if none):", title="Delete Food Review")
            review_date = review_date_dialog.get_input()

            if review_date.strip() == "" or review_date is None:
                break
            elif not App.validate_date(review_date):
                review_date_dialog = customtkinter.CTkInputDialog(text="Invalid date format. Please enter in YYYY-MM-DD format.", title="Delete Food Review")
                continue
            else:
                break
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Enter establishment name (leave blank if none):", title="Delete Food Review")
        establishment_name = establishment_name_dialog.get_input()
        food_name_dialog = customtkinter.CTkInputDialog(text="Enter food name (leave blank if none):", title="Delete Food Review")
        food_name = food_name_dialog.get_input()
        food_review.delete_food_review(self.connection, user_username, review_date, establishment_name, food_name)
    
    # User Inputs
    def create_user_input_dialog_event(self):
        user_username_dialog = customtkinter.CTkInputDialog(text="Input username:", title="Create User")
        user_username = user_username_dialog.get_input()
        if user_username:
            user_password_dialog = customtkinter.CTkInputDialog(text="Input password:", title="Create User")
            user_password = user_password_dialog.get_input()
            if user_password:
                user.create_user(self.connection, user_username, user_password)
            else:
                print("Input password input was canceled")
        else:
            print("Input username input was canceled")

        
    def read_all_users_input_dialog_event(self):
        # Insert process here
        user.read_all_users(self.connection)
    
    def read_certain_user_input_dialog_event(self):
        user_username_dialog = customtkinter.CTkInputDialog(text="Input username:", title="Read Certain User")
        user_username = user_username_dialog.get_input()
        if user_username:
            user.read_certain_user(self.connection, user_username)
        else:
            print("Input username input was canceled")
    
    def update_user_input_dialog_event(self):
        input_attribute_dialog = customtkinter.CTkInputDialog(text="Input attribute to be changed: ", title="Update User")
        input_attribute = input_attribute_dialog.get_input()
        if input_attribute:
            user_username_dialog = customtkinter.CTkInputDialog(text="Input username of the user to be updated: ", title="Update User")
            user_username = user_username_dialog.get_input()
            if user_username:
                input_username_dialog = customtkinter.CTkInputDialog(text=f"Input new {input_attribute} value of {user_username}: ", title="Update User")
                input_username = input_username_dialog.get_input()
                if input_username:
                    user.update_user(self.connection, input_attribute, user_username, input_username)
                else:
                    print("Input username input was canceled")
            else:
                print("Input username input was canceled")
        else:
            print("Input attribute input was canceled")

    
    def delete_user_input_dialog_event(self):
        user_username_dialog = customtkinter.CTkInputDialog(text="Input username:", title="Delete User")
        user_username = user_username_dialog.get_input()
        if user_username:
            user.delete_user(self.connection, user_username)
        else:
            print("Input username input was canceled")


    
    # Summary Report Inputs
    def read_all_food_establishments_input_dialog_event_2(self):
        summary_report.read_all_food_establishments(self.connection)
    
    def read_all_food_reviews_establishment_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name:", title="Read All Food Reviews for an Establishment")
        establishment_name = establishment_name_dialog.get_input()
        if establishment_name:
            summary_report.read_all_food_reviews_establishment(self.connection, establishment_name)
        else:
            print("Input establishment name input was canceled")

    def read_all_food_reviews_item_input_dialog_event(self):
        food_name_dialog = customtkinter.CTkInputDialog(text="Input food name:", title="Read All Food Reviews for a Food Item")
        food_name = food_name_dialog.get_input()
        if food_name:
            summary_report.read_all_food_reviews_item(self.connection, food_name)
        else:
            print("Input food name input was canceled")

    def read_all_food_items_establishment_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name:", title="Read All Food Items for an Establishment")
        establishment_name = establishment_name_dialog.get_input()
        if establishment_name:
            summary_report.read_all_food_items_establishment(self.connection, establishment_name)
        else:
            print("Input establishment name input was canceled")

    def read_all_food_items_establishment_foodtype_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name:", title="Read All Food Items for an Establishment")
        establishment_name = establishment_name_dialog.get_input()
        if establishment_name:
            food_type_dialog = customtkinter.CTkInputDialog(text="Input food type:", title="Read All Food Items for an Establishment")
            food_type = food_type_dialog.get_input()
            if food_type:
                summary_report.read_all_food_items_establishment_foodtype(self.connection, establishment_name, food_type)
            else:
                print("Input food type input was canceled")
        else:
            print("Input establishment name input was canceled")

    
    def read_all_food_reviews_establishment_month_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name:", title="Read All Food Reviews for an Establishment within a Month")
        establishment_name = establishment_name_dialog.get_input()
        if establishment_name:
            month_dialog = customtkinter.CTkInputDialog(text="Input month of reviews to search in {}: ".format(establishment_name), title="Read All Food Reviews for an Establishment within a Month")
            month = month_dialog.get_input()
            if month:
                summary_report.read_all_food_reviews_establishment_month(self.connection, establishment_name, month)
            else:
                print("Input month input was canceled")
        else:
            print("Input establishment name input was canceled")

    def read_all_food_reviews_item_month_input_dialog_event(self):
        food_item_dialog = customtkinter.CTkInputDialog(text="Input food item:", title="Read All Food Reviews for a Food Item within a Month")
        food_item = food_item_dialog.get_input()
        if food_item:
            month_dialog = customtkinter.CTkInputDialog(text=f"Input month of reviews about {food_item}: ", title="Read All Food Reviews for a Food Item within a Month")
            month = month_dialog.get_input()
            if month:
                summary_report.read_all_food_reviews_item_month(self.connection, food_item, month)
            else:
                print("Input month input was canceled")
        else:
            print("Input food item input was canceled")

    
    def read_all_food_establishments_highrating_input_dialog_event(self):
        summary_report.read_all_food_establishments_highrating(self.connection)


    
    def read_all_food_items_establishment_orderprice_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Input establishment name:", title="View All Food Items from an Establishment Arranged According to Price")
        establishment_name = dialog.get_input()
        if establishment_name:
            summary_report.read_all_food_items_establishment_orderprice(self.connection, establishment_name)
        else:
            print("Input establishment name input was canceled")
    
    def read_all_food_items_any_establishment_pricerange_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name:", title="Search Food Items from any Establishment based on a given price range")
        establishment_name = establishment_name_dialog.get_input()
        if establishment_name:
            min_price_dialog = customtkinter.CTkInputDialog(text="Input minimum price:", title="Search Food Items from any Establishment based on a given price range")
            min_price = min_price_dialog.get_input()
            if min_price:
                max_price_dialog = customtkinter.CTkInputDialog(text="Input maximum price:", title="Search Food Items from any Establishment based on a given price range")
                max_price = max_price_dialog.get_input()
                if max_price:
                    try:
                        min_price = float(min_price)
                        max_price = float(max_price)
                        if min_price > max_price:
                            print("Minimum price must be less than or equal to maximum price")
                        elif max_price > 9999.99:
                            print("Maximum price must be less than or equal to 9999.99")
                        else:
                            summary_report.read_all_food_items_any_establishment_pricerange(self.connection, establishment_name, min_price, max_price)
                    except ValueError:
                        print("Please enter a valid number for price")
                else:
                    print("Input maximum price input was canceled")
            else:
                print("Input minimum price input was canceled")
        else:
            print("Input establishment name input was canceled")

    
    def read_all_food_items_any_establishment_foodtype_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name:", title="Search Food Items from establishment based on a given food type")
        establishment_name = establishment_name_dialog.get_input()
        if establishment_name:
            food_type_dialog = customtkinter.CTkInputDialog(text="Input food type:", title="Search Food Items from establishment based on a given food type")
            food_type = food_type_dialog.get_input()
            if food_type:
                summary_report.read_all_food_items_any_establishment_foodtype(self.connection, establishment_name, food_type)
            else:
                print("Input food type input was canceled")
        else:
            print("Input establishment name input was canceled")
    
    def read_all_food_items_any_establishment_pricerange_foodtype_input_dialog_event(self):
        establishment_name_dialog = customtkinter.CTkInputDialog(text="Input establishment name:", title="Search Food Items from any Establishment based on a given price range AND food type")
        establishment_name = establishment_name_dialog.get_input()
        if establishment_name:
            min_price_dialog = customtkinter.CTkInputDialog(text="Input minimum price:", title="Search Food Items from any Establishment based on a given price range AND food type")
            min_price = min_price_dialog.get_input()
            if min_price:
                max_price_dialog = customtkinter.CTkInputDialog(text="Input maximum price:", title="Search Food Items from any Establishment based on a given price range AND food type")
                max_price = max_price_dialog.get_input()
                if max_price:
                    food_type_dialog = customtkinter.CTkInputDialog(text="Input food type:", title="Search Food Items from any Establishment based on a given price range AND food type")
                    food_type = food_type_dialog.get_input()
                    if food_type:
                        try:
                            min_price = float(min_price)
                            max_price = float(max_price)
                            if min_price > max_price:
                                print("Minimum price must be less than or equal to maximum price")
                            elif max_price > 9999.99:
                                print("Maximum price must be less than or equal to 9999.99")
                            else:
                                summary_report.read_all_food_items_any_establishment_pricerange_foodtype(self.connection, establishment_name, min_price, max_price, food_type)
                        except ValueError:
                            print("Please enter a valid number for price")
                    else:
                        print("Input food type input was canceled")
                else:
                    print("Input maximum price input was canceled")
            else:
                print("Input minimum price input was canceled")
        else:
            print("Input establishment name input was canceled")



    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
    def upload_sql_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("SQL Files", "*.sql")])
        if file_path:
            filename = os.path.basename(file_path)
            self.entry.delete(0, customtkinter.END)
            self.entry.insert(0, filename)
            try:
                self.execute_sql_file(file_path, self.connection)
                messagebox.showinfo("Success", "SQL file executed successfully.")
            except Error as e:
                messagebox.showerror("Error", f"Failed to execute SQL file: {e}")

    def execute_sql_file(self, file_path, connection):
        with open(file_path, 'r') as file:
            sql = file.read()
        
        cursor = connection.cursor()
        for statement in sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        update_average_rating(connection)
        connection.commit()
        cursor.close()
            
    def stretch_table(self):
        #Setting the columns to stretch and fill the available space
        for col in self.table["columns"]:
            self.table.column(col, width=100, stretch=True)

        # Placing the table to expand and fill available space
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Ensure the inner_frame expands with its parent widget if needed
        self.inner_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()