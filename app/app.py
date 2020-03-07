import os
from flask import Flask, request
from pymemcache.client.base import Client


def fib(n):
    def put_in_cache(n, fib):
        client = Client(('my_memcached', 11211))
        client.set(str(n), fib)


    def get_from_cache(n):
        client = Client(('my_memcached', 11211))
        if client.get(str(n)):
            result = client.get(str(n)).decode("utf-8")    
            try:
                return int(result)
            except ValueError:
                return None
        return None


    if n == 0:
        return 0
    if n == 1:
        return 1
    if get_from_cache(n):
        return get_from_cache(n)        
    else:
        f = fib(n-1) + fib(n-2)
        put_in_cache(n, f)
        return f


app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

@app.route('/fib')
def fib_ws():
    number = request.args.get('num')
    try:
        number = int(number)
    except ValueError:
        return "Введите число"
    return str(fib(number))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
