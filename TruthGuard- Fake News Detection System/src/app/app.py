import numpy as np
import streamlit as st
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import psycopg2
from datetime import datetime
import os

# ==============================================
# Database Configuration
# ==============================================
class DatabaseManager:
    def __init__(self):
        self.conn_params = {
            "dbname": os.getenv("DB_NAME", "fake_news_db"),
            "user": os.getenv("DB_USER", "news_user"),
            "password": os.getenv("DB_PASS", "your_secure_password"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432")
        }
    
    def _get_connection(self):
        return psycopg2.connect(**self.conn_params)
    
    def _convert_for_postgres(self, value):
        """Convert numpy/pandas types to PostgreSQL-compatible types"""
        if hasattr(value, 'item'):  # numpy types
            return value.item()
        if isinstance(value, (np.integer, np.floating)):
            return float(value) if isinstance(value, np.floating) else int(value)
        if isinstance(value, (pd.Timestamp, datetime)):
            return value.isoformat()
        return str(value)
    
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
            
            # Convert all values
            input_text = str(input_text)[:5000]  # Truncate long text
            prediction_result = str(prediction_result)
            confidence = float(confidence)
            
            cur.execute(sql, (input_text, prediction_result, confidence))
            prediction_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Database error: {error}")
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
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Database error: {error}")
            return False
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
            (SELECT COUNT(*) FROM feedback WHERE is_correct = FALSE) as incorrect_feedback,
            (SELECT COUNT(*) FROM predictions 
             WHERE prediction_time >= NOW() - INTERVAL '24 HOURS') as daily_predictions
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
            st.error(f"Database error: {error}")
        finally:
            if conn is not None:
                conn.close()
        
        return stats
    
    def get_recent_predictions(self, limit=50):
        """Get recent predictions for admin dashboard"""
        sql = """
        SELECT p.prediction_id, p.input_text, p.prediction_result, 
               p.confidence, p.prediction_time,
               f.is_correct, f.user_comment
        FROM predictions p
        LEFT JOIN feedback f ON p.prediction_id = f.prediction_id
        ORDER BY p.prediction_time DESC
        LIMIT %s;
        """
        
        conn = None
        results = None
        try:
            conn = self._get_connection()
            results = pd.read_sql(sql, conn, params=(limit,))
        except (Exception, psycopg2.DatabaseError) as error:
            st.error(f"Database error: {error}")
        finally:
            if conn is not None:
                conn.close()
        
        return results

# ==============================================
# App Configuration
# ==============================================
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stTextArea textarea {
        height: 200px;
    }
    .stButton button {
        width: 100%;
    }
    .correct {
        color: #4CAF50;
    }
    .incorrect {
        color: #F44336;
    }
    .admin-header {
        color: #9C27B0;
    }
    .stat-card {
        border-radius: 10px;
        padding: 15px;
        background-color: #f0f2f6;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================
# Model Loading
# ==============================================
@st.cache_resource
def load_components():
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

model, vectorizer = load_components()
db = DatabaseManager()

# ==============================================
# Main App Functionality
# ==============================================
def main_app():
    st.title("📰 Fake News Detector")
    st.markdown("""
    This app uses machine learning to classify news articles as real or fake. 
    Enter a news article in the text box below and click "Predict" to analyze.
    """)

    # Input text area
    news_input = st.text_area("Enter News Article:", 
                            placeholder="Paste the news article text here...",
                            height=200)

    # Prediction button
    if st.button("Predict", type="primary"):
        if news_input:
            with st.spinner("Analyzing the news article..."):
                # Vectorize input
                vec = vectorizer.transform([news_input])
                
                # Make prediction
                pred = model.predict(vec)
                proba = model._predict_proba_lr(vec)[0]
                confidence = max(proba) * 100
                
                # Save to database
                prediction_id = db.save_prediction(news_input[:5000], pred[0], confidence)
                
                # Display result
                st.markdown("---")
                if pred[0] == "REAL":
                    st.success(f"✅ **Result:** This news is likely REAL (confidence: {confidence:.1f}%)")
                else:
                    st.error(f"❌ **Result:** This news is likely FAKE (confidence: {confidence:.1f}%)")
                
                # Add feedback section
                st.markdown("---")
                st.subheader("Help Improve Our System")
                st.write("Was this prediction correct?")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Yes, Correct", key="correct_btn"):
                        if db.save_feedback(prediction_id, True):
                            st.success("Thank you for your feedback!")
                with col2:
                    if st.button("👎 No, Incorrect", key="incorrect_btn"):
                        comment = st.text_input("Please provide the correct answer or comments:")
                        if comment:
                            if db.save_feedback(prediction_id, False, comment):
                                st.success("Thank you for helping improve the system!")

                # Show statistics
                show_statistics()
        else:
            st.warning("Please enter some text to analyze.")

def show_statistics():
    """Display prediction statistics"""
    stats = db.get_prediction_stats()
    if stats:
        st.markdown("---")
        st.subheader("📊 System Statistics")
        
        total_pred, avg_conf, correct_fb, incorrect_fb, daily_pred = stats
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="stat-card"><h3>Total Predictions</h3><h2>{total_pred}</h2></div>', 
                       unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'<div class="stat-card"><h3>Avg Confidence</h3><h2>{avg_conf:.1f}%</h2></div>', 
                       unsafe_allow_html=True)
        
        with col3:
            accuracy = (correct_fb/(correct_fb+incorrect_fb))*100 if (correct_fb+incorrect_fb) > 0 else 0
            st.markdown(f'<div class="stat-card"><h3>User-Reported Accuracy</h3><h2>{accuracy:.1f}%</h2></div>', 
                       unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'<div class="stat-card"><h3>Today\'s Predictions</h3><h2>{daily_pred}</h2></div>', 
                       unsafe_allow_html=True)

# ==============================================
# Admin Dashboard
# ==============================================
def admin_dashboard():
    st.title("🔒 Admin Dashboard")
    st.markdown('<p class="admin-header">System monitoring and data analysis</p>', 
               unsafe_allow_html=True)
    
    # Password protection (basic)
    admin_password = st.text_input("Enter Admin Password:", type="password")
    if admin_password != os.getenv("ADMIN_PASSWORD", "admin123"):
        st.error("Incorrect admin password")
        return
    
    st.markdown("---")
    
    # System Statistics
    st.subheader("📈 System Overview")
    show_statistics()
    
    st.markdown("---")
    
    # Recent Predictions
    st.subheader("🕒 Recent Predictions")
    limit = st.slider("Number of records to show:", 10, 100, 50)
    
    predictions = db.get_recent_predictions(limit)
    if predictions is not None:
        # Format the dataframe for display
        predictions['prediction_time'] = pd.to_datetime(predictions['prediction_time']).dt.strftime('%Y-%m-%d %H:%M')
        predictions['feedback'] = predictions.apply(
            lambda row: "✅ Correct" if row['is_correct'] == True else ("❌ Incorrect" if row['is_correct'] == False else "No feedback"), 
            axis=1
        )
        
        # Show the dataframe
        st.dataframe(
            predictions[['prediction_id', 'prediction_result', 'confidence', 
                        'prediction_time', 'feedback', 'user_comment']],
            column_config={
                "prediction_id": "ID",
                "prediction_result": "Result",
                "confidence": "Confidence",
                "prediction_time": "Time",
                "feedback": "Feedback",
                "user_comment": "Comments"
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Download option
        csv = predictions.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Full Data as CSV",
            data=csv,
            file_name='fake_news_predictions.csv',
            mime='text/csv'
        )
    
    st.markdown("---")
    
    # Raw SQL Query Section (for advanced admin use)
    st.subheader("⚙️ Database Query")
    query = st.text_area("Enter SQL Query (for advanced users only):", 
                        "SELECT * FROM predictions LIMIT 10;")
    
    if st.button("Execute Query"):
        try:
            conn = db._get_connection()
            result = pd.read_sql(query, conn)
            st.dataframe(result, use_container_width=True)
        except Exception as e:
            st.error(f"Query error: {e}")
        finally:
            if 'conn' in locals() and conn is not None:
                conn.close()

# ==============================================
# App Navigation
# ==============================================
def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Select Mode:", 
                               ["Fake News Detector", "Admin Dashboard"])
    
    if app_mode == "Fake News Detector":
        main_app()
    else:
        admin_dashboard()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info(
        "Fake News Detection System v1.0\n\n"
        "Note: This is a machine learning model and may not be 100% accurate. "
        "Always verify information from multiple reliable sources."
    )

if __name__ == "__main__":
    main()