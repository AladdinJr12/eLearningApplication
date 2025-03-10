#---for emptying all the feedback entries----#

import os
import sys
import django

# Get the absolute path to the Django project's root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ensure Python can find the Django project
sys.path.insert(0, PROJECT_ROOT)  # Use insert(0) instead of append()

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CM3035_Final_Proj.settings")

# Initialize Django
django.setup()

from e_learning_application.models import Feedback

def clear_feedback():
    deleted_count, _ = Feedback.objects.all().delete()
    print(f"✅ Deleted {deleted_count} feedback entries.")

if __name__ == "__main__":
    clear_feedback()
