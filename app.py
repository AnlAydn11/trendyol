from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key ='key' # It is necessary for the flashes. 

def init_db(): # Initialized our D.B. here
    conn =sqlite3.connect('database.db')
    c =conn.cursor()
    
    #Categories table is created
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL UNIQUE)''')

    # Products table is created
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_no TEXT NOT NULL UNIQUE,
                  title TEXT NOT NULL,
                  description TEXT NOT NULL,
                  price REAL NOT NULL,
                  original_price REAL,
                  brand TEXT NOT NULL,
                  category_id INTEGER,
                  image_url TEXT NOT NULL,
                  FOREIGN KEY (category_id) REFERENCES categories (id))''')
    
    #For this site we only have one user, but we had an issue with creating users 
    #table and for some strange reason we wren't able to solve it by saying IF NOT EXISTS.
    c.execute('DROP TABLE IF EXISTS users')
    
    # Created users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE NOT NULL,
                  name TEXT,
                  phone TEXT,
                  address TEXT)''')
    
    # Checked if user exists
    user_exists = c.execute('SELECT COUNT(*) FROM users WHERE email = ?', 
                           ('anil@gmail.com',)).fetchone()[0]
    
    if not user_exists:
        c.execute('INSERT INTO users (email, name) VALUES (?, ?)',
                 ('anil@gmail.com', 'Anil'))

    #Checked if categories exist.
    categories_count = c.execute('SELECT COUNT(*) FROM categories').fetchone()[0]
    
    #If not created one here.
    if categories_count==0:
        categories =[('Women Fashion',),('Men Fashion',),('Electronics',),('Home &Living',),('Cosmetics',),]
        c.executemany('INSERT INTO categories (name) VALUES (?)', categories)

    #We are told to add at least 10 default products. However, we put more than that.
    product_count = c.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    if product_count == 0:
        sample_products = [
            ('P001', 'Mother and Child Collection', 'A heartwarming collection for mothers and children, depicting love and care', 299.99, 399.99, 'FamilyCo', 1, '/static/images/mother_child_1.jpg'),
            ('P002', 'Elegant Night Dress', 'A stylish and comfortable night dress for women, suitable for evening wear', 199.99, 249.99, 'NightWear', 1, '/static/images/female_night_dress_2.jpg'),
            ('P003', 'Tech Pattern Phone Case', 'A modern phone case showcasing advanced technology-inspired design', 79.99, 99.99, 'TechCase', 3, '/static/images/telefone_kilifi_teknoloji_2.jpg'),
            ('P004', 'Fast Charging Device', 'A sleek and compact charging device reflecting technological innovation', 149.99, 199.99, 'PowerTech', 3, '/static/images/teknoloji_şarj.jpg'),
            ('P005', 'Minimalist Phone Case', 'A high-tech phone case with a minimalist and futuristic look', 69.99, 89.99, 'TechCase', 3, '/static/images/telefone_kilifi_teknoloji.jpg'),
            ('P006', 'Casual Outdoor Jacket', 'A fashionable and versatile jacket for casual or outdoor use', 399.99, 499.99, 'OutdoorStyle', 2, '/static/images/jacket.jpg'),
            ('P007', 'Premium Cosmetics Set', 'A chic cosmetic product designed for elegance and usability', 159.99, 199.99, 'BeautyCo', 5, '/static/images/cosmetic_2.jpg'),
            ('P008', 'Women\'s Designer Jacket', 'A trendy jacket for women, perfect for both style and comfort', 449.99, 549.99, 'Fashionista', 1, '/static/images/femalejacket.jpg'),
            ('P009', 'Premium Collection Item', 'A zoomed-in view of our premium product, emphasizing intricate details and quality', 299.99, 399.99, 'LuxBrand', 1, '/static/images/1_org_zoom (1).jpg'),
            ('P010', 'Daily Skincare Essential', 'A beautifully packaged cosmetic item, ideal for daily use', 129.99, 159.99, 'BeautyCo', 5, '/static/images/cosmetic_1.jpg'),
            ('P011', 'Elegant Home Decor', 'A charming home decoration piece that adds elegance to any space', 199.99, 249.99, 'HomeLux', 4, '/static/images/home_decoration_3.jpg'),
            ('P012', 'Modern Home Accent', 'A stylish and modern decorative item for enhancing interior aesthetics', 179.99, 229.99, 'HomeLux', 4, '/static/images/home_decoration_2.jpg'),
            ('P013', 'Designer Collection Piece', 'Another detailed close-up image of our designer product, highlighting craftsmanship shoe', 279.99, 349.99, 'LuxBrand', 1, '/static/images/1_org_zoom (2).jpg'),
            ('P014', 'Comfort Night Dress', 'A comfortable and elegant night dress tailored for women', 189.99, 239.99, 'NightWear', 1, '/static/images/female_night_dress.jpg'),
        ]
        c.executemany('''INSERT INTO products 
                         (product_no, title, description, price, original_price, brand, category_id, image_url)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', sample_products)
    conn.commit()
    conn.close()
    
    
    
