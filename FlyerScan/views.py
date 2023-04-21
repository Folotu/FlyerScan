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
import re
import os
import io
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from .EventParser import startEventParsing
from dotenv import load_dotenv

load_dotenv()

views = Blueprint('views', __name__)

# def gen_frames():
#     camera = cv2.VideoCapture(0)
#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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

    credentials = Credentials.from_service_account_file(
    '.serviceCred.json',
    scopes=['https://www.googleapis.com/auth/drive']
    )

    service = build('drive', 'v3', credentials=credentials)

    parentFolderId = os.getenv('PARENT_FOLDER_ID')

    user = current_user.username

    folder_name = user
    subFolderID = ''
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{parentFolderId}' in parents"
    results = service.files().list(q=query, fields='files(id,name)').execute()
    folders = results.get('files', [])

    if folders: 
        userFolderID = folders[0]['id']

        query = f"mimeType='application/vnd.google-apps.folder' and trashed=false and '{userFolderID}' in parents"
        results = service.files().list(q=query, fields='files(id, name)').execute()
        subfolders = results.get('files', [])

        for fod in subfolders:
            if(fod["name"] == 'UploadedFlyers'):
                subFolderID = fod["id"]
        
    else:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parentFolderId]
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        print(f'Folder "{folder_name}" created with ID: {folder_id}')

        subFolder_metadata = {
            'name': 'UploadedFlyers',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id]
        }
        subFolder = service.files().create(body=subFolder_metadata, fields='id').execute()
        subFolder_id = subFolder.get('id')
        subFolderID = subFolder_id
        subFolderName = subFolder_metadata['name']
        print(f'SubFolder "{subFolderName}" created with ID: {subFolder_id}')

    num_files = ScanHistory.query.filter_by(author=current_user).count()

    # Set the filename based on the number of uploaded files
    filename = f"{num_files + 1}.png"

    image_data = request.form['image_data']

    # Decode the base64-encoded image data
    decoded_image = base64.b64decode(image_data.split(',')[1])

    # Create a file-like object from the decoded image data
    file_like_obj = io.BytesIO(decoded_image)

    # Create a MediaIoBaseUpload object from the file data
    media = MediaIoBaseUpload(file_like_obj, mimetype='image/png')

    # Set the file metadata
    file_metadata = {
        'name': f"{num_files + 1}.png",
        'parents': [subFolderID]
    }

    # Upload the file to Google Drive
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink'
        ).execute()

        toSend = startEventParsing(get_file_id_from_link(file.get("webViewLink")))
        toSend['flyerPath'] = get_file_id_from_link(file.get("webViewLink"))

        calLink = f"https://calndr.link/d/event/?service=outlook&start={toSend['date']} {toSend['start_time']}&end={toSend['date']} {toSend['end_time']}&title={toSend['title']}&timezone=America/Los_Angeles&description={toSend['desc']}&location={toSend['location']}"

        # Create a new ScanHistory object for this upload
        scan_history = ScanHistory(
            author=current_user,
            flyer_name=filename,
            flyer_url=get_file_id_from_link(file.get("webViewLink")),
            calendar_name = toSend['title'],
            calendar_url = calLink
        )
        db.session.add(scan_history)
        db.session.commit()

        return f'File successfully uploaded'and display_file(toSend)
    except HttpError as error:
        return f'An error occurred: {error}'

    # # for now returns Image capture TODO: will link this with overlayed image    
    # return 'Image captured'

def get_file_id_from_link(web_view_link):
    """Parses the unique file ID from a Google Drive webViewLink.

    Args:
        web_view_link (str): The webViewLink of the Google Drive file.

    Returns:
        str: The unique ID of the Google Drive file.
    """
    start_index = web_view_link.find('/d/') + 3
    end_index = web_view_link.find('/', start_index)
    
    flyerUrl = f'https://drive.google.com/uc?id={web_view_link[start_index:end_index]}'
    return flyerUrl


