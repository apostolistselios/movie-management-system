import sys

from redis import Redis


def create_redis_client() -> Redis:
    """Connect to Redis. The application exits if the redis connection is not successful.

    Returns:
        Redis: The created Redis client instance.
    """

    try:
        client = Redis(host="localhost", port=6379, decode_responses=True)
        client.ping()
        print("Connected to Redis")

        return client
    except Exception as error:
        print(f"Redis is not available: {error}")
        sys.exit(1)


def insert_movie(redis: Redis, username: str) -> None:
    """Prompts the user to insert the details of a movie and the saves it to redis.

    If the movie doesnt already exist saves it to redis.
    If it exist does nothing, just informs the user.

    Either way it inserts the user to the movies watchlist.

    Args:
        redis (Redis): the redis client instance
        username (str): the username of the logged in user
    """

    print("\n--- Inserting a movie ---")

    title = input("Enter the movie title: ")
    director = input("Enter the movie director: ")
    release_year = input("Enter the movie release year: ")

    normalized_title = title.replace(" ", "_").lower()
    movie_key = f"movie:{normalized_title}"
    movie_exists = redis.exists(movie_key)
    if not movie_exists:
        print(f"--- Inserting the movie: {title} ---")
        redis.hset(
            movie_key,
            mapping={title: title, director: director, release_year: release_year},
        )
    else:
        print(f"--- Movie: {title} already exists ---")

    redis.sadd(f"{movie_key}:watchlist", username)


def main() -> None:
    redis = create_redis_client()

    username = input("Enter your username: ")

    while True:
        print("\n--- Μένου Redis Movies ---")
        print("(I)nsert Movie | (Q)uery | (S)tatistics | e(X)it")
        choice = input("Option: ").upper()

        if choice == "I":
            insert_movie(redis, username)

        elif choice == "Q":
            # TODO: Υλοποίηση αναζήτησης
            pass
        elif choice == "S":
            # TODO: Υλοποίηση στατιστικών
            pass
        elif choice == "X":
            print("Exiting...")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
