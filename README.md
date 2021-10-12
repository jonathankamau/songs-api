[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c393f5bfb4e64b80bbfb552ed1b7a723)](https://app.codacy.com/gh/jonathankamau/songs-api?utm_source=github.com&utm_medium=referral&utm_content=jonathankamau/songs-api&utm_campaign=Badge_Grade_Settings)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/85d644e77ebd449a9f763dfd95bd3b5f)](https://www.codacy.com/gh/jonathankamau/songs-api/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jonathankamau/songs-api&amp;utm_campaign=Badge_Grade)
[![CircleCi](https://circleci.com/gh/jonathankamau/temperature-query-api.svg?style=svg)](https://app.circleci.com/pipelines/github/jonathankamau/songs-api)
[![Coverage Status](https://coveralls.io/repos/github/jonathankamau/temperature-query-api/badge.svg?branch=main)](https://coveralls.io/github/jonathankamau/songs-api?branch=main)
[![Maintainability](https://api.codeclimate.com/v1/badges/1a97c6de621dc9d1a0e2/maintainability)](https://codeclimate.com/github/jonathankamau/songs-api/maintainability)
![CircleCI](https://img.shields.io/circleci/build/github/jonathankamau/songs-api)
[![PyPI pyversions](https://img.shields.io/badge/Python%20Version-3.9-blue)](https://img.shields.io/badge/Python%20Version-3.9-blue)

# Songs API

Songs API is a API tool that allows the user to retrieve song data, add ratings to a song and retrieve rating metrics.
## Notes on the API and structure
- This API is composed of five endpoints, the resource classes for each can be found [here](api/endpoints/songs).
- The tests for each of the endpoints can be found [here](api/tests)
- The routes for each of the endpoints can be found [here](api/routes)
- The JSON file containing the songs that are loaded to MongoDB when the api server is run can be found [here](songs.json)
-  the entry point for the api when its manually run locally is [manage.py](manage.py) that calls the create_app method in [app.py](app.py)
- In the case of the song data scaling up to millions of document records, I have implemented the following that will aid with performance:
    - Upon running the API, a generator function is used to load the song records in chunks or batches from the JSON file to a list of song objects. Once its complete then a bulk  insert of those song objects is executed using the mongoengine's [insert](http://docs.mongoengine.org/apireference.html#mongoengine.queryset.QuerySet.insert) method. This reduces load on memory and maintains optimal database performance.
    - When retrieving lists of song records I have them queried with [batch_size](https://docs.mongoengine.org/apireference.html#mongoengine.queryset.QuerySet.batch_size) that optimizes bulk reads, reduces the load on the server and maintains good database performance.

### Available Endpoints
|HTTP Method   | Endpoint  | Resource class | Description | Example Usage
| ------------- | --------- | --------- |--------------- |------------------- |
|GET| `/api/v1/songs?page_number={number}&songs_per_page={number}` | SongsListResource | Retrieve a list of songs from the db. ThePagination parameters `page_number` and `songs_per_page` are optional | Without pagination: `/api/v1/songs`  With pagination: `http://127.0.0.1:5000/api/v1/songs?page_number=1&songs_per_page=2`
|GET| `api/v1/songs/difficulty?level={number}` | AverageDifficultyResource | Returns the average difficulty for all songs. the `level` parameter is optional and allows filtering by level | Without level parameter: `http://127.0.0.1:5000/api/v1/songs` With level parameter `http://127.0.0.1:5000/api/v1/songs/difficulty?level=13`
|GET| `/api/v1/songs/search?message={text}` | SongSearchResource | Returns a list of songs that match the search query. `message` is the query parameter used. It takes into account the song's artist and title | `http://127.0.0.1:5000/api/v1/songs/search?message=wishing`
|POST| `/api/v1/songs/rating?song_id={song_id}rating={rating}` | SongRatingResource | Adds a rating between 1 and 5 to a song. `song_id` and  `rating` are both passed as parameters | `http://127.0.0.1:5000/api/v1/songs/rating?song_id=6161da9800813afe5d66fc18&rating=3`
|GET| `http://127.0.0.1:5000/api/v1/songs/rating/metrics?song_id={song_id}` | RatingMetricsResource | Returns the average, lowest and highest rating for a song | `http://127.0.0.1:5000/api/v1/songs/rating/metrics?song_id=6161da9800813afe5d66fc18`


## Getting started with the API
-   The project was built using python 3.9 and the [Flask](https://flask.palletsprojects.com/en/2.0.x/). The API utilizes the [flask-restx](https://flask-restx.readthedocs.io/en/latest/) library.

-   To run this API on your local machine, you will need to clone this project. You can do so using the following command which you can copy and paste on your terminal:

    With HTTPS:

    ```
    git clone https://github.com/jonathankamau/songs-api.git
    ```

    With SSH:

    ```
    git clone git@github.com:jonathankamau/songs-api.git
    ```



### Local Environment Installation

In order to be able to successfully run this project on your local machine, ensure you have the following prerequisites
#### Prerequisites
-   Python 3
-   Docker
-   A Virtual environment (if running manually) based on python 3 within which you will run the project. To set it up, you can follow the guidelines outlined [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#installing-virtualenv)

### Running using Docker
-   Ensure you have Docker installed. You can find information [here](https://www.docker.com/get-started) on how to install Docker on your machine.
-   The root folder contains a [Makefile](/Makefile) that handles the container builds and runs for the test and api environments

#### Running tests
-   While still in the source folder you can run the following command to run the tests in the test environment:

    ```
    make test
    ```

#### Running the app

-   While still in the source folder you can run the following command to run the app in the app environment:

    ```
    make dev
    ```

    This will spin up seperate containers for the api and the mongodb database.

### Running Manually
If you are running the project manually you will need to do the following:
-   Ensure you have setup a virtual environment following the steps [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#installing-virtualenv) and you have navigated to that environment on  your terminal.

-   Install the requirements using this command:
    ```
    pip install -r requirements.txt
    ```

- Run the following docker command that will run MongoDB in a docker container:

    ```
    docker run --detach --name songs_db --publish 127.0.0.1:27017:27017 mongo:4.4
    ```
#### Running tests manually
-   You can then run the tests either using following command:

    ```
    pytest -vv
    ```
#### Running the app manually

-   While still in the source folder you can run the following command to run the api:

    ```
    python manage.py runserver
    ```

## Built With

-   Python 3.9
-   Flask
-   MongoDB

## Author 📚

-   Jonathan Kamau
    -   [Github Profile](https://github.com/jonathankamau)
    -   [Linkedin Profile](https://www.linkedin.com/in/kamaujonathan/)

## License 🤝

-   This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
