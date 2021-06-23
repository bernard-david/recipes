from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        # create a new user and add to database
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('recipes_schema').query_db( query, data )
    
    @classmethod
    def get_user(cls, data):
        # get all of one users information
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db( query, data )
        user = results[0]
        return user

    @classmethod
    def get_by_email(cls, data):
        # get a user by it's email
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('recipes_schema').query_db( query, data )
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate(data):
        # validate a new user's info inputed into the form
        is_valid = True

        name_regex = re.compile(r'[A-Za-z]{2,50}$')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        password_regex = re.compile(r'[A-Za-z0-9]{8,15}$')

        if not name_regex.match(data['first_name']):
            # checks if the name is valid
            is_valid = False
            flash("First name must contain at least two characters and contain only letters")

        if not name_regex.match(data['last_name']):
            # checks if the name is valid
            is_valid = False
            flash("Last name must contain at least two characters and contain only letters")

        if not email_regex.match(data['email']):
            # checks if the email provided is valid
            is_valid = False
            flash("Invalid email address")

        if User.get_by_email(data):
            # checks if an email is already in use
            is_valid = False
            flash("Email already in use. Please provide a different email.")

        if not password_regex.match(data['password']):
            # checks if the password is valid
            id_valid = False
            flash("Password must contain letters and numbers between 8-15 characters")

        if data['confirm_password'] != data['password']:
            # both passwords must match
            is_valid = False
            flash("Passwords must match")
        
        # if form is completed properly then return true
        return is_valid

    

        
        