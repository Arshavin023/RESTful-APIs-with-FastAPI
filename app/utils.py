from passlib.context import CryptContext
# Telling PassLib what is the default hashing algorithm which is bcrypt
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# This function hashes a password
def hash(password: str):
    return pwd_context.hash(password)

#This function compares the hashed password saved on the DB
# and the hash of the password supplied when existing user tries to login
def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)


