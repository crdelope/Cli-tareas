import json
from pathlib import Path
from typing import Any, Callable

import pytest

from tareas import ia
from tareas.errores import IANoDisponible

VARIABLES_IA = (
    "CENTRO_IA_URL",
    "CENTRO_IA_KEY",
    "CENTRO_IA_MODELO",
    "CENTRO_IA_CA",
)


class ProveedorFalso(ia.ProveedorIA):
    def __init__(
        self, texto: str = "resumen de prueba", fallar_en: int | None = None
    ) -> None:
        self.texto = texto
        self.fallar_en = fallar_en
        self.llamadas = 0

    def completar(
        self, sistema: str, usuario: str, max_tokens: int = 200
    ) -> ia.Respuesta:
        self.llamadas += 1
        if self.fallar_en == self.llamadas:
            raise IANoDisponible("Fallo simulado de la IA")
        return ia.Respuesta(self.texto)


@pytest.fixture(autouse=True)
def entorno_aislado(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    for variable in VARIABLES_IA:
        monkeypatch.delenv(variable, raising=False)
    monkeypatch.setattr(ia, "load_dotenv", lambda *_args, **_kwargs: False)


@pytest.fixture
def proveedor_falso() -> type[ProveedorFalso]:
    return ProveedorFalso


@pytest.fixture
def acciones_json() -> Callable[..., Path]:
    def escribir(datos: dict[str, Any] | None = None) -> Path:
        contenido = datos if datos is not None else {
            "version": 1,
            "acciones": [
                {
                    "nombre": "mover-prueba",
                    "descripcion": "Mueve archivos de prueba",
                    "tipo": "mover",
                    "destino": "~/destino",
                    "filtro": {"extensiones": [".txt"]},
                },
                {
                    "nombre": "resumir-prueba",
                    "descripcion": "Resume apuntes de prueba",
                    "tipo": "resumir",
                    "instrucciones": "Resume en una línea.",
                    "filtro": {"extensiones": [".txt"]},
                },
            ],
        }
        ruta = Path("acciones.json")
        ruta.write_text(
            json.dumps(contenido, ensure_ascii=False), encoding="utf-8"
        )
        return ruta

    return escribir
