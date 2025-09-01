from dataclasses import dataclass
from pathlib import Path
import os, yaml
from dotenv import load_dotenv

@dataclass
class Settings:
    base_url: str
    api_url: str
    storage_state_path: str
    headless: bool

_cache = None

def load_settings(env: str = None) -> Settings:
    global _cache
    if _cache: return _cache
    load_dotenv()
    base = yaml.safe_load(Path("config/base.yaml").read_text())
    if env:
        envp = Path(f"config/{env}.yaml")
        if envp.exists():
            base = base | yaml.safe_load(envp.read_text())
    app = base["app"]; pw = base["playwright"]
    _cache = Settings(
        base_url=app["base_url"], api_url=app["api_url"],
        storage_state_path=pw["storage_state_path"], headless=pw["headless"],
    )
    return _cache