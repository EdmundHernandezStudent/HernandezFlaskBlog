import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

#code directly copied from video


# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True

#flash  the secret key to secure sessions
app.config['SECRET_KEY'] = 'your secret key'


#func to connect to database
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory=sqlite3.Row
    return conn

def get_post(post_id):
    conn=get_db_connection()
    post=conn.execute("SELECT * FROM posts WHERE id =?",(post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)

    return post


# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    conn = get_db_connection()
    query= "SELECT * FROM posts"
    posts=conn.execute(query).fetchall()
    conn.close()

    return render_template("index.html", posts=posts)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == "POST":
        title=request.form["title"]
        content=request.form["content"]

        if not title:
            flash("Title is required!")
        elif not content:
            flash("Content is required!")
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO posts (title, content) VALUES (?,?)", (title,content))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("create.html")

#route to edit post
@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post=get_post(id)

    if request.method == "POST":
        title=request.form["title"]
        content=request.form["content"]

        if not title:
            flash("Title is required!")
        elif not content:
            flash("Content is required!")
        else:
            conn = get_db_connection()
            conn.execute("UPDATE posts SET title =?, content=? WHERE id=?", (title,content,id))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))

    return render_template("edit.html",post=post)

# route to delete a post
@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post=get_post(id)
    conn=get_db_connection()
    conn.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('"{}" was deleted'.format(post['title']))

    return redirect(url_for("index"))

    return 


app.run(host="0.0.0.0", port=5001)