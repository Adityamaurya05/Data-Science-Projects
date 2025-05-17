import secrets
import string
from typing import Optional

def generate_password(
    length: int = 16,
    include_upper: bool = True,
    include_lower: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True
) -> Optional[str]:
    """
    Generate cryptographically secure password
    Args:
        length: 8-64 characters
    Returns:
        str: Generated password or None if invalid config
    """
    if not 8 <= length <= 64:
        return None
        
    chars = ''
    if include_upper: chars += string.ascii_uppercase
    if include_lower: chars += string.ascii_lowercase
    if include_digits: chars += string.digits
    if include_symbols: chars += '!@#$%^&*'
    
    if not chars:
        return None
        
    return ''.join(secrets.choice(chars) for _ in range(length))