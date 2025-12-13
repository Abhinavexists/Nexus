import os
import yaml
import pickle
import numpy as np
from pathlib import Path

from src.exception.exception import CustomException
from src.logging.logging import logging


def read_yaml_file(file_path: Path) -> dict:
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise CustomException(e)


def write_yaml_file(file_path: Path, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if Path(file_path).exists():
                os.remove(file_path)
        p = Path(file_path).parent
        p.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)

    except Exception as e:
        raise CustomException(e)


def save_numpy_array_data(file_path: Path, array: np.ndarray):
    try:
        dir_path = Path(file_path).parent
        dir_path.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)

    except Exception as e:
        raise CustomException(e)
    

def load_numpy_array_data(file_path: Path):
    try:
        with open(file_path, 'rb') as file:
            return np.load(file)
    
    except Exception as e:
        raise CustomException(e)


def save_object(file_path: Path, obj: object):
    try:
        logging.info('Entered the save_object method of utils')

        dir_path = Path(file_path).parent
        dir_path.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)

        logging.info('Exited the save_object method of utils')

    except Exception as e:
        raise CustomException(e)


def load_object(file_path: Path):
    try:
        if not Path(file_path).exists():
            raise Exception(f"The file: {file_path} dosen't exist")
        with open(file_path, 'rb') as file_obj:
            print(file_obj)
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e)