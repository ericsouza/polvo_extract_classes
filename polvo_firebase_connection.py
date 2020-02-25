import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
fb_doc_materias = store.collection(u'materias')

def add_materia(materia):

    fb_doc_materias.add({u'cod_materia': materia['cod_materia'],
                u'des_horario_pratica': materia['pratica'],
                u'des_horario_teoria': materia['teoria'],
                u'nom_docente_pratica' : materia['docente_pratica'],
                u'nom_docente_teoria' : materia['docente_teoria'],
                u'nom_materia' : materia['nome_materia'],
                u'array_alunos_matriculados' : materia['alunos'],
                })
