import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_NAME = "fake_news_db"
DB_USER = "news_user"
DB_PASS = "your_secure_password"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_tables():
    """Create the necessary tables in PostgreSQL"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS predictions (
            prediction_id SERIAL PRIMARY KEY,
            input_text TEXT NOT NULL,
            prediction_result VARCHAR(10) NOT NULL,
            confidence FLOAT NOT NULL,
            prediction_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id SERIAL PRIMARY KEY,
            prediction_id INTEGER REFERENCES predictions(prediction_id),
            is_correct BOOLEAN NOT NULL,
            user_comment TEXT,
            feedback_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """         
    )
    
    conn = None
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        
        cur = conn.cursor()
        
        # Create tables
        for command in commands:
            cur.execute(command)
        
        # Close communication
        cur.close()
        conn.commit()
        print("Tables created successfully!")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()