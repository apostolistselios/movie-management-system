# Analysis

- **Movie Insertion**, it will be a [Hash](https://redis.io/docs/latest/develop/data-types/hashes/).

  This way, we achieve **O(1) complexity** when searching for a movie’s data
  and when checking whether a movie already exists or not.
  - Key: `movie:title` (normalized title, possibly with underscores)
  - Values:
    - title
    - director
    - release_year

- **Watchlist**, it will be a [Set](https://redis.io/docs/latest/develop/data-types/sets/) of users.

  This way, we ensure the creation of a watchlist with **unique users (no duplicates)**,
  enable calculation of the total number of users who have the current movie in their watchlist,
  and support popularity metrics since we need the count of unique users per movie in the database.
  - Key: `movie:title:watchlist` (normalized title, possibly with underscores)
  - Values: Set of usernames

- **Trending Score**, it will be a [Sorted Set](https://redis.io/docs/latest/develop/data-types/sorted-sets/).

  This way, we automatically calculate the most popular movies, since the Sorted Set
  keeps entries ordered based on a score.
  - Key: `trending_score:movies`
  - Values: movie titles (normalized title, possibly with underscores)

- **User History**, it will be a [Capped List](https://redis.io/docs/latest/develop/data-types/lists/#capped-lists)

  This way, we will automatically keep and display the last 5 movies searched by the current user.
  - Key: `user:username:history` (normalized username, possibly with underscores)
  - Values:
