"""Motor de ejecución de acciones sobre ficheros."""

import re
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from tareas.errores import TareasError


@dataclass
class Resultado:
    """Resultado de aplicar una acción a un archivo."""

    origen: Path
    destino: Path | None
    estado: str
    motivo: str = ""


def buscar_accion(acciones: list[dict[str, Any]], nombre: str) -> dict[str, Any]:
    """Devuelve la acción con ese nombre o lanza TareasError si no existe."""
    for accion in acciones:
        if accion.get("nombre") == nombre:
            return accion
    raise TareasError(
        f"No existe ninguna acción llamada '{nombre}' en acciones.json"
    )


def ejecutar(
    accion: dict[str, Any],
    carpeta: str | Path,
    simular: bool = False,
    preguntar: Callable[[str], bool] | None = None,
) -> list[Resultado]:
    """Aplica una acción de tipo mover a los archivos de una carpeta."""
    if accion.get("tipo") != "mover":
        raise TareasError(
            f"La acción '{accion.get('nombre', '')}' es de tipo "
            f"'{accion.get('tipo', '')}'; por ahora solo se puede ejecutar 'mover'"
        )

    origen = Path(carpeta).expanduser()
    if not origen.is_dir():
        raise TareasError(f"La carpeta {origen} no existe o no es una carpeta")

    destino_texto = accion.get("destino")
    if not isinstance(destino_texto, str) or not destino_texto:
        raise TareasError(
            f"La acción '{accion.get('nombre', '')}' no tiene un destino válido"
        )
    destino = Path(destino_texto).expanduser()
    if destino.exists() and not destino.is_dir():
        raise TareasError(f"El destino {destino} existe pero no es una carpeta")

    filtro = accion.get("filtro") or {}
    archivos = sorted(
        (
            ruta
            for ruta in origen.iterdir()
            if ruta.is_file() and _cumple_filtro(ruta, filtro)
        ),
        key=lambda ruta: ruta.name.lower(),
    )

    resultados: list[Resultado] = []
    nombres_usados: set[str] = set()

    for archivo in archivos:
        objetivo = destino / archivo.name

        if objetivo.exists() or objetivo.name in nombres_usados:
            libre = _nombre_libre(destino, archivo.name, nombres_usados)
            if simular:
                resultados.append(
                    Resultado(
                        archivo,
                        libre,
                        "simulado",
                        "ya existe en el destino; se renombraría",
                    )
                )
                nombres_usados.add(libre.name)
                continue

            mensaje = (
                f"Ya existe '{objetivo.name}' en {destino}. "
                f"¿Moverlo como '{libre.name}'?"
            )
            if preguntar is None or not preguntar(mensaje):
                resultados.append(
                    Resultado(
                        archivo,
                        None,
                        "saltado",
                        f"ya existe '{objetivo.name}' en el destino",
                    )
                )
                continue
            objetivo = libre

        if simular:
            resultados.append(Resultado(archivo, objetivo, "simulado"))
        else:
            destino.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(archivo), str(objetivo))
            except OSError as error:
                raise TareasError(
                    f"No se pudo mover {archivo}: {error}"
                ) from error
            resultados.append(Resultado(archivo, objetivo, "movido"))

        nombres_usados.add(objetivo.name)

    return resultados


def _cumple_filtro(archivo: Path, filtro: dict[str, Any]) -> bool:
    """Comprueba si un archivo cumple todos los criterios del filtro."""
    if not filtro:
        return True

    extensiones = filtro.get("extensiones")
    if extensiones is not None:
        permitidas = {extension.lower() for extension in extensiones}
        if archivo.suffix.lower() not in permitidas:
            return False

    patron = filtro.get("patron")
    if patron is not None and not re.search(patron, archivo.name):
        return False

    dias = filtro.get("mas_antiguo_que_dias")
    if dias is not None:
        edad_dias = (time.time() - archivo.stat().st_mtime) / 86400
        if edad_dias <= dias:
            return False

    mb = filtro.get("mayor_que_mb")
    if mb is not None:
        if archivo.stat().st_size <= mb * 1024 * 1024:
            return False

    return True


def _nombre_libre(destino: Path, nombre: str, usados: set[str]) -> Path:
    """Devuelve un nombre que no exista, añadiendo 1 antes de la extensión."""
    candidato = destino / nombre
    if not candidato.exists() and candidato.name not in usados:
        return candidato

    base = candidato.stem
    sufijo = candidato.suffix
    numero = 1
    while True:
        nuevo_nombre = f"{base}{'1' * numero}{sufijo}"
        candidato = destino / nuevo_nombre
        if not candidato.exists() and nuevo_nombre not in usados:
            return candidato
        numero += 1
