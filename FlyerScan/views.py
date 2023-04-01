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
import os

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
            return render_template('landing.html', toSend=toSend,)    
        
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
    user = current_user.username

    directory = f'FlyerScan/static/UserStatic/{user}/UploadedFlyers'
    if not os.path.exists(directory):
        os.makedirs(directory)

    num_files = ScanHistory.query.filter_by(author=current_user).count()

    # Set the filename based on the number of uploaded files
    filename = f"{num_files + 1}.png"

    # Decode the base64-encoded image data
    decoded_image = base64.b64decode(image_data.split(',')[1])
    # Save the image to a file or database
    with open(os.path.join(directory, filename), 'wb') as f:
        f.write(decoded_image)

    # Create a new ScanHistory object for this upload
    scan_history = ScanHistory(
        author=current_user,
        flyer_name=filename,
        flyer_url=os.path.join(directory, filename)
    )
    db.session.add(scan_history)
    db.session.commit()

    relative_path = os.path.join(directory, filename).split("FlyerScan", 1)[1]

    # Redirect the user to a page to display the overlayed uploaded file
    return 'Image captured' and display_file(relative_path)   

    # # for now returns Image capture TODO: will link this with overlayed image    
    # return 'Image captured'



@views.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Save the file to a directory or database
    # file.save('FlyerScan/static/UploadedImages/uploadedImage.png')
    user = current_user.username
    directory = f'FlyerScan/static/UserStatic/{user}/UploadedFlyers'
    if not os.path.exists(directory):
        os.makedirs(directory)

    num_files = ScanHistory.query.filter_by(author=current_user).count()

    # Set the filename based on the number of uploaded files
    filename = f"{num_files + 1}.png"

    # Save the file with the new filename
    file.save(os.path.join(directory, filename))

    # Create a new ScanHistory object for this upload
    scan_history = ScanHistory(
        author=current_user,
        flyer_name=filename,
        flyer_url=os.path.join(directory, filename)
    )
    db.session.add(scan_history)
    db.session.commit()

    relative_path = os.path.join(directory, filename).split("FlyerScan", 1)[1]
    print(relative_path)

    # Redirect the user to a page to display the overlayed uploaded file
    return display_file(relative_path)


@views.route('/display_file')
def display_file(flyerPath):
    # Render a template to display the uploaded file
    return render_template('display_file.html', flyerPath=flyerPath)