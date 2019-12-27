import datetime as dt
from typing import Any, Dict, Optional

from pydantic import conint, constr
from pydantic.dataclasses import dataclass

from ..auth import CUENTA_FIELDNAMES, compute_signature, join_fields
from ..types import digits, truncated_str
from .base import Resource


@dataclass
class Cuenta(Resource):
    """
    Based on:
    https://stpmex.zendesk.com/hc/es/articles/360038242071-Registro-de-Cuentas-de-Personas-f%C3%ADsicas
    """

    _endpoint = '/cuentaModule'

    nombre: truncated_str(50)
    apellidoPaterno: truncated_str(50)
    cuenta: digits(18, 18)
    rfcCurp: digits(max_length=18)

    apellidoMaterno: Optional[truncated_str(50)] = None
    genero: Optional[constr(regex=r'H|M')] = None
    fechaNacimiento: Optional[dt.date] = None
    # Not including Nacido en Extranjero is discrimination!
    entidadFederitva: Optional[conint(ge=1, le=32)] = None
    actividadEconimica: Optional[conint(ge=28, le=74)] = None
    calle: Optional[truncated_str(60)] = None
    # Hmmm ... should REALLY support alphanumeric
    numExterior: Optional[digits(max_length=10)] = None
    numInterior: Optional[digits(max_length=5)] = None
    colonia: Optional[truncated_str(50)] = None
    alcaldiaMunicipio: Optional[truncated_str(50)] = None
    codigoPostal: Optional[digits(5, 5)] = None
    paisNacimiento: Optional[conint(ge=1, lt=242)] = None
    email: Optional[constr(max_length=150)] = None
    idIdentificacion: Optional[digits(max_length=20)] = None
    telefono: Optional[digits(max_length=10)] = None

    @property
    def firma(self):
        joined_fields = join_fields(self, CUENTA_FIELDNAMES)
        return compute_signature(self._client.pkey, joined_fields)

    def _alta_fisica(self) -> Dict[str, Any]:
        ...
