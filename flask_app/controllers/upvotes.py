from flask import render_template, redirect, request,session, Markup
from flask_app import app
from flask_app.models import user,post,comment
from flask_app.models import upvote
import humanize 
import markdown2

@app.route('/post/<int:id>/upvote')
def upvote_post(id): 
    if 'user_id' not in session: 
      return redirect('/logout')
    data = {
        "user_id":session['user_id'], 
        "post_id":id}
    all_upvotes = upvote.Upvote.get_all_upvote_by_post({"post_id":id})
    print("ALL UPVOTES---->",all_upvotes)
    if all_upvotes == () : 
        upvote.Upvote.upvote_post(data)
    else:
      add = True
      for vote in all_upvotes:
        if ("user_id" in vote and vote["user_id"] == session['user_id']) and ("comment_id" in vote and vote["comment_id"] == None):
          add = True
        else: 
          add = False
      if (add == False):
          upvote.Upvote.upvote_post(data)
    return redirect('/')

@app.route('/post/<int:id>/downvote')
def downvote_post(id): 
    if 'user_id' not in session: 
      return redirect('/logout')
    data = {
        "user_id":session['user_id'], 
        "post_id":id}
    upvote.Upvote.downvote_post(data)
    return redirect('/')

@app.route('/post/<int:id>/upvote/<int:id2>')
def upvote_comment(id,id2): 
    if 'user_id' not in session: 
      return redirect('/logout')
    data = {
        "user_id":session['user_id'], 
        "post_id":id,
        "comment_id":id2}
    all_upvotes = upvote.Upvote.get_all_upvote_by_comment({"comment_id":id2})
    print("ALL UPVOTES---->",all_upvotes)
    if all_upvotes == () : 
        upvote.Upvote.upvote_comment(data)
    else:
      add = True
      for vote in all_upvotes:
        if ("user_id",session['user_id']) in vote.items():
          add = True
        else: 
          add = False
      if (add == False):
          upvote.Upvote.upvote_comment(data)
      print(add)
    return redirect('/')

@app.route('/post/<int:id>/downvote/<int:id2>')
def downvote_comment(id,id2): 
    if 'user_id' not in session: 
      return redirect('/logout')
    print("---------->",id2)
    data = {
        "user_id":session['user_id'], 
        "comment_id":id2}
    upvote.Upvote.downvote_comment(data)
    return redirect('/')