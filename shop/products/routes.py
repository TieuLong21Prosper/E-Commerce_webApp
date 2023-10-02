import secrets, os
from flask import current_app, flash, redirect, render_template, url_for, request, session
from shop import db, app, photos, products
from .models import Brand, Category, Addproduct
from .forms import Addproducts
from shop.admin import routes

@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    products = Addproduct.query.filter(Addproduct.stock > 0).paginate(page=page, per_page=4)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', products=products, brands=brands, categories=categories)

@app.route('/category/<int:id>')
def filter_byCategory(id):
    category = Addproduct.query.filter_by(category_id = id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', category = category, categories = categories, brands = brands)

@app.route('/brand/<int:id>')
def filter_byBrand(id):
    brand = Addproduct.query.filter_by(brand_id = id)
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('products/index.html', brand = brand, brands = brands, categories = categories)

@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The Brand {getbrand} was added to your database successfully', 'success')
        db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('products/addbrand.html', brands='brands')

@app.route('/updatebrand/<int:id>', methods=['GET','POST'])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = brand
        flash(f'The Brand {updatebrand.name} was updated successfully', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update Brand', updatebrand=updatebrand)

@app.route('/updatecategory/<int:id>', methods=['GET','POST'])
def updatecategory(id):
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecategory.name = category
        flash(f'The Category {updatecategory.name} was updated successfully', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html', title='Update Category', updatecategory=updatecategory)

@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if request.method == 'POST':
        getbrand = request.form.get('category')
        cat = Category(name=getbrand)
        db.session.add(cat)
        flash(f'The Category {getbrand} was added to your database successfully', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('products/addbrand.html')

@app.route('/addproduct', methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        redirect(url_for('login'))
    brands = Brand.query.all()
    Categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.desc.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_bytes(10).hex() + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_bytes(10).hex() + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_bytes(10).hex() + ".")
        
        addpro = Addproduct(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,brand_id=brand,category_id=category,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addpro)
        flash(f'The Product {name} has been added to your database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html', title='Add Product', form=form, brands=brands, categories=Categories)

@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    brands = Brand.query.all()
    categories = Category.query.all()
    product = Addproduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    #define var product contains data of form
    form = Addproducts(request.form)
    #put data to form
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.colors = form.colors.data
        product.desc = form.desc.data
        product.brand_id = brand
        product.category_id = category
        product.category_id = request.form.get('category')
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_bytes(10).hex() + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_bytes(10).hex() + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_bytes(10).hex() + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_bytes(10).hex() + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_bytes(10).hex() + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_bytes(10).hex() + ".")
        db.session.commit()
        flash(f'The Product {product.name} has been updated', 'success')
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.desc.data = product.desc
    #get pictures
    return render_template('products/updateproduct.html', form=form, bands=brands, categories=categories, product=product)

@app.route('/deletebrand/<int:id>', methods=['POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        
        flash(f'The Brand {brand.name} has been deleted','success')
        db.session.commit()
        return redirect(url_for('brands'))
    flash(f'The Brand {brand.name} can not be deleted', 'danger')
    return redirect(url_for('brands'))

@app.route('/deletecategory/<int:id>', methods=['POST'])
def deletecategory(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        flash(f'The Category {category.name} has been deleted','success')
        db.session.commit()
        return redirect(url_for('categories'))
    flash(f'The Categpry {category.name} can not be deleted', 'danger')
    return redirect(url_for('categories'))

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method == 'POST':
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
            except Exception as e:
                print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The Product {product.name} has been deleted','success')
        return redirect(url_for('admin'))
    flash(f'The Product {product.name} can not be deleted', 'danger')
    return redirect(url_for('admin'))