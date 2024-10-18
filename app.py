import requests
from flask import Flask, render_template, Response, redirect, request, jsonify, url_for
import os
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os

from controllers.OrderController import OrderController
from controllers.ProductController import ProductController
from controllers.ProductTypeController import ProductTypeController
from controllers.WhoolStockController import WhoolStockController

load_dotenv()
database = os.getenv("DATABASE")

app = Flask(__name__)

#Static folder route
app.static_folder = 'static'  

#Web app secret key (Need to change)
app.secret_key = '123456789' 



# Login route

@app.route('/', methods=['GET'])
def main():
    
    connection = OrderController(database)
    current_month_orders = connection.read_current_month_order()
    return render_template('main.html', orders=current_month_orders)


# Product routes


@app.route('/product', methods=['GET'])
def product():
    
    connection = ProductController(database)
    products = connection.read_all_product()
    return render_template('product.html', products=products)

@app.route('/product-add', methods=['GET', 'POST'])
def add_product():

    if 'productName' in request.form:
        name = request.form['productName']
        
        data = {"name": name}

        connection = ProductController(database)
        connection.write_product(data)
        
        return redirect(url_for('product'))
    
@app.route('/product-update', methods=['GET', 'POST'])
def update_product():
    
    connection = ProductController(database)
    products = connection.read_all_product()
    
    product_id = int(request.form['productId'])
    name = request.form['productName']
    
    data = {'name': name }
    
    connection.update_product(product_id, data)
    
    return redirect(url_for('product'))

@app.route('/product-delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    
    connection = ProductController(database)
    connection.delete_product(product_id)
    
    return redirect(url_for('product'))


# Product Type routes 


@app.route('/product-type/<int:product_id>', methods=['GET', 'POST'])
def product_type(product_id):
    
    connection = ProductTypeController(database)
    product_types = connection.read_filtered_product_type(product_id)
    product_types = [{'id':product.id, 'name': product.name, 'price': product.price, 'parent':product.product.id} for product in product_types]
    return jsonify(product_types)


@app.route('/product-type-add', methods=['GET', 'POST'])
def add_product_type():

    if 'productTypeName' in request.form and 'productTypeParent' in request.form and 'productTypePrice' in request.form:
        name = request.form['productTypeName']
        product_id = request.form['productTypeParent']
        price = request.form['productTypePrice']
        
        data = {"name": name, "product_id":product_id, "price":price} 

        connection = ProductTypeController(database)
        connection.write_product_type(data)
        
        return redirect(url_for('product'))
    
    
@app.route('/product-type-delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product_type(product_id):
    
    connection = ProductTypeController(database)
    connection.delete_product_type(product_id)
    
    return redirect(url_for('product'))

@app.route('/product-type-update', methods=['GET', 'POST'])
def update_product_type():
    
    connection = ProductTypeController(database)
    
    product_type_id = int(request.form['productTypeId'])
    name = request.form['updateProductTypeName']
    product_id = request.form['updateProductTypeParent']
    price = request.form['updateProductTypePrice']
    
    data = {'name': name, 'product_id':product_id, 'price':price }
    
    connection.update_product_type(product_type_id, data)
    
    return redirect(url_for('product'))


# Whool Stock routes


@app.route('/whool-stock', methods=['GET'])
def whool_stock():
    
    connection = WhoolStockController(database)
    whools = connection.read_all_whool_stock()
    return render_template('whool_stock.html', whools=whools)

@app.route('/whool-stock-add', methods=['GET', 'POST'])
def add_whool_stock():

    if 'whoolColor' in request.form and 'whoolQuantity' in request.form:
        color = request.form['whoolColor']
        quantity = int(request.form['whoolQuantity'])
        last_update = datetime.now()
        
        data = {"color": color, "quantity": quantity, "last_update":last_update}

        connection = WhoolStockController(database)
        connection.write_whool_stock(data)
        
        return redirect(url_for('whool_stock'))

@app.route('/whool-stock-update', methods=['GET', 'POST'])
def update_whool_stock():
    
    connection = WhoolStockController(database)
    
    whool_stock_id = int(request.form['stockId'])
    color = request.form['updateWhoolColor']
    quantity = request.form['updateWhoolQuantity']
    
    data = {'color': color, 'quantity':quantity }
    
    connection.update_whool_stock(whool_stock_id, data)
    
    return redirect(url_for('whool_stock'))

@app.route('/whool-stock-delete/<int:whool_stock_id>', methods=['GET', 'POST'])
def delete_whool_stock_id(whool_stock_id):
    
    connection = WhoolStockController(database)
    connection.delete_whool_stock(whool_stock_id)
    
    return redirect(url_for('whool_stock'))
    

    
if __name__ == "__main__": 
    app.run(host="127.0.0.1", port=5000, debug=True)   