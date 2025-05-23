import psycopg2
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.conn_params = {
            "dbname": "fake_news_db",
            "user": "news_user",
            "password": "your_secure_password",
            "host": "localhost",
            "port": "5432"
        }
    
    def _get_connection(self):
        return psycopg2.connect(**self.conn_params)
    
    def save_prediction(self, input_text, prediction_result, confidence):
        """Save prediction to database"""
        sql = """
        INSERT INTO predictions(input_text, prediction_result, confidence)
        VALUES(%s, %s, %s) RETURNING prediction_id;
        """
        
        conn = None
        prediction_id = None
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute(sql, (input_text, prediction_result, confidence))
            prediction_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        
        return prediction_id
    
    def save_feedback(self, prediction_id, is_correct, user_comment=None):
        """Save user feedback to database"""
        sql = """
        INSERT INTO feedback(prediction_id, is_correct, user_comment)
        VALUES(%s, %s, %s);
        """
        
        conn = None
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute(sql, (prediction_id, is_correct, user_comment))
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
    
    def get_prediction_stats(self):
        """Get statistics about predictions and feedback"""
        sql = """
        SELECT 
            COUNT(*) as total_predictions,
            AVG(confidence) as avg_confidence,
            (SELECT COUNT(*) FROM feedback WHERE is_correct = TRUE) as correct_feedback,
            (SELECT COUNT(*) FROM feedback WHERE is_correct = FALSE) as incorrect_feedback
        FROM predictions;
        """
        
        conn = None
        stats = None
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            cur.execute(sql)
            stats = cur.fetchone()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        
        return stats