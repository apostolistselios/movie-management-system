# Technical Report

## Complexity based on Redis Documentation

The code uses `HSET`, `HGETALL`, `EXISTS`, `SADD`, `SCARD`, `ZINCRBY`, `ZREVRANGE`, `LPUSH`, `LTRIM`, `LRANGE`, `SCAN`, and `FT.SEARCH`.

The Redis documentation states that [`HSET`](https://redis.io/docs/latest/commands/hset/) is `O(1)` per field/value pair, while [`HGETALL`](https://redis.io/docs/latest/commands/hgetall/) is `O(N)` with respect to the number of fields in the hash. [`EXISTS`](https://redis.io/docs/latest/commands/exists/) is `O(N)` with respect to the number of keys being checked, so in this project, where one key is checked, it is practically `O(1)`.

For Sets, [`SADD`](https://redis.io/docs/latest/commands/sadd/) is `O(1)` per element, and [`SCARD`](https://redis.io/docs/latest/commands/scard/) is `O(1)`, which directly matches the need for unique users per watchlist.

For Sorted Sets, [`ZINCRBY`](https://redis.io/docs/latest/commands/zincrby/) has a complexity of `O(log N)`, and [`ZRANGE`](https://redis.io/docs/latest/commands/zrange/) has a complexity of `O(log N + M)`, where `M` is the number of elements returned.

For Lists, [`LPUSH`](https://redis.io/docs/latest/commands/lpush/) is `O(1)` per element, [`LTRIM`](https://redis.io/docs/latest/commands/ltrim/) is `O(N)` with respect to the number of elements removed, and [`LRANGE`](https://redis.io/docs/latest/commands/lrange/) is `O(S+N)` with respect to the distance from the start/end and the number of elements returned. In this specific project, the history is limited to 5 elements, so the practical cost remains constant.

[`SCAN`](https://redis.io/docs/latest/commands/scan/) is `O(1)` per call but `O(N)` for a full iteration. The complexity of [`FT.SEARCH`](https://redis.io/docs/latest/commands/ft.search/) depends on the query and the results, while the Redis Search documentation states that fuzzy terms are written as `%term%` and are based on Levenshtein distance.

## System Description

The Movie Management System is a Python command-line application that uses Redis Stack to manage movie data and user interactions. The system supports movie insertion, typo-tolerant title search, movie watchlists, trending score tracking, and each user’s last 5 searched movies.

The code uses the following Redis data structures:

| Feature             | Redis structure    | Example key                          |
| ------------------- | ------------------ | ------------------------------------ |
| Movie details       | Hash               | `movie:<normalized_title>`           |
| Movie watchlist     | Set                | `movie:<normalized_title>:watchlist` |
| Trending score      | Sorted Set         | `trending_score:movies`              |
| User search history | List               | `user:<username>:history`            |
| Fuzzy title search  | Redis Search Index | `movies_title_idx`                   |

## Hash for movie details

Each movie is stored as a Redis Hash with a key such as `movie:<normalized_title>`. The normalization process converts titles such as `The Matrix` into `the_matrix`. The Hash stores the fields `title`, `director`, and `release_year`.

A Hash is appropriate because a movie is a record with named attributes. Storing the movie as a plain string would require manual parsing, while storing it as a List would not represent the meaning of the fields correctly.

In the code, insertion is performed with `hset()` in the `MovieRepository.add()` method, retrieval is performed with `hgetall()` in the `MovieRepository.get()` method, and existence checking is performed with `exists()` in the `MovieRepository.exists()` method.

Complexity:

| Operation             | Command   | Complexity                                |
| --------------------- | --------- | ----------------------------------------- |
| Check if movie exists | `EXISTS`  | `O(1)` for one key                        |
| Store 3 fields        | `HSET`    | `O(1)` per field, constant for 3 fields   |
| Retrieve movie data   | `HGETALL` | `O(N)`, where `N` is the number of fields |

Since `N` is fixed and small, the retrieval cost is effectively `O(1)` for this application.

## Set for movie watchlists

Each movie has a Redis Set with a key such as `movie:<normalized_title>:watchlist`. The Set stores the usernames of users who have shown interest in the movie.

A Set is the correct choice because each user must be counted only once. If a List were used, the same username could appear multiple times, and the application would need an additional linear duplicate check with `O(N)` cost.

In the code, users are added with `sadd()` in `MovieRepository.add_to_watchlist()`, while the number of interested users is retrieved with `scard()` in `MovieRepository.get_watch_count()`.

Complexity:

| Operation   | Command | Complexity      |
| ----------- | ------- | --------------- |
| Add user    | `SADD`  | `O(1)` per user |
| Count users | `SCARD` | `O(1)`          |

Therefore, the Set provides fast insertion, automatic uniqueness, and constant-time cardinality.

## Sorted Set for trending score

Global trending popularity is stored in a Redis Sorted Set with the key `trending_score:movies`. Each member is the normalized movie title, and its score is the number of searches.

A Sorted Set is suitable because the system needs both score updates and ranking. A plain Hash could store the scores, but finding the top 3 movies would require reading all scores and sorting them, which costs `O(N log N)`.

In the code, the score is incremented with `zincrby()` in `MovieRepository.increment_trending_score()`. The top movies are retrieved with `zrange()` in `MovieRepository.get_top_trending()`.

Complexity:

| Operation                  | Command   | Complexity     |
| -------------------------- | --------- | -------------- |
| Increment popularity score | `ZINCRBY` | `O(log N)`     |
| Retrieve top `M`           | `ZRANGE`  | `O(log N + M)` |

In this application, `M = 3`, so retrieving the top trending movies is effectively `O(log N)`. This makes the Sorted Set ideal for ranking, leaderboards, and top-N queries.

## List for user search history

Each user has a Redis List with the key `user:<username>:history`. Every new search is pushed to the front with `LPUSH`, so the newest search appears first. Then the list is trimmed to 5 elements with `LTRIM`.

A List is appropriate because search history is chronological. Order matters, so a Set would not fit. A Sorted Set would also be unnecessarily complex because no explicit timestamp or score is required; the insertion order already captures recency.

In the code, history updates are performed in `UserRepository.add_to_history()` with `lpush()` and `ltrim()`. Retrieval is performed in `UserRepository.get_history()` with `lrange()`.

Complexity:

| Operation         | Command  | Complexity                                  |
| ----------------- | -------- | ------------------------------------------- |
| Add new search    | `LPUSH`  | `O(1)`                                      |
| Keep only 5 items | `LTRIM`  | `O(N)` in removed elements                  |
| Retrieve history  | `LRANGE` | `O(N)`, practically `O(1)` because `N <= 5` |

Because the history is always capped to 5 items, these operations have constant practical cost in this application.

## 6. Redis Search index for fuzzy title search

The application creates a Redis Search index named `movies_title_idx` on the `title` field of movie hashes. This is implemented in `RedisClient.create_movie_title_index()` using `TextField("title")` and `IndexDefinition(prefix=["movie:"], index_type=IndexType.HASH)`.

Fuzzy search is implemented in `_get_title_search_query()`, where each search term is wrapped with `%`, for example `@title:(%matrx%)`. This allows the application to detect small spelling mistakes.

The Redis Search index is important because it avoids manually scanning every movie title in Python. Without an index, fuzzy search would require checking all `N` titles, with at least `O(N)` cost, plus the similarity-comparison cost for every title. With Redis Search, the query is handled by a specialized index, and the code requests only the first result using `paging(0, 1)`.

The exact complexity of `FT.SEARCH` is `O(Ν)` but also depends on the query, indexed terms, and result set size. However, from an architectural perspective, it is more appropriate than a linear scan over all stored movie hashes.

## Conclusion

The selected Redis data structures are appropriate for the application requirements:

| Requirement               | Selected structure | Justification                                        |
| ------------------------- | ------------------ | ---------------------------------------------------- |
| Store movie details       | Hash               | Movie data is a small set of named fields            |
| Unique users in watchlist | Set                | Ensures uniqueness without linear duplicate checks   |
| Trending ranking          | Sorted Set         | Supports efficient score updates and top-K retrieval |
| Recent user history       | List               | Naturally preserves chronological order              |
| Fuzzy title search        | Redis Search Index | Avoids manual linear scanning of all titles          |

Overall, the design uses each Redis structure for the role it supports best. Frequent operations such as adding users to watchlists, counting interested users, updating history, and retrieving top trending movies remain efficient. The most expensive operation is the full popularity metrics report, because it requires scanning all movies and sorting them.