@views.route('/upload_file', methods=['POST'])
def upload_file():

    credentials = Credentials.from_service_account_file(
    '.serviceCred.json',
    scopes=['https://www.googleapis.com/auth/drive']
    )

    service = build('drive', 'v3', credentials=credentials)

    parentFolderId = os.getenv('PARENT_FOLDER_ID')

    user = current_user.username

    folder_name = user
    subFolderID = ''
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{parentFolderId}' in parents"
    results = service.files().list(q=query, fields='files(id,name)').execute()
    folders = results.get('files', [])

    if folders: 
        userFolderID = folders[0]['id']

        query = f"mimeType='application/vnd.google-apps.folder' and trashed=false and '{userFolderID}' in parents"
        results = service.files().list(q=query, fields='files(id, name)').execute()
        subfolders = results.get('files', [])

        for fod in subfolders:
            if(fod["name"] == 'UploadedFlyers'):
                subFolderID = fod["id"]

    else:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parentFolderId]
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        print(f'Folder "{folder_name}" created with ID: {folder_id}')

        subFolder_metadata = {
            'name': 'UploadedFlyers',
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id]
        }
        subFolder = service.files().create(body=subFolder_metadata, fields='id').execute()
        subFolder_id = subFolder.get('id')
        subFolderID = subFolder_id
        subFolderName = subFolder_metadata['name']
        print(f'SubFolder "{subFolderName}" created with ID: {subFolder_id}')

    num_files = ScanHistory.query.filter_by(author=current_user).count()

    # Set the filename based on the number of uploaded files
    filename = f"{num_files + 1}.png"

    file_data = request.files['file']

    # Create a MediaIoBaseUpload object from the file data
    media = MediaIoBaseUpload(file_data, mimetype=file_data.content_type)

    # Set the file metadata
    file_metadata = {
        'name': f"{num_files + 1}.png",
        'parents': [subFolderID]
    }

    # Upload the file to Google Drive
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink'
        ).execute()
        
        #return f'File successfully uploaded'
        toSend = startEventParsing(get_file_id_from_link(file.get("webViewLink")))
        toSend['flyerPath'] = get_file_id_from_link(file.get("webViewLink"))

        calLink = f"https://calndr.link/d/event/?service=outlook&start={toSend['date']} {toSend['start_time']}&end={toSend['date']} {toSend['end_time']}&title={toSend['title']}&timezone=America/Los_Angeles&description={toSend['desc']}&location={toSend['location']}"

        # Create a new ScanHistory object for this upload
        scan_history = ScanHistory(
            author=current_user,
            flyer_name=filename,
            flyer_url=get_file_id_from_link(file.get("webViewLink")),
            calendar_name = toSend['title'],
            calendar_url = calLink
        )
        db.session.add(scan_history)
        db.session.commit()

        return display_file(toSend)
    
    except HttpError as error:
        return f'An error occurred: {error}'
    
@views.route('/edit_file/<int:id>', methods=['GET', 'POST'])
def edit_post(id):

    ## 
    newData = ScanHistory.query.filter_by(author=current_user, id = id).all()
    ## new disctionary to store flyer info
    flyerInfo = {}
    ## template for grabbing data from string
    template = {'title':r"title=(.*?)&",
                    'date':r"start=(.*?)\s",
                    'start_time':r"start=.*?\s(.*?)&" ,
                    'end_time':r"end=.*?\s(.*?)&",
                    'location':r"location=(.*)",
                    'description':r"description=(.*?)&"
        }
    ## grabs string data at specific points
    for key, flyerInfo in template.items():
        match = re.search(template, newData.calendar_url)
        if match:
            flyerInfo[key] = match.group(1)

    ## if method is simply GET, displays current info on flyer
    if request.method == "GET":
        return display_file(flyerInfo)
    
    ## if method is post, gets new entry data from input fields and sets to 
    ## new dictionary editData
    elif request.method == "POST":
        editData = {}
        editData['title'] = request.form.get('title')
        editData['date'] = request.form.get('date')
        editData['start_time'] = request.form.get('start_time')
        editData['end_time'] = request.form.get('end_time')
        editData['location'] = request.form.get('location')
        editData['description'] = request.form.get('description')
        
        ## for loop to replace flyerInfo data with new values
        for key, value in editData.items():
            if key in flyerInfo:
                flyerInfo[key] = value
        
        updatedCal = ScanHistory(author = current_user, calendar_url = flyerInfo)
        db.session.add(updatedCal)
        db.session.commit()
        ## returns display with new flyerInfo
        return display_file(flyerInfo)


@views.route('/display_file')
def display_file(toSend):
    # Render a template to display the uploaded file
    return render_template('display_file.html', toSend=toSend)

@views.route('/history', methods=['GET'])
def displayHistory():
    
    userScanHist = ScanHistory.query.filter_by(author=current_user).all()

    return render_template("history.html", userScanHist=userScanHist)


@views.route('/account', methods=['GET', 'POST'])
def displayAccount():
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if username:
            current_user.username = username

        if email:
            current_user.email = email

        if password and password == confirm_password:
            current_user.password = generate_password_hash(password)

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('views.displayAccount'))

    return render_template('account.html', title='Account')