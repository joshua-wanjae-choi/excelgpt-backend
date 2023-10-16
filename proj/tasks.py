from .celery import app


@app.task
def add(x, y):
    exec('echo "hello world" >> aaa')
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task(serializer='json')
def run(source: str):
    try:
        exec(source)
    except Exception as e:
        return e
    return True
