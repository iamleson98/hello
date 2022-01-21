#
# author: Le Van Son
# lvson1@cmcglobal.vn
#

from dataclasses import dataclass
import pandas as pd
import os.path
from typing import (
    Dict,
    List,
    Union,
    Optional,
)
import aws_config
import boto3

VALID_PANDAS_FILE_EXTENSIONS = [".csv", ".xlsx", ".xls", ".json"]
S3 = boto3.client('s3')


class FileNotFoundException(Exception):
    pass


def readExcelToDataframe(filePath: str, sheetName: Optional[List[str]] = None) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    readExcelToDataframe reads given file and returns a pandas DataFrame.
    """
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"file {filePath} does not exist")

    extension = os.path.splitext(filePath)[1]
    if extension not in [".xlsx", ".xls"]:
        raise Exception("invalid file type")

    return pd.read_excel(filePath, sheet_name=sheetName)


def readCsvToDataFrame(filePath: str) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"file {filePath} does not exist")

    extension = os.path.splitext(filePath)[1]
    if extension != ".csv":
        raise Exception("invalid file type")

    return pd.read_csv(filePath)
