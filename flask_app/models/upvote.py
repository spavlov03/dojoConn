from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, comment , post

class Upvote: 
    DB = 'dojo_connect'

    def __init__(self,data):
      self.user_id = data['user_id']
      self.post_id = None
      self.comment_id = None

    @classmethod
    def upvote_post(cls,post_data): 
        query = 'INSERT INTO upvotes (user_id,post_id) VALUES (%(user_id)s,%(post_id)s);'
        result = connectToMySQL(cls.DB).query_db(query,post_data)
        print("UPVOTING POST-----",result)
        return result
    
    @classmethod
    def get_all_upvotes(cls): 
        query = "SELECT * FROM upvotes"
        result = connectToMySQL(cls.DB).query_db(query)
        return result