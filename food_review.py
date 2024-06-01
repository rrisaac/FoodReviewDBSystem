import mysql.connector

# Add parameters if necessary.
# Be verbose: Display all necessary data to explicitly state what's being done. Check food_establishment.py for reference.

# Create Food Review
def create_food_review(connection, review_type, review_message, review_date, review_rating, food_name, establishment_name, user_username):
    try:
        print("\nCreating food review...")
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO foodReview(review_type, review_message, review_date, review_rating, review_fooditemid, review_foodestablishmentid, review_userid)
            VALUES (
                %s, %s, %s, %s,
                (SELECT food_id FROM foodItem WHERE food_name = %s),
                (SELECT establishment_id FROM foodEstablishment WHERE establishment_name = %s),
                (SELECT user_id FROM user WHERE user_username = %s)
            )
        """, (review_type, review_message, review_date, review_rating, food_name, establishment_name, user_username))
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
def update_food_review(connection):
    print("\nUpdating food review...")
    # Insert python-sql query logic here

# Delete Food Review 
def delete_food_review(connection):
    print("\nDeleting food review...")
    # Insert python-sql query logic here
