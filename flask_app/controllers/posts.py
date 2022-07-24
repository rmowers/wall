from unicodedata import category
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post

@app.route("/create/post", methods=["POST"])
def create_post():
    if "user_id" not in session:
        return redirect("/")
    data = {
        "content" : request.form["content"],
        "user_id" : session["user_id"]
    }
    if request.form["content"] == "":
        flash("Cannot create an empty post", "make_post")
        return redirect("/dashboard")
    else:
        post.Post.save(data)
    return redirect("/dashboard")


@app.route("/like/post/<int:id>")
def like_post(id):
    if "user_id" not in session:
        return redirect("/")
    liked_post = post.Post.get_one_with_likes({"id":id})
    if session["user_id"] not in liked_post.liked_by:
        like_data = {"user_id": session["user_id"], "post_id" : id}
        post.Post.like(like_data)
    return redirect("/dashboard")


@app.route("/delete/post/<int:id>")
def delete_post(id):
    if "user_id" not in session:
        return redirect("/")
    get_one_with_user = post.Post.get_one_with_user({"id":id})
    if session["user_id"] != get_one_with_user.creator.id:
        flash("You cannot delete a post that isn't yours","post_action")
        return redirect("/dashboard")
    data = {
        "id" : id,
    }
    post.Post.delete_post(data)
    return redirect("/dashboard")