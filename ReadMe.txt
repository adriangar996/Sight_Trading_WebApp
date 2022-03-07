Set up Project:
1. Install/Update Node.js & Python to their respective latest version: (https://www.python.org/downloads/ , https://nodejs.org/en/)
2. Install/Update Pip: $ python3 -m ensurepip --upgrade
3. Navigate to Project's root directory: cd /path-to-project-dir
4. Create Virtual Environment: python3 -m venv <enviroment_name>
5. Activate Virtual Environment: <enviroment_name>/bin/activate
6. Install Project's Python Dependencies on Project's Virtual Environment: python3 -m pip install -r requirements.txt
7. Install Node.js Dependencies: npm install
8. Make Django's sqlite3 database migrations: python3 manage.py makemigrations
9. Migrate Django's sqlite3 database: python3 manage.py migrate
10.Run Development Server: python3 manage.py runserver

Front-end ToDo:
-Fix full vertical page fill
-add password container in account
-Create High Contrast Version
-Create Dark Version
-Popup for password Change
-Popup for password Recovery

Back-end ToDo:
-Mail Client
-Password Recovery Scripts
-Password Change Scripts
-Entry Error text Styling->Justification To center & text-color to red
-Create Settings Page scripts
-Create Notifications Scripts
-Connect Notifications Page
-Connect High Contrast Version
-Connect Dark Version
-Send user temporary password when forgot password is processed
