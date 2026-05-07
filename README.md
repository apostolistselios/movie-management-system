# Movie Management System

A small Python command-line application for managing movies and user activity with
Redis Stack. The app stores movie details, tracks which users are interested in
each movie, records recent user searches, and ranks movies by search popularity.

## Features

- Add movies with title, director, and release year.
- Search movies by title with fuzzy matching through RediSearch.
- Automatically add the current user to a movie watchlist when they insert or search for a movie.
- Track a trending score every time a movie is queried.
- Keep each user's last 5 searched movies.
- Show platform statistics:
  - top 3 trending movies
  - current user's recent search history
  - unique interested-user counts per movie

## Tech Stack

- Python 3.10+
- Redis Stack
- RediSearch
- Docker Compose

## Project Structure

```text
.
|-- docker-compose.yml      # Redis Stack service
|-- requirements.txt        # Python dependencies
|-- docs/
|   |-- analysis.md         # Redis data-structure analysis
|   `-- requirements.md     # Assignment requirements
`-- src/
    |-- app.py              # CLI entry point
    |-- movies.py           # Movie repository and Redis operations
    |-- redis_client.py     # Redis connection and search index setup
    |-- users.py            # User history repository
    `-- utils.py            # Input and string helpers
```

## Redis Data Model

The application uses four Redis data structures:

| Data                | Redis structure | Example key                  |
| ------------------- | --------------- | ---------------------------- |
| Movie details       | Hash            | `movie:the_matrix`           |
| Movie watchlist     | Set             | `movie:the_matrix:watchlist` |
| Trending scores     | Sorted Set      | `trending_score:movies`      |
| User search history | List            | `user:alice:history`         |

Movie titles are normalized for keys, so `The Matrix` becomes `movie:the_matrix`.

## How to Run

### 1. Start Redis Stack

```bash
docker compose up -d
```

This starts:

- Redis on `localhost:6379`
- RedisInsight on `http://localhost:8001`

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python src/app.py
```

The app asks for a username and then opens the interactive menu:

```text
--- Menu Redis Movies ---
(I)nsert Movie | (Q)uery | (S)tatistics | e(X)it
Option:
```

## Examples

### Insert a movie

```text
Enter your username: alice

--- Menu Redis Movies ---
(I)nsert Movie | (Q)uery | (S)tatistics | e(X)it
Option: I

--- Inserting a movie ---
Enter the movie title: The Matrix
Enter the movie director: The Wachowskis
Enter the movie release year: 1999
--- Inserting the movie: The Matrix ---
```

The movie is stored in Redis and `alice` is added to its watchlist.

### Query a movie

```text
--- Menu Redis Movies ---
(I)nsert Movie | (Q)uery | (S)tatistics | e(X)it
Option: Q
Please enter a movie title: Matrix
Did you mean 'The Matrix' that already exists in the database? (Y/N): Y

--- Movie Information ---
Title: The Matrix
Director: The Wachowskis
Release Year: 1999
Number of users that watched the movie: 1
```

Querying a movie adds the current user to the watchlist, increments the movie's
trending score, and stores the title in the user's recent search history.

### View statistics

```text
--- Menu Redis Movies ---
(I)nsert Movie | (Q)uery | (S)tatistics | e(X)it
Option: S

--- Statistics ---

Top 3 trending movies:
1. The Matrix (Trending Score: 1)

Your last 5 searched movies:
1. The Matrix

Popularity metrics:
The Matrix: 1 interested users
```

### Fuzzy search example

If a similar title already exists, the app asks for confirmation:

```text
Please enter a movie title: Matrxi
Did you mean 'The Matrix' that already exists in the database? (Y/N): Y
```

## Useful Commands

Stop Redis Stack:

```bash
docker compose down
```

Stop Redis Stack and remove persisted Redis data:

```bash
docker compose down
rm -rf redis_data
```

## Notes

- Redis Stack is required because the app uses RediSearch for fuzzy title matching.
- Redis data is persisted in the local `redis_data/` directory through Docker Compose.
- If Redis is not running, the app exits with a connection error.
