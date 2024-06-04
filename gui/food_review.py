import mysql.connector
import project
# Add parameters if necessary.
# Be verbose: Display all necessary data to explicitly state what's being done. Check food_establishment.py for reference.

# Create Food Review
def create_food_review(connection, review_message, review_date, review_rating, food_name, establishment_name, user_username):
    try:
        cursor = connection.cursor(buffered=True)
        if establishment_name is None or establishment_name.strip() == "":
            print("You can't create a food review not associated to an establishment.") # No food and establishment
            return
        elif food_name is None or food_name.strip() == "":
            # Check if the establishment exists
            query = "SELECT establishment_name FROM foodEstablishment WHERE establishment_name = %s;"
            cursor.execute(query, (establishment_name,))
            result = cursor.fetchone()
            if result is None:
                print("Please input a valid establishment name.")
                return (query % (establishment_name,))
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
            query = """
            SELECT food_name
            FROM foodItem
            WHERE food_foodestablishmentid = (
                SELECT establishment_id
                FROM foodestablishment
                WHERE establishment_name = %s
            );
            """
            cursor.execute(query, (establishment_name,))

            result = cursor.fetchone()
            print(result)
            if result is None:
                print("Please input a food name that is associated to an establishment.")
                return (query % (establishment_name,))
            
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

        cursor.execute(query, tuple(params))
        project.update_average_rating(connection)
        connection.commit()
        print("Food review created successfully.")
        return(query % tuple(params))
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to create Food Review.\n")
        

# Read All Food Reviews
def read_all_food_reviews(connection):
    try: 
        print("\nReading all food reviews...")
        cursor = connection.cursor()
        query = "SELECT * FROM foodreview;"
        cursor.execute(query)

        foodreviews = cursor.fetchall()
        if foodreviews:
            print("\n")
            for foodreview in foodreviews:
                    print(foodreview)
                    print("\n")
        else:
            print("There are currently no food reviews.")
            return (query, [])
        
        print("Food reviews read successfully.")
        return (query, foodreviews)
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
        print(foodreviews)
        # If foodreviews exist
        if foodreviews:
            for foodreview in foodreviews:
                print(foodreview)
        else:
            print("There exist no food reviews.")
            return (query, [])
        
        return(query % tuple(params), foodreviews)
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to retreive a certain food review")

# Update Food Review
def update_food_review(connection, food_name, user_username, establishment_name, review_date, input_attribute, input_value):
    try:
        cursor = connection.cursor()
        print("\nUpdating food review...")
        # Verify if the user exists
        query = "SELECT user_id FROM user WHERE user_username = %s"
        cursor.execute(query, (user_username,))
        user_id = cursor.fetchone()
        if user_id is None:
            print("User does not exist")
            return (query % (user_username,))

        
        # This checks whether an additional query is needed or not.
        if food_name and food_name.strip() != "":
            # Verify if the establishment and the food item exist
            query = "SELECT establishment_id FROM foodEstablishment WHERE establishment_name = %s"
            params = [establishment_name]
            cursor.execute(query, tuple(params))

            establishment_id = cursor.fetchone()
            if establishment_id is None:
                print("Establishment does not exist")
                return (query % tuple(params))
            # Check if food exists
            query = "SELECT food_id FROM foodItem WHERE food_name = %s AND food_foodestablishmentid = %s"
            params = [food_name, establishment_id[0]]
            cursor.execute(query, tuple(params))
            food_id = cursor.fetchone()
            if food_id is None:
                print("Food Item does not exist in the specified establishment")
                return (query % tuple(params))

            added_query = "(review_fooditemid = (SELECT food_id FROM foodItem WHERE food_name = %s)"
            params = [input_value, user_username, review_date, 1, food_name]
        else:
            # Check if the establishment exists
            query = "SELECT establishment_name FROM foodEstablishment WHERE establishment_name = %s"
            params = [establishment_name]
            cursor.execute(query, tuple(params))
            result = cursor.fetchone()
            if result is None:
                print("Please input a valid establishment name.")
                return (query % tuple(params))

            added_query = "(review_foodestablishmentid = (SELECT establishment_id FROM foodEstablishment WHERE establishment_name = %s))"
            params = [input_value, user_username, review_date, 0, establishment_name]
        
        
        # Query that takes in a dynamic attribute
        query = """
            UPDATE foodReview
            SET {} = %s
            WHERE review_userid = (SELECT user_id FROM user WHERE user_username = %s)
            AND review_date = %s
            AND review_type = %s
            AND {};
        """.format(input_attribute, added_query) # Format according to the dynamic attribute and the additional query

        print(query)
        
        cursor.execute(query, tuple(params))
        
        # Error handling to check if an update happened:
        if cursor.rowcount == 0:
            print("No rows were affected.")
            connection.commit()
            return (query % tuple(params))
        
        project.update_average_rating(connection)
        connection.commit()
        print("Food review updated successfully.")
        return (query % tuple(params))
    
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
            return (query % tuple(params))

        project.update_average_rating(connection)
        connection.commit()
        print("Food review deleted successfully.")
        return (query % tuple(params))
    
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to delete food review")
