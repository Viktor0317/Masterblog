"""
Flask Blog Application

This is a simple blog application built using Flask, where users can:
- View all blog posts
- Add new blog posts
- Update existing blog posts
- Delete blog posts

Data is stored in a JSON file instead of a database.
"""

from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)


def load_posts():
    """
    Load blog posts from the JSON file.

    Returns:
        list: A list of dictionaries representing blog posts.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(file_path, 'r') as file:
        return json.load(file)


def save_posts(posts):
    """
    Save the updated list of blog posts to the JSON file.

    Args:
        posts (list): A list of dictionaries representing blog posts.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(file_path, 'w') as file:
        json.dump(posts, file, indent=4)


def fetch_post_by_id(post_id):
    """
    Fetch a single blog post by its unique ID.

    Args:
        post_id (int): The ID of the blog post to retrieve.

    Returns:
        dict or None: The blog post if found, otherwise None.
    """
    blog_posts = load_posts()
    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None  # Return None if not found


@app.route('/')
def index():
    """
    Display the homepage with all blog posts.

    Returns:
        str: Rendered HTML template displaying blog posts.
    """
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle adding a new blog post.

    - If GET request, display the form to create a new post.
    - If POST request, save the new post and redirect to homepage.

    Returns:
        str: Rendered template or redirect to homepage.
    """
    if request.method == 'POST':
        blog_posts = load_posts()

        new_post = {
            "id": max(post["id"] for post in blog_posts) + 1 if blog_posts else 1,
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content")
        }

        blog_posts.append(new_post)
        save_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle updating an existing blog post.

    - If GET request, display the form pre-filled with the post's data.
    - If POST request, update the post and save changes.

    Args:
        post_id (int): The ID of the blog post to update.

    Returns:
        str: Rendered template or redirect to homepage.
    """
    blog_posts = load_posts()

    for post in blog_posts:
        if post["id"] == post_id:
            if request.method == 'POST':
                post["author"] = request.form.get("author")
                post["title"] = request.form.get("title")
                post["content"] = request.form.get("content")

                save_posts(blog_posts)
                return redirect(url_for('index'))

            return render_template('update.html', post=post)

    return "Post not found", 404


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """
    Handle deleting a blog post.

    - Removes the specified post from the list.
    - Saves the updated list and redirects to homepage.

    Args:
        post_id (int): The ID of the blog post to delete.

    Returns:
        Response: Redirect to homepage after deletion.
    """
    blog_posts = load_posts()
    blog_posts = [post for post in blog_posts if post["id"] != post_id]
    save_posts(blog_posts)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
