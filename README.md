# user-api

<p>This is a FastAPI Project that interacts with two tables(Users, Addresses) in the database.</p>
# This Project is built using Python. It uses the following libraries and frameworks:
<ol>
<li>FastAPI  </li>
<li>SQLAlchemy </li>
<li>Postgresql </li>
<li>Alembic </li>
<li>Pytest </li>
<li>Docker, Dotdocker and Docker Compose</li>
</ol>

You can do the following actions to the table:

Address Table:
1- Create address
2- Get all addresses
3- Get address by id
4- Delete address
5- Update address

User Table:
1- Create user
2- Get all users
3- Get user by id
4- Get users by gender
5- Delete user by id
6- Update user by id


<p>To run this project in your machine all you need is Docker. If docker was not installed on your machine, go ahead and install it then follow the instructions below.</p>

# To run this project on your machine follow these instructions:
1) Open your terminal from the user-api folder where the Dockerfile exists.
2) Incase docker was not running on your system write the following command: "systemctl start docker" 
3) To start dotdocker write: "dotdocker start" if u were using linux and needed permission write "sudo dotdocker start"
4) Now to build and install the required files for this project: "docker-compose build user-api-service"
5) after successfully building this project, you can run it on your machine using the following command: "docker-compose up user-api-service"
6) Congratulations, you have the project running on your machine. Now all you have to do to use it is to go to the following URL in your browser: "http://userapi.docker/docs" 

If you want to make sure all the services is up and running with no problems using pytest run the following command in the terminal:
"docker-compose run --rm user-api-test"
