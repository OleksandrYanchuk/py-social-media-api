import subprocess

# Install requirements
subprocess.run(['pip', 'install', '-r', 'requirements.txt'], check=True)

# Perform migrations
subprocess.run(['python', 'manage.py', 'migrate', 'user'], check=True)
subprocess.run(['python', 'manage.py', 'migrate', 'social_media_service'], check=True)
subprocess.run(['python', 'manage.py', 'migrate'], check=True)
# Runserver
subprocess.run(['python', 'manage.py', 'runserver'], check=True)
