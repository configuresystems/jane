from app.modules.domains.views import web as domains
from app.modules.users.views import web as users
from flask import render_template, flash, redirect, session, url_for, request, Markup
from app import app

app.register_blueprint(domains)
app.register_blueprint(users)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html",
        #title='Current Callbacks',
        #test='Current Callbacks',
        #callbacks=callbacks,
        )
