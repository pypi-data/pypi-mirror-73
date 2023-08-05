# mavis.cluster.main

## split\_clusters()

For a set of clusters creates a bed file representation of all clusters.
Also splits the clusters evenly into multiple files based on the user parameters (min_clusters_per_file, max_files)

```python
def split_clusters(
    clusters, outputdir, batch_id, min_clusters_per_file=0, max_files=1, write_bed_summary=True
):
```

**Args**

- clusters
- outputdir
- batch_id
- min_clusters_per_file
- max_files
- write_bed_summary

**Returns**

- `list`: of output file names (not including the bed file)

