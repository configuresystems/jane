from app.modules.overview.views import web as overview
from app.modules.domains.views import web as domains
from app.modules.users.views import web as users
from app.core.logging.views import web as logs
from flask import render_template, flash, redirect, session, url_for, request, Markup
from app import app

app.register_blueprint(overview)
app.register_blueprint(domains)
app.register_blueprint(users)
app.register_blueprint(logs)

if not overview:
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template("index.html",
            #title='Current Callbacks',
            #test='Current Callbacks',
            #callbacks=callbacks,
            )
