from redis import Redis
from rq import Queue

# Connect to Redis running locally
redis_conn = Redis(host="localhost", port=6379)

# Create an RQ queue named 'default'
task_queue = Queue("default", connection=redis_conn)