# HP Spectre x360 pen

hps360pen is a sample tool to map HP Spectre x360 ap00xxxx stock pen buttons.

For now, only the pen's bottom button is supported and is mapped to emulate the right mouse button.

# Quick start

Install hps360pen using pip

```shell script
pip install hps360pen
```

At the console, start hps360pen

```shell script
hps360pen
```

By default, hps360pen try to use the ELAN PEN event device. If it fails, you can
try to list available evdev and choose the right device.

```shell script
hps360pen --list
```

# Credits

This sample tool use [evdev](https://pypi.org/project/evdev/) and [click](https://pypi.org/project/click/).