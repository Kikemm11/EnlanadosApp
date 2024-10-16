import requests
from flask import Flask, render_template, Response, redirect, request, jsonify, url_for
import os
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os

from controllers.OrderController import OrderController
from controllers.ProductController import ProdutController

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

@app.route('/product', methods=['GET'])
def product():
    
    connection = ProdutController(database)
    products = connection.read_all_product()
    return render_template('product.html', products=products)

@app.route('/product-add', methods=['GET', 'POST'])
def add_product():

    if 'productName' in request.form:
        name = request.form['productName']
        
        data = {"name": name}

        connection = ProdutController(database)
        products = connection.read_all_product()
        connection.write_product(data)
        
        return redirect(url_for('product'))
    
@app.route('/product-update', methods=['GET', 'POST'])
def update_product():
    
    connection = ProdutController(database)
    products = connection.read_all_product()
    
    product_id = int(request.form['productId'])
    name = request.form['productName']
    
    data = {'name': name }
    
    connection.update_product(product_id, data)
    
    return redirect(url_for('product'))

@app.route('/product-delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    
    connection = ProdutController(database)
    products = connection.read_all_product()
    connection.delete_product(product_id)
    
    return redirect(url_for('product'))
    

    
if __name__ == "__main__": 
    
    app.run(host="127.0.0.1", port=5000, debug=True)   