import mysql.connector

# View all food establishments
def read_all_food_establishments(connection):
    print("\nViewing all food establishments...")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM foodEstablishment;")
        establishments = cursor.fetchall()

        if establishments:
            print("\n")
            for establishment in establishments:
                print(establishment)
            print("\n")
        else:
            print("\nNo food establishments found.\n")

    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch food establishments.\n")
    
# View all food reviews for an establishment
def read_all_food_reviews_establishment(connection):
    print("\nViewing all food reviews for an establishment...")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM foodReview WHERE review_foodestablishmentid = %s;", (establishment_id,))
        reviews = cursor.fetchall()

        if reviews:
            print("\n")
            for review in reviews:
                print(review)
            print("\n")
        else:
            print("\nNo food reviews found for this establishment.\n")

    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch food reviews.\n")
    
# View all food reviews for a food item
def read_all_food_reviews_item(connection, food_item_id):
    print("\nViewing all food reviews for a food item...")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM foodReview WHERE review_fooditemid = %s;", (food_item_id,))
        reviews = cursor.fetchall()

        if reviews:
            print("\n")
            for review in reviews:
                print(review)
            print("\n")
        else:
            print("\nNo food reviews found for this food item.\n")

    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch food reviews.\n")
    
# View all food items from an establishment 
def read_all_food_items_establishment(connection):
    print("\nViewing all food items from an establishment...")
    # Insert python-sql query logic here
    
# View all food items from an establishment that belong to a food type
def read_all_food_items_establishment_foodtype(connection, establishment_name, food_type):
    print(f"\nViewing all food items from \"{establishment_name}\" that belong to food type \"{food_type}\"...")
    # Insert python-sql query logic here
    
    # Constructing the SQL query
    query = f"""
    SELECT * FROM foodItem
    WHERE (food_type LIKE '%{food_type}%')
    AND (food_foodestablishmentid = (
        SELECT establishment_id FROM foodEstablishment
        WHERE establishment_name = "{establishment_name}"
    ));
    """
        
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Fetching the results
        results = cursor.fetchall()
        
        # If there are instances...
        if results:
            print("\n")
            for row in results:
                print(row)
            print("\n")
        
        # Else, empty set...
        else:
            print(f"\nNo food items found from \"{establishment_name}\" that belong to food type \"{food_type}\".\n")
    
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch food items.\n")
    
    
# View all reviews made within a month for an establishment
def read_all_food_reviews_establishment_month(connection, establishment_name, month):
    print(f"\nViewing all reviews made within {month} for \"{establishment_name}\"...")

    # Constructing the SQL query
    query = f"""
    SELECT * FROM foodReview 
    WHERE review_foodestablishmentid = 
        (SELECT establishment_id FROM foodEstablishment 
        WHERE establishment_name = "{establishment_name}") 
        AND MONTH(review_date) =  MONTH(STR_TO_DATE('{month}', '%M'
    ));
    """
        
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Fetching the results
        results = cursor.fetchall()
        
        # If there are instances...
        if results:
            print("\n")
            for row in results:
                print(row)
            print("\n")
        
        # Else, empty set...
        else:
            print(f"\nNo food reviews found from \"{establishment_name}\" during {month}.\n")
    
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch food reviews.\n")
    
# View all reviews made within a month for an food item
def read_all_food_reviews_item_month(connection, food_item, month):
    print(f"\nViewing all \"{food_item}\" reviews during {month}...")
    
    # Constructing the SQL query
    query = f"""
    SELECT * FROM foodReview 
    WHERE review_fooditemid = 
        (SELECT food_id FROM foodItem 
        WHERE food_name = '{food_item}') 
        AND MONTH(review_date) =  MONTH(STR_TO_DATE('{month}', '%M'
    ));
    """

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        
        # Fetching the results
        results = cursor.fetchall()
        
        # If there are instances...
        if results:
            print("\n")
            for row in results:
                print(row)
            print("\n")
        
        # Else, empty set...
        else:
            print(f"\nNo food reviews about \"{food_item}\" during {month}.\n")
    
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch food reviews.\n")
    
