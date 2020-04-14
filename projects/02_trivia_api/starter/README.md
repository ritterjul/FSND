# Full Stack Trivia API Project 

This Trivia project allows users to play a trivia game and test their general knowledge either for themselves or against friends. The API can:

1. Display questions - both all questions and by category.
2. Delete questions.
3. Add questions.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started
### Installing Dependencies

Developers should have Python3, pip3, node, and npm installed. 

### Frontend dependencies
#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from https://nodejs.com/en/download.

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the frontend directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```
### Backend Dependencies 

Once you have a Python virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided, by executing from within the `/backend` folder in your terminal:
```bash
psql trivia < trivia.psql
```

## Running the server

To run the server, execute from within the `/backend` folder in your terminal:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing
To run the tests, execute from within the `/backend` folder in your terminal:
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
``` 

## API Reference

### Getting Started 
Base URL: Currently this application is only hosted locally. The backend is hosted at http://127.0.0.1:5000/
Authentication: This version does not require authentication or API keys.

### Error Handling

There are three types of errors the API will return:
- 400 - bad request
- 404 - resource not found
- 422 - unprocessable

### Endpoints

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None
- Returns: An JSON object with a key categories, that contains a object of id: category_string key:value pairs.
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
  "categories: {
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
    },
  "success": true
}
```

#### GET '/categories/<int:id>/questions'
- Fetches paginated (groups of 10) questions of a category specified by id
- Request Arguments: None
- Returns a JSON object with a key questions, that contains paginated questions from a specified category
- Sample: `curl http://127.0.0.1:5000/categories/3/questions`
```
{
  "current_category": 3, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

#### GET '/questions'
- Fetches paginated (groups of 10) questions of all categories
- Request Arguments: None
- Returns a JSON object with a key questions, that contains paginated questions from all categories
- Sample: `curl http://127.0.0.1:5000/questions`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
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
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

#### POST '/questions'
- Creates a new question
- Request Arguments: JSON with keys question (string), answer (string), difficulty (integer), category (integer)
- Returns JSON with a key id, that contains the id of the created question in database
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question": "How tall is Table Mountain?", "answer": "1085m", "difficulty": 3, "category": "3" }'`
```
{
  "id": 25,  
  "success": true
}
```

#### POST '/questions/search'
- Fetches paginated (groups of 10) questions containing a search term (case-insensitive)
- Request Arguments: JSON with key searchTerm (string)
- Returns a JSON object with key questions, that contains the paginated questions containing the search term
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "artist"}'`
```
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```
#### DELETE '/questions/<int:id>'
- Deletes a question by id
- Request Arguments: None
- Sample: `curl http://127.0.0.1:5000/questions/4 -X DELETE`
```
  {
    "success": true
  }
```


#### POST '/quizzes'
- Allows user to play the trivia game
- Request Arguments: JSON object with keys previous question (list of ids of already played questions) and quiz_category (dict of chosen category with keys type (string) and id (int))
- Returns JSON object with key question, that contains a randomly chosen questions which was not already played
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [13], "quiz_category": {"type": "Geography", "id": "3"}}'`
```
{
  "question": {
    "answer": "Agra", 
    "category": 3, 
    "difficulty": 2, 
    "id": 15, 
    "question": "The Taj Mahal is located in which Indian city?"
  }, 
  "success": true
}
```


