Here's a step-by-step guide with proper formatting for setting up and running your Django project:

---

### Prerequisites:
- **Python 3.10 or above** installed on your system.
- **PostgreSQL** server running with a database named `task_manage`, a username `postgre`, and a password `Admin`.

---

### 1. Setup Instructions:

1. **Unzip the project** and navigate to the project directory.

2. **Start your PostgreSQL server**.

3. **Create the database**:
    - Create a table named `task_manage` in PostgreSQL with the username `postgre` and password `Admin`.

4. **Install pipenv**:
    - Open the terminal and run:
    ```bash
    pip install pipenv
    ```

5. **Install project dependencies**:
    - Run the following command in the project directory:
    ```bash
    pipenv install -r requirements.txt
    ```

6. **Database migration**:
    - Run the following commands to apply database migrations:
    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

7. **Create a superuser**:
    - Run the following command to create an admin superuser for accessing the Django admin panel:
    ```bash
    python3 manage.py createsuperuser
    ```

8. **Run the server**:
    - Start the server by running:
    ```bash
    python3 manage.py runserver
    ```

---

### 2. Accessing the Application:

- After successfully running the server, you can access:
    - **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
    - **API Documentation**:
        - **Redoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
        - **Swagger**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---

### 3. Using the API:

- To use the API, you need to authenticate with a **JWT token**.

#### Steps to Get JWT Token:
1. **Create a JWT Token**:
   - Hit the `/auth/jwt/create/` API endpoint to obtain the access token.
   
2. **Send the JWT Token**:
   - If you're using a **browser**, add the token via the [ModHeader Chrome extension](https://chrome.google.com/webstore/detail/modheader/).
     - Add a header with the key `Authorization` and value `JWT <your_token>`.
   - If you're using **Postman**, include the token in the header:
     - Key: `Authorization`
     - Value: `JWT <your_token>`

---

### 4. API Endpoints:

- **Tasks API**:  
   - Endpoint: `/api/tasks/`  
   - Format: GET, POST, PUT, DELETE operations for task management.

---

This should allow you to set up the project, run the server, access the API, and authenticate with a JWT token to test the functionalities.
