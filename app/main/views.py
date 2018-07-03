import json

from flask import Flask, render_template, redirect, request, url_for, flash, make_response, jsonify
from flask_login import login_required, current_user 

from . import main
from ..models import Post, User
from .forms import PostForm
from app import db, moment
from .errors import page_not_found

@main.route("/")
def index():
    return render_template("index.html")

#添加文件,评论
@main.route("/post/", methods=["GET", "POST"])
def post():
    form = PostForm() 
    if request.method == "POST":
        if form.validate_on_submit():
            body = form.body.data
            post = Post(body=body, author=current_user._get_current_object(), )
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('.post'))
    return render_template("posts.html", form=form)

@main.route("/articles/")
def showPosts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("_posts.html", posts = posts)

@main.route("/article/<int:a_id>/", methods=['GET', 'POST'])
@login_required
def showArticle(a_id):
    user = current_user._get_current_object()
    if request.method == "POST":
        response = make_response("不能为空")
        if True:
            body = request.form.get("comment")
            if len(body) == 0:
                return response
            # father = Post.query.filter_by(id=a_id)
            # if father:
            #     f = father[0]
            #     f_path = f.path 
            #     my_path = f.path + str(a_id) +","
            #     print(my_path)
            # else:
            #     return response
            comment = Post(comment=body, author=user, pid=a_id)
            db.session.add(comment)
            db.session.flush() 
            db.session.refresh(comment)
            comment.make_path(sub=False)
            db.session.commit()
            flash("发表成功")

    comments = Post.query.filter_by(pid = a_id)
    post = Post.query.filter_by(id=a_id).first()
    is_collect = user.isCollection(a_id)
    if not post:
        redirect(url_for('.page_not_found'))
    return render_template("article.html", post=post, comments=comments.all(), is_collect = is_collect)   

@main.route("/is_collect/", methods=["POST"])
@login_required
def is_collect():
    user = current_user._get_current_object()
    data_json=request.get_data().decode('utf-8')
    data_dict=json.loads(data_json)
    value = data_dict['value']
    if value == 1:
        user.addCollection(data_dict['pid'])
    else:
        user.rmCollection(data_dict['pid'])   

    response = make_response("good")
    return response

@main.route("/sub_comment/", methods=["GET", "POST"])
@login_required
def comments():
    if request.method == "POST":
        response = make_response("不能为空")
        data = request.get_data().decode("utf-8")
        data_dict = json.loads(data)
        user = current_user._get_current_object()
        body = data_dict["body"]
        a_id = data_dict["pid"]
        print(type(data_dict))
        print(data_dict)
        if len(body) == 0:
            return response

        # father = Post.query.filter_by(id=int(a_id))   
        # if father:
        #     f = father[0]
        #     f_path = f.path 
        #     my_path = f.path + str(a_id) +","
        #     print(my_path)
        # else:
        #     return response
            
        comment = Post(comment=body, author=user, pid=a_id)
        db.session.add(comment)
        db.session.flush() 
        db.session.refresh(comment)
        comment.make_path()
        db.session.commit()
        return jsonify({"data": "ok"})

@main.route("/show_sub_comment/", methods=["GET"])
def showSubComment():
    data = request.get_data().decode("utf-8")
    data_dict = json.loads(data)
    pid = data_dict["pid"]

    sub_comment = Post.query.filter_by(path_)      
