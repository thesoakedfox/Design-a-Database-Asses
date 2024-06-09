'''code to execute sql queries by Andi Dai 05/09'''
import sqlite3
#importing

DATABASE = 'pokemon.db'

ADMIN_USERNAME = 'OSS'
ADMIN_PASSWORD = 'BOSS'
STOP_COMMAND = 'stop'
DATABASE = 'pokemon.db'

YN = ['y', 'n']


def admin_login():
    username = input("Please enter username(OSS): ")
    password = input("Please enter password(BOSS): ")
    
    if username.upper()== ADMIN_USERNAME and password.upper() == ADMIN_PASSWORD:
        print("Login successful!")
        return True
    else:
        print("Invalid credentials. Access denied.")
        return False
    
def get_table_definition(DATABASE, table):
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info('{table}')")
        table_info = cur.fetchall()
        if table_info:
            print(f"Table '{table}' definition:")
            for column in table_info:
                print(f"Column ID: {column[0]}, Name: {column[1]}, Type: {column[2]}, Not Null: {column[3]}, Default Value: {column[4]}, Primary Key: {column[5]}")
        else:
            print(f"Table '{table}' does not exist.")

def ask_for_table_input():
    print("You will now be asked to input some info for the table you are creating (type 'stop' at anytime to cancel table creation)")
    table = input("Enter table name: ")
    if table.lower() == STOP_COMMAND:
        print("Cancelling table creation.")
        return None, None
    

    columns = {}
    primary_key = False
    
    while True:
        col_name = input("Enter column name (leave blank to finish): ")
        if col_name.lower() == STOP_COMMAND:
            print("Cancelling table creation.")
            return None, None
        elif not col_name:
            break

        col_def = input(f"Enter data type for column '{col_name}': ").upper()
        if col_def.lower() == STOP_COMMAND:
            print("Cancelling table creation.")
            return None, None
        while col_def.lower() not in ['int', 'integer', 'text', 'real', 'blob']:
            print("Invalid data type.\nTypes allowed are: INT, INTEGER, TEXT, REAL, BLOB")
            col_def = input(f"Enter data type for column '{col_name}': ")
            if col_def.lower() == STOP_COMMAND:
                print("Cancelling table creation.")
                return None, None

        allow_null = input(f"Should column '{col_name}' allow null values? (Y/N): ")
        if allow_null.lower() == STOP_COMMAND:
                print("Cancelling table creation.")
                return None, None
        while allow_null.lower() not in YN:
            print("Invalid input. Please enter 'Y' or 'N'.")
            allow_null = input(f"Should column '{col_name}' allow null values? (Y/N): ")
            if allow_null.lower() == STOP_COMMAND:
                print("Cancelling table creation.")
                return None, None
        if allow_null.lower() == 'n':
            col_def += " NOT NULL"

        is_unique = input(f"Should column '{col_name}' be unique? (Y/N): ")
        if is_unique.lower()== STOP_COMMAND:
                print("Cancelling table creation.")
                return None, None
        while is_unique.lower() not in YN:
            print("Invalid input. Please enter 'Y' or 'N'.")
            is_unique = input(f"Should column '{col_name}' be unique? (Y/N): ")
            if is_unique.lower()== STOP_COMMAND:
                print("Cancelling table creation.")
                return None, None
        if is_unique.lower() == 'y':
            col_def += " UNIQUE"

        if not primary_key:
            is_primary_key = input(f"Is column '{col_name}' a primary key? (Y/N): \n")
            if is_primary_key.lower()== STOP_COMMAND:
                    print("Cancelling table creation.")
                    return None, None
            while is_primary_key.lower() not in YN:
                print("Invalid input. Please enter 'Y' or 'N'.")
                is_primary_key = input(f"Is column '{col_name}' a primary key? (Y/N): ")
                if is_primary_key.lower()== STOP_COMMAND:
                    print("Cancelling table creation.")
                    return None, None
            if is_primary_key.lower() == 'y':
                col_def += " PRIMARY KEY"
                primary_key = True
     
        foreign_key = input(f"Is column '{col_name}' a foreign key? (Y/N): ")
        if foreign_key.lower()== STOP_COMMAND:
                print("Cancelling table creation.")
                return None, None
        while foreign_key.lower() not in YN:
            print("Invalid input. Please enter 'Y' or 'N'.")
            foreign_key = input(f"Is column '{col_name}' a foreign key? (Y/N): ")
            if foreign_key.lower()== STOP_COMMAND:
                print("Cancelling table creation.")
                return None, None
        if foreign_key.lower() == 'y':
            while True:
                ref_table = input(f"Enter the referenced table for the foreign key: ")
                if ref_table.lower()== STOP_COMMAND:
                  print("Cancelling table creation.")
                  return None, None
                ref_column = input(f"Enter the referenced column for the foreign key: ")
                if ref_column.lower()== STOP_COMMAND:
                    print("Cancelling table creation.")
                    return None, None
                try:
                    # Check if the referenced table and column exist in the database
                    with sqlite3.connect(DATABASE) as conn:
                        cur = conn.cursor()
                        cur.execute(f"PRAGMA table_info('{ref_table}')")
                        table_info = cur.fetchall()
                        if not any(ref_column == col[1] for col in table_info):
                            raise ValueError(f"Column '{ref_column}' does not exist in table '{ref_table}'")
                        break  
                except Exception as e:
                    print("Error:", e)
                    continue
            col_def += f" REFERENCES {ref_table}({ref_column})"
        columns[col_name] = col_def
    
    if not columns:
        print("No columns defined. Cancelling table creation.")
        return None, None
    
    return table, columns

