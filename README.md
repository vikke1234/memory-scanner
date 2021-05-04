# Memory scanner
With the help of this program you can scan and use the process 
of elimination to find a variable in memory.

[Latest release](https://github.com/vikke1234/ot-project/releases/tag/v0.2.0)

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
2. ***NOTE*** this step is required IF you don't wish to execute as root
```shell
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope
```
It will configure the system so that you're allowed to read from another processes' memory.
If you do not do this you will need to run the program as root. It will reset if you reboot
your machine, you can look [here](https://unix.stackexchange.com/questions/329504/proc-sys-kernel-yama-ptrace-scope-keeps-resetting-to-1)
for more information as to how to have it persistent. You can read more about `ptrace_scope`
[here](https://www.kernel.org/doc/Documentation/security/Yama.txt).

TL;DR if it's 0, you allow any process to read anothers memory. 1 the process must have
a predefined relationship with an inferior process. 2. admin only, 3. no process may
read anothers memory.

If you wish to disable the `ptrace_scope` you may simply execute the following command.
```shell
echo 2 | sudo tee /proc/sys/kernel/yama/ptrace_scope
```

Which will essetially require sudo access once again to read from another process. Another
reasonable one is also `1`, if you place `3` into the file you can't use e.g. `gdb` since it
works via it.


3. Start the program with
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

### Lint
```shell
poetry run invoke lint
```

### Freeze
```shell
poetry run invoke freeze
```