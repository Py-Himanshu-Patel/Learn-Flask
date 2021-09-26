from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from flasker.auth import login_required
from flasker.db import get_db

blog_blueprint = Blueprint('blog', __name__)
