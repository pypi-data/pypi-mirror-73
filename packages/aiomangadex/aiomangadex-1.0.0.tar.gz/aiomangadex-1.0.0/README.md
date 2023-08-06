# aiomangadex

[![Build Status](https://travis-ci.org/lukesaltweather/aiomangadex.svg?branch=master)](https://travis-ci.org/lukesaltweather/aiomangadex)
[![Documentation Status](https://readthedocs.org/projects/aiomangadex/badge/?version=latest)](https://aiomangadex.readthedocs.io/en/latest/?badge=latest)

An asynchronous API wrapper for mangadex.

  

# Basic Usage
```python
import aiomangadex
import aiohttp
import asyncio

async def fetch(id):
    session = aiohttp.ClientSession()
    manga = await aiomangadex.fetch_manga(id, session)
    await session.close()
    print(manga.description)

asyncio.get_event_loop().run_until_complete(fetch(34198))
```

### For more info, visit the docs [here.](https://aiomangadex.readthedocs.io)
