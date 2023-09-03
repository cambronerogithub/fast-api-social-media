# Backend clone  of social media app by using FastAPI

#### This API  has 4 routes

## 1) Post route

#### This route is reponsible for creating post, deleting post, updating post and Checkinh post

## 2) Users route

#### This route is about creating users and searching user by id

## 3) Auth route

#### This route is about login system

## 4) Vote route

 #### This route is about likes or vote system and this route contain code for upvote or back vote there is not logic about down vote

# how to run locally
First clone this repo by using following command
````

git clone https://github.com/cambronerogithub/fast-api-social-media

````
then 
````

cd fast-api-social-media

````

In case you want you can create a virtual environment:

- pip install virtualenv
- virtualenv ./venv
- To activate the virtualenv you can run the following command: ./venv/Scripts/activate

````
Please install the dependencies through pip
````
pip install -r ./requirements.txt
````

Then go this repo folder in your local computer run following command
````

uvicorn main:app --reload

````

Then you can use following link to use the  API

````

http://127.0.0.1:8000/docs 

````

## After run this API you need a database in postgres, in this case you can use PostgreSQL Version: 13 in the following link: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
Create a database in postgres then create a file name .env and write the following things in your file 

````
DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = {passward_that_you_set}
DATABASE_NAME = {your database name}
DATABASE_USERNAME = {your username}
SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60 (or you can place less minutes if you want this value must be an integer)

````
### Note: SECRET_KEY in this exmple is just a psudo key. You need to get a key for youself and you can get the SECRET_KEY from fastapi documention: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/


````

After all of this to make it easier for you import the colection I have added in this project from the folder called: Colections and Environments, also please make sure you select the DEV environment

Please note that if you want to use the APIs first (Locally) you need to:

- Create an user with Post User
- Call the endpoint Login User (please note you should send in the Body form-data the email and the password of the user created), in order to verify if it works you should receive an access_token
- You now can do whatever you want, create posts, delete posts, get posts ...

