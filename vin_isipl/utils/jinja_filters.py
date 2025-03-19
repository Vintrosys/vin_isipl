import re

def ireplace(string, old, new):
    """Case insensitive string replace."""
    return re.sub(re.escape(old), new, string, flags=re.IGNORECASE)
