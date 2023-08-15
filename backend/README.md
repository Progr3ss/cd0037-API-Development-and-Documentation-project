# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.




### Usage
Once the server is up and running, you can use the Trivia API to interact with the trivia question database. The API provides the following endpoints:




## Usage

Once you have successfully started the Flask development server and the Trivia API is running, you can interact with the API using various endpoints to perform different actions on the trivia question database. Below are details about each available endpoint and how to use them.

### Endpoints

1. **GET /categories**

   This endpoint allows you to retrieve a list of all available categories.

   **Example Request:**
   ```
   GET /categories
   ```

   **Example Response:**
   ```json
   {
       "success": true,
       "categories": [
           {
               "id": 1,
               "type": "Science"
           },
           {
               "id": 2,
               "type": "History"
           },
           // ...
       ]
   }
   ```

2. **GET /questions?page=page_number**

   Retrieve a paginated list of trivia questions. Each page contains 10 questions.

   **Example Request:**
   ```
   GET /questions?page=2
   ```

   **Example Response:**
   ```json
   {
       "success": true,
       "questions": [
           {
               "id": 11,
               "question": "What is the capital of France?",
               "answer": "Paris",
               "category": 3,
               "difficulty": 2
           },
           {
               "id": 12,
               "question": "Which planet is known as the Red Planet?",
               "answer": "Mars",
               "category": 1,
               "difficulty": 2
           },
           // ...
       ],
       "total_questions": 20,
       "categories": {
           "1": "Science",
           "2": "History",
           // ...
       },
       "current_category": null
   }
   ```

3. **DELETE /questions/:question_id**

   Delete a question by its ID.

   **Example Request:**
   ```
   DELETE /questions/5
   ```

   **Example Response:**
   ```json
   {
       "success": true,
       "deleted": 5
   }
   ```

4. **POST /questions**

   Add a new question to the database.

   **Example Request:**
   ```json
   POST /questions
   {
       "question": "What is the largest mammal?",
       "answer": "Blue Whale",
       "category": 1,
       "difficulty": 3
   }
   ```

   **Example Response:**
   ```json
   {
       "success": true,
       "created": 21
   }
   ```

5. **POST /questions/search**

   Search for questions using a search term.

   **Example Request:**
   ```json
   POST /questions/search
   {
       "searchTerm": "capital"
   }
   ```

   **Example Response:**
   ```json
   {
       "success": true,
       "questions": [
           {
               "id": 11,
               "question": "What is the capital of France?",
               "answer": "Paris",
               "category": 3,
               "difficulty": 2
           }
       ],
       "total_questions": 1,
       "current_category": null
   }
   ```

6. **GET /categories/:category_id/questions**

   Get a list of questions belonging to a specific category.

   **Example Request:**
   ```
   GET /categories/2/questions
   ```

   **Example Response:**
   ```json
   {
       "success": true,
       "questions": [
           {
               "id": 6,
               "question": "Which ancient civilization built the pyramids?",
               "answer": "Egyptians",
               "category": 2,
               "difficulty": 2
           },
           {
               "id": 7,
               "question": "Who was the first President of the United States?",
               "answer": "George Washington",
               "category": 2,
               "difficulty": 1
           }
       ],
       "total_questions": 2,
       "current_category": "History"
   }
   ```

7. **POST /quizzes**

   Get a random question for playing a quiz.

   **Example Request:**
   ```json
   POST /quizzes
   {
       "previous_questions": [1, 2, 3],
       "quiz_category": {"id": 1, "type": "Science"}
   }
   ```

   **Example Response:**
   ```json
   {
       "success": true,
       "question": {
           "id": 4,
           "question": "What is the chemical symbol for gold?",
           "answer": "Au",
           "category": 1,
           "difficulty": 2
       }
   }
   ```

### Error Handling

The Trivia API provides error handling for specific HTTP status codes to help you understand and troubleshoot issues that might arise during API usage.

- **404: Resource not found**

  If the requested resource (endpoint) does not exist, you will receive a 404 error along with an error message.

  **Example Response:**
  ```json
  {
      "success": false,
      "error": "Not found"
  }
  ```

- **422: Unprocessable entity**

  If there is an issue with the data you provided in the request, resulting in the inability to process the request, you will receive a 422 error along with an error message.

  **Example Response:**
  ```json
  {
      "success": false,
      "error": "Unprocessable entity"
  }
  ```






## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
