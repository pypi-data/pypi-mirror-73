# mavis.schedule.scheduler

## class Scheduler

Class responsible for methods interacting with the scheduler

### Scheduler.\_\_init\_\_()

```python
def __init__(self, concurrency_limit=None, remote_head_ssh=''):
```

**Args**

- concurrency_limit (`int`): the maximum allowed concurrent processes. Defaults to one less than the total number available
- remote_head_ssh

### Scheduler.command()

Wrapper to deal with subprocess commands. If configured and not on the head node currently, will send the command through ssh

```python
def command(self, command, shell=False):
```

**Args**

- command (`list or str`): the command can be a list or a string and is passed to the subprocess to be run
- shell

**Returns**

- `str`: the content returns from stdout of the subprocess


### Scheduler.submit()

submit a job to the scheduler

```python
def submit(self, job):
```

**Args**

- job

### Scheduler.update\_info()

update the information about the job from the scheduler

```python
def update_info(self, job):
```

**Args**

- job


### Scheduler.format\_dependencies()

returns a string representing the dependency argument

```python
def format_dependencies(self, job):
```

**Args**

- job


## class SlurmScheduler

**inherits** [Scheduler](#class-scheduler)

Class for formatting commands to match a SLURM scheduler system
SLURM docs can be found here https://slurm.schedmd.com

### SlurmScheduler.submit()

runs a subprocess sbatch command

```python
def submit(self, job):
```

**Args**

- job ([Job](../job/#class-job)): the job to be submitted

### SlurmScheduler.parse\_sacct()

parses content returned from the sacct command

```python
@classmethod
def parse_sacct(cls, content):
```

**Args**

- content (`str`): the content returned from the sacct command

### SlurmScheduler.parse\_scontrol\_show()

parse the content from the command: scontrol show job <JOBID>

```python
@classmethod
def parse_scontrol_show(cls, content):
```

**Args**

- content (`str`): the content to be parsed

### SlurmScheduler.update\_info()

Pull job information about status etc from the scheduler. Updates the input job

```python
def update_info(self, job):
```

**Args**

- job ([Job](../job/#class-job)): the job to be updated

### SlurmScheduler.cancel()

cancel a job

```python
def cancel(self, job, task_ident=None):
```

**Args**

- job ([Job](../job/#class-job)): the job to be cancelled
- task_ident (`int`): the task id to be cancelled (instead of the entire array)

### SlurmScheduler.format\_dependencies()

returns a string representing the dependency argument

```python
def format_dependencies(self, job):
```

**Args**

- job ([Job](../job/#class-job)): the job the argument is being built for


## class SgeScheduler

**inherits** [Scheduler](#class-scheduler)

Class for managing interactions with the SGE scheduler

### SgeScheduler.parse\_qacct()

parses the information produced by qacct

```python
@classmethod
def parse_qacct(cls, content):
```

**Args**

- content (`str`): the content returned from the qacct command

### SgeScheduler.parse\_qstat()

parses the qstat content into rows/dicts representing individual jobs

```python
@classmethod
def parse_qstat(cls, content, job_id):
```

**Args**

- content (`str`): content returned from the qstat command
- job_id


### SgeScheduler.submit()

runs a subprocess sbatch command

```python
def submit(self, job):
```

**Args**

- job ([Job](../job/#class-job)): the job to be submitted

### SgeScheduler.update\_info()

runs a subprocess scontrol command to get job details and add them to the current job

```python
def update_info(self, job):
```

**Args**

- job ([Job](../job/#class-job)): the job information is being gathered for

### SgeScheduler.cancel()

cancel a job or a specific task of an array job

```python
def cancel(self, job, task_ident=None):
```

**Args**

- job ([Job](../job/#class-job)): the job to cancel
- task_ident (`int`): if specified, will cancel the given task instead of the whole array or job

### SgeScheduler.format\_dependencies()

returns a string representing the dependency argument

```python
def format_dependencies(self, job):
```

**Args**

- job


## class TorqueScheduler

**inherits** [SgeScheduler](#class-sgescheduler)

Class for managing interactions with the Torque scheduler

### TorqueScheduler.format\_dependencies()

returns a string representing the dependency argument

```python
def format_dependencies(self, job):
```

**Args**

- job

### TorqueScheduler.parse\_qstat()

parses the qstat content into rows/dicts representing individual jobs

```python
@classmethod
def parse_qstat(cls, content):
```

**Args**

- content (`str`): content returned from the qstat command

### TorqueScheduler.submit()

runs a subprocess qsub command

```python
def submit(self, job):
```

**Args**

- job ([Job](../job/#class-job)): the job to be submitted

### TorqueScheduler.update\_info()

runs a subprocess scontrol command to get job details and add them to the current job

```python
def update_info(self, job):
```

**Args**

- job ([Job](../job/#class-job)): the job information is being gathered for

### TorqueScheduler.cancel()

cancel a job

```python
def cancel(self, job, task_ident=None):
```

**Args**

- job ([Job](../job/#class-job)): the job to be cancelled
- task_ident (`int`): if specified then a single task will be cancelled instead of the whole job or array


## time\_format()

Converts a total seconds to a str format "H:M:S"

```python
def time_format(total_seconds):
```

**Args**

- total_seconds

## consecutive\_ranges()

Given a list of integers, return a list of ranges

```python
def consecutive_ranges(numbers):
```

**Args**

- numbers

**Examples**

```python
>>> consecutive_ranges([1, 2, 3, 4, 5, 9, 10, 14, 18])
[(1, 5), (9, 10), (14, 14), (18, 18)]
```

