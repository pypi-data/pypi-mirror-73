# mavis.illustrate.elements

This is the primary module responsible for generating svg visualizations

## HEX_WHITE

```python
HEX_WHITE = '#FFFFFF'
```

## HEX_BLACK

```python
HEX_BLACK = '#000000'
```

## draw\_legend()

generates an svg group object representing the legend

```python
def draw_legend(config, canvas, swatches, border=True):
```

**Args**

- config
- canvas
- swatches
- border



## draw\_ustranscript()

builds an svg group representing the transcript. Exons are drawn in a track with the splicing
information and domains are drawn in separate tracks below

if there are multiple splicing variants then multiple exon tracks are drawn

```python
def draw_ustranscript(
    config,
    canvas,
    pre_transcript,
    target_width=None,
    breakpoints=[],
    labels=LabelMapping(),
    colors={},
    mapping=None,
    reference_genome=None,
    masks=None,
):
```

**Args**

- config
- canvas (`svgwrite.drawing.Drawing`): the main svgwrite object used to create new svg elements
- pre_transcript ([Transcript](../../annotate/genomic/#class-transcript)): the transcript being drawn
- target_width (`int`): the target width of the diagram
- breakpoints (List\[[Breakpoint](../../breakpoint/#class-breakpoint)\]): the breakpoints to overlay
- labels
- colors
- mapping
- reference_genome
- masks

## draw\_genes()

draws the genes given in order of their start position trying to minimize
the number of tracks required to avoid overlap

```python
def draw_genes(
    config,
    canvas,
    genes,
    target_width,
    breakpoints=None,
    colors=None,
    labels=None,
    plots=None,
    masks=None,
):
```

**Args**

- config
- canvas (`svgwrite.drawing.Drawing`): the main svgwrite object used to create new svg elements
- genes (List\[[Gene](../../annotate/genomic/#class-gene)\]): the list of genes to draw
- target_width (`int`): the target width of the diagram
- breakpoints (List\[[Breakpoint](../../breakpoint/#class-breakpoint)\]): the breakpoints to overlay
- colors (Dict\[`str`,[Gene](../../annotate/genomic/#class-gene)\]): dictionary of the colors assigned to each Gene as
- labels
- plots
- masks



## draw\_exon()

generates the svg object representing an exon

```python
def draw_exon(config, canvas, exon, width, height, fill, label='', translation=None):
```

**Args**

- config
- canvas (`svgwrite.drawing.Drawing`): the main svgwrite object used to create new svg elements
- exon ([Exon](../../annotate/genomic/#class-exon)): the exon to draw
- width (`int`): the pixel width
- height (`int`): the pixel height
- fill (`str`): the fill color to use for the exon
- label
- translation

## draw\_template()

Creates the template/chromosome illustration

Return:
svgwrite.container.Group: the group element for the diagram

```python
def draw_template(
    config, canvas, template, target_width, labels=None, colors=None, breakpoints=None
):
```

**Args**

- config
- canvas
- template
- target_width
- labels
- colors
- breakpoints

## draw\_gene()

generates the svg object representing a gene

```python
def draw_gene(config, canvas, gene, width, height, fill, label='', reference_genome=None):
```

**Args**

- config
- canvas (`svgwrite.drawing.Drawing`): the main svgwrite object used to create new svg elements
- gene ([Gene](../../annotate/genomic/#class-gene)): the gene to draw
- width (`int`): the pixel width
- height (`int`): the pixel height
- fill (`str`): the fill color to use for the gene
- label
- reference_genome
