# Cobertura Merge

Utility to merge multiple cobertura xml files into one.

- Input file are provided as variable number of command line arguments.
- Output file is provided using `--output` or `-o` argument or default to `coverage.xml`.

## Help Message

```
usage: cobertura-merge [-h] [--output coverage.xml] input.xml [input.xml ...]

Utility to merge multiple cobertura xml files into one.

positional arguments:
  input.xml             input cobertura xml to be merged

optional arguments:
  -h, --help            show this help message and exit
  --output coverage.xml, -o coverage.xml
                        output cobertura xml to be merged
```

## Road Map

- [x] Fix working directory.
- [ ] Add pre commit hooks.
- [ ] Add test cases.
- [ ] Add build pipeline.
- [ ] Publish to pypi via release pipeline ?
