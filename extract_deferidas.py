import PyPDF2
import re
import firebase_python
import json
import helpers

ra_regex = re.compile(r"^\d{11}$|^\d{8}$")
turma_regex = re.compile(r".*-\d\d(SA|SB)$")
end_page_turmas_regex = re.compile(r"^\d{1,2}\s\/\s\d\d$")

def create_class_students_dict(input_ras, input_cod_turmas):
    ra_list = []
    cod_turmas_list = []

    with open(input_ras, 'r', encoding='utf-8') as file:
        ra_list = file.readlines()

    with open(input_cod_turmas, 'r', encoding='utf-8') as file:
        cod_turmas_list = file.readlines()

    dic = {}

    for i in range(len(ra_list)):
        ra_list[i] = ra_list[i].replace('\n', '')
    
    for i in range(len(cod_turmas_list)):
        cod_turmas_list[i] = cod_turmas_list[i].replace('\n', '')

    for i in range(len(cod_turmas_list)):
        if cod_turmas_list[i] in dic:
            dic[cod_turmas_list[i]].append(ra_list[i])
        else:
            dic[cod_turmas_list[i]] = list()
            dic[cod_turmas_list[i]].append(ra_list[i])

    with open('aulas.json', 'w', encoding='utf-8') as json_file:
        json.dump(dic, json_file, indent=4)

    return dic

