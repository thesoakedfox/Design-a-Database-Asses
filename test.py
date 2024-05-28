'''code to execute sql queries by Andi Dai 05/09'''
import sqlite3
#importing

DATABASE = 'pokemon.db'

def select_name_type():
#creating func
    with sqlite3.connect(DATABASE) as conn:
        #with statement
        cur = conn.cursor()
        #creating cursor
        sql = '''SELECT p.id, p.name, t1.name, t2.name from pokemon
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
        print("+------+-----------------+---------------+---------------+")

        #printing results



if __name__ == "__main__":
    select_name_type()
