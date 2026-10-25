from app import db
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped
import enum

class StatusEnum(enum.Enum):
    EM_ESPERA = "Em espera"
    PROCESSANDO = "Processando"
    FINALIZADO = "Finalizado"


class Videos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(80), nullable=False)
    nome_arquivo: Mapped[str] = mapped_column(String(100), nullable=False)
    tamanho: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), default=StatusEnum.EM_ESPERA)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    def __init__(self, titulo, nome_arquivo, tamanho, user_id):
       self.titulo = titulo
       self.nome_arquivo = nome_arquivo
       self.tamanho = tamanho 
       self.user_id = user_id

class Usuarios(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    senha: Mapped[str] = mapped_column(String(255))
    limite: Mapped[int] = mapped_column(default=100)
    limite_usado: Mapped[int] = mapped_column(default=0)

    def __init__(self, nome: str, email: str, senha: str):
        self.nome = nome
        self.email = email
        self.senha = senha