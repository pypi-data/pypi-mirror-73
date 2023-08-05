# mavis.illustrate.scatter

## class ScatterPlot

holds settings that will go into matplotlib after conversion using the mapping system

### ScatterPlot.\_\_init\_\_()

```python
def __init__(
    self,
    points,
    y_axis_label,
    ymax=None,
    ymin=None,
    xmin=None,
    xmax=None,
    hmarkers=None,
    height=100,
    point_radius=2,
    title='',
    yticks=None,
    colors=None,
    density=1,
    ymax_color='#FF0000',
):
```

**Args**

- points
- y_axis_label
- ymax
- ymin
- xmin
- xmax
- hmarkers
- height
- point_radius
- title
- yticks
- colors
- density
- ymax_color


## bam\_to\_scatter()

pull data from a bam file to set up a scatter plot of the pileup

```python
def bam_to_scatter(
    bam_file,
    chrom,
    start,
    end,
    density,
    strand=None,
    axis_name=None,
    ymax=None,
    min_mapping_quality=0,
    ymax_color='#FF0000',
):
```

**Args**

- bam_file (`str`): path to the bam file
- chrom (`str`): chromosome name
- start (`int`): genomic start position for the plot
- end (`int`): genomic end position for the plot
- density
- strand (`STRAND`): expected strand
- axis_name (`str`): axis name
- ymax (`int`): maximum value to plot the y axis
- min_mapping_quality (`int`): minimum mapping quality for reads to be considered in the plot
- ymax_color

**Returns**

- [ScatterPlot](#class-scatterplot): the scatter plot representing the bam pileup

## draw\_scatter()

given a xmapping, draw the scatter plot svg group

```python
def draw_scatter(ds, canvas, plot, xmapping, log=DEVNULL):
```

**Args**

- ds ([DiagramSettings](../constants/#class-diagramsettings)): the settings/constants to use for building the svg
- canvas (`svgwrite.canvas`): the svgwrite object used to create new svg elements
- plot ([ScatterPlot](#class-scatterplot)): the plot to be drawn

- log
