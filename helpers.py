import json

def write_json(data, filename): 
    with open(filename,'w', encoding='utf8') as f: 
        json.dump(data, f, ensure_ascii=False, indent=4) 

def append_result_json(aula):
    
    with open('aulas_json.json', encoding='utf8') as json_file: 
        aulas = json.load(json_file) 
        temp = aulas['aulas'] 
    
        temp.append(aula) 
      
    write_json(aulas, 'aulas_json.json')