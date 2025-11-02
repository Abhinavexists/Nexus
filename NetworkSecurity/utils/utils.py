import os
import sys
import yaml
import pickle
from pathlib import Path

from NetworkSecurity.exception.exception import CustomException
from NetworkSecurity.logging.logging import logging

def read_yaml_file(file_path: Path):
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomException(e)
    
def write_yaml_file(file_path: Path, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if Path(file_path).exists:
                os.remove(file_path)
        p = Path(file_path).parent
        p.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)

    except Exception as e:
        raise CustomException(e)