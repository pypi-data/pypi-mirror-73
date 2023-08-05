# mavis.schedule.local

## class LocalJob

**inherits** [Job](../job/#class-job)


### LocalJob.check\_complete()

check that the complete stamp associated with this job exists

```python
def check_complete(self):
```



## class LocalScheduler

**inherits** [Scheduler](../scheduler/#class-scheduler)

Scheduler class for dealing with running mavis locally

### LocalScheduler.\_\_init\_\_()

```python
def __init__(self, *pos, **kwargs):
```

### LocalScheduler.submit()

Add a job to the pool

```python
def submit(self, job):
```

**Args**

- job ([LocalJob](#class-localjob)): the job to be submitted

### LocalScheduler.wait()

wait for everything in the current pool to finish

```python
def wait(self):
```




