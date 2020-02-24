import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore


cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()

def add_materia(materia):
    """
        des_horario_pratica: (string)
        des_horario_teoria: (string)
        nom_docente_pratica: (string)
        nom_docente_teoria: (string)
        nom_materia: (string)
        array_alunos_matriculados: (array(string))

    """

    fb_doc = store.collection(u'materias')
    fb_doc.add({u'cod_turma': materia['cod_turma'],
                u'des_horario_pratica': materia['pratica'],
                u'des_horario_teoria': materia['teoria'],
                u'nom_docente_pratica' : materia['docente_pratica'],
                u'nom_docente_teoria' : materia['docente_teoria'],
                u'nom_materia' : materia['nome_materia'],
                u'array_alunos_matriculados' : materia['alunos'],
                })

"""
doc_ref = store.collection(u'alunos')
try:
    docs = doc_ref.get()
    for doc in docs:
        print(u'Doc Data:{}'.format(doc.to_dict()))
except google.cloud.exceptions.NotFound:
    print(u'Missing data')

"""