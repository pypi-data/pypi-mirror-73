# mavis.schedule.pipeline

## PROGNAME

```python
PROGNAME = shutil.which('mavis')
```

## SHEBANG

```python
SHEBANG = '#!/bin/bash'
```

## SCHEDULERS_BY_NAME

```python
SCHEDULERS_BY_NAME = {
    sched.NAME: sched for sched in [SlurmScheduler, TorqueScheduler, LocalScheduler, SgeScheduler]
```

## class Pipeline







### Pipeline.check\_status()

Check all jobs for completetion. Report any failures, etc.

```python
def check_status(self, submit=False, resubmit=False, log=DEVNULL):
```

**Args**

- submit (`bool`): submit any pending jobs
- resubmit
- log

### Pipeline.read\_build\_file()

read the configuration file which stored the build information concerning jobs and dependencies

```python
@classmethod
def read_build_file(cls, filepath):
```

**Args**

- filepath (`str`): path to the input config file

### Pipeline.write\_build\_file()

write the build.cfg file for the current pipeline. This is the file used in re-loading the pipeline
to check the status and report failures, etc. later.

```python
def write_build_file(self, filename):
```

**Args**

- filename (`str`): path to the output config file


## stringify\_args\_to\_command()

takes a list of arguments and prepares them for writing to a bash script

```python
def stringify_args_to_command(args):
```

**Args**

- args

## parse\_run\_time()

parses the run time listed at the end of a file following mavis conventions

```python
def parse_run_time(filename):
```

**Args**

- filename

## run\_conversion()

Converts files if not already converted. Returns a list of filenames

```python
def run_conversion(config, libconf, conversion_dir, assume_no_untemplated=True):
```

**Args**

- config
- libconf
- conversion_dir
- assume_no_untemplated

## validate\_args()

Pull arguments from the main config and library specific config to pass to validate

```python
def validate_args(config, libconf):
```

**Args**

- config ([MavisConfig](../../config/#class-mavisconfig)): the main program config
- libconf ([LibraryConfig](../../config/#class-libraryconfig)): library specific configuration

## annotate\_args()

Pull arguments from the main config and library specific config to pass to annotate

```python
def annotate_args(config, libconf):
```

**Args**

- config ([MavisConfig](../../config/#class-mavisconfig)): the main program config
- libconf ([LibraryConfig](../../config/#class-libraryconfig)): library specific configuration

## summary\_args()

Pull arguments from the main config and library specific config to pass to summary

```python
def summary_args(config):
```

**Args**

- config ([MavisConfig](../../config/#class-mavisconfig)): the main program config

## cluster\_args()

Pull arguments from the main config and library specific config to pass to cluster

```python
def cluster_args(config, libconf):
```

**Args**

- config ([MavisConfig](../../config/#class-mavisconfig)): the main program config
- libconf ([LibraryConfig](../../config/#class-libraryconfig)): library specific configuration
