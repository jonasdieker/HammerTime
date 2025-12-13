import yaml
import os

def read_api_key():
    with open("secrets.yaml") as f:
        secrets = yaml.safe_load(f)
    os.environ["ANTHROPIC_API_KEY"] = secrets["claude_key"]