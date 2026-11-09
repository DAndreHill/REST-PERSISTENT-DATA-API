REST Persistent Data API

Project Description

This project is a RESTful API developed using Python and Flask. It manages clinical records and stores patient information using SQLite and a JSON Lines file.

Technologies Used

* Python
* Flask
* SQLAlchemy
* Pydantic
* SQLite
* JSON Lines

Features

* Creates clinical records using POST requests.
* Retrieves stored clinical records using GET requests.
* Validates patient information using Pydantic.
* Stores records in an SQLite database.
* Saves records to a JSON Lines file.
* Includes error handling and logging.

How to Run

1. Install the required packages using pip install -r requirements.txt.
2. Start the application using python main.py.
3. Open http://127.0.0.1:8000/clinical/ in a browser to retrieve records.
4. Use a POST request to /clinical/ with JSON patient information to create a record.

Testing

The application was tested using POST and GET requests. A test patient record was successfully created, stored, and retrieved from the database. The JSON Lines file was also verified to contain the saved record.