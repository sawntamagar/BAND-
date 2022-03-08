from flask import request, jsonify, make_response,session
import validators
from flask_restx import Resource, fields, Namespace
from flask_login import login_required,  current_user
from app.user.models import User

admin_ns = Namespace('Admin', description = 'this is for the user authentication')

admin_model = admin_ns.model(
    "Admin", {
        "id": fields.Integer(),
        "username": fields.String()
    }
)


@admin_ns.route('/admin')
class Admin(Resource):
    
    @admin_ns.expect(admin_model)    
    # @auth_ns.marshal_with(admin_model)
    @login_required
    def post(self ):
        
        id= current_user.id
        if id <= 10:
            return jsonify({"message":"you are accessed to admin page"})
        else:
            return jsonify({"message":"you need to be admin to access to this page"})
        
        