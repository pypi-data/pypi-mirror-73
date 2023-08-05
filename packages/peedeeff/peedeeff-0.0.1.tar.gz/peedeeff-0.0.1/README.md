# Py Peedeeff
`python` client for peedeeff

## Usage

```python
from peedeeff import Peedeeff

r = Peedeeff.get_pdf(apiKey='yourapikey', html = '<h1>Hello World</h1>', 
    pageConfig={
        'size':'A4', 
        'printBackground': True,
        'margin': { 
            'top': '1cm', 
            'right': '1cm', 
            'bottom': '1cm', 
            'left': '1cm' 
            }
        }) 

r.status

pdf =r.content

```

Copyright Peedeeff All rights reserved