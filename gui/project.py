import tkinter
import tkinter.messagebox
import customtkinter
from CTkTable import *

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

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
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="Inspect Data")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, fg_color="#b30000", hover_color="#800303",command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Source SQL File")
        self.entry.grid(row=3, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text= "Upload SQL Dummy Data")
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

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Food Establishment"), dynamic_resizing=False, width=280,
                                                        values=["Create Food Establishment", "Read All Food Establishments", "Read Certain Food Establishment/s", "Update Food Establishment", "Delete Food Establishment",])
        self.optionmenu_1.grid(row=0, column=0, padx=30, pady=(20, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Food Establishment"), text="Open Input Dialog",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=0, column=1, padx=30, pady=(20, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Food Item"), text="CTkLabel on Food Item")
        self.label_tab_2.grid(row=0, column=0, padx=10, pady=20)
        
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

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()