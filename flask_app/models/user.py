from flask_app.config.mysqlconnection import connectToMySQL

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db = "wall"
    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.likes = []

    @classmethod
    def save(cls, data):
        # print("-------BEFORE-------")
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s)"
        print(data)
        print("-------AFTER-------")
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls): 
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        if len(results) <1:
            return users
        else:
            for row in results:
                users.append(cls(row))
        return users


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL("wall").query_db(query,user)
        if len(results) >= 1:
            flash("Username already taken.","register",)
            is_valid = False
        if len(user['username']) < 2:
            flash("Username must be at least 2 characters.")
            is_valid = False
        if len(user['email']) < 3:
            flash("Email not valid.", "register")
            is_valid = False
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("wall").query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.","register")
        if user['password'] != user["confirm_password"]:
            flash("Passwords must match")
            is_valid = False
        # print(user["agree"])
        if 'agree' not in user:
            # print("this is working..?")
            flash("Must agree to be nice to everyone on FaceTerGramChat.", 'register')
            is_valid = False
        return is_valid
