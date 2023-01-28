from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

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
  
  @classmethod
  def add_commment(cls, comment_data):
    query = "INSERT INTO comments ( comment, created_at, updated_at, post_id, user_id ) VALUES ( %(comment)s, NOW(), NOW(), %(post_id)s, %(user_id)s );"

    return connectToMySQL(cls.DB).query_db(query, data)

  @classmethod
  def get_comments_by_post(cls, data):
    query = "SELECT * FROM comments JOIN posts ON comments.post_id = posts.id WHERE posts.id = %(id)s;"
    results = connectToMySQL(cls.DB).query_db(query)
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
      post = post.Post(one_comment_post_info)
      comment.post = post 
      print('Comment is--', comment)
    return comment

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
