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
from controllers.StatusController import StatusController
from controllers.CityController import CityController
from controllers.PaymentMethodController import PaymentMethodController 
from controllers.OrderWhoolController import OrderWhoolController

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



# Order routes


@app.route('/order', methods=['GET', 'POST'])
def order():
    
    
    order_connection = OrderController(database)
    status_connection = StatusController(database)
    
    statuses = status_connection.read_all_status()
    
    if request.method == 'GET':
        orders = order_connection.read_current_month_order() 
        
    else:
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        status = request.form['orderStatus']
        
        orders = order_connection.read_filter_order(start_date, end_date, status)
        
    return render_template('order.html', orders=orders, statuses=statuses)

@app.route('/order-add', methods=['GET', 'POST'])
def add_order():

    if request.method == 'GET':
        
        city_connection = CityController(database)
        product_connection = ProductController(database)
        product_type_connection = ProductTypeController(database)
        payment_method_connection = PaymentMethodController(database)
        whool_stock_connection = WhoolStockController(database)
        
        cities = city_connection.read_all_city()
        products = product_connection.read_all_product()
        product_types = product_type_connection.read_all_product_type()
        payment_methods = payment_method_connection.read_all_payment_method()
        whool_stocks = whool_stock_connection.read_all_whool_stock()
        
        return render_template('order_add.html', cities=cities, products=products, product_types=product_types, payment_methods=payment_methods, whool_stocks=whool_stocks)
    
    else:
        
        order_connection = OrderController(database)
        order_whool_connection = OrderWhoolController(database)
        
        client = request.form['orderClient']
        city = request.form['orderCity']
        description = request.form['orderDescription']
        
        product_type = request.form['orderProductType']
        added_price = request.form['orderAddedPrice']
        credit = request.form['orderCredit']
        payment_method = request.form['orderPaymentMethod']

        selected_whool_stock_ids = request.form.getlist('whool_stocks')
        estimated_date = request.form['orderEstimatedDate']

        selected_whool_stock_ids = [int(whool) for whool in selected_whool_stock_ids]
        
        data = {'client': client,
                'city_id': int(city),
                'description': description,
                'product_type_id': int(product_type),
                'added_price': float(added_price) if added_price != '' else 0.0,
                'credit': float(credit) if credit != '' else 0.0,
                'payment_method_id': int(payment_method),
                'estimated_date': estimated_date
                }

        order_id = order_connection.write_order(data)

        for whool_stock_id in selected_whool_stock_ids:
            data = {'order_id': order_id, 'whool_stock_id': whool_stock_id}
            order_whool_connection.write_order_whool_stock(data)
        
        
        return redirect(url_for('order'))
        
@app.route('/order-deliver/<int:order_id>', methods=['GET', 'POST'])
def deliver_order(order_id):
    
    order_connection = OrderController(database)
    order_connection.deliver_order(order_id) 
    
    return jsonify({'message': 'Product delivered successfully!'}), 200

@app.route('/order-cancel/<int:order_id>', methods=['GET', 'POST'])
def cancel_order(order_id):
    
    order_connection = OrderController(database)
    order_connection.cancel_order(order_id) 
    
    return jsonify({'message': 'Product delivered successfully!'}), 200

@app.route('/order-detail/<int:order_id>', methods=['GET', 'POST'])
def detail_order(order_id):
    
    
    if request.method == 'GET':
        
        city_connection = CityController(database)
        product_connection = ProductController(database)
        product_type_connection = ProductTypeController(database)
        payment_method_connection = PaymentMethodController(database)
        status_connection = StatusController(database)
        order_connection = OrderController(database)
        whool_stock_connection = WhoolStockController(database)
        
        cities = city_connection.read_all_city()
        products = product_connection.read_all_product()
        product_types = product_type_connection.read_all_product_type()
        payment_methods = payment_method_connection.read_all_payment_method()
        statuses = status_connection.read_all_status()
        order = order_connection.read_one_order(order_id)

        whool_colors = [whool.color for whool in order.whool_stocks]
        whool_stocks = whool_stock_connection.read_all_whool_stock()
        
        return render_template('order_detail.html', cities=cities, products=products, product_types=product_types, payment_methods=payment_methods, statuses=statuses, order=order, whool_colors=whool_colors, whool_stocks=whool_stocks)
    
    else:
        
        order_connection = OrderController(database)
        order_whool_connection = OrderWhoolController(database)
        
        client = request.form['orderClient']
        city = request.form['orderCity']
        description = request.form['orderDescription']
        
        product_type = request.form['orderProductType']
        added_price = request.form['orderAddedPrice']
        credit = request.form['orderCredit']
        payment_method = request.form['orderPaymentMethod']
        
        estimated_date = request.form['orderEstimatedDate']
        selected_whool_stock_ids = request.form.getlist('whool_stocks')

        selected_whool_stock_ids = [int(whool) for whool in selected_whool_stock_ids]
        
        data = {'client': client,
                'city_id': int(city),
                'description': description,
                'product_type_id': int(product_type),
                'added_price': float(added_price) if added_price != '' else 0.0,
                'credit': float(credit) if credit != '' else 0.0,
                'payment_method_id': int(payment_method),
                'estimated_date': estimated_date
                }

        order_connection.update_order(order_id, data)

        if selected_whool_stock_ids:
            order_whool_connection.update_order_whool_stock(order_id, selected_whool_stock_ids)

        return redirect(url_for('order'))
    

@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    
    if request.method == 'GET':
        
        return render_template('statistics.html')
    
    else:
        
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        order_connection = OrderController(database)
        
        data = order_connection.statistics_data(start_date, end_date)
        
        revenue = data['revenue']
        payment_methods_data = data['payment_methods_data']
        revenues_data = data['revenues_data']
        products_data = data['products_data']

        dates = {'start_date': start_date, 'end_date': end_date}
        
        return render_template('statistics.html', revenue=revenue, payment_methods_data=payment_methods_data, revenues_data=revenues_data, products_data=products_data, dates=dates)
        


if __name__ == "__main__": 
    app.run(host="127.0.0.1", port=5000, debug=True)   