# Movie Management System in Redis

## Introduction

The goal of this assignment is to implement an application in Python that will
manage movie information and user interactions using Redis.
Choosing the appropriate data structure is critical for the system’s efficiency,
as the application requires handling complex relationships and real-time statistics.

## Required Data Structures

For the full implementation of the application, it is mandatory to use the following four (4)
Redis data structures: **Hashes, Sets, Sorted Sets, Lists**.

The correct mapping of each operation to the appropriate structure is part of the evaluation
and must be justified in the technical report.

## Functional Requirements

When the application starts, it asks the user for a username. It then provides the following
menu of operations:

### Movie Insertion

The user enters the **Title**, **Director**, and **Release Year** of a movie.
The system must check whether the movie (i.e., the title) already exists in the database.5

- If it exists, overwriting its data is **not allowed**, and the user is automatically added
  to the movie’s watchlist.
- If the movie is new, its full details are stored, and the user who inserted it is added
  to the movie’s watchlist.

### Search & Interaction (Query)

The user searches for a movie by title. During the search, the following actions are
automatically performed:

1. **Information Retrieval**: The movie details are displayed along with the total number
   of users who have it in their watchlist.
2. **Watchlist**: The searching user is automatically added to the movie’s watchlist,
   ensuring that each user is counted only once.
3. **Trending Score**: The movie’s popularity increases in the database.
4. **History**: The movie title is added to the user’s personal history.
   The system must keep only the last 5 searches for each user.

### Statistics & Ranking

The system displays aggregated statistics:

1. **Global Trending**: The top three (3) most popular movies on the platform based on
   total searches.
2. **User History**: The last 5 movies searched by the current user.
3. **Popularity Metrics**: The number of unique users who have shown interest in each
   movie in the database.

## Smart Search & Fault Tolerance

Implement a **Smart Search (Fuzzy Search)** mechanism that makes the application resilient
to typos and case differences (case insensitivity) when inserting or searching for a movie.

The goal is that if a user types a title with minor errors (e.g., _"Incepton"_ instead of _"Inception"_),
the system should detect the similarity and ask the user if they meant the existing movie.

### Implementation Hints:

1. **Case Insensitivity**: A simple but effective technique is converting all title keys
   to lowercase before storing or searching in Redis.

2. **Redis Search (Redis Stack)**:
   Using the Redis Search module allows the use of the `%` operator (e.g., `%Incepton%`),
   which automatically computes the Levenshtein distance between strings.
   (You will need to create an index for searching by movie title—refer to Redis documentation.)

3. **N-grams Mapping**: Alternatively, you can split titles into small chunks
   (e.g., 2 or 3 characters) and use Sets to identify titles with many common segments
   (Jaccard similarity logic).

4. **User Confirmation**: When a similar title is detected, the application should pause
   the insertion or search process and ask the user for confirmation (Y/N) before proceeding.

---

To use Full-Text Search capabilities, it is recommended to install **Redis Stack**
(instead of the basic Redis server), as it includes all the necessary modules.
If you are using Docker, the `redis/redis-stack` image is the most suitable choice.
