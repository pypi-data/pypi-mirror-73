# json_context

Use JSON as context!

```python
from json_context import json_context

with json_context('cache.json') as cache:
	print(cache)
	... ... ...
	cache.write()
	... ... ...
```

`json_context` will read the specified JSON file and write the changes!

You can use `write()` to manually write the changes any time!
