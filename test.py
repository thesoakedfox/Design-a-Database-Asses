'''code to execute sql queries by Andi Dai 05/09'''
import sqlite3
#importing

DATABASE = 'pokemon.db'

ADMIN_USERNAME = 'OSS'
ADMIN_PASSWORD = 'BOSS'

DATABASE = 'pokemon.db'

YN = ['y', 'n']


def admin_login():
    username = input("Please enter username(OSS): ")
    password = input("Please enter password(BOSS): ")
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login successful!")
        return True
    else:
        print("Invalid credentials. Access denied.")
        return False
    
def create_table(DATABASE, table, columns):

    table = input("Enter table name: ")

    columns = {}
    
    while True:
        col_name = input("Enter column name (leave blank to finish): ")
        if not col_name:
            break
        col_def = input(f"Enter data type for column '{col_name}': ")

        while True:
            allow_null = input(f"Should column '{col_name}' allow null values? (Y/N): ")
            if allow_null.lower() in YN:
                break
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

        if allow_null.lower() == 'n':
            col_def += " NOT NULL"

        while True:
            is_unique = input(f"Should column '{col_name}' be unique? (Y/N): ")
            if is_unique.lower() in YN:
                break
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")

        if is_unique.lower() == 'y':
           col_def += " UNIQUE"



    q_table = f'"{table}"'
    columns_def = ", ".join([f'"{col_name}" {col_def}' for col_name, col_def in columns.items()])
    sql = f'''
    DROP TABLE IF EXISTS {q_table};
    CREATE TABLE {q_table} ({columns_def});'''
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        if not cur:
            raise Exception('Connection failed.')
        else:
            print("Connected")
            cur.executemany(sql)
            conn.commit()
            print(f"Table '{table}' created successfully.")
        









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
        sql = '''SELECT p.id, p.name, t1.name, t2.name FROM pokemon
           p JOIN type as t1 on p.type_1 = t1.type_id LEFT JOIN type
            as t2 on p.type_2 = t2.type_id;'''
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

if __name__ == "__main__":
    create_table()
               