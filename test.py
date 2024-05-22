'''code to execute sql queries by Andi Dai 05/09'''
import sqlite3
#importing

DATABASE = 'pokemon.db'

def select_name_type():
#creating func
    with sqlite3.connect(DATABASE) as conn:
        #with statement
        cursor = conn.cursor()
        #creating cursor
        sql = "SELECT p.id, p.name, t1.name, t2.name from pokemon p JOIN type as t1 on p.type_1 = t1.type_id LEFT JOIN type as t2 on p.type_2 = t2.type_id;"
        #writing query
        cursor.execute(sql)
        results = cursor.fetchall()
        #executing and fetching
        for poke in results:
            if poke[2] is not None:
                if poke[3] is not None:
                    print(poke[0], poke[1], poke[2], poke[3])
                else:
                    print(poke[0], poke[1], poke[2])
            elif poke[3] is not None:
                print(poke[0], poke[1], poke[3])
            else:
                print(poke[0], poke[1])
        #printing results

if __name__ == "__main__":
    select_name_type()
