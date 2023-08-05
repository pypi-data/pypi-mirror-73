# Logging extensions
![Upload Python Package](https://github.com/AlexXTW/logging_utils/workflows/Upload%20Python%20Package/badge.svg)

Utilities package for logging various entities.

## Installation
```{bash}
pip install logging-extensions
```

## Usage
```{python}
from logging_extensions.functions import log_function

@log_function
def hello_world():
  print("hello world!")
```
