from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, post
import pprint 

class Post:
    db = "wall"
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # self.username = data["poster"]
        self.creator = None
        self.liked_by = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);"
        print(data)
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def like(cls, data):
        query = "INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls): 
        query = "SELECT posts.*,users.username as poster FROM posts LEFT JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query)
        wall_posts = []
        if len(results) <1:
            return wall_posts
        else:
            for row in results:
                wall_posts.append(cls(row))
        print(wall_posts)
        print(results)
        return wall_posts

    @classmethod
    def get_all_with_likes(cls):
        query = """SELECT * FROM posts 
LEFT JOIN users AS creator ON posts.user_id = creator.id LEFT JOIN likes ON posts.id = likes.post_id LEFT JOIN users ON users.id = likes.user_id  ORDER BY posts.created_at DESC;"""
        results = connectToMySQL(cls.db).query_db(query)
        pprint.pprint(results, sort_dicts=False)
        previous = 0
        # count = 0
        all_posts = []
        for row in results:
            if not all_posts or not row["id"] == all_posts[-1].id:
                current_post = cls(row)
                c = {
                    "id" : row["creator.id"],
                    "username" : row["username"],
                    "email" : row["email"],
                    "password" : None,
                    "created_at" : row["creator.created_at"],
                    "updated_at" : row["creator.updated_at"],
                }
                current_post.creator = user.User(c)
                if not row["users.id"] == None:
                    u = {
                        "id" : row["users.id"],
                        "username" : row["users.username"],
                        "email" : row["users.email"],
                        "password" : None,
                        "created_at" : row["users.created_at"],
                        "updated_at" : row["users.updated_at"],
                    }
                    current_post.liked_by.append(user.User(u))
                all_posts.append(current_post)
                # count += 1
            else:
                if not row["users.id"] == None:
                    u = {
                        "id" : row["users.id"],
                        "username" : row["users.username"],
                        "email" : row["users.email"],
                        "password" : None,
                        "created_at" : row["users.created_at"],
                        "updated_at" : row["users.updated_at"],
                    }
                    all_posts[-1].liked_by.append(user.User(u))
        return all_posts


    @classmethod
    def get_one_with_likes(cls, data):
        query = "SELECT * FROM posts LEFT JOIN likes ON likes.post_id = posts.id WHERE posts.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        post_with_likes = cls(results[0])
        for row in results:
            post_with_likes.liked_by.append(row["likes.user_id"])
        return post_with_likes

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM posts LEFT JOIN users on posts.user_id = users.id WHERE posts.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        post_with_user = cls(results[0])
        u = {
            "id" : results[0]["users.id"],
            "username" : results[0]["username"],
            "email" : results[0]["email"],
            "password" : None,
            "created_at" : results[0]["users.created_at"],
            "updated_at" : results[0]["users.updated_at"],
        }
        post_with_user.creator = user.User(u)
        return post_with_user


    @classmethod
    def liked_by(cls, data):
        query = "INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def delete_post(cls,data):
        query = "DELETE FROM posts WHERE posts.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
