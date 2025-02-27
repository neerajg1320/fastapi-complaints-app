import sqlalchemy
from db import metadata
from models.enums import ComplaintState


complaint = sqlalchemy.Table(
    "complaints",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("photo_url", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("amount", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column(
        "created_at", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()
    ),
    sqlalchemy.Column(
        "status",
        sqlalchemy.Enum(ComplaintState),
        nullable=False,
        server_default=ComplaintState.pending.name,
    ),
    sqlalchemy.Column(
        "complainer_id", sqlalchemy.ForeignKey("users.id"), nullable=False
    ),
)
