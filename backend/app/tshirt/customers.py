from flask_restx import Resource, Namespace, fields
from flask import request, make_response,jsonify

from .models import Customer

customer_ns = Namespace('customer', description='api for all customer')

customer_model = customer_ns.model(
    "customer", {
        "id":fields.Integer(),
        "name": fields.String(),
        "email": fields.String(),
        "location": fields.String(),
        "phone_number": fields.Integer()
    }
)

@customer_ns.route('/details')
class CustomerResource(Resource):
    
    @customer_ns.expect(customer_model)
    def post(self):
             
        data = request.get_json()
        
        new_customer = Customer(
        name = data.get('name'),
        location = data.get('location'),
        email = data.get('email'),
        phone_number = data.get('phone_number')
        )
        new_customer.save()
        
        return make_response(jsonify({"message":"user details created successfully"}), 201)  
    
    
    
    
     
        
@customer_ns.route('/details/<int:id>')
class detail_of_customer(Resource):
    
    @customer_ns.marshal_with(customer_model)
    @customer_ns.expect(customer_model)    
    def get(self, id):
        to_get_one_customer = Customer.query.get_or_404(id)
        
        to_get_one_customer.save()
        
        return to_get_one_customer  
    
    
    
    @customer_ns.marshal_with(customer_model)
    @customer_ns.expect(customer_model)  
    def  put(self, id):
        
        customer_to_update = Customer.query.get_or_404(id)
        
        data = request.get_json()
        
        customer_to_update.update(data.get('name'), data.get('location'), data.get('phone_number'))
        
        return customer_to_update
    
    
    @customer_ns.marshal_with(customer_model)
    def delete(self, id):
        
        customer_to_delete = Customer.query.get_or_404(id)
        
        customer_to_delete.delete()
        
        return customer_to_delete
        