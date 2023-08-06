# Object File Handlers

A wrapper for writing simpler pickle code. save and load python objects in one line.

## To save a python object to file system.

```python
from OFHandlers import save_object, load_object

x=[i for i in range(4)]

#save object to local file system.
save_object(path="./x.file",object=x)

#load object to current python environment
x_loaded=load_object(path="./x.file")

```

## Installation 

```
pip install simpler-pickle
```