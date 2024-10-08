"""
Permisos v4, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import MyIsDeletedError, MyNotExistsError
from hercules.core.permisos.models import Permiso
from hercules.v4.modulos.crud import get_modulo
from hercules.v4.roles.crud import get_rol


def get_permisos(
    database: Session,
    modulo_id: int = None,
    rol_id: int = None,
) -> Any:
    """Consultar los permisos activos"""
    consulta = database.query(Permiso)
    if modulo_id is not None:
        modulo = get_modulo(database, modulo_id)
        consulta = consulta.filter_by(modulo_id=modulo.id)
    if rol_id is not None:
        rol = get_rol(database, rol_id)
        consulta = consulta.filter_by(rol_id=rol.id)
    return consulta.filter_by(estatus="A").order_by(Permiso.id.desc())


def get_permiso(database: Session, permiso_id: int) -> Permiso:
    """Consultar un permiso por su id"""
    permiso = database.query(Permiso).get(permiso_id)
    if permiso is None:
        raise MyNotExistsError("No existe ese permiso")
    if permiso.estatus != "A":
        raise MyIsDeletedError("No es activo ese permiso, está eliminado")
    return permiso
