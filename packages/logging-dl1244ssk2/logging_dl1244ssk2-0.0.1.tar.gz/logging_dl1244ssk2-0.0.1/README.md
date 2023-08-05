# Logging utilities
![Upload Python Package](https://github.com/AlexXTW/logging_utils/workflows/Upload%20Python%20Package/badge.svg)

Utilities package for logging various entities.

## Installation
```{bash}
pip install logging_utils
```

## Usage
```{python}
from logging_utils.functions import log_function

@log_function
def hello_world():
  print("hello world!")
```
