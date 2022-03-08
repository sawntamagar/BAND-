from flask_restx import Resource, fields, Namespace, marshal_with
from flask import request,jsonify
from flask_login import login_required, current_user
from .models import Order, Customer


order_tshirt_ns = Namespace('order_tshirt', description = 'this is for ordering the tshirt')

order_model = order_tshirt_ns.model(
    "Order", {
        "size": fields.String(),
        "quantity": fields.Integer()
       
    }
)

@order_tshirt_ns.route('/customer/<int:customer_id>/tshirts')
class TshirtsResource(Resource):
    
    @order_tshirt_ns.marshal_with(order_model)
    @order_tshirt_ns.expect(order_model)   
    def post(self, customer_id):
        data = request.get_json()
        new_order = Order(
            size = data.get('size'),
            quantity = data.get('quantity'), customer_id=customer_id
        )                  
        new_order.save()
        return new_order, 201
    
    
#get  order by specific user
@order_tshirt_ns.route('/customer/<int:customer_id>/tshirt/<int:id>')
class TshirtResource(Resource):
    
    @order_tshirt_ns.marshal_with(order_model)
    def get(self, customer_id, id):
        
        order = Order.query.filter_by(id=id).first()
        
        return order
        
@order_tshirt_ns.route('/customer/<int:customer_id>/tshirt/<int:id>/edit')
class TshirtResource(Resource):    
    @order_tshirt_ns.marshal_with(order_model)
    def put(self,customer_id, id):
        order_to_update =  Order.query.filter_by(id=id).first()
        data = request.get_json()
        order_to_update.update(data.get('size'), 
                               data.get('quantity'))
        
        return order_to_update
           
@order_tshirt_ns.route('/customer/<int:customer_id>/tshirt/<int:id>/delete')
class TshirtResource(Resource):        
    @order_tshirt_ns.marshal_with(order_model)
    def delete(self,customer_id,id):
        order_to_delete =  Order.query.filter_by(id=id).first()
        order_to_delete.delete()
         
        return order_to_delete
        


    
    