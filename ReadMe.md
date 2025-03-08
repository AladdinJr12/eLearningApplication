1. Start by starting your virtual environment: For me this was done by typing this into the terminal:
cd "C:\Users\Aladdin\Desktop\Advanced Web dev\myenv\Scripts"
.\activate
2. Next cd to the directory "CM3035_Final_Proj: and install the project's dependencies with the command "pip install -r requirements.txt"
3. Start the PostgreSQL server, for me this was done with the command: " "
& "C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" start -D "C:\Users\Aladdin\Desktop\Advanced Web dev\W3" -l "C:\Users\Aladdin\Desktop\Advanced Web dev\W3\logfile" -o "-p 5432"   
4. Optional: For running the unit tests, use the command "python manage.py test"
5. Start the project's server with "python manage.py runserver"
6. Open a second terminal and start the redis server with "redis-server"
7. Start a third terminal and activate the virtual envioronment for that terminal. 
8. For this terminal, run the command "daphne -b 0.0.0.0 -p 8001 CM3035_Final_Proj.asgi:application"
9. Now just copy and paste the localhost link generated from the first terminal on your browsers and you will able to try out this application!
10. Note that unit tests can be tested by running "python manage.py test"


11. User Credentials
The following users have been created for testing purposes:

Superuser:
Username: Admin69
Password: Higurashi1983
Student Users:
Email: Student2@mail.com

Password: Higurashi1983
Email: Student3@mail.com

Password: Higurashi1983
Teacher Users:
Email: Teacher1@mail.com

Password: Higurashi1983
Email: Teacher2@mail.com

Password: Higurashi1983
