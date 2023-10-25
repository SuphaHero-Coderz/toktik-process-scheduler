import json

import redis
import os
import time
import requests

class RedisResource:
    REDIS_QUEUE_LOCATION = os.getenv('REDIS_QUEUE', 'localhost')
    QUEUE_NAME = 'queue:encode'

    host, *port_info = REDIS_QUEUE_LOCATION.split(':')
    port = tuple()
    if port_info:
        port, *_ = port_info
        port = (int(port),)

    conn = redis.Redis(host=host, *port)

sub = RedisResource.conn.pubsub(ignore_subscribe_messages=True)
sub.subscribe("chunk")

while True:
    msg = sub.get_message()
    if msg:
        print(f"new message in channel {msg['channel']}: {msg['data']}")
        url_post = "http://backend:80/update_video_status"
        requests.post(url_post, json=json.loads(msg['data']))
        time.sleep(10)
