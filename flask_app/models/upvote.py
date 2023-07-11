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
        query = 'INSERT INTO votes (user_id,post_id) VALUES (%(user_id)s,%(post_id)s);'
        result = connectToMySQL(cls.DB).query_db(query,post_data)
        return result
    
    @classmethod
    def downvote_post(cls,post_data): 
        query = 'DELETE from votes WHERE user_id=%(user_id)s AND post_id=%(post_id)s AND comment_id IS NULL;'
        result = connectToMySQL(cls.DB).query_db(query,post_data)
        return result
    
    @classmethod
    def get_all_upvote_by_post(cls,post_data): 
        query = "SELECT * FROM votes WHERE post_id = %(post_id)s AND comment_id IS NULL"
        result = connectToMySQL(cls.DB).query_db(query,post_data)
        return result
    
    @classmethod
    def upvote_comment(cls,post_data): 
        query = 'INSERT INTO votes (user_id,post_id,comment_id) VALUES (%(user_id)s,%(post_id)s,%(comment_id)s);'
        result = connectToMySQL(cls.DB).query_db(query,post_data)
        return result
    
    @classmethod
    def downvote_comment(cls,post_data): 
        query = 'DELETE from votes WHERE user_id=%(user_id)s AND comment_id=%(comment_id)s;'
        result = connectToMySQL(cls.DB).query_db(query,post_data)
        return result
    
    @classmethod
    def get_all_upvote_by_comment(cls,post_data): 
        query = "SELECT * FROM votes WHERE comment_id = %(comment_id)s"
        result = connectToMySQL(cls.DB).query_db(query,post_data)
        return result
