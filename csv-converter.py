import pandas as pd
import glob
import os


def get_and_convert_files():
    path = os.getcwd()  # get filepath
    csv_files = glob.glob(os.path.join(path, "*.csv"))  # collect all csv files
    # read every csv files, read all columns in float format rename columns
    # because column's name can be random, but end of the name always stand
    # constant
    for f in csv_files:
        csv_input = pd.read_csv(f, sep=',', header=0, index_col=False,
                                decimal=',')
        cols = csv_input.columns
        flag = 0
        for col in cols:
            csv_input[col] = csv_input[col].astype(float)
            if '.w' in col or ',w' in col:
                csv_input.rename(
                    columns={f'{col}': 'v/n'},
                    inplace=True
                )
            elif '.tau' in col or ',tau' in col:
                csv_input.rename(
                    columns={col: 'F/T'},
                    inplace=True
                )
            elif 'f[3]' in col:
                csv_input.rename(
                    columns={col: 'Fax'},
                    inplace=True
                )
            if 'f[1]' in col:
                frame_1 = col
            if 'f[2]' in col:
                frame_2 = col
            if 'Fq' in col:
                flag = 1  # prepare to use flag, cause in initial files can be
                # with another pre-calculated column with that name
        csv_input.rename(columns={'time': 't'}, inplace=True)
        csv_input.insert(3, 'm/J', '0.00000000000000')
        # calculate new column with help of other columns
        if flag == 0:
            csv_input.insert(
                4,
                'Fq',
                (csv_input[f'{frame_1}'] ** 2 + csv_input[
                    f'{frame_2}'] ** 2) ** 0.5)
        # drop columns because they are not needed in other program
        csv_input.drop(columns=[frame_1, frame_2], axis=1, inplace=True)
        # delete Unnamed columns if they appeared
        csv_input = csv_input.loc[
                    :, ~csv_input.columns.str.contains('^Unnamed')
                    ]
        # correct positions of columns in csv file
        csv_input = csv_input[['t', 'v/n', 'F/T', 'm/J', 'Fq', 'Fax']]
        # write file with csv name and with txt extension
        csv_input.to_csv(f'{f}.txt', sep="\t", index=False,
                         float_format='%.14f')


if __name__ == '__main__':
    get_and_convert_files()