def create_table(DATABASE, table, columns):
    if table is None or columns is None:
        print("Table creation cancelled.")
        return
    #check if table exists and drop/add new according to need
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name= ? ", (table,))
        if cur.fetchone():
            print(f"Table '{table}' already exists.")
            print("1. Drop the existing and create a new table")
            print("2. Add new columns to the existing table")
            print("3. Cancel table creation")
            userinput = input("Enter your choice (1-3): ")
            
            if userinput == '1':
                cur.execute(f"DROP TABLE IF EXISTS {table}")
                with sqlite3.connect(DATABASE) as conn:
                    cur = conn.cursor()
                    # Query to get all table names
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cur.fetchall()
                    if tables:
                        print("List of tables currently in the database:")
                        for table in tables:
                            print(table[0])
                print(f"Table '{table}' dropped.")
            elif userinput == '2':
                for col_name, col_def in columns.items():
                    try:
                        cur.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_def}")
                        print(f"Column '{col_name}' added to table '{table}'.")
                    except sqlite3.OperationalError as e:
                        print(f"Error adding column '{col_name}':", e)
                        conn.rollback
                conn.commit()
                cur.execute(f"SELECT * FROM ")
                print(f"Table '{table}' updated successfully.")
                get_table_definition(DATABASE, table)
                return
            elif userinput == '3':
                print("Table creation cancelled.")
                return
            else:
                print("Invalid input. Table creation cancelled.")
    print("\nTable Name:", table)
    print("Columns:")
    for col_name, col_def in columns.items():
        print(f"- {col_name}: {col_def}")
    confirmation = input("Do you want to proceed with table creation? (Y/N): ")
    while confirmation not in YN:
        print("Invalid input. Please enter 'Y' or 'N'.")
        confirmation = input("Do you want to proceed with table creation? (Y/N): ")
    if confirmation.lower() != 'y':
        print("Table creation cancelled.")
        return None, None
    
    q_table = f'"{table}"'
    columns_def = ", ".join([f'"{col_name}" {col_def}' for col_name, col_def in columns.items()])
    sql = f'''CREATE TABLE {q_table} ({columns_def});'''
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        if not cur:
            raise Exception('Connection failed.')
        else:
            try:
                cur.executescript(sql)
                conn.commit()
                print(f"Table '{table}' created successfully.")
            except sqlite3.Error as e:
                print("An error occurred:", e)
                conn.rollback()










