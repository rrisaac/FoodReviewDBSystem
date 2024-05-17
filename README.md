# Food Information System

This program delves into the SQL queries that power the CRUD operations within our food information system. We'll explore how these queries enable the creation, retrieval, modification, and deletion of data pertaining to food establishments, food items, food reviews, and users.

## Key Features

- **CRUD food establishments to the database.**
- **CRUD food items to the database.**
- **CRUD food reviews to the database.**
- **CRUD food users to the database.**
- **Use Python as the programming language to facilitate SQL database management system**
- **Handle database connection and error management.**

## Getting Started

### Prerequisites

- Python 3.x
- MySQL connector for Python
- MySQL database

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/FoodEstablishmentDBManager.git
    cd FoodEstablishmentDBManager
    ```

2. Install the required Python packages:
    ```bash
    pip install mysql-connector-python
    ```

### Configuration

1. Update the database configuration in your script:
    ```python
    connection = mysql.connector.connect(
        host="your_host",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    ```

### Usage

- To retrieve and display all food establishments:
    ```python
    read_all_food_establishments(connection)
    ```

- To add a new food establishment:
    ```python
    add_food_establishment(connection, name, type)
    ```

- To update an existing food establishment:
    ```python
    update_food_establishment(connection, id, name, type)
    ```

- To delete a food establishment:
    ```python
    delete_food_establishment(connection, id)
    ```

### Example

Here's an example of how to use the `read_all_food_establishments` function:

```python
import mysql.connector

def read_all_food_establishments(connection):
    print("\nReading all Food Establishments...")
    try:
        cursor = connection.cursor()
        
        # Fetch column names
        cursor.execute("SHOW COLUMNS FROM foodEstablishment")
        columns = [column[0] for column in cursor.fetchall()]
        
        # Fetch establishments
        cursor.execute("SELECT * FROM foodEstablishment;")
        establishments = cursor.fetchall()
        
        # If there are instances...
        if establishments:
            # Print headers
            print("{:<4}{:<20}{:<10}".format(columns[0], columns[1], columns[2]))
            print("-" * 34)
            
            # Print establishment data
            for establishment in establishments:
                print("{:<4}{:<20}{:<10}".format(establishment[0], establishment[1], establishment[2]))
            print("\n")
        # Else, empty set...
        else:
            print("\nNo Food Establishments found.\n")
    except mysql.connector.Error as err:
        print("\nError:", err)
        print("Failed to fetch Food Establishments.\n")

# Example connection
connection = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="your_database"
)

# Example usage
read_all_food_establishments(connection)

## Contributors

- **Rey Isaac Jr.**
- **Beatrice Elaine Capule**
- **Klenn Jakek Borja**

