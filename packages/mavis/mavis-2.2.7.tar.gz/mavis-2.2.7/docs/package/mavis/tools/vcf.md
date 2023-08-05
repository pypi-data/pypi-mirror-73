# mavis.tools.vcf

## parse\_bnd\_alt()

parses the alt statement from vcf files using the specification in vcf 4.2/4.2.

Assumes that the reference base is always the outermost base (this is based on the spec and also manta results as
the spec was missing some cases)

```python
def parse_bnd_alt(alt):
```

**Args**

- alt

## convert\_record()

converts a vcf record

```python
def convert_record(record, record_mapping={}, log=DEVNULL):
```

**Args**

- record
- record_mapping
- log

!!! note
	CT = connection type, If given this field will be used in determining the orientation at the breakpoints.
	From https://groups.google.com/forum/#!topic/delly-users/6Mq2juBraRY, we can expect certain CT types for
	certain event types
	- translocation/inverted translocation: 3to3, 3to5, 5to3, 5to5
	- inversion: 3to3, 5to5
	- deletion: 3to5
	- duplication: 5to3

## convert\_file()

process a VCF file

```python
def convert_file(input_file: str, file_type: str, log):
```

**Args**

- input_file (`str`): the input file name
- file_type (`str`): the input type
- log

**Raises**

- `err`: [description]
