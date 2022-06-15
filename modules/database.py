import sqlite3

table_name = 'transactions'

def db_connect():
    '''function for connecting to database'''
    db_path = "database.db"
    try:
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            query = '''CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, 
                                                                news TEXT NOT NULL,
                                                                date TEXT NOT NULL,
                                                                time TEXT NOT NULL,
                                                                moneym INTEGER NOT NULL,
                                                                riskm INTEGER NOT NULL,
                                                                asset TEXT NOT NULL, 
                                                                exptime TEXT NOT NULL,
                                                                result TEXT NOT NULL,
                                                                situation TEXT NOT NULL,
                                                                url TEXT,
                                                                details TEXT)'''
            cursor.execute(query)
            db.commit()
    except Exception:
        print("[ERROR] Error during connection to database")
    return db