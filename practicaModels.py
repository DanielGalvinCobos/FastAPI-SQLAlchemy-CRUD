from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean
from practicaDatabase import Base

class Tarea(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None]
    completada: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"Tarea(id={self.id!r}, titulo={self.titulo!r}, completada={self.completada!r})"