# View all establishments with a high average rating
def read_all_food_establishments_highrating(connection):
    try:
        query = "SELECT * FROM foodestablishment WHERE establishment_averagerating >= 4;"
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            for result in results:
                print(result, "\n")
        else:
            print("There are currently no food establishments with a high (>=4) average rating") 
       
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch food establishments.")

    # Insert python-sql query logic here
    
# View all food items from an establishment arranged according to price
def read_all_food_items_establishment_orderprice(connection, establishment_name):
    try:
        print("\nViewing all food items from an establishment arranged according to price...")
        query = "SELECT * FROM fooditem WHERE food_foodestablishmentid = (SELECT establishment_id FROM foodestablishment WHERE establishment_name = %s) ORDER BY food_price;"
        cursor = connection.cursor()
        cursor.execute(query,(establishment_name,))
        results = cursor.fetchall()

        if results:
            for result in results:
                print("\n", result)
        else:
            print(f"There are currently no food items in the specified establishment '{establishment_name}'")
            
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch food items from an establishment according to food price.")
    # Insert python-sql query logic here
    
# Search food items from any establishment based on a given price range
def read_all_food_items_any_establishment_pricerange(connection, establishment_name, min_price, max_price):
    try:
        print("\nSearching food items from any establishment based on a given price range...")
        query = "SELECT * FROM fooditem WHERE food_foodestablishmentid = (SELECT establishment_id FROM foodestablishment WHERE establishment_name = %s) AND (food_price BETWEEN %s AND %s);"
        cursor = connection.cursor()
        cursor.execute(query, (establishment_name, min_price, max_price))
        results = cursor.fetchall()
        if results:
            for result in results:
                print("\n", result)
        else:
            print(f"Failed to fetch food items from an establishment '{establishment_name}' from food price {min_price} to {max_price}.")

    except mysql.connector.Error as err:
        print("\nError:", err)
        print(f"Failed to retrieve any food items in establishment {establishment_name} with specified food price {min_price} to {max_price}")
    # Insert python-sql query logic here
    
# Search food items from establishment based on a given food type
def read_all_food_items_any_establishment_foodtype(connection, establishment_name, food_type):
    try:
        print("\nSearching food items from establishment based on a given food type...")
        query = f"SELECT * FROM fooditem WHERE food_foodestablishmentid = (SELECT establishment_id FROM foodestablishment WHERE establishment_name = %s) AND (food_type LIKE '%{food_type}%');"
        cursor = connection.cursor()
        cursor.execute(query, (establishment_name,))
        results = cursor.fetchall()
        if results:
            for result in results:
                print("\n", result)
        else:
            print(f"Failed to fetch food items from an establishment '{establishment_name}' with food type {food_type}")

    except mysql.connector.Error as err:
        print("\nError:", err)
        print(f"Failed to retrieve any food items in establishment {establishment_name} with specified food type {food_type}")
    
# Search food items from any establishment based on a given price range AND food type
def read_all_food_items_any_establishment_pricerange_foodtype(connection, establishment_name, min_price, max_price, food_type):
    try:
        print("\nSearching food items from any establishment based on a given price range AND food type...")
        query = f"SELECT * FROM fooditem WHERE food_foodestablishmentid = (SELECT establishment_id FROM foodestablishment WHERE establishment_name = %s) AND (food_price BETWEEN %s AND %s) AND (food_type LIKE '%{food_type}%');"
        cursor = connection.cursor()
        cursor.execute(query, (establishment_name, min_price, max_price))
        results = cursor.fetchall()
        if results:
            for result in results:
                print("\n", result)
        else:
            print(f"Failed to fetch food items from an establishment '{establishment_name}' from food price {min_price} to {max_price} with food type {food_type}.")

    except mysql.connector.Error as err:
        print("\nError:", err)
        print(f"Failed to retrieve any food items in establishment {establishment_name} with specified food price {min_price} to {max_price} with food type {food_type}")
    # Insert python-sql query logic here
