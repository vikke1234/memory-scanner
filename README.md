# Memory scanner
With the help of this program you can scan and use the process 
of elimination to find a variable in memory.

### Python version
This has been tested with `python 3.9`, it will probably work with
an older one as long as it's above 3.5 due to the `typing` module. 
I do not guarantee it will work on anything below `3.9` though.

## Documentation
- [Project spec](documentation/project_spec.md)
- [Hours spent](documentation/hours_spent.md)
- [Architecture](documentation/architecture.md)

## Installation
1. Install dependencies
```shell
poetry install
```
2. Start the program with
```shell
poetry run invoke start
```

## Command line stuff
### Start
```shell
poetry run invoke start
```

### Testing
```shell
poetry run invoke test
```

### Coverage
```shell
poetry run invoke coverage
```

### Coverage report
```shell
poetry run invoke coverage-report
```