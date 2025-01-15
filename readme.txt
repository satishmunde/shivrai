to Setup the django project you need python 3.10 and above version installed in your system

unzip the project and go to the project directory.
start your postgre server
create table name "task_manage" in postgres db with "postgre" username and
"Admin" password

open terminal and run command "pip install pipenv"

then  run command " pip install -r requirements.txt"

for perfroming data base migration "python3 manage.py makemigrations" after that "python3 manage.py migrate"

after that create super user for that run command "python3 manage.py createsuperuser"


then for running server runn command "python3 manage.py runserver"

after successfully running the server you can assess 

admin panel at /admin/
api documentation for 
        redoc - /redoc/
        swaggger - /swaggger/

to access the  api you need the jwt token 

for that /auth/jwt/create/  - hit this api and get access token 

and add "JWT token" in this format 
if you are using browser the add modheader crome extension  then pass the  token 

and for postman send this token into the headers 

Add key "Authorization" and value "JWT token"

then you are above to test the poject 


for api 

    /api/tasks/


