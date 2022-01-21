#
# Author: le Van Son, lvson1@cmcglobal.vn
#
from ctypes import Union
import sys
from typing import Any, Dict
import pandas as pd
import utils
import mapping
import numpy as np


def createPivotTable(df: pd.DataFrame, dfFrameType: str) -> pd.DataFrame:
    """:dfFrameType must be 'nissan' or 'falcon'"""

    values: str = ""
    index: list[str] = []

    if dfFrameType == "nissan":
        values = "ContractQuantity"
        index = ["ProductCode", "ContractMonth", "Account"]
    else:
        values = "Quantity"
        index = ["Account Number", "Contract Ticker"]

    return pd.pivot_table(df, values=values, index=index, aggfunc=np.sum)


def transform(productCode: str, contractMonth: str) -> str:
    cor = mapping.MAPPING_DATA[str(productCode)]
    return f"F-XOSE-{cor}-{contractMonth}"

def export():
    pass

def compare(falconDf: pd.DataFrame, contractTicker: str, accountNumber: str):
    df: pd.DataFrame = falconDf[falconDf["Contract Ticker"].str.endswith(
        contractTicker)]
    anotherDf: pd.DataFrame = df[df["Account Number"].str.endswith(str(accountNumber))]
    try:
        return anotherDf["Quantity"].sum()
    except:
        return 0


def main():
    fileList = sys.argv[1:]

    nissanFile: str = ""
    falconFile: str = ""

    if len(fileList) != 2:
        raise Exception("You must provide both nissan and falcon files")

    if "Futures Options Position" in fileList[0]:
        falconFile, nissanFile = fileList
    else:
        nissanFile, falconFile = fileList

    nissanDf: Union[pd.DataFrame, Dict[str, pd.DataFrame]] = None
    falconDf: Union[pd.DataFrame, Dict[str, pd.DataFrame]] = None

    try:
        nissanDf = utils.readCsvToDataFrame(nissanFile) if \
            nissanFile.endswith(".csv") else \
            utils.readExcelToDataframe(nissanFile)
    except Exception as e:
        print(e)
        return
    else:
        if isinstance(nissanDf, dict):
            nissanDf: pd.DataFrame = list(nissanDf.items())[0][1]

    try:
        falconDf: pd.DataFrame = utils.readCsvToDataFrame(falconFile) if \
            falconFile.endswith(".csv") else \
            utils.readExcelToDataframe(falconFile)
    except Exception as e:
        print(e)
        return
    else:
        if isinstance(falconDf, dict):
            falconDf = list(falconDf.items())[0][1]

    nissanPivot = createPivotTable(nissanDf, "nissan")
    falconPivot = createPivotTable(falconDf, "falcon")

    nissanPivot.reset_index(inplace=True)
    falconPivot.reset_index(inplace=True)

    nissanPivot["Contract Ticker"] = list(
        map(transform, nissanPivot["ProductCode"], nissanPivot["ContractMonth"]))
    nissanPivot["SumOfQuantity"] = list(map(lambda x, y: compare(
        falconPivot, x, y), nissanPivot["Contract Ticker"], nissanPivot["Account"]))

    nissanPivot["Comparision"] = nissanPivot["SumOfQuantity"] + nissanPivot["ContractQuantity"]

    misMatchDf = nissanPivot[nissanPivot["Comparision"] != 0]
    
    print(misMatchDf)

if __name__ == "__main__":
    main()
