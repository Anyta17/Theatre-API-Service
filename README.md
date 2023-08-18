# Theatre API Service 

Django-rest-framework project allows visitors of the Theatre to make Reservations online and choose needed seats, without going physically to the Theatre

## Setup Instructions

To set up the project locally, follow these steps:

1. Clone the repository:

    ```
    git clone https://github.com/Anyta17/Theatre-API-Service.git
    ```

2. Navigate to the project directory:

    ```
    cd theatre_service
    ```

3. Create a virtual environment and activate it:

    ```
    python -m venv venv
    venv\Scripts\activate
    ```

4. Install the required dependencies:
    
    ```
    pip install -r requirements.txt
    ```

5. Apply migrations to set up the database:

   ```
   python manage.py migrate
   ```

6. Run the development server:

   ```
   python manage.py runserver
   ```
   
# API Endpoints

The API provides the following endpoints:

* `/api/plays/`: List and create plays.
* `/api/plays/<int:pk>/`: Retrieve, update, and delete individual plays.
* `/api/performances/`: List and create performance instances.
* `/api/performances/<int:pk>/`: Retrieve, update, and delete individual performance instances.
* `/api/actors/`: List and create actors.
* `/api/actors/<int:pk>/`: Retrieve, update, and delete individual actors.
* `/api/genres/`: List and create genres.
* `/api/genres/<int:pk>/`: Retrieve, update, and delete individual genres.
* `/api/theatre-halls/`: List and create theatre halls.
* `/api/theatre-halls/<int:pk>/`: Retrieve, update, and delete individual theatre halls.
* `/api/tickets/`: List and create tickets.
* `/api/tickets/<int:pk>/`: Retrieve, update, and delete individual tickets.
* `/api/reservations/`: List and create reservations.
* `/api/reservations/<int:pk>/`: Retrieve, update, and delete individual reservations.
