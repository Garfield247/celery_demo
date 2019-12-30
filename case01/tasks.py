from celery import Celery

#app = Celery("tasks",broker="redis://localhost")
#app = Celery("tasks",broker="pyamqp://",backend="redis://localhost")
app = Celery("tasks",broker="redis://localhost:6379/1",backend="redis://localhost:6379/2")


@app.task
def add(x,y):
    return x + y

