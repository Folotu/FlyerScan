import base64
from flask import Blueprint, render_template, request, flash, jsonify, abort, redirect, url_for, Response
from flask_login import login_required, current_user
from . import db, app
import json
from .models import *
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.file import FileField
import cv2

views = Blueprint('views', __name__)

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@views.route('/', methods=['GET','POST'])
def index():
        toSend = {}
        
        if (current_user.is_anonymous):
            toSend['person'] = "Guest"
        else:
            toSend['person'] = current_user.username
            toSend['posterToScan'] = FileField('Flyer')

        return render_template('index.html', toSend=toSend)

@views.route('/camera', methods=['GET','POST'])
def video_viewer():
    # if request.method == 'GET':
    #     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # else: 
    #     pass
    return render_template('camera.html')
     
@views.route('/process_image', methods=['POST'])
def process_image():
    image_data = request.form['image_data']
    # Decode the base64-encoded image data
    decoded_image = base64.b64decode(image_data.split(',')[1])
    # Save the image to a file or database
    with open('FlyerScan/static/CapturedImages/capturedImage.png', 'wb') as f:
        f.write(decoded_image)
    # for now returns Image capture TODO: will link this with overlayed image    
    return 'Image captured'

@views.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Save the file to a directory or database
    file.save('FlyerScan/static/UploadedImages/uploadedImage.png')
    # Redirect the user to a page to display the uploaded file
    return redirect(url_for('views.display_file'))

@views.route('/display_file')
def display_file():
    # Render a template to display the uploaded file
    return render_template('display_file.html')