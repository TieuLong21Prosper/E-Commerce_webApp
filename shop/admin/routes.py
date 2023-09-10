from flask import flash, render_template, session, request, redirect, url_for

from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from shop.products.models import Addproduct, Brand, Category
from .models import User

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)

@app.route('/brands')
def brands():
    if 'email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='Brand Page', brands=brands)

@app.route('/categories')
def categories():
    if 'email' not in session:
        flash('Please login first.', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='Category Page', categories=categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,password=hash_password)
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
                flash(f'Email {form.email.data} already exists', 'danger')
                # return redirect(url_for('register'))
        else:
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome {form.name.data}, Thank you for registering', 'success')
            return redirect(url_for('home'))
    return render_template('admin/register.html', form=form, title="Registration Page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data}, You are Login successfully', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong username or password please try again', 'warning')

    return render_template('admin/login.html', form=form, title="Login Page")