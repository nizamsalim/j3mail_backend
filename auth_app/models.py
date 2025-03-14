from dataclasses import dataclass

@dataclass
class SignupBody:
    name:str
    email:str
    password:str

@dataclass
class LoginBody:
    email:str
    password:str

class User:
    def __init__(self,_id,email,name,password):
        self._id = _id
        self.email = email
        self.name = name
        self.password = password
        self.is_authenticated = True

# Create your models here.
