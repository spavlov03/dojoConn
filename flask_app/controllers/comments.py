from flask import render_template, redirect, request,session
from flask_app import app
from flask_app.models import user,post,comment

@app.route("/post/<int:id>/comment",methods=['POST'])
def add_comment(id): 
  if 'user_id' not in session: 
    return redirect('/logout')
  if not comment.Comment.comment_validation(request.form): 
    return redirect(f'/post/{id}')
  data = {
    "comment": request.form['comment'], 
    "post_id": id, 
    "user_id": request.form['user_id']
  }
  print("DATA when adding comment",data)
  comment.Comment.add_commment(data)
  return redirect(f"/post/{id}")

@app.route("/post/<int:post_id>/comment/<int:id>/delete")
def delete_comment(id,post_id):
  if 'user_id' not in session: 
    return redirect('/logout')
  data = {"id":id}
  comment.Comment.delete_comment(data)
  return redirect(f"/post/{post_id}")