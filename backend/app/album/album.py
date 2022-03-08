from flask_restx import Resource, Namespace, fields, marshal_with
from flask import request, make_response,jsonify

from .models import Album

album_ns = Namespace('Album', description='api for all Album')

album_model = album_ns.model(
    "customer", {
        "id":fields.Integer(),
        "album_name": fields.String()  
    }
)

@album_ns.route('/details')
class CustomerResource(Resource):
    
    @album_ns.expect(album_model)
    def post(self):
             
        data = request.get_json()
        
        new_album = Album(
        album_name = data.get('album_name')
        )
        new_album.save()
        
        return make_response(jsonify({"message":"album created"}), 201)  
    
           
@album_ns.route('/details/<int:id>')
class detail_of_customer(Resource):
    
    @album_ns.marshal_with(album_model)
    @album_ns.expect(album_model)    
    def get(self, id):
        to_get_one_album = Album.query.get_or_404(id)
        
        to_get_one_album.save()
        
        return to_get_one_album 
    
    
    
    @album_ns.marshal_with(album_model)
    @album_ns.expect(album_model)  
    def  put(self, id):
        
        album_to_update = Album.query.get_or_404(id)
        
        data = request.get_json()
        
        album_to_update.update(data.get('album_name'))
        
        return album_to_update
    
    
    @album_ns.marshal_with(album_model)
    def delete(self, id):
        
        album_to_delete = Album.query.get_or_404(id)
        
        album_to_delete.delete()
        
        return album_to_delete
        