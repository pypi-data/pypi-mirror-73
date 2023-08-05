# mavis.tools

## convert\_tool\_output()

Reads output from a given SV caller and converts to a set of MAVIS breakpoint pairs. Also collapses duplicates

```python
def convert_tool_output(
    fnames,
    file_type=SUPPORTED_TOOL.MAVIS,
    stranded=False,
    log=DEVNULL,
    collapse=True,
    assume_no_untemplated=True,
):
```

**Args**

- fnames
- file_type
- stranded
- log
- collapse
- assume_no_untemplated


