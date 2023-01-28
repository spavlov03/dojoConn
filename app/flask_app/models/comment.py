from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import post, user

class Comment:
  DB = "dojo_connect"

  def __init__(self, data):
    self.id = self['id']
    self.comment = self['comment']
    self.created_at = self['created_at']
    self.updated_at = self['updated_at']
    self.post_id = self['post_id']
    self.user_id = self['user_id'] 
    self.post = NONE
    self.comment_poster = NONE
  
  @classmethod
  def add_commment(cls, comment_data):
    query = "INSERT INTO comments ( comment, created_at, updated_at, post_id, user_id ) VALUES ( %(comment)s, NOW(), NOW(), %(post_id)s, %(user_id)s );"

    return connectToMySQL(cls.DB).query_db(query, data)

  @classmethod
  def get_comments_by_post(cls, data):
    query = "SELECT * FROM comments JOIN posts ON comments.post_id = posts.id JOIN users ON posts.user_id = users.id WHERE posts.id = %(id)s;"
    results = connectToMySQL(cls.DB).query_db(query)
    comments = []
    for row in results:
      one_comment = cls(row)
      one_comments_post_info = {
        'id': row['posts.id'],
        'title': row['posts.title'],
        'technology': row['posts.technology'],
        'description': row['posts.description'],
        'created_at': row['posts.created_at'],
        'updated_at': row['posts.updated_at'],
      }
      one_comments_user_info = {
        'id': row['users.id'],
        'first_name': row['first_name'],
        "last_name":row['last_name'], 
        "email":row['email'], 
        'password':row['password'], 
        "created_at": row['created_at'],
        "updated_at": row['updated_at']
      }
      comment_poster = user.User(one_comments_user_info)
      one_comment.user = comment_poster
      post = post.Post(one_comment_post_info)
      one_comment.post = post 
      comments.append(one_comment)
      print('Comment is ', comment)
    return comments

  @classmethod
  def update_comment(cls, data):
    query = "UPDATE comments SET comment = %(comment)s, updated_at = NOW() WHERE id = %(id)s;"    
    result = connectToMySQL(cls.DB).query_db(query, data)
    print("Updating Comment",result)
    return result

  @classmethod
  def delete_comment(cls, data):
    query = "DELETE FROM comments WHERE id = %(id)s;"
    result = connectToMySQL(cls.DB).query_db(query,data)
    return result 

  @staticmethod
  def comment_validation(comment):
    is_valid = True
    if len(post['comment']) <1: 
      flash("comment is required")
      is_valid = False
    return is_valid
