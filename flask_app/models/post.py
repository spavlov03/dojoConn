from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, comment, upvote

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
    self.votes = []

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
  def get_one_post_by_id(cls,data): 
    query = "SELECT * FROM posts WHERE id=%(id)s"
    result = connectToMySQL(cls.DB).query_db(query,data)
    return result

  @classmethod
  def edit_post(cls,post_data): 
    query = "UPDATE posts SET title=%(title)s,technology=%(technology)s,description=%(description)s WHERE id=%(id)s"
    result = connectToMySQL(cls.DB).query_db(query,post_data)
    print("Updating Post",result)
    return result

  @classmethod
  def get_all_posts(cls): 
    query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id ORDER BY posts.created_at DESC;"  
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
    query = "SELECT posts.*, users.id AS creator_id, users.first_name AS creator_first_name, users.last_name AS creator_last_name, users.email AS creator_email, users.password AS creator_password, users.created_at AS creator_created_at, users.updated_at AS creator_updated_at FROM posts JOIN users ON posts.user_id = users.id WHERE technology=%(technology)s ORDER BY posts.created_at DESC;"

    result = connectToMySQL(cls.DB).query_db(query,data)
    
    print(result)
    return result
  
  @classmethod
  def get_all_upvotes_by_post(cls): 
    query = "SELECT * FROM posts JOIN upvotes ON posts.id = upvotes.post_id"  
    result = connectToMySQL(cls.DB).query_db(query)
    print("RESULUTS IN UPVOTES----",result)
    posts = []
    for row in result: 
      post = cls(row)
      post_upvotes = {
        "user_id": row['user_id'],
        "post_id": row['post_id']
      }
      upvotes = upvote.Upvote(post_upvotes)
      post.votes = upvotes
      posts.append(post)
    return posts

  @classmethod
  def get_all_posts_by_user(cls, data):
    query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id WHERE user_id = %(id)s;"
    result = connectToMySQL(cls.DB).query_db(query,data)
    posts = []
    for row in result:
      post = cls(row)
      posts.append(post)
    return posts

  @classmethod
  def delete_post(cls,data): 
    query = "DELETE FROM posts WHERE id=%(id)s;"
    result = connectToMySQL(cls.DB).query_db(query,data)
    return result 
  
  @classmethod
  def search(cls,data): 
    query = "posts.*, users.id AS creator_id, users.first_name AS creator_first_name, users.last_name AS creator_last_name, users.email AS creator_email, users.password AS creator_password, users.created_at AS creator_created_at, users.updated_at AS creator_updated_at FROM posts JOIN users ON posts.user_id = users.id LIKE %(title)s ORDER BY posts.created_at DESC;"
    # query = "SELECT * FROM posts WHERE title=%(title)s;"
    result = connectToMySQL(cls.DB).query_db(query,data)
    print("Search Result is --- ",result)
    return result
# Need to fix search 
  
  # i added this method to count the # of comments of each post -Maleko
  @classmethod
  def commentCount(cls, post_id):
    query = " SELECT COUNT(*) AS total_comments FROM comments WHERE post_id = %(post_id)s; "
    data = {'post_id': post_id}
    result = connectToMySQL(cls.DB).query_db(query, data)
    return result


  @staticmethod
  def post_validation(post): 
    is_valid = True
    if len(post['title']) <1: 
      flash("Tile is required", "title")
      is_valid = False
    if len(post['technology']) <1: 
      flash("Must select Technology", 'technology')
      is_valid = False
    if len(post['description']) <1: 
      flash("Must enter description", 'description')
      is_valid = False
    return is_valid
