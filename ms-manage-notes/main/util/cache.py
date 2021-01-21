import concurrent.futures
import urllib.request
from cachetools import cached, LRUCache, TTLCache


@cached(cache=LRUCache(maxsize=32))  # item discarded if size exceeds 32 keys
def get_sum(arr):
    return sum(arr)

@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_value(key):
    return some_fun(key)

def some_fun(key):
    return key

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))

"""
2. MARSHMELLOW:
This is a library which helps when serialization/deserialization are needed. For example, in the above requests HTTP call, we want to load the JSON response in a python class. Then, we can load the JSON response directly into a schema which is having post_load decorator which maps the entities into a class. For serializing the class so as to send it over the network, the python can be dumped in a schema. If a particular field should not be displayed in the response on some condition, we have to write a BaseSchema which removes a particular key in response to some condition.

a) In-Memory Caching[cachetools]: The items are stored in the heap memory of the application. cachetools provides decorator supporting LRU and TTL based caching algorithms. In LRU, if the cache is full, the item being used very least recently will be discarded and In TTL algorithms, an item is discarded when it exceeds over a particular time duration. Sample example:

@cached(cache=LRUCache(maxsize=32)) #item discarded if size exceeds 32 keys
def get_sum(arr):
    return sum(arr)

@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_value(key):
    return some_fun(key)

b) File-Based Caching: This cache stores the items on the disk. The class werkzeug.contrib.cache.FileSystemCache takes the file directory path where the items will be stored in the system, threshold, and timeout. Sample example:
from werkzeug.contrib.cache import FileSystemCache
fs_cache = FileSystemCache("/tmp", threshold=64, timeout=120)
fs_cache.set(key)  # to set a key

c) Memcached Cache [pymemcache]: The items are stored on distributed systems where items can be stored in a large amount of large size and can be accessed from any host. The class werkzeug.contrib.cache.MemcachedCache takes the tuple of server addresses, timeout, and prefix key if any. Pymemcache is created by Pinterest, which implements different hashing techniques to store the items on the server.

"""
