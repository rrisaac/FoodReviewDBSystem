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

        connection.commit()
        print("Food review read successfully.")

    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to read Food Reviews.\n")


# Read Certain Review/s
def read_certain_food_review(connection):
    print("\nReading certain food review...")
    # Insert python-sql query logic here

# Update Food Review
def update_food_review(connection):
    print("\nUpdating food review...")
    # Insert python-sql query logic here

# Delete Food Review 
def delete_food_review(connection):
    print("\nDeleting food review...")
    # Insert python-sql query logic here