def extract_turmas_from_txt(text_file='deferidas.txt'):
    turmas = []

    with open('deferidas.txt', 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
        
        for line in all_lines:
            if turma_regex.match(line):
                turmas.append(line)
    
    with open('lista_turmas.txt', 'w', encoding='utf-8') as file:
        file.writelines(turmas)


def extract_ra_from_txt(text_file='deferidas.txt'):
    
    ra_list = []

    with open('deferidas.txt', 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
        
        for line in all_lines:
            if ra_regex.match(line):
                ra_list.append(line)
    
    with open('lista_ra.txt', 'w', encoding='utf-8') as file:
        file.writelines(ra_list)

def extract_text_from_pdf(input_pdf, output_txt):
    pdf_file = open(input_pdf, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)

    number_of_pages = read_pdf.getNumPages()

    pdf_content = []

    for i in range(number_of_pages):
        print(f'appending page {i} of {number_of_pages}')
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        pdf_content.append(page_content)

    pdf_file.close()

    with open(output_txt, 'w', encoding='utf-8') as deferidas:   
        c = 1
        for page in pdf_content:
            print(f'page {c} of {number_of_pages}')
            deferidas.write(page)
            c+=1

def clean_page_header(input_file, output_file):
    document = []
    with open(input_file, 'r', encoding='utf-8') as file:
        document = file.readlines()

    cleaned_list = []

    i = 0
    while True:
        if turma_regex.match(document[i]):
            break
        else:
            i+=1


    document_size = len(document)
    while i < document_size:
        if end_page_turmas_regex.match(document[i]):
            i+=10
        else:
            cleaned_list.append(document[i])
            i+=1

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(cleaned_list)
    
def get_class_from_index(raw_list, indexes_list, index, aulas_com_ra_list):
    try:
        single_turma = "".join(raw_list[indexes_list[index]:indexes_list[index+1]])
    except IndexError:
        single_turma = "".join(raw_list[indexes_list[index]:])
    #print(single_turma)
    #single_turma = single_turma.replace('\n', ' ')
    #print('\n'+single_turma+'\n')
    
    init_turma = re.search(r'.*-\d\d(SA|SB)', single_turma).start()
    end_turma = re.search(r'.*-\d\d(SA|SB)', single_turma).end()
    cod_turma = single_turma[init_turma:end_turma]

    init_nome_turma = end_turma + 1
    end_nome_turma = single_turma.find(')') + 1
    nome_turma = single_turma[init_nome_turma:end_nome_turma].replace('\n', '')

    aula_init_pattern = r'segunda|terca|quarta|quinta|sexta|sabado'
    aula_end_pattern = r'semanal|quinzenal'

    aulas_teoria = []
    aulas_pratica = []

    string_search_aulas = single_turma

    while True:
        if not (re.search(aula_init_pattern, string_search_aulas)):
            break

        init_aula = re.search(aula_init_pattern, string_search_aulas).start()
        end_aula = re.search(aula_end_pattern, string_search_aulas).end()
        aula = string_search_aulas[init_aula:end_aula].replace('\n', '')
        if 'quinzenal II' in string_search_aulas[init_aula:end_aula+3]:
            aula += ' II'
            end_aula += 3
        elif 'quinzenal I' in string_search_aulas[init_aula:end_aula+3]:
            aula+= ' I'
            end_aula += 2

        aulas_pratica.append(aula) if 'Lab.' in aula else aulas_teoria.append(aula)
        string_search_aulas = string_search_aulas[end_aula:]

    docentes_list = string_search_aulas.lstrip().splitlines()

    docente_teoria = ''
    docente_pratica = ''

    if (len(aulas_teoria) != 0 and len(aulas_pratica) != 0):
        #print('tem aula teoria e tbm aula pratica')

        while len(docentes_list) > 2:
            docentes_list.remove(min(docentes_list, key=len))
        try:
            docente_teoria = docentes_list[0]
        except:
            pass
        try:    
            docente_pratica = docentes_list[1]
        except:
            pass

    else:
        if (len(aulas_pratica) == 0):
            docente_teoria = max(docentes_list, key=len)

        if (len(aulas_teoria) == 0):
            docente_pratica = max(docentes_list, key=len)

    """
    print('codigo: '+cod_turma)
    print('classe: '+nome_turma)
    print('teoria: ', end='')
    print(aulas_teoria)
    print('pratica: ', end='')
    print(aulas_pratica)
    print('docenteTeoria: ' + docente_teoria)
    print('docentePratica: ' + docente_pratica)
    """

    teoria = ",".join(aulas_teoria)
    pratica = ",".join(aulas_pratica)

    lista_ras_aula = []
    if cod_turma in aulas_com_ra_list:
        lista_ras_aula = aulas_com_ra_list[cod_turma]

    materia_dict = {
        'cod_turma' : cod_turma,
        'nome_materia' : nome_turma,
        'teoria' : teoria,
        'pratica' : pratica,
        'docente_teoria' : docente_teoria,
        'docente_pratica' : docente_pratica,
        'alunos' : lista_ras_aula
    }

    return materia_dict

    #print('oq sobrou: ' + docentes)
    
def treat_aulas(input, output):
    all_lines = []
    with open(input, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
    
    indexes = []

    for i in range(len(all_lines)):
        if turma_regex.match(all_lines[i]):
            indexes.append(i)

    aulas_com_ra_list = create_class_students_dict('lista_ra.txt', 'lista_turmas.txt')

    #materia_dict = get_class_from_index(all_lines, indexes, 0, aulas_com_ra_list)
    
    indexes_size = len(indexes)
    for i in range(len(indexes)):
        aux = i+1
        print(f'working: {aux} / {indexes_size}')
        materia_dict = get_class_from_index(all_lines, indexes, i, aulas_com_ra_list)
        
        helpers.append_result_json(materia_dict)

        #firebase_python.add_materia(materia_dict)
    
    """
    for i in range(len(indexes)):
        all_lines[indexes[i]]
    


    with open(output, 'w', encoding='utf-8') as file:
        file.writelines(indexes)
    """

#extract_text_from_pdf('deferidas.pdf', 'deferidas.txt')

#extract_ra_from_txt()
#extract_turmas_from_txt()

#extract_text_from_pdf('turmas.pdf', 'turmas_raw.txt')

#clean_page_header('turmas_raw.txt', 'turmas.txt')

#treat_aulas('turmas.txt', 'treated_aulas.txt')
#treat_aulas('turmas_cleaned_header_debugging.txt', 'treated_aulas.txt')

