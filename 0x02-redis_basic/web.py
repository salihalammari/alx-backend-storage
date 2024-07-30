#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and returns it """
import redis
import requests
r = redis.Redis()

count = 0


def get_page(url: str) -> str:
    """ track how many times a particular URL was accessed in the key
        "count:{url}"
        and cache the result with an expiration time of 10 seconds """
    cached_content = r.get(f"cached:{url}")
    if cached_content:
        return cached_content.decode('utf-8')
    resp = requests.get(url)
    page_content = resp.text
    r.setex(f"cached:{url}", 10, page_content)
    r.incr(f"count:{url}")

    return page_content


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
