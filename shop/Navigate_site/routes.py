import secrets, os
from flask import current_app, flash, redirect, render_template, url_for, request, session
from shop import db, app, Navigate_site
from shop.admin import routes

@app.route('/')
def home():
    return render_template('Navigate_site/index.html')