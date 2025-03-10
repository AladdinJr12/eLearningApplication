python manage.py generateschema --format openapi-json > bioweb_schema.json

to run celery for us run:
celery -A app_name worker --loglevel=info --pool=solo

#---For migrations---#
python manage.py makemigrations
python manage.py migrate

#---COmmand for removing all previous migrations----#
rm e_learning_application/migrations/0*.py

#---for server--#
python manage.py runserver
daphne appName.routing:application
daphne chat.routing:application
daphne -b 0.0.0.0 -p 8001 CM3035_Final_Proj.asgi:application

#----for virtual environment_--#
cd "C:\Users\Aladdin\Desktop\Advanced Web dev\myenv\Scripts"
.\activate

#---for cd to projecr after activating virtual environment---//
cd ../../AdvWebDevFinalProj/CM3035_Final_proj 


#---For redis---#
redis-server
ctrl c to stop it

#---for starting the server---#
& "C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" start -D "C:\Users\Aladdin\Desktop\Advanced Web dev\W3" -l "C:\Users\Aladdin\Desktop\Advanced Web dev\W3\logfile" -o "-p 5432"      


SELECT * FROM django_migrations WHERE app = 'genedata';

INSERT INTO django_migrations (app, name, applied)
VALUES ('genedata', '0002_auto_20200805_1452', NOW());


#---for postgress sql----#
psql -U Aladdin -d postgres

#---the database I am using----#
learningwebsite_db

#--for testing password in postgress sql:-------#
psql -U "Aladdin" -d postgres -W


#---admin user---#
Admin69
password is higurashi reference


#---for creating superuser---------#
python manage.py createsuperuser


#---postgress sql user----#
Aladdin
Password = The usual;

#--for collecting static---#
python manage.py collectstatic

#---for starting apache---#
open command prompt:
cd to C:\Apache24\bin>

httpd.exe -k restart


#-----python shell for checking model entries---------------#
python manage.py shell
from e_learning_application.models import *
print(McqQuestion.objects.all())



#---for running unit test---#
python manage.py test


#---github----#
git status
git add .
git commit -m "Updated to have status updates in homepage + for teachers to view other users accounts"
git push origin main


#---heroku stuff--#

heroku login
heroku create randomName
git status
git remote -v
git remote add heroku github_project_link
example is: https://github.com/AladdinJr12/eLearningApplication.git

git add .

git commit -m "random comment"

git push heroku master
