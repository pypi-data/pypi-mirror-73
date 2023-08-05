# mavis.schedule.constants

## JOB_STATUS

```python
JOB_STATUS = MavisNamespace(
    'SUBMITTED',
    'COMPLETED',
    'ERROR',
    'RUNNING',
    'FAILED',
    'PENDING',
    'CANCELLED',
    NOT_SUBMITTED='NOT SUBMITTED',
    UNKNOWN='UNKNOWN',
    __name__='mavis.schedule.constants.JOB_STATUS',
)
```

## SCHEDULER

```python
SCHEDULER = MavisNamespace(
    'SGE', 'SLURM', 'TORQUE', 'LOCAL', __name__='mavis.schedule.constants.SCHEDULER'
)
```

## MAIL_TYPE

```python
MAIL_TYPE = MavisNamespace(
    'BEGIN', 'END', 'FAIL', 'ALL', 'NONE', __name__='mavis.schedule.constants.MAIL_TYPE'
)
```

## STD_OPTIONS

```python
STD_OPTIONS = ['memory_limit', 'queue', 'time_limit', 'import_env', 'mail_user', 'mail_type']
```

## OPTIONS

```python
OPTIONS = WeakMavisNamespace(__name__='mavis.schedule.constants.options')
```

## cumulative\_job\_state()

Given a set of states, return a single state based on the reporting priority

```python
def cumulative_job_state(states):
```

**Args**

- states
