from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


# Function to load blog posts from JSON file
def load_posts():
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(file_path, 'r') as file:
        return json.load(file)


# Function to save blog posts to JSON file
def save_posts(posts):
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(file_path, 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    blog_posts = load_posts()  # Load posts from JSON
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        blog_posts = load_posts()  # Load current posts

        # Get form data
        new_post = {
            "id": max(post["id"] for post in blog_posts) + 1 if blog_posts else 1,  # Generate unique ID
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content")
        }

        # Append new post and save
        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))  # Redirect to home page

    return render_template('add.html')  # Render the add post form


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
