from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Post:
  DB = "dojo_connect"

  def __init__(self,data):
    self.id = data['id']
    self.title = data['title']
    self.technology = data['technology']
    self.description = data['description']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.user_id = data['user_id']
    self.creator = None
    # self.likes = []

  @classmethod
  def add_post(cls,post_data): 
    query = "INSERT into posts (title,technology,description,user_id) VALUES (%(title)s,%(technology)s,%(description)s,%(user_id)s);"
    result = connectToMySQL(cls.DB).query_db(query,post_data)
    return result 
  
  @classmethod
  def get_one_post_by_id_with_user(cls,data): 
    query = "SELECT * FROM posts JOIN users on posts.user_id = users.id WHERE posts.id = %(id)s;"
    result = connectToMySQL(cls.DB).query_db(query,data)
    print(result)
    for row in result: 
      post = cls(row)
      post_creator_info = { 
        "id":row['users.id'], 
        "first_name":row['first_name'], 
        "last_name":row['last_name'], 
        "email":row['email'], 
        'password':row['password'], 
        "created_at": row['created_at'],
        "updated_at": row['updated_at']
      }
      creator = user.User(post_creator_info)
      post.creator = creator
      print('The post is---',post)
    return post

  @classmethod
  def edit_post(cls,post_data): 
    query = "UPDATE posts SET title=%(title)s,technology=%(technology)s,description=%(description)s WHERE id=%(id)s"
    result = connectToMySQL(cls.DB).query_db(query,post_data)
    print("Updating Post",result)
    return result

  @classmethod
  def get_all_posts(cls): 
    query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id;"  
    result = connectToMySQL(cls.DB).query_db(query)
    posts = []
    for row in result: 
      post = cls(row)
      post_creator_info = {
        "id":row['users.id'], 
        "first_name": row['first_name'],
        "last_name": row['last_name'],
        "email": row['email'],
        "password": row['password'],
        "created_at": row['created_at'],
        "updated_at": row['updated_at']
      }
      creator = user.User(post_creator_info)
      post.creator = creator
      posts.append(post)
    return posts

  @classmethod
  def get_all_posts_by_tech(cls,data): 
    query = "SELECT * FROM posts WHERE technology=%(technology)s;"
    result = connectToMySQL(cls.DB).query_db(query,data)
    print(result)
    return result

  @classmethod
  def delete_post(cls,data): 
    query = "DELETE FROM posts WHERE id=%(id)s;"
    result = connectToMySQL(cls.DB).query_db(query,data)
    return result 
  
  @classmethod
  def search(cls,data): 
    query = "SELECT * FROM posts WHERE INSTR(title,'{$%(title)s}' >0"
    result = connectToMySQL(cls.DB).query_db(query,data)
    print(result)
    return result
# Need to fix search 
  @staticmethod
  def post_validation(post): 
    is_valid = True
    if len(post['title']) <1: 
      flash("Tile is required")
      is_valid = False
    if len(post['technology']) <1: 
      flash("Must select Technology")
      is_valid = False
    if len(post['description']) <1: 
      flash("Must enter description")
      is_valid = False
    return is_valid