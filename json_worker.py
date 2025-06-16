import json
from pathlib import Path

from data.logger import Logger

logger = Logger(__name__) 

def load_json(name):
    input_path = Path(f"data/json/{name}.json")
    
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"Loaded {name} from {input_path}")
        return data
    except FileNotFoundError:
        logger.warning(f"File {input_path} not found!")
        return None
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in {input_path}!")
        return None


def save_json(name, file):
    output_path = Path(f"data/json/{name}.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(file, f, ensure_ascii=False, indent=4)
    
    logger.info(f"Saved {name} to {output_path}")
