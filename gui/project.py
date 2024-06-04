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

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


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
        
        
        # create table
        self.table = CTkTable(self, row=10, column=5, width=250, hover=True)
        self.table.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(0, 0), sticky="nsew")

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
            print("diretso na yung pagoperate process")
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
            print("diretso na yung pagoperate process")
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
            print("diretso na yung pagoperate process")
        elif selected_value == "Read Certain User/s":
            self.read_certain_user_input_dialog_event()
        elif selected_value == "Update User":
            self.update_user_input_dialog_event()
        elif selected_value == "Delete User":
            self.delete_user_input_dialog_event()
            
    def dynamic_command_summary_report(self):
        selected_value = self.optionmenu_5.get()
        if selected_value == "View all food establishments":
            self.read_all_food_establishments_input_dialog_event()
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
        print("diretso na yung pagoperate process")
        # Insert process here
        food_establishment.read_all_food_establishments(self.connection)
        
    
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
        print("diretso na yung pagoperate process")
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
            
            # Insert process here
        else:
            print("Food name input was canceled")
    
    # Food Review Inputs
    def create_food_review_input_dialog_event(self):
        print("wait")
        
    def read_all_food_reviews_input_dialog_event(self):
        print("wait")
    
    def read_certain_food_review_input_dialog_event(self):
        print("wait")
    
    def update_food_review_input_dialog_event(self):
        print("wait")
    
    def delete_food_review_input_dialog_event(self):
        print("wait")
    
    # User Inputs
    def create_user_input_dialog_event(self):
        print("wait")
        
    def read_all_users_input_dialog_event(self):
        print("wait")
    
    def read_certain_user_input_dialog_event(self):
        print("wait")
    
    def update_user_input_dialog_event(self):
        print("wait")
    
    def delete_user_input_dialog_event(self):
        print("wait")
    
    # Summary Report Inputs
    def read_all_food_establishments_input_dialog_event(self):
        print("wait")
    
    def read_all_food_reviews_establishment_input_dialog_event(self):
        print("wait")
    
    def read_all_food_reviews_item_input_dialog_event(self):
        print("wait")
    
    def read_all_food_items_establishment_input_dialog_event(self):
        print("wait")
    
    def read_all_food_items_establishment_foodtype_input_dialog_event(self):
        print("wait")
    
    def read_all_food_reviews_establishment_month_input_dialog_event(self):
        print("wait")
    
    def read_all_food_reviews_item_month_input_dialog_event(self):
        print("wait")
    
    def read_all_food_establishments_highrating_input_dialog_event(self):
        print("wait")
    
    def read_all_food_items_establishment_orderprice_input_dialog_event(self):
        print("wait")
    
    def read_all_food_items_any_establishment_pricerange_input_dialog_event(self):
        print("wait")
    
    def read_all_food_items_any_establishment_foodtype_input_dialog_event(self):
        print("wait")
    
    def read_all_food_items_any_establishment_pricerange_foodtype_input_dialog_event(self):
        print("wait")

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
        connection.commit()
        cursor.close()


if __name__ == "__main__":
    app = App()
    app.mainloop()