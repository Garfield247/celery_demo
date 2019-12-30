# Celery

Celery 是一个简单、灵活、可靠的分布式系统，可以处理大量的消息，同时提供维护这样一个系统所需的工具。

## 简单的celery demo

### 服务代码

**`tasks.py`**

```python
from celery import Celery

app = Celery("tasks",broker="redis://localhost")

@app.task
def add(x,y):
    return x + y
```

> Celery 的第一个参数是当前模块名称
>
> broker 关键字参数，消息代理默认是RabbitMQ，使用amqp: / / localhost，对于 Redis，您可以使用 Redis: / / localhost。

### 运行worker服务

现在可以通过执行带有 worker 参数的程序来运行 worker:

```shell
$ celery -A tasks worker --loglevel=info
```

Terminal输出：

```shell


celery@CatMandeMacBook-Pro.local v4.4.0 (cliffs)

Darwin-19.2.0-x86_64-i386-64bit 2019-12-30 14:29:07

[config]
.> app:         tasks:0x1088f2518
.> transport:   redis://localhost:6379//
.> results:     disabled://
.> concurrency: 8 (prefork)
.> task events: OFF (enable -E to monitor tasks in this worker)

[queues]
.> celery           exchange=celery(direct) key=celery


[tasks]
  . tasks.add

[2019-12-30 14:29:07,479: INFO/MainProcess] Connected to redis://localhost:6379//
[2019-12-30 14:29:07,489: INFO/MainProcess] mingle: searching for neighbors
[2019-12-30 14:29:08,511: INFO/MainProcess] mingle: all alone
[2019-12-30 14:29:08,527: INFO/MainProcess] celery@CatMandeMacBook-Pro.local ready.
```

### 调用服务

```python
>>> from tasks import add
>>> add.delay(4, 4)
```

Terminal output

```
[2019-12-30 14:42:32,972: INFO/MainProcess] Received task: tasks.add[b3d261ab-89e1-4f48-9d78-e839ab8f96fb]
[2019-12-30 14:42:32,973: INFO/ForkPoolWorker-8] Task tasks.add[b3d261ab-89e1-4f48-9d78-e839ab8f96fb] succeeded in 9.836500248638913e-05s: 8
```

### 配置后端

如果想跟踪任务的状态，celery需要存储或发送状态到某个地方。 有几个内置的结果后端可供选择: sqlalchemy / django ORM、 Memcached、 Redis、 RPC (rabbitmq / amqp) 

```python
app = Celery("tasks",broker="pyamqp://",backend="redis://localhost")
app = Celery("tasks",broker="redis://localhost:6379/1",backend="redis://localhost:6379/2")
```

现在配置了结果后端，再次调用该任务。 这一次，您将保留调用任务时返回的 AsyncResult 实例:

```python
>>> result = add.delay(4, 4)
```

Ready ()方法返回任务是否已经完成处理:

```python
>>> result.ready()
False
```

你可以等待结果完成，但这种方法很少使用，因为它将异步调用转换为同步调用:

```python
>>> result.get(timeout=1)
8
```

如果任务引发异常，get ()将重新引发异常，但是您可以通过指定 propagate 参数来覆盖这个异常:

```python
>>> result.get(propagate=False)
```

如果任务引发了异常，你也可以访问原始的回溯:

```python
>>> result.traceback
```

