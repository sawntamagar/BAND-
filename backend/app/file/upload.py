import os
from io import BytesIO
from flask import request, send_file, jsonify
from flask_restx import Resource, fields, Namespace 
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.file.models import Upload
from app import db
from app import myapp

upload_ns = Namespace('upload', description = 'this is for the merchandise')

upload_model = upload_ns.model(
    "upload", {
       "filename": fields.String()
    }
)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 


@upload_ns.route('/user/<int:users_id>/tshirt')
class TshirtsResource(Resource):
    
    # @login_required
    @upload_ns.expect(upload_model)   
    def post(self, users_id):
        if 'file' not in request.files:
            flash('No file part')
            return {"message": "no file part"}
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return {"message": "No file selected"}
        if file and allowed_file(file.filename):
            upload = Upload(filename= file.filename, data = file.read(), users_id=users_id)
            upload.save()
            return f'uploaded: {file.filename}'
        
       
@upload_ns.route('/download/<int:id>')
class TshirtsResource(Resource):
    
    # @upload_ns.marshal_with(upload_model)
    @upload_ns.expect(upload_model)   
    def get(self,id):
        upload = Upload.query.filter_by(id=id).first()
        return send_file(BytesIO(upload.data),attachment_filename=upload.filename, as_attachment=True)     
    
    
@upload_ns.route('/user/<int:users_id>/delete/<int:id>')
class TshirtsResource(Resource):
    
    # @upload_ns.marshal_with(upload_model)
    @upload_ns.expect(upload_model)   
    def delete(self,users_id, id):

        file_to_delete = Upload.query.filter_by(id=id).first()
        file_to_delete.delete()
      
        return jsonify({"message":"file successfully deleted"})
            
    