Set up Project:
1. Install/Update Node.js & Python to their respective latest version: (https://www.python.org/downloads/ , https://nodejs.org/en/)
2. Install/Update Pip: $ python3 -m ensurepip --upgrade
3. Navigate to Project's root directory: cd /path-to-project-dir
4. Create Virtual Environment: python3 -m venv <enviroment_name>
5. Activate Virtual Environment: <enviroment_name>/bin/activate
6. Install Project's Python Dependencies on Project's Virtual Environment: python3 -m pip install -r requirements.txt
7. Navigate to Django's Templates directory: cd /path-to-djangoproject-templates-dir
8. Install Node.js Dependencies: npm install
9. Navigate back to root folder: cd /path-to-project-dir
10.Make Django's sqlite3 database migrations: python3 manage.py makemigrations
11.Migrate Django's sqlite3 database: python3 manage.py migrate
12.Run Development Server: python3 manage.py runserver



Front-end ToDo:
-Fix Notifications.html
-Delete PortfolioIndex Card Title container
-Add Add-Stock Pop-up Form in Portfolio & Watch-list
-Add Stock Selector and Delete Stock button on Charts containers
-Entry Error text Styling->Justification To center & text-color to red
-Fix about carrousel arrows
-Sign-up instead of sign-in on sign in page nav button
-Change footer sign up link to signin.html for signup.html page
-User email and sign-out link instead of sign-in button after login
-Add Prediction periods columns to portfolio/watchlist tables
-Create High Contrast Version
-Create Dark Version

Back-end ToDo:
-Connect Account Page
-Create Settings Page scripts
Connect Settings Page
-Connect Portfolio/Watchlist Charts and tables
-Create Notifications Scripts
-Connect Notifications Page
-Connect High Contrast Version
-Connect Dark Version

