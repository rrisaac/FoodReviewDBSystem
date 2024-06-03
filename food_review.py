import mysql.connector
import project
# Add parameters if necessary.
# Be verbose: Display all necessary data to explicitly state what's being done. Check food_establishment.py for reference.

# Create Food Review
def create_food_review(connection, review_message, review_date, review_rating, food_name, establishment_name, user_username):
    try:
        if establishment_name is None or establishment_name.strip() == "":
            print("You can't create a food review not associated to an establishment.") # No food and establishment
            return
        elif food_name is None or food_name.strip() == "":
            review_type = 0 # If there is no food
            query = """
            INSERT INTO foodReview(review_type, review_message, review_date, review_rating, review_foodestablishmentid, review_userid)
            VALUES (
                %s, %s, %s, %s,
                (SELECT establishment_id FROM foodEstablishment WHERE establishment_name = %s),
                (SELECT user_id FROM user WHERE user_username = %s)
            );
            """
            params = [review_type, review_message, review_date, review_rating, establishment_name, user_username]
        else:
            review_type = 1  # If both food and establishment is specified
            query = """
            INSERT INTO foodReview(review_type, review_message, review_date, review_rating, review_fooditemid, review_userid)
            VALUES (
                %s, %s, %s, %s,
                (SELECT food_id from foodItem where food_name = %s),
                (SELECT user_id FROM user WHERE user_username = %s)
            );
            """
            params = [review_type, review_message, review_date, review_rating, food_name, user_username]

        cursor = connection.cursor()
        cursor.execute(query, tuple(params))
        project.update_average_rating(connection)
        connection.commit()
        print("Food review created successfully.")
    
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to create Food Review.\n")
        

# Read All Food Reviews
def read_all_food_reviews(connection):
    try: 
        print("\nReading all food reviews...")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM foodreview;")
        foodreviews = cursor.fetchall()
        if foodreviews:
            print("\n")
            for foodreview in foodreviews:
                    print(foodreview)
                    print("\n")
        else:
            print("There are currently no food reviews.")
        print("Food reviews read successfully.")
        
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to read Food Reviews.\n")


# Read Certain Review/s
def read_certain_food_reviews(connection, food_name, user_username, establishment_name, review_date):
    try:
        print("\nReading certain food review...")
        # 1=1 is there to act like a placeholder
        query = "SELECT * FROM foodReview WHERE 1=1"
        # Array that contains the parameters
        params = [] 
        
        if user_username is not None and user_username.strip() != "":
            query += " AND review_userid = (SELECT user_id FROM user WHERE user_username = %s)"
            params.append(user_username)
        
        if food_name is not None and food_name.strip() != "":
            query += " AND review_fooditemid = (SELECT food_id FROM foodItem WHERE food_name = %s)"
            params.append(food_name)
        
        if establishment_name is not None and establishment_name.strip() != "":
            query += " AND review_foodestablishmentid = (SELECT establishment_id FROM foodEstablishment WHERE establishment_name = %s)"
            params.append(establishment_name)

        if review_date is not None and review_date.strip() != "":
            query += " AND review_date = (SELECT review_date from foodreview WHERE review_date = %s)"
            params.append(review_date)

        # Add a semicolon to end the query
        query += ";"  
        # print(query) # debug
        cursor = connection.cursor()
        # Cursor takes in a query, and an array of parameters
        cursor.execute(query, tuple(params))
        foodreviews = cursor.fetchall()

        # If foodreviews exist
        if foodreviews:
            for foodreview in foodreviews:
                print(foodreview)
        else:
            print("There exist no food reviews.")

    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to retreive a certain food review")

# Update Food Review
def update_food_review(connection, food_name, user_username, establishment_name, review_date, input_attribute, input_value):
    try:
        print("\nUpdating food review...")
        # This checks whether an additional query is needed or not.
        if food_name and food_name.strip() != "":
            added_query = """(review_foodestablishmentid = (SELECT establishment_id FROM foodEstablishment WHERE establishment_name = %s)
            OR review_fooditemid = (SELECT food_id FROM foodItem WHERE food_name = %s))"""
            params = [input_value, user_username, review_date, 0 if food_name is None else 1, establishment_name, food_name]
        else:
            added_query = "(review_foodestablishmentid = (SELECT establishment_id FROM foodEstablishment WHERE establishment_name = %s))"
            params = [input_value, user_username, review_date, 0 if food_name is None else 1, establishment_name]
        
        
        # Query that takes in a dynamic attribute
        query = """
            UPDATE foodReview
            SET {} = %s
            WHERE review_userid = (SELECT user_id FROM user WHERE user_username = %s)
            AND review_date = %s
            AND review_type = %s
            AND {};
        """.format(input_attribute, added_query) # Format according to the dynamic attribute and the additional query

        cursor = connection.cursor()
        cursor.execute(query, tuple(params))
        
        # Error handling to check if an update happened:
        if cursor.rowcount == 0:
            print("No rows were affected.")
            connection.commit()
            return
        
        project.update_average_rating(connection)
        connection.commit()
        print("Food review updated successfully.")
    
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Unable to update food review")


# Delete Food Review 
def delete_food_review(connection, user_username, review_date, establishment_name, food_name):
    try:
        print("\nDeleting food review...")
        query = "DELETE FROM foodreview WHERE 1=1"
        params = [user_username, review_date, establishment_name, food_name]
        params_query = [
            "review_userid = (SELECT user_id FROM user WHERE user_username = %s)",
            "review_date = (SELECT review_date from foodreview WHERE review_date = %s)",
            "review_foodestablishmentid = (SELECT establishment_id from foodestablishment WHERE establishment_name = %s)",
            "review_fooditemid = (SELECT food_id from fooditem WHERE food_name = %s)",
        ]
        if((establishment_name != "" and establishment_name is not None) and (food_name != "" and food_name is not None)):
            params.remove(establishment_name)
            params_query.pop(2)
        placeholder = params.copy()

        # This adds parameters in the query
        for x  in range(0,(len(params))):
            if params[x] is not None and params[x] != "":
                query += " AND {}".format(params_query[x])
            else:
                # Remove params if it is empty
                placeholder.remove(params[x])

        params = placeholder # Replace the old params with the updated params
        query += ";"
        cursor = connection.cursor()
        cursor.execute(query, params)
        if cursor.rowcount == 0:
            print("No deletions occurred.")
            connection.commit()
            return

        project.update_average_rating(connection)
        connection.commit()
        print("Food review deleted successfully.")
    
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to delete food review")
