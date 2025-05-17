from passlib.hash import argon2
from passlib.exc import MissingBackendError
import os
import base64
from cryptography.fernet import Fernet

# =============================================
# Backend Availability Check
# =============================================
def _verify_argon2_backend():
    """Verify Argon2 backend is available"""
    try:
        # Test hash/verify to check backend
        test_hash = argon2.hash("test")
        argon2.verify("test", test_hash)
    except MissingBackendError:
        raise RuntimeError(
            "Argon2 backend missing - please install argon2-cffi\n"
            "Run: pip install argon2-cffi"
        )

# Perform check when module loads
_verify_argon2_backend()

# =============================================
# Password Hashing Functions
# =============================================
def hash_master_password(password: str) -> tuple:
    """
    Securely hash a master password with Argon2
    Returns tuple of (hashed_password, salt_hex)
    """
    # Using Argon2's default type (which is Argon2id in modern versions)
    hashed = argon2.using(
        salt=os.urandom(16),  # 128-bit salt
        rounds=10,             # Number of iterations
        memory_cost=65536,     # 64MB memory usage
        parallelism=4,         # Number of parallel threads
    ).hash(password)
    
    # Extract the salt from the hash (it's stored in the hash string)
    # Format: $argon2id$v=19$m=65536,t=10,p=4$salt$hash
    parts = hashed.split('$')
    salt_hex = parts[4] if len(parts) > 4 else ''
    
    return hashed, salt_hex

def verify_master_password(password: str, hashed_password: str) -> bool:
    """Verify password against stored hash"""
    try:
        return argon2.verify(password, hashed_password)
    except Exception as e:
        print(f"Verification error: {e}")  # Debug output
        return False

# =============================================
# Encryption Functions
# =============================================
def generate_key_from_password(password: str, salt: bytes) -> bytes:
    """
    Derive encryption key from password using Argon2
    """
    # Using the same parameters as password hashing for consistency
    kdf_hash = argon2.using(
        salt=salt,
        rounds=10,
        memory_cost=65536,
        parallelism=4,
    ).hash(password)
    
    # Use the first 32 bytes of the hash as key material
    key_material = kdf_hash[:32].encode()
    return base64.urlsafe_b64encode(key_material)

def encrypt_data(data: str, key: bytes) -> str:
    """
    Encrypt data using Fernet (AES-128)
    """
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str, key: bytes) -> str:
    """
    Decrypt data using Fernet
    """
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data.encode()).decode()

# =============================================
# Security Configuration
# =============================================
SECURITY_PARAMS = {
    'argon2_rounds': 10,
    'argon2_memory': 65536,  # 64MB
    'argon2_parallelism': 4,
    'salt_size': 16  # 128-bit
}