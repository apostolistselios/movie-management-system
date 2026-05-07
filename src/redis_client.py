import sys

from redis import Redis
from redis.commands.search.field import TextField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.exceptions import ResponseError


class RedisClient:
    """Singleton that manages the Redis connection."""

    MOVIES_TITLE_INDEX = "movies_title_idx"
    _instance: "RedisClient | None" = None

    def __new__(cls) -> "RedisClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False

        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        self.redis = self.connect()
        self.create_movie_title_index()
        self._initialized = True

    def connect(self) -> Redis:
        """Connect to Redis. The application exits if the connection fails.

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

    def create_movie_title_index(self) -> None:
        """Creates a RediSearch index for movie titles stored in hashes."""

        try:
            self.redis.ft(self.MOVIES_TITLE_INDEX).create_index(
                fields=[TextField("title")],
                definition=IndexDefinition(
                    prefix=["movie:"],
                    index_type=IndexType.HASH,
                ),
            )
        except ResponseError as error:
            if "Index already exists" not in str(error):
                raise

    def escape_search_term(self, term: str) -> str:
        """Escapes RediSearch query syntax characters in a single term.

        RediSearch uses some characters as part of its query syntax.
        For example, characters like ":" or "-" can change the meaning of a search
        query if they are not escaped.

        This method keeps letters, numbers, and underscores as they are, and prefixes
        every other character with "\\" so Redis treats it as part of the search term.

        For example: "Spider-Man" becomes "Spider\\-Man".

        Args:
            term (str): the search term to escape.

        Returns:
            str: the escaped search term.
        """

        return "".join(
            character
            if character.isalnum() or character == "_"
            else f"\\{character}"
            for character in term
        )
