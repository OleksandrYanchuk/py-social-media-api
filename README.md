# Social Media API

The API allow users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and perform basic social media actions.

## Setup and Local Installation

### To set up and run the project locally, follow these steps:

#### 1.  Clone the repository:

```python
git clone https://github.com/OleksandrYanchuk/py-social-media-api.git
```
#### 2. Open the folder:
```python
cd py-social-media-api
```
#### 3. Create a virtual environment:
```python
python -m venv venv
```
#### 4. Activate the virtual environment:
   
##### - For Windows:
```python
venv\Scripts\activate
```
##### -	For macOS and Linux:
```python
source venv/bin/activate
```
#### 5. Setting up Environment Variables:

##### 1. Rename a file name `.env_sample` to `.env` in the project root directory.

##### 2. Make sure to replace `SECRET_KEY` with your actual secret key.

#### 6. For run application manually make next steps:

```python
pip install -r requirements.txt
```
```python
python manage.py migrate user
```
```python
python manage.py migrate social_media_service
```
```python
python manage.py migrate
```
```python
python manage.py runserver
```
#### 7. Open your web browser and go to http://localhost:8000 to access the application.

#### 8. For convenience, a test user has been created
##### e-mail: user@user.com
##### pass: 1234user
###### For correct operation, it may be necessary to update the access token, for this you need to take the following steps:
###### - you can get a refresh token at the following link:
```python
http://localhost:8000/api/user/token/
```
##### - after which you need to follow the link to generate a new access token:
```python
http://localhost:8000/api/user/token/refresh/
```
##### also, for correct operation, you need to install an extension for working with request and response headers, for example ModHeader.
##### you need to enter "Authorization" in the name field, and "Bearer <your access tiken>" in the value field.

#### After all previous steps py-social-media-api will work correctly.