@app.route('/')
def home():
    conn =sqlite3.connect('database.db')
    conn.row_factory =sqlite3.Row
    c =conn.cursor()
    
    categories =c.execute('SELECT * FROM categories').fetchall()
    products =c.execute('''
        SELECT p.*, c.name as category_name 
        FROM products p 
        JOIN categories c ON p.category_id = c.id 
        ORDER BY RANDOM() 
        LIMIT 8
        ''').fetchall()
    
    conn.close()
    return render_template('home.html',categories=categories, products=products)

@app.route('/search')
def search():
    query =request.args.get('q', '')
    price_range =request.args.get('price_range')
    selected_categories= request.args.getlist('category')
    selected_brands=request.args.getlist('brand')
    sort_by=request.args.get('sort', 'relevance')
    
    conn =sqlite3.connect('database.db')
    conn.row_factory =sqlite3.Row
    c =conn.cursor()
    
    query_parts =[]#This is our base query
    params =[]
    
    if query:
        query_parts.append("(p.title LIKE ? OR p.description LIKE ? OR p.brand LIKE ?)")
        params.extend([f'%{query}%'] * 3)
    
    #Price range filters are here
    if price_range:
        if price_range == '0-100':
            query_parts.append("p.price BETWEEN 0 AND 100")
        elif price_range == '101-200':
            query_parts.append("p.price BETWEEN 101 AND 200")
    
    #Category filters are here
    if selected_categories:
        placeholders = ','.join(['?' for _ in selected_categories])
        query_parts.append(f"p.category_id IN ({placeholders})")
        params.extend(selected_categories)
    
    #Brand filters are here
    if selected_brands:
        placeholders = ','.join(['?' for _ in selected_brands])
        query_parts.append(f"p.brand IN ({placeholders})")
        params.extend(selected_brands)
    
    where_clause =' AND '.join(query_parts) if query_parts else '1'
    
    #Sorting methods
    order_by ={
        'price_low': 'p.price ASC',
        'price_high': 'p.price DESC',
        'newest': 'p.id DESC',
        'relevance': 'p.id DESC'  #Our default sorting method is this
    }.get(sort_by, 'p.id DESC')
    
    sql =f'''
        SELECT p.*, c.name as category_name 
        FROM products p 
        JOIN categories c ON p.category_id = c.id 
        WHERE {where_clause}
        ORDER BY {order_by}
    '''
    
    products =c.execute(sql, params).fetchall()
    
    # Got all of the categories and unique brands for filtering here
    categories =c.execute('SELECT * FROM categories').fetchall()
    brands =[row[0] for row in c.execute('SELECT DISTINCT brand FROM products').fetchall()]
    conn.close()
    
    return render_template('search.html',
                         products=products,
                         query=query,
                         categories=categories,
                         brands=brands,
                         price_range=price_range,
                         selected_categories=selected_categories,
                         selected_brands=selected_brands,
                         sort_by=sort_by)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn =sqlite3.connect('database.db')
    conn.row_factory =sqlite3.Row
    c =conn.cursor()
    product =c.execute('''
        SELECT p.*, c.name as category_name 
        FROM products p 
        JOIN categories c ON p.category_id = c.id 
        WHERE p.id = ?
    ''', (product_id,)).fetchone()
    
    if product is None:#If non existing product is asked for, we send the request to 404.html
        conn.close()
        return render_template('404.html'), 404

    #Got the related products from same category here.
    related_products = c.execute('''
        SELECT * FROM products 
        WHERE category_id = ? AND id != ? 
        LIMIT 4
    ''', (product['category_id'], product_id)).fetchall()
    conn.close()
    return render_template('detail.html', product=product, related_products=related_products)

@app.route('/category/<int:category_id>')
def category(category_id):
    conn =sqlite3.connect('database.db')
    conn.row_factory =sqlite3.Row
    c =conn.cursor()
    
    category =c.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
    products =c.execute('''
        SELECT p.*, c.name as category_name 
        FROM products p 
        JOIN categories c ON p.category_id = c.id 
        WHERE c.id = ?
    ''',(category_id,)).fetchall()
    
    categories =c.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return render_template('category.html',category=category,products=products,categories=categories)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/account')
def account():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    user = c.execute('SELECT * FROM users WHERE email = ?', ('anıl@gmail.com',)).fetchone()
    conn.close()
    return render_template('account.html', user=user)

@app.route('/account/edit', methods=['GET', 'POST'])
def edit_account():
    conn =sqlite3.connect('database.db')
    conn.row_factory =sqlite3.Row
    c =conn.cursor()
    if request.method =='POST':
        name =request.form.get('name')
        phone =request.form.get('phone')
        address =request.form.get('address')
        try:
            c.execute('''UPDATE users 
                        SET name = ?, phone = ?, address = ?
                        WHERE email = ?''',
                     (name, phone, address, 'anil@gmail.com'))
            conn.commit()
            flash('Profile updated successfully!')
            return redirect(url_for('account'))  # We made sure to return in this part of the code.
        finally:
            conn.close()
    
    #If the request is a GET request.
    try:
        user =c.execute('SELECT * FROM users WHERE email = ?', ('anil@gmail.com',)).fetchone()
        return render_template('edit_account.html',user=user) # We made sure to return here
    finally:
        conn.close()

if __name__ == '__main__':
    os.makedirs('static/images',exist_ok=True)
    init_db()
    app.run(debug=True)