# mavis.pairing.pairing

## product\_key()

unique id for the product row

```python
def product_key(bpp):
```

**Args**

- bpp

## predict\_transcriptome\_breakpoint()

for a given genomic breakpoint and the target transcript. Predicts the possible transcriptomic
breakpoints that would be expected based on the splicing model for abrogated splice sites

```python
def predict_transcriptome_breakpoint(breakpoint, transcript):
```

**Args**

- breakpoint ([Breakpoint](../../breakpoint/#class-breakpoint)): the genomic breakpoint
- transcript ([PreTranscript](../../annotate/genomic/#class-pretranscript)): the transcript

!!! note
	see [theory - pairing similar events](/background/theory/#pairing-similar-events)



## equivalent()

compares two events by breakpoint position to see if they are equivalent

```python
def equivalent(event1, event2, distances=None):
```

**Args**

- event1
- event2
- distances

## pair\_by\_distance()

for a set of input calls, pair by distance

```python
def pair_by_distance(calls, distances, log=DEVNULL, against_self=False):
```

**Args**

- calls
- distances
- log
- against_self

## inferred\_equivalent()

comparison of events using product prediction and breakpoint prediction

```python
def inferred_equivalent(event1, event2, reference_transcripts, distances=None):
```

**Args**

- event1
- event2
- reference_transcripts
- distances
