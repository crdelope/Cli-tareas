"""Carga y validación de acciones.json."""

import json
import re
from pathlib import Path
from typing import Any

from tareas.errores import AccionNoValida, ConfigError

TIPOS_VALIDOS = {"mover", "copiar", "renombrar", "borrar"}
PATRON_NOMBRE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def cargar_acciones(ruta: str | Path) -> list[dict[str, Any]]:
    """Lee acciones.json, valida su contenido y devuelve la lista de acciones."""
    ruta = Path(ruta)
    if not ruta.is_file():
        raise ConfigError(f"No se encuentra el fichero {ruta.resolve()}")

    try:
        texto = ruta.read_text(encoding="utf-8")
    except OSError as error:
        raise ConfigError(f"No se puede leer {ruta}: {error}") from error

    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as error:
        raise ConfigError(
            f"El JSON de {ruta} no es válido "
            f"(línea {error.lineno}, columna {error.colno}): {error.msg}"
        ) from error

    if not isinstance(datos, dict):
        raise ConfigError("La raíz de acciones.json debe ser un objeto JSON")

    version = datos.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version != 1:
        raise ConfigError("El campo 'version' debe ser el número 1")

    acciones = datos.get("acciones")
    if not isinstance(acciones, list):
        raise ConfigError("El campo 'acciones' debe ser una lista")

    nombres_vistos: set[str] = set()
    for indice, accion in enumerate(acciones, start=1):
        _validar_accion(accion, indice, nombres_vistos)

    return acciones


def _validar_accion(accion: Any, indice: int, nombres_vistos: set[str]) -> None:
    if not isinstance(accion, dict):
        raise ConfigError(f"La acción número {indice} debe ser un objeto JSON")

    nombre = accion.get("nombre")
    referencia = nombre if isinstance(nombre, str) and nombre else f"número {indice}"

    if not isinstance(nombre, str) or not nombre:
        raise AccionNoValida(referencia, "nombre", "es obligatorio y debe ser texto")

    if not PATRON_NOMBRE.fullmatch(nombre):
        raise AccionNoValida(
            nombre,
            "nombre",
            "debe estar en minúsculas y usar solo guiones como separador",
        )

    if nombre in nombres_vistos:
        raise AccionNoValida(
            nombre, "nombre", "está repetido; los nombres deben ser únicos"
        )
    nombres_vistos.add(nombre)

    descripcion = accion.get("descripcion")
    if not isinstance(descripcion, str) or not descripcion.strip():
        raise AccionNoValida(
            nombre, "descripcion", "es obligatoria y debe ser un texto no vacío"
        )

    tipo = accion.get("tipo")
    if not isinstance(tipo, str) or tipo not in TIPOS_VALIDOS:
        raise AccionNoValida(
            nombre,
            "tipo",
            f"debe ser uno de: {', '.join(sorted(TIPOS_VALIDOS))}",
        )

    if tipo in {"mover", "copiar"}:
        _campo_texto_obligatorio(accion, nombre, "destino")

    if tipo == "renombrar":
        _campo_texto_obligatorio(accion, nombre, "plantilla")

    if tipo == "borrar" and "confirmar" in accion:
        if not isinstance(accion["confirmar"], bool):
            raise AccionNoValida(nombre, "confirmar", "debe ser true o false")

    if "filtro" in accion:
        _validar_filtro(accion["filtro"], nombre)


def _campo_texto_obligatorio(
    accion: dict[str, Any], nombre: str, campo: str
) -> None:
    valor = accion.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise AccionNoValida(
            nombre,
            campo,
            f"es obligatorio para el tipo '{accion.get('tipo')}' "
            "y debe ser un texto no vacío",
        )


def _validar_filtro(filtro: Any, nombre: str) -> None:
    if not isinstance(filtro, dict):
        raise AccionNoValida(nombre, "filtro", "debe ser un objeto JSON")

    if "extensiones" in filtro:
        extensiones = filtro["extensiones"]
        if not isinstance(extensiones, list):
            raise AccionNoValida(
                nombre, "filtro.extensiones", "debe ser una lista de textos"
            )
        for extension in extensiones:
            if (
                not isinstance(extension, str)
                or not extension.startswith(".")
                or len(extension) < 2
            ):
                raise AccionNoValida(
                    nombre,
                    "filtro.extensiones",
                    f"'{extension}' debe ser un texto que empiece por punto, "
                    "por ejemplo '.jpg'",
                )

    if "patron" in filtro:
        patron = filtro["patron"]
        if not isinstance(patron, str) or not patron:
            raise AccionNoValida(
                nombre, "filtro.patron", "debe ser una expresión regular no vacía"
            )
        try:
            re.compile(patron)
        except re.error as error:
            raise AccionNoValida(
                nombre,
                "filtro.patron",
                f"la expresión regular no es válida: {error}",
            ) from error

    for campo in ("mas_antiguo_que_dias", "mayor_que_mb"):
        if campo in filtro:
            valor = filtro[campo]
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                raise AccionNoValida(
                    nombre, f"filtro.{campo}", "debe ser un número"
                )
