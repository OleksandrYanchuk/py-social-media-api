# Social Media API

The API allow users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and perform basic social media actions.

## Setup and Local Installation

### To set up and run the project locally, follow these steps:

#### 1.  Clone the repository:

```python
git clone https://github.com/OleksandrYanchuk/py-social-media-api.git
```
#### 2. Create a virtual environment:
```python
python -m venv venv
```
#### 3. Activate the virtual environment:
   
##### - For Windows:
```python
venv\Scripts\activate
```
##### -	For macOS and Linux:
```python
source venv/bin/activate
```
#### 4. Install the project dependencies:
```python
pip install -r requirements.txt
```
#### 5. Apply database migrations:
```python
python manage.py migrate
```
#### 6. Create a superuser to access the admin panel:
```python
python manage.py createsuperuser
```
#### 7. Start the development server:
```python
python manage.py runserver
```
#### 8. Open your web browser and go to http://localhost:8000 to access the application.

## For convenience, a test user has been created
#### e-mail: user@user.com
#### pass: 1234user
