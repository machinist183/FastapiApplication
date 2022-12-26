from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = "auto")

def hash_pass(password):
    return pwd_context.hash(password)

def verify_pass(input_pass , hashed_pass):
    return pwd_context.verify(input_pass , hashed_pass)
