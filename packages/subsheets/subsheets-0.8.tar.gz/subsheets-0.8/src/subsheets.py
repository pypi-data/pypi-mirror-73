import os
import sys
import glob

import click
import pandas as pd

from .printing import splash_screen
from .prompt import main_menu_prompt


csv_sheets = []
xlsx_sheets = []


def get_csv_df(files):
    for file in files:
        csv_sheets.append(str(file))
        yield pd.read_csv(file)


def get_xlsx_df(files):
    for file in files:
        xlsx_sheets.append(str(file))
        yield pd.read_excel(file)

@click.command()
@click.option('-n', '--name', prompt=True)
def excel_to_subsheets(name):
    name = name + ".xlsx"
    writer = pd.ExcelWriter(name, engine='xlsxwriter')

    user_input = input("Enter the path of directory which contains files: ")
    if os.path.isdir(user_input):
        os.chdir(user_input)
    else:
        print("Directory does not exists.")
    
    csv_files = glob.glob('*.csv')
    xlsx_files = glob.glob('*.xls')
    xlsx_files.extend(glob.glob('*.xlsx'))

    df_for_each_csv_file = get_csv_df(csv_files)
    df_for_each_xlsx_file = get_xlsx_df(xlsx_files)

    for idx, df in enumerate(df_for_each_csv_file):
        df.to_excel(writer, sheet_name='{0}'.format(csv_sheets[idx]))

    for idx, df in enumerate(df_for_each_xlsx_file):
        df.to_excel(writer, sheet_name='{0}'.format(xlsx_sheets[idx]))

    writer.save()


@click.command()
@click.option('-i', '--input', prompt=True, type=click.File('rb'))
def subsheets_to_excel(input):
    xls = pd.ExcelFile(input)
    sheet_to_df_map = {}
    df = pd.DataFrame()
    for sheet_name in xls.sheet_names:
        if sheet_name.endswith('.csv'):
            sheet = xls.parse(sheet_name)
            sheet.to_csv(sheet_name, index=False)
        elif sheet_name.endswith('.xls') or sheet_name.endswith('.xlsx'):
            writer = pd.ExcelWriter(sheet_name, engine='xlsxwriter')
            sheet = xls.parse(sheet_name)
            sheet.to_excel(writer, sheet_name='{0}'.format(sheet_name))
            writer.save()


@click.command()
@click.option('-no-splash',
              is_flag=True,
              default=False,
              help="Don't display splash screen")
def main(no_splash):
    if not no_splash:
        splash_screen()

    selection = main_menu_prompt().lower().strip()
    if selection.startswith("1."):
        print('Excels to subsheets')
        excel_to_subsheets()
    elif selection.startswith("2."):
        print('subsheets in a excel to excel files')
        subsheets_to_excel()


if __name__ == '__main__':
    main()