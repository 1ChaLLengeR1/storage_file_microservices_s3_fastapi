import random
import string

def createRandom(name: str, length: int = 5) -> str:
    random_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    return f"{name}_{random_chars}"