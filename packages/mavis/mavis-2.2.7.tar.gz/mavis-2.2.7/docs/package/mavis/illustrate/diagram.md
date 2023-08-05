# mavis.illustrate.diagram

This is the primary module responsible for generating svg visualizations

## HEX_WHITE

```python
HEX_WHITE = '#FFFFFF'
```

## HEX_BLACK

```python
HEX_BLACK = '#000000'
```

## draw\_sv\_summary\_diagram()

this is the main drawing function. It decides between layouts
where each view-level is split into one or two diagrams (side-by-side)
dependant on whether the event is interchromosomal, within a single
transcript, etc.

Diagrams have four levels
- template
- gene
- transcript
- fusion transcript/translation

```python
def draw_sv_summary_diagram(
    config,
    ann,
    reference_genome=None,
    templates=None,
    ignore_absent_templates=True,
    user_friendly_labels=True,
    template_display_label_prefix='',
    draw_reference_transcripts=True,
    draw_reference_genes=True,
    draw_reference_templates=True,
    draw_fusion_transcript=True,
    stack_reference_transcripts=False,
):
```

**Args**

- config
- ann ([Annotation](../../annotate/variant/#class-annotation)): the annotation object to be illustrated
- reference_genome (`Dict[str,str]`): reference sequences
- templates (List\[[Template](../../annotate/genomic/#class-template)\]): list of templates, used in drawing the template-level view


- template_display_label_prefix (`str`): the character to precede the template label
- draw_reference_transcripts
- draw_reference_genes
- draw_reference_templates
- draw_fusion_transcript
- stack_reference_transcripts

