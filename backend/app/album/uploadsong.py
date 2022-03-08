import os
from io import BytesIO
from flask import request, send_file, jsonify
from flask_restx import Resource, fields, Namespace 
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.file.models import Upload
from app import db
from app import myapp
from .models import UploadSong

song_ns = Namespace('song', description = 'Api for songs')

song_model = song_ns.model(
    "upload", {
       "filename": fields.String()
    }
)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 


@song_ns.route('/album/<int:album_id>/song')
class SongResource(Resource):
    
    # @login_required
    @song_ns.expect(song_model)   
    def post(self, album_id):
        if 'file' not in request.files:
            flash('No file part')
            return {"message": "no file part"}
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return {"message": "No file selected"}
        if file and allowed_file(file.filename):
            upload = UploadSong(filename= file.filename, data = file.read(), album_id=album_id)
            upload.save()
            return f'uploaded: {file.filename}'
        
       
@song_ns.route('/download/<int:id>')
class SongResource(Resource):
    
    @song_ns.expect(song_model)   
    def get(self,id):
        upload = UploadSong.query.filter_by(id=id).first()
        return send_file(BytesIO(upload.data),attachment_filename=upload.filename, as_attachment=True)     
    
    
@song_ns.route('/album/<int:album_id>/delete/song/<int:id>')
class TshirtsResource(Resource):
    
    @song_ns.expect(song_model)   
    def delete(self,album_id, id):

        file_to_delete = UploadSong.query.filter_by(id=id).first()
        file_to_delete.delete()
      
        return jsonify({"message":"file successfully deleted"})
            