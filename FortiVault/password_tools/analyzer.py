from zxcvbn import zxcvbn

def analyze_password(password: str) -> dict:
    """
    Analyze password strength using zxcvbn
    Returns:
        dict: {
            'score': 0-4,
            'warning': str,
            'suggestions': list,
            'crack_time': str
        }
    """
    result = zxcvbn(password)
    return {
        'score': result['score'],
        'warning': result['feedback']['warning'],
        'suggestions': result['feedback']['suggestions'],
        'crack_time': result['crack_times_display']['offline_slow_hashing_1e4_per_second']
    }