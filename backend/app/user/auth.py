from flask import request, jsonify, make_response,session
import validators
from flask_restx import Resource, fields, Namespace
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.user.models import User


auth_ns = Namespace('auth', description = 'this is for the user authentication')


signup_model = auth_ns.model(
    "SignUp", {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String()
        
    }
)

login_model = auth_ns.model(
    "Login", {
        "username": fields.String(),
        "password": fields.String() 
    }
)    
 
users_model = auth_ns.model(
   "AllUsers", {
        "id": fields.Integer(),
        "username": fields.String(),
        "email": fields.String(),
        
    }
)
   
@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
             
        data = request.get_json()
        username = data.get('username')
        
        db_user = User.query.filter_by(username=username).first()
        
        if db_user is not None:
            return jsonify({"message":f"user with {username} already exist"})
           
        new_user = User(
            
            username = data.get('username'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password'))
            
            
        )
        
        new_user.save()
        
        return make_response(jsonify({"message":"user create successfully"}), 201)  
    
           
@auth_ns.route('/login')
class Login(Resource):
    # @auth_ns.marshal_with(login_model)
    @auth_ns.expect(login_model)    
    def post(self):
        
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        db_user = User.query.filter_by(username=username).first()
        
        
        if db_user and check_password_hash(db_user.password, password):
            login_user(db_user)
            return make_response(jsonify({"message":"you have logged in successfully"}), 201) 
        else:
            return jsonify({"message":"please try again or signup"})
             
             
           
@auth_ns.route('/logout/<int:id>')
class LogOut(Resource):
    @login_required
    def post(self, id):
        
        db_user = User.query.get(id)
       
        logout_user()
        return jsonify({"message":"you have sucessfully logged out."})
        
        
        
@auth_ns.route('/users')
class AllUsers(Resource):
    
    @auth_ns.marshal_list_with(users_model)
    def get(self):
        
        users = User.query.all()
        
        return users        
             
             
    #to get only one user
    
@auth_ns.route('/user/<int:id>')
class OneUser(Resource):
    
    @auth_ns.marshal_with(users_model)
    def get(self, id):
        
        to_get_one_user = User.query.get_or_404(id)
        
        to_get_one_user.save()
        
        return to_get_one_user   
        
    # Api to change the username for all users
    
    
    @auth_ns.marshal_with(users_model)
    @login_required
    def  put(self, id):
        
        user_to_update = User.query.get_or_404(id)
        
        data = request.get_json()
        
        user_to_update.update(data.get('username'), data.get('email'))
        
        return user_to_update
    
    
    @auth_ns.marshal_with(users_model)
    def delete(self, id):
        
        user_to_delete = User.query.get_or_404(id)
        
        user_to_delete.delete()
        
        return user_to_delete
    
            
            
            

        
        
        
                    
         