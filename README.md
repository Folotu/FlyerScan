# FlyerScan

Start with a creating virtual environment

~~~
 python -m venv venv
~~~

Then activate the virtual environment

Activate environment for windows
~~~
 venv/Scripts/Activate
~~~
Activate environment for linux/darwin
~~~
source venv/bin/activate
~~~

Then install the requirements in the virtual environment 

~~~
 pip install -r requirements.txt
~~~

Then run the main flask file

~~~
 python manage.py 
~~~
Open another terminal with the environment active, then load up the models with 
~~~
 python BERTmanage.py 
~~~

You'll have to create a service worker account in order to use Google Drive to store the images as we did, and store the credentials into the .serviceCred.json file. PARENT_FOLDER_ID refers to the id of the Google drive folder you'll be using to store the images. 

You'll also have to get client id and client id secret for github and google in order to use the social login for both, enter the details into the .env file. You'll also need to get OCR_API_KEY, the OCR api key can be gotten from https://ocr.space/OCRAPI for free. 
