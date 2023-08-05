# mavis.validate.call

## class EventCall

**inherits** [BreakpointPair](../../breakpoint/#class-breakpointpair)

class for holding evidence and the related calls since we can't freeze the evidence object
directly without a lot of copying. Instead we use call objects which are basically
just a reference to the evidence object and decisions on class, exact breakpoints, etc


### EventCall.\_\_init\_\_()

```python
def __init__(
    self,
    b1,
    b2,
    source_evidence,
    event_type,
    call_method,
    contig=None,
    contig_alignment=None,
    untemplated_seq=None,
):
```

**Args**

- b1
- b2
- source_evidence
- event_type (`SVTYPE`): the type of structural variant
- call_method (`CALL_METHOD`): the way the breakpoints were called
- contig ([Contig](../../assemble/#class-contig)): the contig used to call the breakpoints (if applicable)
- contig_alignment
- untemplated_seq


### EventCall.complexity()

The sequence complexity for the call. If called by contig then the complexity of the
contig sequence, otherwise an average of the sequence complexity of the support based
on the call method

```python
def complexity(self):
```

### EventCall.support()

return a set of all reads which support the call

```python
def support(self):
```

### EventCall.is\_supplementary()

check if the current event call was the target event given the source evidence object or an off-target call, i.e.
something that was called as part of the original target.
This is important b/c if the current event was not one of the original target it may not be fully investigated in
other libraries

```python
def is_supplementary(self):
```

### EventCall.add\_flanking\_support()

counts the flanking read-pair support for the event called. The original source evidence may
have contained evidence for multiple events and uses a larger range so flanking pairs here
are checked specifically against the current breakpoint call

```python
def add_flanking_support(self, flanking_pairs, is_compatible=False):
```

**Args**

- flanking_pairs
- is_compatible

**Returns**

- `Tuple[Set[str],int,int]`:  * set of str - set of the read query_names * int - the median insert size * int - the standard deviation (from the median) of the insert size

!!! note
	see [theory - determining flanking support](/background/theory/#determining-flanking-support)





### EventCall.flanking\_metrics()

computes the median and standard deviation of the flanking pairs. Note that standard
deviation is calculated wrt the median and not the average. Also that the fragment size
is calculated as a range so the start and end of the range are used in computing these
metrics

```python
def flanking_metrics(self):
```

**Returns**

- `Tuple[float,float]`: the median fragment size and the fragment size standard deviation wrt the median




### EventCall.characterize\_repeat\_region()

For a given event, determines the number of repeats the insertion/duplication/deletion is following.
This is most useful in flagging homopolymer regions. Will raise a ValueError if the current event is
not an expected type or is non-specific.

```python
@staticmethod
def characterize_repeat_region(event, reference_genome):
```

**Args**

- event
- reference_genome

**Returns**

- `Tuple[int,str]`: the number of repeats and the repeat sequence

### EventCall.flatten()

converts the current call to a dictionary for a row in a tabbed file

```python
def flatten(self):
```



## filter\_consumed\_pairs()

given a set of read tuples, returns all tuples where neither read in the tuple is in the consumed set

```python
def filter_consumed_pairs(pairs, consumed_reads):
```

**Args**

- pairs (`Set[Tuple[pysam.AlignedSegment,pysam.AlignedSegment]]`): pairs to be filtered
- consumed_reads: (Set[pysam.AlignedSegment)]: set of reads that have been used/consumed

**Returns**

- `Set[Tuple[pysam.AlignedSegment,pysam.AlignedSegment]]`: set of filtered tuples

**Examples**

```python
>>> pairs = {(1, 2), (3, 4), (5, 6)}
>>> consumed_reads = {1, 2, 4}
>>> filter_consumed_pairs(pairs, consumed_reads)
{(5, 6)}
```


!!! note
	this will work with any hash-able object


## call\_events()

generates a set of event calls based on the evidence associated with the source_evidence object
will also narrow down the event type

```python
def call_events(source_evidence):
```

**Args**

- source_evidence ([Evidence](../base/#class-evidence)): the input evidence

**Returns**

- List\[[EventCall](#class-eventcall)\]: list of calls



