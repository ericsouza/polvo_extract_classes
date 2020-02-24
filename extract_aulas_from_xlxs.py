#import polvo_firebase_connection as pfc

import pandas as pd

pd.set_option('display.max_columns', None)

df_2pdf = pd.read_excel('turmas_online2pdf.xlsx')

print(df_2pdf.head())