# mavis.validate.base

## class Evidence

**inherits** [BreakpointPair](../../breakpoint/#class-breakpointpair)






### Evidence.collect\_from\_outer\_window()

determines if evidence should be collected from the outer window (looking for flanking evidence)
or should be limited to the inner window (split/spanning/contig only)

```python
def collect_from_outer_window(self):
```

**Returns**

- `bool`: True or False





### Evidence.supporting\_reads()

convenience method to return all flanking, split and spanning reads associated with an evidence object

```python
def supporting_reads(self):
```

### Evidence.collect\_spanning\_read()

spanning read: a read covering BOTH breakpoints

This is only applicable to small events. Do not need to look for soft clipped reads
here since they will be collected already

```python
def collect_spanning_read(self, read):
```

**Args**

- read (`pysam.AlignedSegment`): the putative spanning read

**Returns**

- `bool`:  - True: the read was collected and stored in the current evidence object - False: the read was not collected

### Evidence.collect\_compatible\_flanking\_pair()

checks if a given read meets the minimum quality criteria to be counted as evidence as stored as support for
this event

```python
def collect_compatible_flanking_pair(self, read, mate, compatible_type):
```

**Args**

- read (`pysam.AlignedSegment`): the read to add
- mate (`pysam.AlignedSegment`): the mate
- compatible_type (`SVTYPE`): the type we are collecting for

**Returns**

- `bool`:  - True: the pair was collected and stored in the current evidence object - False: the pair was not collected

**Raises**

- `ValueError`: if the input reads are not a valid pair

!!! note
	see [theory - types of flanking evidence](/background/theory/#compatible-flanking-pairs)

### Evidence.collect\_flanking\_pair()

checks if a given read meets the minimum quality criteria to be counted as evidence as stored as support for
this event

```python
def collect_flanking_pair(self, read, mate):
```

**Args**

- read (`pysam.AlignedSegment`): the read to add
- mate (`pysam.AlignedSegment`): the mate

**Returns**

- `bool`:  - True: the pair was collected and stored in the current evidence object - False: the pair was not collected

**Raises**

- `ValueError`: if the input reads are not a valid pair
: see [theory - types of flanking evidence](/background/theory/#types-of-flanking-evidence)


### Evidence.collect\_split\_read()

adds a split read if it passes the criteria filters and raises a warning if it does not

```python
def collect_split_read(self, read, first_breakpoint):
```

**Args**

- read (`pysam.AlignedSegment`): the read to add
- first_breakpoint (`bool`): add to the first breakpoint (or second if false)

**Returns**

- `bool`:  - True: the read was collected and stored in the current evidence object - False: the read was not collected

**Raises**

- [NotSpecifiedError](../../error/#class-notspecifiederror): if the breakpoint orientation is not specified

### Evidence.decide\_sequenced\_strand()

given a set of reads, determines the sequenced strand (if possible) and then returns the majority
strand found

```python
def decide_sequenced_strand(self, reads):
```

**Args**

- reads

**Returns**

- `STRAND`: the sequenced strand

**Raises**

- `ValueError`: input was an empty set or the ratio was not sufficient to decide on a strand

### Evidence.assemble\_contig()

uses the split reads and the partners of the half mapped reads to create a contig
representing the sequence across the breakpoints

if it is not strand specific then sequences are sorted alphanumerically and only the
first of a pair is kept (paired by sequence)

```python
def assemble_contig(self, log=DEVNULL):
```

**Args**

- log

### Evidence.load\_evidence()

open the associated bam file and read and store the evidence
does some preliminary read-quality filtering

```python
def load_evidence(self, log=DEVNULL):
```

**Args**

- log




