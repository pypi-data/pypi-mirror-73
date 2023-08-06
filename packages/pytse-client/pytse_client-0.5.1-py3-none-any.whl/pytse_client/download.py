from concurrent.futures.thread import ThreadPoolExecutor
from io import StringIO
from pathlib import Path
from typing import List, Union

import pandas as pd
from requests import HTTPError
import jdatetime

from pytse_client import config, symbols_data, tse_settings
from pytse_client.utils import requests_retry_session


def download(
        symbols: Union[List, str],
        write_to_csv: bool = False,
        include_jdate: bool = False,
        base_path: str = config.DATA_BASE_PATH):
    if symbols == "all":
        symbols = symbols_data.all_symbols()
    elif isinstance(symbols, str):
        symbols = [symbols]

    df_list = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        for symbol in symbols:
            ticker_index = symbols_data.get_ticker_index(symbol)
            if ticker_index is None:
                ticker_index = get_symbol_id(symbol)
                if ticker_index is None:
                    raise Exception("Can not found ticker name")
                else:
                    symbols_data.append_symbol_to_file(ticker_index, symbol)

            future = executor.submit(
                download_ticker_daily_record,
                ticker_index
            )
            df: pd.DataFrame = future.result()
            if df.shape[0] == 0:
                continue
            df = df.iloc[::-1]
            df = df.rename(
                columns=FIELD_MAPPINGS
            )
            df = df.drop(columns=["<PER>", "<OPEN>", "<TICKER>"])
            df.date = pd.to_datetime(df.date, format="%Y%m%d")
            if include_jdate:
                df['jdate'] = ""
                df.jdate = df.date.apply(
                    lambda gregorian:
                    jdatetime.date.fromgregorian(date=gregorian))
            df.set_index("date", inplace=True)
            df_list[symbol] = df

            if write_to_csv:
                Path(base_path).mkdir(parents=True, exist_ok=True)
                df.to_csv(
                    f'{base_path}/{symbol}.csv')

    if len(df_list) != len(symbols):
        print("Warning, download did not complete, re-run the code")
    return df_list


def download_ticker_daily_record(ticker_index: str):
    url = tse_settings.TSE_TICKER_EXPORT_DATA_ADDRESS.format(ticker_index)
    response = requests_retry_session().get(url, timeout=10)
    try:
        response.raise_for_status()
    except HTTPError:
        return download_ticker_daily_record(ticker_index)

    data = StringIO(response.text)
    return pd.read_csv(data)


def to_arabic(string: str):
    return string.replace('ک', 'ك').replace('ی', 'ي').strip()


def get_symbol_id(symbol_name: str):
    url = tse_settings.TSE_SYMBOL_ID_URL.format(symbol_name.strip())
    response = requests_retry_session().get(url, timeout=10)
    try:
        response.raise_for_status()
    except HTTPError:
        raise Exception("Sorry, tse server did not respond")

    symbol_full_info = response.text.split(';')[0].split(',')
    if(to_arabic(symbol_name) == symbol_full_info[0].strip()):
        return symbol_full_info[2]  # symbol id
    return None


FIELD_MAPPINGS = {
    "<DTYYYYMMDD>": "date",
    "<FIRST>": "open",
    "<HIGH>": "high",
    "<LOW>": "low",
    "<LAST>": "close",
    "<VOL>": "volume",
    "<CLOSE>": "adjClose",
    "<OPENINT>": "count",
    "<VALUE>": "value"
}
