from flask import render_template, redirect, request,session,flash,url_for
import humanize
from flask_app import app
from flask_app.models import user, post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    if 'user_id' in session: 
        return redirect('/dashboard')
    all_posts = post.Post.get_all_posts()

    #i added the following code block to count the number of comments of each post -Maleko
    comments = {}
    for post_item in all_posts:
        post_item.humanized_time = humanize.naturaltime(post_item.created_at)
        post_id = post_item.id
        count_result = post.Post.commentCount(post_id)
        comment_sum = count_result[0]['total_comments']
        comments[post_id]= comment_sum
    return render_template('index.html', all_posts = all_posts, comments=comments)

@app.route("/register")
def register(): 
    return render_template('register.html')

@app.route("/register_user",methods=["POST"])
def register_user(): 
    if not user.User.validate_user(request.form):
        return redirect("/register")
    data = {
            "first_name":request.form['first_name'],
            "last_name":request.form['last_name'],
            "email":request.form['email'],
            "password":bcrypt.generate_password_hash(request.form['password'])
        }
    user_id = user.User.register(data)
    session['user_id'] = user_id

    return redirect("/dashboard")

@app.route("/login")
def login(): 
    return render_template('login.html')

@app.route('/login_user',methods=["POST"])
def login_user():
    users = user.User.get_user_info_by_email(request.form)
    if not users:
        flash("Invalid Email/Password","login")
        return redirect('/login')
    if not bcrypt.check_password_hash(users.password, request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect('/login')
    session['user_id'] = users.id
    return redirect("/dashboard")
    

@app.route('/user/<int:id>')
def view_user(id): 
    data = {"id":id}
    user_info = user.User.get_user_by_id(data)
    posts_by_user = post.Post.get_all_posts_by_user(data)
    if 'user_id' not in session: 
        return render_template('view_user.html', user_info=user_info,posts_by_user=posts_by_user)
    logged_user_data={"id":session['user_id']}
    logged_user = user.User.get_user_by_id(logged_user_data)
    return render_template('view_user.html', user_info=user_info,logged_user=logged_user,posts_by_user=posts_by_user)

@app.route('/user/<int:id>/edit')
def edit_user(id): 
    if 'user_id' not in session: 
        return redirect('/logout')
    if session['user_id'] != id:
        return redirect(f'/user/{id}')
    data = {"id":id}
    user_info = user.User.get_user_by_id(data)
    logged_user = user.User.get_user_by_id(data)
    return render_template('edit_user.html', user_info=user_info,logged_user=logged_user)

@app.route('/user/edit/<int:id>',methods=["POST"])
def user_edit(id): 
    if 'user_id' not in session: 
        return redirect('/logout')
    # user_id = session['user_id']
    # if not user.User.validate_user(request.form):  Might have to do separate validation of update
    #     return redirect(url_for('edit_user',id=user_id))
    data = { 
        'id' : id,
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email']
    }
    user.User.update_user(data)
    # return redirect(url_for('view_user',id=user_id)) This way works too. 
    return redirect(f"/user/{id}")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

