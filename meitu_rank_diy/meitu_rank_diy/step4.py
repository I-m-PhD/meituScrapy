import pathlib
import pandas as pd


def process_csv2():
    if pathlib.Path('model.csv').exists():
        d = pd.read_csv('model.csv', encoding='utf-8')
        nd = d.sort_values(by=['M.SCORE'], axis=0, ascending=False, inplace=False)
        nd.to_csv('model_sorted.csv', index=False, header=True)
    else:
        print('CSV FILE NOT FOUND')


process_csv2()
