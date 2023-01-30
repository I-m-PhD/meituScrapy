import pathlib
import pandas as pd


def process_csv():
    if pathlib.Path('mid.csv').exists():
        d = pd.read_csv('mid.csv', encoding='utf-8')
        nd = d.sort_values(by=['M.ID'], axis=0, ascending=False, inplace=False)
        nd.to_csv('mid_sorted.csv', index=False, header=True)
    else:
        print('CSV FILE NOT FOUND')


process_csv()
