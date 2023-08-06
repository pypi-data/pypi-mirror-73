# stitch-api

Stitch python client library.

## Installation

`pip install stitch-api`

## pipenv

`pipenv install` uses the Pipefile to install package dependencies.

## Usage

Must get API key from Stitch Account
Basic API usage getting list of all Sources:

```python
from stitch_api.sources import Sources

client = Sources('your-stitch-application-api-token')
client.fetch_sources()
```