"""Capa de acceso a un proveedor de IA."""

import os
from dataclasses import dataclass

import httpx
from dotenv import find_dotenv, load_dotenv

from tareas.errores import IANoDisponible

TIEMPO_MAXIMO = 30.0


@dataclass
class Respuesta:
    """Texto devuelto por el modelo."""

    texto: str


class ProveedorIA:
    """Interfaz común de los proveedores de IA."""

    def completar(
        self, sistema: str, usuario: str, max_tokens: int = 200
    ) -> Respuesta:
        """Devuelve la respuesta del modelo a una petición."""
        raise NotImplementedError


class ProveedorCentro(ProveedorIA):
    """Proveedor que habla con el servidor de IA del centro."""

    def __init__(self) -> None:
        load_dotenv(find_dotenv(usecwd=True))
        self.url = _variable("CENTRO_IA_URL").rstrip("/")
        self._clave = _variable("CENTRO_IA_KEY")
        self.modelo = _variable("CENTRO_IA_MODELO")

    def completar(
        self, sistema: str, usuario: str, max_tokens: int = 200
    ) -> Respuesta:
        datos = {
            "model": self.modelo,
            "messages": [
                {"role": "system", "content": sistema},
                {"role": "user", "content": usuario},
            ],
            "max_tokens": max_tokens,
        }
        cabeceras = {
            "Authorization": f"Bearer {self._clave}",
            "Content-Type": "application/json",
        }

        try:
            respuesta = httpx.post(
                f"{self.url}/chat/completions",
                headers=cabeceras,
                json=datos,
                timeout=TIEMPO_MAXIMO,
            )
        except httpx.TimeoutException as error:
            raise IANoDisponible(
                "El servidor de IA tarda demasiado en responder"
            ) from error
        except httpx.ConnectError as error:
            raise IANoDisponible(
                "No hay conexión con el servidor de IA"
            ) from error
        except httpx.HTTPError as error:
            raise IANoDisponible(
                "No se pudo contactar con el servidor de IA"
            ) from error

        if respuesta.status_code == 401:
            raise IANoDisponible("La clave de IA ha sido rechazada (401)")
        if respuesta.status_code == 429:
            raise IANoDisponible(
                "Hay demasiadas peticiones al servidor de IA (429); "
                "inténtalo más tarde"
            )
        if respuesta.status_code >= 400:
            raise IANoDisponible(
                "El servidor de IA devolvió un error "
                f"(código {respuesta.status_code})"
            )

        try:
            contenido = respuesta.json()["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError) as error:
            raise IANoDisponible(
                "El servidor de IA devolvió una respuesta no válida"
            ) from error

        if contenido is None:
            contenido = ""
        if not isinstance(contenido, str):
            raise IANoDisponible(
                "El servidor de IA devolvió una respuesta no válida"
            )

        return Respuesta(contenido)


def _variable(nombre: str) -> str:
    """Lee una variable de entorno obligatoria sin mostrar su valor."""
    valor = os.environ.get(nombre)
    if not valor:
        raise IANoDisponible(
            f"Falta la variable {nombre} en el archivo .env"
        )
    return valor
