# Analysis

- **Movie Insertion**, it will be a hash set.

  This way, we achieve **O(1) complexity** when searching for a movie’s data
  and when checking whether a movie already exists or not.
  - Key: `movie:title` (normalized title, possibly with underscores)
  - Values:
    - title
    - director
    - release_year

- **Watchlist**, it will be a set of users.

  This way, we ensure the creation of a watchlist with **unique users (no duplicates)**,
  enable calculation of the total number of users who have the current movie in their watchlist,
  and support popularity metrics since we need the count of unique users per movie in the database.
  - Key: `movie:title:watchlist` (normalized title, possibly with underscores)
  - Values: Set of usernames

- **Trending Score**, it will be a sorted set.

  This way, we automatically calculate the most popular movies, since the Sorted Set
  keeps entries ordered based on a score.
  - Key: `trending_score:movies`
  - Values: movie titles (normalized title, possibly with underscores)

- **User History**: The last 5 movies searched by the current user.
  - Key: `user:username:history` (normalized username, possibly with underscores)
  - Values: List
