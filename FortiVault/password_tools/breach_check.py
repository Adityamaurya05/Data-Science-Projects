import hashlib
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_breach(password: str) -> int:
    """
    Check password against HIBP API
    Returns:
        int: Number of breaches found (-1 if API error)
    """
    try:
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1[:5], sha1[5:]
        
        response = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={"Add-Padding": "true"},
            timeout=3
        )
        
        for line in response.text.splitlines():
            if line.startswith(suffix):
                return int(line.split(':')[1])
        return 0
    except Exception:
        return -1