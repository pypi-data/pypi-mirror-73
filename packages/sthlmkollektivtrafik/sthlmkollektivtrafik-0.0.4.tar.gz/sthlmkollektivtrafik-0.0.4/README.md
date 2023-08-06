# sthlmkollektivtrafik


## Usage

### Platsuppslag
```python
from sthlmkollektivtrafik import platsuppslag

result = platsuppslag.search("apiKey", "searchStringy")

result.name
result.id
result.type

result.all
result.code
result.responses
result.stations
```

### Realtidsinformation
```python
from sthlmkollektivtrafik import realtidsinformation

result = realtidsinformation.departure("apiKey", "stationId", "timewindow")

result.trains
result.buses
result.metros

result.all
```

### Störningsinformation
```python
from sthlmkollektivtrafik import storningsinformation

result = realtidsinformation.departure("apiKey", "stationId")

result.all
result.headers
result.details
```