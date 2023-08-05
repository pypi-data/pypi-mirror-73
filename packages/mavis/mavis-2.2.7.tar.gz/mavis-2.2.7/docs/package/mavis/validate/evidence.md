# mavis.validate.evidence

## class GenomeEvidence

**inherits** [Evidence](../base/#class-evidence)


### GenomeEvidence.generate\_window()

given some input breakpoint uses the current evidence setting to determine an
appropriate window/range of where one should search for supporting reads

```python
def generate_window(self, breakpoint):
```

**Args**

- breakpoint ([Breakpoint](../../breakpoint/#class-breakpoint)): the breakpoint we are generating the evidence window for

**Returns**

- [Interval](../../interval/#class-interval): the range where reads should be read from the bam looking for evidence for this event



## class TranscriptomeEvidence

**inherits** [Evidence](../base/#class-evidence)


### TranscriptomeEvidence.traverse()

given some genomic position and a distance. Uses the input transcripts to
compute all possible genomic end positions at that distance if intronic
positions are ignored

```python
def traverse(self, start, distance, direction, strand=STRAND.NS, chrom=None):
```

**Args**

- start (`int`): the genomic start position
- distance (`int`): the amount of exonic/intergenic units to traverse
- direction (`ORIENT`): the direction wrt to the positive/forward reference strand to traverse
- strand
- chrom



### TranscriptomeEvidence.distance()

give the current list of transcripts, computes the putative exonic/intergenic distance
given two genomic positions. Intronic positions are ignored

Intergenic calculations are only done if exonic only fails

```python
def distance(self, start, end, strand=STRAND.NS, chrom=None):
```

**Args**

- start
- end
- strand
- chrom

### TranscriptomeEvidence.generate\_window()

given some input breakpoint uses the current evidence setting to determine an
appropriate window/range of where one should search for supporting reads

```python
def generate_window(self, breakpoint):
```

**Args**

- breakpoint ([Breakpoint](../../breakpoint/#class-breakpoint)): the breakpoint we are generating the evidence window for

**Returns**

- [Interval](../../interval/#class-interval): the range where reads should be read from the bam looking for evidence for this event


### TranscriptomeEvidence.exon\_boundary\_shift\_cigar()

given an input read, converts deletions to N when the deletion matches the exon boundaries. Also shifts alignments
to correspond to the exon boundaries where possible

```python
def exon_boundary_shift_cigar(self, read):
```

**Args**

- read


