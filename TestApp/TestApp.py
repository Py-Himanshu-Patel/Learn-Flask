from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def hello_world():
	return "<p>Hello Flask</p>"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

# both redirect to same page 
# http://127.0.0.1:8000/projects/ 
# http://127.0.0.1:8000/projects
@app.route('/projects/')
def projects():
    return 'The project page'

# http://127.0.0.1:8000/about   - works
# http://127.0.0.1:8000/about/  - 404
@app.route('/about')
def about():
    return 'The about page'



if __name__ == "__main__":
	app.run(debug=True)
