Set up Project In Development Form:
1. Install/Update Python to its latest version: (https://www.python.org/downloads/)
2. Install/Update Pip: $ python3 -m ensurepip --upgrade
3. Navigate to Project's root directory: cd /path-to-project-dir
4. Create Virtual Environment: python3 -m venv <enviroment_name>
5. Activate Virtual Environment: <enviroment_name>/bin/activate
6. Install Project's Python Dependencies on Project's Virtual Environment: python3 -m pip install -r requirements.txt
8. Make Django's database migrations: python3 manage.py makemigrations
9. Migrate Django's database: python3 manage.py migrate
10.Run Development Server: python3 manage.py runserver
