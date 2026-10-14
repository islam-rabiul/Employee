import os
from redis import Redis
from rq import Queue

# Get the Redis URL from environment variables, defaulting to the Docker service hostname
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Connect to Redis
redis_conn = Redis.from_url(redis_url)

# Initialize the RQ Queue
task_queue = Queue("default", connection=redis_conn)