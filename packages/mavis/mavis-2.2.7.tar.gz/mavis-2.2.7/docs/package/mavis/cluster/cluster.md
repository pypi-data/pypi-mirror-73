# mavis.cluster.cluster

## class BreakpointPairGroupKey

**inherits** `[]`




## merge\_integer\_intervals()

Merges a set of integer intervals into a single interval where the center is the
weighted mean of the input intervals. The weight is inversely proportional to the
length of each interval. The length of the final interval is the average of the lengths
of the input intervals capped in size so that it never extends beyond the union of the
input intervals

```python
def merge_integer_intervals(*intervals, weight_adjustment=0):
```



## merge\_by\_union()

for a given set of breakpoint pairs, merge the union of all pairs that are
within the given distance (cluster_radius)

```python
def merge_by_union(input_pairs, group_key, weight_adjustment=10, cluster_radius=200):
```

**Args**

- input_pairs
- group_key
- weight_adjustment
- cluster_radius

## merge\_breakpoint\_pairs()

two-step merging process

1. merges all 'small' (see cluster_initial_size_limit) events as the union of all events that
fall within the cluster_radius
2. for all remaining events choose the 'best' merge for any event within cluster_radius of an
existing node. Otherwise the node is added unmerged. The events in the second phase are
done in order of smallest total breakpoint interval size to largest

```python
def merge_breakpoint_pairs(
    input_pairs, cluster_radius=200, cluster_initial_size_limit=25, verbose=False
):
```

**Args**

- input_pairs (List\[[BreakpointPair](../../breakpoint/#class-breakpointpair)\]): the pairs to be merged
- cluster_radius
- cluster_initial_size_limit (`int`): maximum size of breakpoint intervals allowed in the first merging phase
- verbose

**Returns**

- Dict\[[BreakpointPair](../../breakpoint/#class-breakpointpair),List\[[BreakpointPair](../../breakpoint/#class-breakpointpair)\]\]: mapping of merged breakpoint pairs to the input pairs used in the merge
