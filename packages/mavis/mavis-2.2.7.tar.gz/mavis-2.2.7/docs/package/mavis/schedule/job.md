# mavis.schedule.job

## class LogFile

stores information about the log status

### LogFile.\_\_init\_\_()

```python
def __init__(self, filename, status, message=None):
```

**Args**

- filename (`str`): path to the logfile
- status (`LogFile.STATUS`): the status of the logfile
- message (`str`): the message parsed from the logfile. Generally this is an error from the log

### LogFile.parse()

given a file parse to see if it looks like a complete log file (contains run time),
was truncated, or reported an error

```python
@classmethod
def parse(cls, filename):
```

**Args**

- filename


## class Job


### Job.display\_name()

Used for identifying this job in an ini config file

```python
@property
def display_name(self):
```

**Args**

- self


### Job.logfile()

returns the path to the logfile with job name and job id substituted into the stdout pattern

```python
def logfile(self):
```

### Job.complete\_stamp()

returns the path to the expected complete stamp

```python
def complete_stamp(self):
```



## class ArrayJob

**inherits** [Job](#class-job)

Class for dealing with array jobs. Jobs with many tasks

### ArrayJob.\_\_init\_\_()

```python
def __init__(self, stage, task_list, **kwargs):
```

**Args**

- stage
- task_list (`Union[List,int]`): the ids of tasks in the job array


### ArrayJob.get\_task()

returns a task by task id

```python
def get_task(self, task_ident):
```

**Args**

- task_ident




### ArrayJob.complete\_stamp()

returns the path to the expected complete stamp

```python
def complete_stamp(self, task_ident):
```

**Args**

- task_ident






## class TorqueArrayJob

**inherits** [ArrayJob](#class-arrayjob)




## class Task





