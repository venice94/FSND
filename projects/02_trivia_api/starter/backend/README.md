# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints

GET '/categories'
GET '/questions'
GET '/categories/<cat_id>/questions'
POST '/questions'
POST '/questions/search'
DELETE '/questions/<qn_id>'
GET '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request arguments: None
- Returns: A dictionary of categories with id:type key value pair.
Sample Request: localhost:5000/categories
Sample Response:
"categories":{
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
},
"success":true,

GET '/questions'
- Fetches an array of questions in the current category, with their answers and difficulty levels
- Request arguments: None
- Returns: List of categories, current category, number of questions in the current category as well as an array of te questions in the current category.
Sample Request: localhost:5000/questions
Sample Response:
"categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
},
"current_category": "Science",
"total_questions": 3,
"success":true,
"questions": [
    {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    }
]

GET '/categories/<cat_id>/questions'
- Fetches an array of questions in the specified category, with their answers and difficulty levels.
- Request arguments: category id
- Returns: Current category, number of questions in the current category as well as an array of te questions in the current category.
Sample Request: localhost:5000/categories/1/questions
Sample Response:
"current_category": "Science",
"total_questions": 3,
"success":true,
"questions": [
    {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
    },
    {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    }
]

POST '/questions'
- Adds a new question to the database
- Request arguments: Question, category, answer and difficulty level
- Returns: Result of the request
Sample Request: localhost:5000/questions
"question":"What is the question?",
"answer":"This is the answer.",
"difficulty":3,
"category":2
Sample Response:
"success":true

POST '/questions/search'
- Search for questions based on the search term given. Search term is case insensitive.
- Request arguments: search term
- Returns: Questions that match the search term given.
Sample Request: localhost:5000/questions/search
"searchTerm":"world cup"
Sample Response:
"questions": [
    {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
        "answer": "Uruguay",
        "category": 6,
        "difficulty": 4,
        "id": 11,
        "question": "Which country won the first ever soccer World Cup in 1930?"
    }
],
"success": true

DELETE '/questions/<qn_id>'
- Deletes the specified question
- Request argument: question id
- Returns: Result of the request
Sample Request: localhost:5000/questions/1
Sample Response:
"success":true

GET '/quizzes'
- Randomly fetches a question from the specified category. If no category is specified, the question will be fetched from any category.
- Request argument: Previous questions, quiz category
- Returns: Question with answer and difficulty level
Sample Request: localhost:5000/quizzes
"previous_questions":[1,2,3],
    "quiz_category":{
        "id":1
    }
Sample Response:
question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
},
"success": true

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```