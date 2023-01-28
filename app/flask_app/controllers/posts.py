from flask import render_template, redirect, request,session
from flask_app import app
from flask_app.models import user,post

@app.route("/dashboard")
def dashboard():
    # if "user_id" not in session:
    #     return redirect("/logout")
    data = {"id": session['user_id']}
    logged_user = user.User.get_user_by_id(data)
    all_posts = post.Post.get_all_posts()
    return render_template('dashboard.html',logged_user = logged_user,all_posts=all_posts)

@app.route("/post/add")
def new_post(): 
  if 'user_id' not in session: 
    return redirect('/logout')
  data = {"id": session['user_id']}
  logged_user = user.User.get_user_by_id(data)
  return render_template('create_post.html', logged_user=logged_user)

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

@app.route("/post/<int:id>/")
def view_post(id):
  if 'user_id' not in session: 
    return redirect('/logout')
  data = {"id": session['user_id']}
  post_data = {"id":id}
  this_post = post.Post.get_one_post_by_id_with_user(post_data)
  logged_user = user.User.get_user_by_id(data)
  return render_template("view_post.html",this_post=this_post,logged_user=logged_user)

@app.route("/post/<int:id>/edit")
def edit_post(id):
  if 'user_id' not in session: 
    return redirect('/logout')
  post_data = {"id":id}
  this_post = post.Post.get_one_post_by_id_with_user(post_data)
  data = {"id": session['user_id']}
  logged_user = user.User.get_user_by_id(data)
  return render_template("edit_post.html",this_post=this_post,logged_user=logged_user)

@app.route("/post/edit/<int:id>",methods=['POST'])
def post_edit(id): 
  if 'user_id' not in session: 
    return redirect('/logout')
  data = { 
    'id':id, 
    'title':request.form['title'], 
    "technology" : request.form['technology'], 
    "description": request.form['description']
  }
  post.Post.edit_post(data)
  return redirect(f"/post/{id}")

@app.route("/discussion_board")
def discussion_board(): 
  if 'user_id' not in session: 
    return redirect('/logout')
  data = {"id": session['user_id']}
  logged_user = user.User.get_user_by_id(data)
  all_posts = post.Post.get_all_posts()
  return render_template('discussion_board.html',logged_user = logged_user,all_posts=all_posts)

@app.route("/posts/<technology>")
def posts_by_tech(technology): 
  if 'user_id' not in session: 
    return redirect('/logout')
  data = {"technology":technology}
  all_posts=post.Post.get_all_posts_by_tech(data)
  return render_template("/discussions.html",all_posts=all_posts)
