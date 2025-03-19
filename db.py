import sqlite3

# -------------------------------------------------------------------
# Database Initialization and Connection
# -------------------------------------------------------------------
def init_db(db_name="om.db"):
    """
    Initialize the SQLite database and create the 'om' table if it does not exist.
    """
    conn = sqlite3.connect(db_name, check_same_thread=False)
    cursor = conn.cursor()
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS om (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT NOT NULL,
            tech_stack TEXT NOT NULL,
            experience TEXT NOT NULL,
            desired_positions TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    return conn, cursor


def save_candidate_data(conn, cursor, candidate_data):
    """
    Save candidate details into the database.
    """
    try:
        cursor.execute(
            '''
            INSERT INTO om (full_name, email, phone, location, tech_stack, experience, desired_positions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                candidate_data.get("name"),
                candidate_data.get("email"),
                candidate_data.get("phone"),
                candidate_data.get("location"),
                ", ".join(candidate_data.get("tech_stack", [])),
                str(candidate_data.get("experience")),
                candidate_data.get("suggested_positions", "Not available"),
            ),
        )
        conn.commit()
        return True
    except Exception as e:
        return str(e)
