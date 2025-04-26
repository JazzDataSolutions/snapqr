# backend/app/models.py
from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

class FotoUsuarioLink(SQLModel, table=True):
    foto_id: int = Field(foreign_key="foto_evento.id", primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", primary_key=True)

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(unique=True, nullable=False))
    nombre: str
    foto_perfil_url: Optional[str] = None

    credencial: Optional["Credencial"] = Relationship(back_populates="usuario", sa_relationship_kwargs={"uselist":False})
    fotos_evento: List["FotoEvento"] = Relationship(back_populates="usuarios", link_model=FotoUsuarioLink)

class Credencial(SQLModel, table=True):
    usuario_id: int = Field(foreign_key="usuario.id", primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    usuario: Usuario = Relationship(back_populates="credencial")

class FotoEvento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    s3_key: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    procesada: bool = Field(default=False)

    usuarios: List[Usuario] = Relationship(back_populates="fotos_evento", link_model=FotoUsuarioLink)

class Embedding(SQLModel, table=True):
    __tablename__ = "embedding"
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", nullable=False)
    vector: List[float] = Field(
        default_factory=list,
        sa_column=Column(JSONB, nullable=False)
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)


class QRContacto(SQLModel, table=True):
    __tablename__ = "qr_contacto"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    usuario_id: int = Field(foreign_key="usuario.id", nullable=False)
    qr_data: dict = Field(
        sa_column=Column("qr_data", JSONB, nullable=False)
    )
    qr_url: str = Field(nullable=False)
    generado_en: datetime = Field(default_factory=datetime.utcnow)

    # Relación inversa al modelo Usuario
    usuario: "Usuario" = Relationship(back_populates="qr_contactos")
