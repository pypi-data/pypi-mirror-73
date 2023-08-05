# GhostPort Python SDK

## Installation

`pip install ghostport`

## Usage

### Initialize the Client

```python
from ghostport import GhostPort

client = GhostPort('YOUR_TOKEN')
```

### Get all keys and values

```python
flags = client.get_flag_values()

print(flags) # Prints out a dictionary of flag keys to values
```

### Get a flag's value

```python
value = client.get_flag_value('doTheThing')

print(value) # Prints out the value of the flag
```
