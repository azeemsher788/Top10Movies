# Top100Movies

## Overview
Top100Movies is a Flask-based web application that allows users to search for movies, add them to a personal list, and rate and review them. The application fetches movie data from an external API and stores user ratings and reviews in a local database.

## Features
- **Movie Search**: Search for movies using the Movie Database API.
- **Add Movies**: Add movies to your personal list.
- **Rate and Review**: Rate and review movies in your list.
- **Dynamic Ranking**: Movies are dynamically ranked based on user ratings.

## Technologies Used
- **Python**: Core programming language.
- **Flask**: Web framework for building the application.
- **SQLAlchemy**: ORM for database management.
- **WTForms**: For form handling and validation.
- **Requests**: For making HTTP requests to the Movie Database API.

## Setup Instructions
1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/Top100Movies.git
    cd Top100Movies
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    - Create a `.env` file in the root directory.
    - Add the required API keys and other configurations in the `.env` file.

4. **Run the application**:
    ```sh
    python main.py
    ```

## Usage
- The application allows users to search for movies, add them to their list, and provide ratings and reviews.
- Ensure that the database is properly set up and accessible.


## License
This project is licensed under the MIT License.