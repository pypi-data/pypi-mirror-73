# mavis.summary.summary


## filter\_by\_call\_method()

Filters a set of breakpoint pairs to returns the call with the most evidence.
Prefers contig evidence over spanning over split over flanking, etc.

```python
def filter_by_call_method(bpp_list):
```

**Args**

- bpp_list

## group\_events()

group events together and join data attributes

```python
def group_events(events):
```

**Args**

- events

## group\_by\_distance()

groups a set of calls based on their proximity. Returns a new list of calls where close calls have been merged

```python
def group_by_distance(calls, distances):
```

**Args**

- calls
- distances

## annotate\_dgv()

given a list of bpps and a dgv reference, annotate the events that are within the set distance of both breakpoints

```python
def annotate_dgv(bpps, dgv_regions_by_reference_name, distance=0):
```

**Args**

- bpps
- dgv_regions_by_reference_name
- distance

## get\_pairing\_state()

given two libraries, returns the appropriate descriptor for their matched state

```python
def get_pairing_state(
    current_protocol,
    current_disease_state,
    other_protocol,
    other_disease_state,
    is_matched=False,
    inferred_is_matched=False,
):
```

**Args**

- current_protocol (`PROTOCOL`): the protocol of the current library
- current_disease_state (`DISEASE_STATUS`): the disease status of the current library
- other_protocol (`PROTOCOL`): protocol of the library being comparing to
- other_disease_state (`DISEASE_STATUS`): disease status of the library being compared to
- is_matched (`bool`): True if the libraries are paired
- inferred_is_matched

**Returns**

- `(PAIRING_STATE)`: descriptor of the pairing of the two libraries

