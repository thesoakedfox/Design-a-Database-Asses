'''code to execute sql queries by Andi Dai 05/09'''
import sqlite3
#importing

DATABASE = 'pokemon.db'

def fetch_all_data():
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
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

fetch_all_data()

def select_name_type():
#creating func
    with sqlite3.connect(DATABASE) as conn:
        #with statement
        cur = conn.cursor()
        #creating cursor
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
    fetch_all_data()
               