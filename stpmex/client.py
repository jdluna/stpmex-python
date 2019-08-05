from dataclasses import asdict

from OpenSSL import crypto
from zeep import Client as SoapClient

from .exc import InvalidPassphrase
from .orden import Orden

DEFAULT_WSDL = (
    'https://demo.stpmex.com:7024/speidemo/webservices/SpeiActualizaServices?'
    'wsdl'
)


class Client:
    def __init__(
        self,
        empresa: str,
        priv_key: str,
        priv_key_passphrase: str,
        prefijo: int,
        wsdl_path: str = DEFAULT_WSDL,
    ):
        self.empresa = empresa
        try:
            self._unencrypted_priv_key = crypto.load_privatekey(
                crypto.FILETYPE_PEM,
                priv_key,
                priv_key_passphrase.encode('ascii'),
            )
        except crypto.Error:
            raise InvalidPassphrase
        self.prefijo = prefijo
        self.soap_client = SoapClient(wsdl_path)

    def soap_orden(self, orden: Orden):
        SoapOrden = self.soap_client.get_type('ns0:ordenPagoWS')
        soap_orden = SoapOrden(**asdict(orden))
        soap_orden.empresa = self.empresa
        return soap_orden

    def registrar_orden(self, orden: Orden):
        SoapOrden = self.soap_client.get_type('ns0:ordenPagoWS')
        soap_orden = SoapOrden(**asdict(orden))
        soap_orden.empresa = self.empresa
        return self.soap_client.service['registraOrden'](soap_orden)
