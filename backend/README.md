# Just mocking the backend for now


You can get the initial AI response to the user input like so:

```python
import requests

response = requests.post(
    "http://localhost:8000/receive_user_prompt",
    json={"prompt": "I need steel beams for construction"}
)
print(response.json())
```