import polvo_firebase_connection as pfc
import pandas as pd

# this must be false so that the data can be saved in firestore
DEBUG = True

### FUNCTIONS

def create_class_students_dict(df):
    dic = {}
    ra_list = df['RA'].tolist()
    cod_turmas_list = df['COD. TURMA'].tolist()

    rows_number = df.shape[0]
    
    for i in range(rows_number):
        if cod_turmas_list[i] in dic:
            dic[cod_turmas_list[i]].append(ra_list[i])
        else:
            dic[cod_turmas_list[i]] = list()
            dic[cod_turmas_list[i]].append(ra_list[i])


    return dic

def create_students_classes_dataframe_from_xlsx(xlsx_file):
    labels = ['RA', 'COD. TURMA']
    df = pd.read_excel('students_classes.xlsx')

    df = df.rename(columns={'RA            disc.' : 'RA'})

    df.drop(df[(df[labels[0]] == 'RA            disc.') & (df[labels[1]] == labels[1])].index, inplace=True)
    df.reset_index(inplace=True)
    df = df.drop('index', 1)

    df = df.iloc[:,0:2]

    rows_number = df.shape[0]
    for i in range(rows_number):
        df.at[i, 'RA'] = df['RA'][i].split()[0]

    return df

def create_classes_dataframe_from_xlsx(xlsx_file):
    labels = ['Código', 'Disicplina - turma', 'teoria', 'prática', 'docente teoria', 'docente prática']
    df = pd.read_excel(xlsx_file)

    df.drop(df[(df[labels[0]] == labels[0]) & (df[labels[1]] == labels[1]) & (df[labels[5]] == labels[5])].index, inplace=True)
    df.reset_index(inplace=True)
    df = df.drop('index', 1)

    df.loc[df[labels[2]] == 0, labels[2]] = ''
    df.loc[df[labels[3]] == 0, labels[3]] = ''
    df.loc[df[labels[4]] == 0, labels[4]] = ''
    df.loc[df[labels[5]] == 0, labels[5]] = ''

    df = df.fillna('')

    return df

def get_missings_ra_list_in_classes(xlsx_file, classes_dict):
    df = create_classes_dataframe_from_xlsx(xlsx_file)

    number_of_classes = df.shape[0]
    missing_ras_list = []

    for i in range(number_of_classes):

        if not df['Código'][i] in classes_dict:
            missing_ras_list.append(df['Código'][i])

    return missing_ras_list

def insert_classes(xlsx_file, classes_dict):
    
    df = create_classes_dataframe_from_xlsx(xlsx_file)

    number_of_classes = df.shape[0]

    for i in range(number_of_classes):
        aux = i+1
        print(f'working: {aux} / {number_of_classes}')
        
        materia_dict = {
                'cod_materia' : df['Código'][i],
                'nome_materia' : df['Disicplina - turma'][i],
                'teoria' : df['teoria'][i],
                'pratica' : df['prática'][i],
                'docente_teoria' : df['docente teoria'][i] if df['teoria'][i] != '' else '',
                'docente_pratica' : df['docente prática'][i] if df['prática'][i] != '' else '',
                'alunos' : classes_dict[df['Código'][i]] if df['Código'][i] in classes_dict else list()
            }

        if not DEBUG:
            pfc.add_materia(materia_dict)


### SCRIPT

deferidas_df = create_students_classes_dataframe_from_xlsx('students_classes.xlsx')

classes_dict = create_class_students_dict(deferidas_df)

print('working in SA classes...')
insert_classes('turmas_sa.xlsx', classes_dict)

print('\nworking in SBC classes...')
insert_classes('turmas_sbc.xlsx', classes_dict)

# below it's printed out classes withou any student in both campus
missing_ras_list_sa = get_missings_ra_list_in_classes('turmas_sa.xlsx', classes_dict)
missing_ras_list_sbc = get_missings_ra_list_in_classes('turmas_sbc.xlsx', classes_dict)

print('\nthe following classes does not have any student in SA:')
for missing in missing_ras_list_sa:
    print(missing)

print('\nthe following classes does not have any student in SBC:')
for missing in missing_ras_list_sbc:
    print(missing)
