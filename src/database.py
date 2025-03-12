import sqlite3

def setup_database():
    try:
        with sqlite3.connect('papers.db') as conn:
            # Set up DB
            sql = '''CREATE TABLE "papers" (
                  "uid" INTEGER PRIMARY KEY AUTOINCREMENT,
                  "id" varchar NOT NULL,
                  "title" varchar NOT NULL,
                  "uri" varchar NOT NULL
                  PRIMARY KEY ("uid")
                );'''
    
            # Create  a cursor
            cur = conn.cursor()

            # execute the INSERT statement
            cur.execute(sql)

            # commit the changes
            conn.commit()


    except sqlite3.Error as e:
        print(e)
