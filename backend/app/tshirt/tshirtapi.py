from flask import  json, request, jsonify, send_from_directory, url_for
import os
from flask_login import login_required
import urllib.request
from werkzeug.utils import secure_filename
from flask_restx import Resource, fields, Namespace 
# from .models import File
from app import myapp


tshirt_ns = Namespace('tshirt', description = 'this is for the merchandise')


tshirt_model = tshirt_ns.model(
    "Tshirt", {
        "name": fields.String(),
        "description": fields.String() 
    }
)

 

 
# UPLOAD_FOLDER = 'static/uploads'
# myapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# myapp.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])
 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
    

@tshirt_ns.route('/upload')
class Upload(Resource):
    
    @tshirt_ns.expect(tshirt_model)
    @login_required
    def post(self):
        
       if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(myapp.config['UPLOAD_FOLDER'], filename))
            return jsonify({'message':'file is saved'})
        return jsonify({'message':'file is uploaded successfully'})
   