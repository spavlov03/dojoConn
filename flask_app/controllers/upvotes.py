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
    upvote.Upvote.upvote_post(data)
    return redirect('/')