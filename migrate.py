import os
from app import create_app, redis_client

app = create_app()

def clean_redis_db():
    redis_client.flushdb()
    print("Redis database cleaned.")

if __name__ == "__main__":
    clean_redis_db()
