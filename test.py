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
            poke_info = [poke[0], poke[1]]
            for i in range(2, len(poke)):
                if poke[i] is not None:
                    poke_info.append(poke[i])
            print(poke_info)
        #printing results



if __name__ == "__main__":
    select_name_type()
