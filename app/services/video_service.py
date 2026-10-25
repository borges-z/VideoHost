from app.modelos import Videos
from app import db, app
import os
from app.modelos import StatusEnum

def salvar_video(dados, titulo_string, titulo_original):
    dir = os.path.join(app.root_path, app.config['VIDEOS_FOLDER'], titulo_string)
    extensao = titulo_original.split('.')[-1]
    if not os.path.isfile(dir):
        os.makedirs(dir)
    dados.save(os.path.join(dir, f'ext.{extensao}'))

def tamanho_video(dados):
    dados.seek(0, 2) 
    tamanho_bytes = dados.tell()
    dados.seek(0)
    return tamanho_bytes

def verificar_arquivo(arquivo, nome):
    dir = os.path.join(app.root_path, app.config['VIDEOS_FOLDER'], arquivo, nome)
    if not os.path.isfile(dir):
        return False
    dir = os.path.join(app.root_path, app.config['VIDEOS_FOLDER'], arquivo)
    return dir

def registrar_video(titulo, nome_arquivo, tamanho, user_id):
    video = Videos(titulo, nome_arquivo, tamanho, user_id)
    db.session.add(video)
    db.session.commit()

def obter_todos_videos_usuario(id):
    return Videos.query.filter_by(user_id=id).all()

def buscar_video(cod):
    video = Videos.query.filter_by(nome_arquivo=cod, status=StatusEnum.FINALIZADO).first()
    if video:
        return os.path.join(app.config['VIDEOS_FOLDER'], video.nome_arquivo)
    return None