import email
from pickle import TRUE
from time import sleep
from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL

email_pattern = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
names_validators = re.compile("^[a-zA-Z]+$")
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users (first_name,last_name, password,email,created_at) VALUES (%(first_name)s, %(last_name)s, %(password)s, %(email)s, NOW())"
        results = connectToMySQL('login_registration').query_db(query,data)
        print(results)
        return results

    @classmethod
    def get_Current_user_info(cls,data):
        query = "SELECT * FROM users WHERE id=%(create)s;"
        results = connectToMySQL('login_registration').query_db(query,data)
        return results

    @classmethod
    def check_if_email_exists(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_registration").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return True

    @classmethod
    def check_password_email_login(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("login_registration").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def check_registration_fields(data):
        is_valid = False
        if data['password2'] != data['password_confirm2']:
            is_valid = True
            flash('passwords do not match!')

        if len(data['password']) < 8:
            is_valid = True
            flash('passwords is to short!')

        if not email_pattern.match(data['email']):
            is_valid = True
            flash('Not a valid Email!')
     
        if not names_validators.match(data['first_name']):
            if len(data['first_name']) < 2:
                flash('first name needs to be at least 2 characters and all letters')
                is_valid = True
     
        if not names_validators.match(data['last_name']):
            if len(data['last_name']) < 2:
                flash('Last name needs to be at least 2 characters and all letters')
                is_valid = True

        email_holder = data['email'].split('@')
        if email_holder == data['email'].split('@'):
            if len(email_holder[0]) > 2:
                holder = User.check_if_email_exists(data)
                if holder != False:
                    flash("email already exists")
                    is_valid = True
            elif len(email_holder[0]) < 2:
                flash('email needs to be more then 2 charaters')
                is_valid = True
                    
        return is_valid

