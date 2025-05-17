# FortiVault
# Password Manager Application

## Overview

A secure password manager application built with Python and Streamlit that allows users to:
- Securely store and manage passwords
- Encrypt sensitive data with a master password
- Access passwords across multiple devices (when deployed with a database)

## Features

- **Secure Authentication**: Uses Argon2 for password hashing with configurable security parameters
- **Data Encryption**: AES-128 encryption for stored passwords using Fernet
- **User Management**: Registration and login system
- **Password Storage**: Store website/service credentials with optional notes and URLs
- **Responsive UI**: Clean Streamlit interface with expandable sections

## Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: PostgreSQL
- **Security**:
  - Argon2 for password hashing
  - AES-128 for data encryption
  - Secure key derivation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/password-manager.git
   cd password-manager
   ```

2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with your database credentials:
   ```
   DB_HOST=your_database_host
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_PORT=your_database_port
   ```

5. Initialize the database:
   - Make sure PostgreSQL is running
   - Create the necessary tables (see Database Setup section)

## Database Setup

The application requires a PostgreSQL database with the following tables:

1. Users table:
   ```sql
   CREATE TABLE users (
       user_id SERIAL PRIMARY KEY,
       username VARCHAR(255) UNIQUE NOT NULL,
       master_password_hash VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

2. Passwords table:
   ```sql
   CREATE TABLE passwords (
       password_id SERIAL PRIMARY KEY,
       user_id INTEGER REFERENCES users(user_id),
       service_name VARCHAR(255) NOT NULL,
       username VARCHAR(255) NOT NULL,
       encrypted_password TEXT NOT NULL,
       url VARCHAR(255),
       notes TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

## Running the Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Security Features

- **Master Password Protection**: 
  - Uses Argon2id with:
    - 128-bit salt
    - 10 iterations
    - 64MB memory cost
    - 4 parallel threads
- **Data Encryption**:
  - AES-128 encryption for all stored passwords
  - Unique encryption key derived from master password
- **Secure Session Management**:
  - Session state cleared on logout
  - No persistent storage of master password



## Future Enhancements

- Password strength meter
- Two-factor authentication
- Password sharing (secure)
- Browser extension integration
- Mobile app version
- Password expiration reminders

## Contributing

Contributions are welcome! Please open an issue or pull request for any improvements.

## License

MIT License (include full license text if desired)