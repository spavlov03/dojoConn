from flask import render_template, redirect, request,session
from flask_app import app
from flask_app.models import user,post

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": session['user_id']}
    all_posts = post.Post.get_all_posts()
    return render_template('dashboard.html',user = user.User.get_user_by_id(data),all_posts=all_posts)

@app.route("/post/add")
def new_post(): 
  if 'user_id' not in session: 
    return redirect('/logout')
  data = {"id":session['user_id']}
  return render_template('add_post.html', user=user.User.get_user_by_id(data))

@app.route("/add/post",methods=['POST'])
def add_post(): 
  if 'user_id' not in session: 
    return redirect('/logout')
  if not post.Post.post_validation(request.form): 
    return redirect('/post/add')
  data = {
    "title" : request.form['title'], 
    "technology" : request.form['technology'], 
    "description": request.form['description'], 
    'user_id': session['user_id']
  }
  post.Post.add_post(data)
  return redirect('/dashboard')

