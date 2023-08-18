from flask import render_template, redirect, request,session, Markup
from flask_app import app
from flask_app.models import user,post,comment
import humanize 
import markdown2
# messing around with different markdown editors -maleko
# from flask_ckeditor import CKEditor
# ckeditor = CKEditor()


@app.route("/dashboard")
def dashboard():
    # would like to add a # limit of posts displayed per page eventually -maleko
    page = request.args.get('page', 1, type=int)
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": session['user_id']}
    logged_user = user.User.get_user_by_id(data)
    all_posts = post.Post.get_all_posts()
    
    # added this for markdown purposes -maleko
    for post_item in all_posts:
      post_item.description = markdown2.markdown(post_item.description)
    
    #i added the following code block to count the number of comments of each post -Maleko
    comments = {}
    for post_item in all_posts:
      post_item.humanized_time = humanize.naturaltime(post_item.created_at)
      post_id = post_item.id
      count_result = post.Post.commentCount(post_id)
      comment_sum = count_result[0]['total_comments']
      comments[post_id]= comment_sum
    postsVotes = {}
    for post_item in all_posts: 
        post_id = post_item.id
        count_result = post.Post.postsVotesCount(post_id)
        votes_sum = count_result[0]['total_upvotes']
        # print("Count Result",votes_sum)
        postsVotes[post_id]= votes_sum
    return render_template('dashboard.html',logged_user = logged_user,all_posts=all_posts, comments=comments,postsVotes=postsVotes)

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
    post_data = {"id": id}
    this_post = post.Post.get_one_post_by_id_with_user(post_data)
    post_upvotes = post.Post.postsVotesCount(id)
    post_comments = comment.Comment.get_comments_by_post(post_data)
    print("POST COMMENTS-----",post_comments)
    comments_count = {}
    for com in post_comments: 
      comments_count[com.id] = post.Post.commentsVotesCount(com.id)
    print("Comments for post---->>>",comments_count)
    if 'user_id' not in session:
        this_post.humanized_time = humanize.naturaltime(this_post.created_at)
        this_post.description = markdown2.markdown(this_post.description)
        for comment_obj in post_comments:
            comment_obj.humanized_time = humanize.naturaltime(comment_obj.created_at)
        return render_template("view_post.html", this_post=this_post, post_comments=post_comments, post_upvotes=post_upvotes, comments_count=comments_count)

    data = {"id": session['user_id']}
    logged_user = user.User.get_user_by_id(data)
    this_post.humanized_time = humanize.naturaltime(this_post.created_at)
    this_post.description = markdown2.markdown(this_post.description)
    for comment_obj in post_comments:
        comment_obj.humanized_time = humanize.naturaltime(comment_obj.created_at)
    return render_template("view_post.html", this_post=this_post, logged_user=logged_user, post_comments=post_comments,post_upvotes=post_upvotes,comments_count=comments_count)

# @app.route("/post/<int:id>/")
# def view_post(id):
#   post_data = {"id":id}
#   this_post = post.Post.get_one_post_by_id_with_user(post_data)
#   post_comments = comment.Comment.get_comments_by_post(post_data)

  
#   if 'user_id' not in session: 
#     this_post.humanized_time = humanize.naturaltime(this_post.created_at)
#     this_post.description = markdown2.markdown(this_post.description)
#     return render_template("view_post.html",this_post=this_post,post_comments=post_comments)
  
#   data = {"id": session['user_id']}
#   logged_user = user.User.get_user_by_id(data)
#   this_post.humanized_time = humanize.naturaltime(this_post.created_at)
#   this_post.description = markdown2.markdown(this_post.description)
#   return render_template("view_post.html",this_post=this_post,logged_user=logged_user,post_comments=post_comments)

@app.route("/post/<int:id>/edit")
def edit_post(id):
  if 'user_id' not in session: 
    return redirect('/logout')
  post_data = {"id":id}
  this_post = post.Post.get_one_post_by_id_with_user(post_data)
  if session['user_id'] != this_post.user_id:
        return redirect(f'/post/{id}')
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

@app.route("/post/<int:id>/delete")
def delete_post(id): 
  if 'user_id' not in session: 
    return redirect('/logout')
  data = {"id":id}
  this_post = post.Post.get_one_post_by_id_with_user(data)
  if session['user_id'] != this_post.user_id:
        return redirect(f'/post/{id}')
  post_data = {"post_id":id}
  comment.Comment.delete_all_comments_of_post(post_data)
  post.Post.delete_post(data)
  return redirect("/dashboard")

@app.route("/discussion_board")
def discussion_board(): 
  all_posts = post.Post.get_all_posts()
  if 'user_id' not in session: 

    return render_template('discussion_board.html',all_posts=all_posts)

  data = {"id": session['user_id']}
  logged_user = user.User.get_user_by_id(data)
  # all_posts = post.Post.get_all_posts()
  return render_template('discussion_board.html',logged_user = logged_user,all_posts=all_posts)


@app.route("/posts/<technology>")
def posts_by_tech(technology): 
    data = {"technology": technology}
    posts_data = post.Post.get_all_posts_by_tech(data)
    
    logged_user = None
    if 'user_id' in session:
        logged_user_data = {"id": session['user_id']}
        logged_user = user.User.get_user_by_id(logged_user_data)

    all_posts = []
    comments = {}

    for post_data in posts_data:
        p = post.Post(post_data)
        p.markdown_content = Markup(markdown2.markdown(p.description))
        p.humanized_time = humanize.naturaltime(p.created_at)

    postsVotes = {}
    for post_item in all_posts: 
        post_id = post_item.id
        count_result = post.Post.postsVotesCount(post_id)
        votes_sum = count_result[0]['total_upvotes']
        # print("Count Result",votes_sum)
        postsVotes[post_id]= votes_sum

        post_id = p.id
        count_result = post.Post.commentCount(post_id)
        comment_sum = count_result[0]['total_comments']
        comments[post_id] = comment_sum
        
        creator_info = {
            "id": post_data["creator_id"],
            "first_name": post_data["creator_first_name"],
            "last_name": post_data["creator_last_name"],
            "email": post_data["creator_email"],
            "password": post_data["creator_password"],
            "created_at": post_data["creator_created_at"],
            "updated_at": post_data["creator_updated_at"]
        }
        creator = user.User(creator_info)
        p.creator = creator

        all_posts.append(p)

    return render_template("/discussions.html", all_posts=all_posts, logged_user=logged_user, comments=comments, postsVotes=postsVotes)

# WORKING
# @app.route("/search",methods=["POST"])
# def search(): 
#   # data = {'title':'%'+request.form['search']+'%'}
#   data = {'title':request.form['search']}
#   search = "search"
#   all_posts=post.Post.search(data)
#   if 'user_id' not in session:
#     return render_template("/discussions.html",all_posts=all_posts,search=search)
#   logged_user_data = {"id": session['user_id']}
#   logged_user = user.User.get_user_by_id(logged_user_data)
#   return render_template("/discussions.html",all_posts=all_posts, logged_user=logged_user,search=search)

@app.route("/search", methods=["POST"])
def search():
    data = {'title': request.form['search']}
    search = "search"
    all_posts = post.Post.search(data)
    logged_user = None
    
    if 'user_id' in session:
        logged_user_data = {"id": session['user_id']}
        logged_user = user.User.get_user_by_id(logged_user_data)
        return render_template("/discussions.html", all_posts=all_posts, logged_user=logged_user, search=search)
    
    return render_template("/discussions.html", all_posts=all_posts, search=search, logged_user=logged_user)

  