def add_data():
    pass
    
#function to fetch all data    
def fetch_all_data():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        if not cur:
            raise Exception('Connection failed.')
        else: print("Connected")
        
        sql = '''SELECT p.id, p.name, p.total_stat, p.hp, p.atk, p.def, p.sp_atk, p.sp_def, p.spd, p.gen, p.legend, t1.name, t2.name 
                 FROM pokemon p 
                 JOIN type as t1 on p.type_1 = t1.type_id 
                 LEFT JOIN type as t2 on p.type_2 = t2.type_id;'''
        cur.execute(sql)
        results = cur.fetchall()
        #print the results
        print_table(results)



# Function to print data 
def print_table(data):  
    print("+------+---------------------------+-------------+-----+-----+-----+--------+--------+-----+-----+--------+----------+----------+")
    print("|  ID  |            Name           | Total Stat  |  HP | ATK | DEF | Sp.Atk | Sp. Def| SPD | GEN | LEGEND |  Type 1  |  Type 2  |")
    print("+------+---------------------------+-------------+-----+-----+-----+--------+--------+-----+-----+--------+----------+----------+")
    
    # Data rows
    for row in data:
        type_1 = row[-2] if row[-2] else "-"
        type_2 = row[-1] if row[-1] else "-"
        row = row[:-2] + (type_1, type_2)
        print("| {:<4} | {:<25} | {:<11} | {:<3} | {:<3} | {:<3} | {:<6} | {:<6} | {:<3} | {:<3} | {:<6} | {:<8} | {:<8} |".format(*row))
    print("+------+---------------------------+-------------+-----+-----+-----+--------+--------+-----+-----+--------+----------+----------+")

#function to select name and type
def select_name_type():
#creating func
    with sqlite3.connect(DATABASE) as conn:
        #with statement
        cur = conn.cursor()
        #creating cursor
        if not cur:
            raise Exception('Connection failed.')
        else: print("Connected")
        sql = '''
        SELECT p.id, p.name, t1.name, t2.name FROM pokemon p 
        JOIN type as t1 on p.type_1 = t1.type_id 
        LEFT JOIN type as t2 on p.type_2 = t2.type_id;
        '''
        #writing query
        cur.execute(sql)
        results = cur.fetchall()
        #executing and fetching
        print("+------+-----------------+---------------+---------------+")
        print("|  ID  |      Name       |    Type 1     |    Type 2     |")
        print("+------+-----------------+---------------+---------------+")
        for poke in results:
            id_, name, type_1, type_2 = poke
            type_1 = type_1 if type_1 else "-"
            type_2 = type_2 if type_2 else "-"
            print(f"| {id_:<4} | {name:<25} | {type_1:<9} | {type_2:<9} |")
        print("+------+---------------------------+-----------+-----------+")
        #printing results


#main code
def main():
    while True:
        print("\nWhat would you like to do?")
        print("1. Admin Login")
        print("2. Create a new table(Admin Only)")
        print("3. Add data to a table")
        print("4. Fetch all data")
        print("5. Select name and type(to be refined)")
        print("6. Exit\n")
        userinput = input('')

        if userinput == '1':
            if admin_login():
                print("Logged in as admin.")
        elif userinput == '2':
            if admin_login():
                table, columns = ask_for_table_input()
                if table is None or columns is None:
                    continue
                create_table(DATABASE, table, columns)
            
                
        elif userinput == '3':
            add_data()
        elif userinput == '4':
            fetch_all_data()
        elif userinput == '':
            select_name_type()
        elif userinput == '':
            print("Exited.")
            break
        else:
            print("Invalid input. Please enter a number between 1 and 5.")
if __name__ == "__main__":
    main()
               