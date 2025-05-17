import streamlit as st
from database import get_db_connection
from security import (
    hash_master_password,
    verify_master_password,
    encrypt_data,
    decrypt_data,
    generate_key_from_password
)
import os

# Page configuration
st.set_page_config(page_title="Password Manager", layout="wide")

# Session state initialization
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'master_key' not in st.session_state:
    st.session_state.master_key = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

def login_page():
    st.title("Password Manager Login")
    
    with st.form("login_form"):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT user_id, master_password_hash FROM users WHERE username = %s", 
                (username,)
            )
            result = cur.fetchone()
            
            if result:
                user_id, stored_hash = result
                if verify_master_password(password, stored_hash):
                    # Generate encryption key from password
                    salt = os.urandom(16)
                    st.session_state.master_key = generate_key_from_password(password, salt)
                    st.session_state.authenticated = True
                    st.session_state.user_id = user_id
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Incorrect password")
            else:
                st.error("Username not found")
            conn.close()

def register_page():
    st.title("Register New User")
    
    with st.form("register_form"):
        username = st.text_input("Username").strip()
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            if password != confirm_password:
                st.error("Passwords don't match")
                return
                
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Check if username exists
            cur.execute("SELECT username FROM users WHERE username = %s", (username,))
            if cur.fetchone():
                st.error("Username already exists")
                conn.close()
                return
                
            # Hash password and store
            hashed_password, _ = hash_master_password(password)
            cur.execute(
                "INSERT INTO users (username, master_password_hash) VALUES (%s, %s) RETURNING user_id",
                (username, hashed_password)
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            
            st.success("Registration successful! Please login.")

def password_manager_page():
    st.title("Password Manager")
    
    # Add new password
    with st.expander("Add New Password"):
        with st.form("add_password_form"):
            service = st.text_input("Service/Website")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            url = st.text_input("URL (optional)")
            notes = st.text_area("Notes (optional)")
            submit_button = st.form_submit_button("Save Password")
            
            if submit_button:
                encrypted_password = encrypt_data(password, st.session_state.master_key)
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    """INSERT INTO passwords 
                    (user_id, service_name, username, encrypted_password, url, notes)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (st.session_state.user_id, service, username, encrypted_password, url, notes)
                )
                conn.commit()
                conn.close()
                st.success("Password saved successfully!")
    
    # View passwords
    st.subheader("Your Saved Passwords")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT password_id, service_name, username, encrypted_password, url, notes 
        FROM passwords WHERE user_id = %s""",
        (st.session_state.user_id,)
    )
    passwords = cur.fetchall()
    conn.close()
    
    for pwd in passwords:
        pwd_id, service, username, encrypted_pwd, url, notes = pwd
        with st.expander(f"{service} - {username}"):
            decrypted_pwd = decrypt_data(encrypted_pwd, st.session_state.master_key)
            st.text_input("Password", value=decrypted_pwd, type="password", key=f"pwd_{pwd_id}")
            st.text(f"URL: {url}" if url else "No URL provided")
            st.text(f"Notes: {notes}" if notes else "No notes")
            
            if st.button("Delete", key=f"del_{pwd_id}"):
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM passwords WHERE password_id = %s", (pwd_id,))
                conn.commit()
                conn.close()
                st.rerun()

# Main app flow
if not st.session_state.authenticated:
    login_tab, register_tab = st.tabs(["Login", "Register"])
    with login_tab:
        login_page()
    with register_tab:
        register_page()
else:
    password_manager_page()
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.master_key = None
        st.session_state.user_id = None
        st.rerun()