from flask import render_template, flash, redirect, session, url_for, request, Markup
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html",
        #title='Current Callbacks',
        #test='Current Callbacks',
        #callbacks=callbacks,
        )
