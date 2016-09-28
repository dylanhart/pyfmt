# pyfmt

A [Jupyter Notebook][1] magic to embed syntax highlighted parts of python files.

[1]: http://jupyter.org/

## Usage

usage: `%pyfmt [<selection>[,...]] <file>`

### Selection Syntax

|type|syntax|
|-|-|
|region|`r<region-name>`|
|lines|`l<start>:<end>`|


### example cell

```
import pyfmt
%pyfmt rmyregion code.py
```

