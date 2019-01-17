from flask import Blueprint

home = Blueprint("home",__name__,template_folder="home")

import app.home.views