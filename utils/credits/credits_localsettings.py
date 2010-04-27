import sys, os
from django.core.management import setup_environ


project_path = os.path.split(os.getcwd())[0] # Assume to run the scrpit from the mp3 project_path
sys.path.append(project_path)
from mp3 import settings
setup_environ(settings)

APP_PATH = settings.PROJECT_PATH + '/utils/credits'
