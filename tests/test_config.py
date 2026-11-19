import json
from pathlib import Path
from typing import Any

import pytest

from tareas.config import cargar_acciones
from tareas.errores import TareasError

CASOS_VALIDOS = [
    pytest.param(
        {
            "nombre": "mover-valido",
            "descripcion": "Mueve fotos",
            "tipo": "mover",
            "destino": "~/destino",
            "filtro": {"extensiones": [".jpg"]},
        },
        id="mover-valido",
    ),
    pytest.param(
        {
            "nombre": "renombrar-valido",
            "descripcion": "Renombra fotos",
            "tipo": "renombrar",
            "plantilla": "foto-{n:03}{ext}",
            "filtro": {"extensiones": [".jpg"]},
        },
        id="renombrar-valido",
    ),
    pytest.param(
        {
            "nombre": "borrar-valido",
            "descripcion": "Borra temporales",
            "tipo": "borrar",
            "filtro": {"extensiones": [".tmp"]},
            "confirmar": True,
        },
        id="borrar-valido",
    ),
    pytest.param(
        {
            "nombre": "resumir-valido",
            "descripcion": "Resume apuntes",
            "tipo": "resumir",
            "instrucciones": "Resume en cinco líneas.",
            "max_caracteres": 500,
        },
        id="resumir-valido",
    ),
    pytest.param(
        {
            "nombre": "clasificar-valido",
            "descripcion": "Clasifica apuntes",
            "tipo": "clasificar",
            "categorias": ["trabajo", "otros"],
            "instrucciones": "Clasifica el texto.",
            "max_caracteres": 500,
        },
        id="clasificar-valido",
    ),
]

CASOS_INVALIDOS = [
    pytest.param(
        {
            "nombre": "mover-invalido",
            "descripcion": "Mueve fotos",
            "tipo": "mover",
        },
        "destino",
        id="mover-sin-destino",
    ),
    pytest.param(
        {
            "nombre": "renombrar-invalido",
            "descripcion": "Renombra fotos",
            "tipo": "renombrar",
        },
        "plantilla",
        id="renombrar-sin-plantilla",
    ),
    pytest.param(
        {
            "nombre": "borrar-invalido",
            "descripcion": "Borra temporales",
            "tipo": "borrar",
            "filtro": {"extensiones": [".tmp"]},
            "confirmar": "si",
        },
        "confirmar",
        id="borrar-confirmar-no-booleano",
    ),
    pytest.param(
        {
            "nombre": "resumir-invalido",
            "descripcion": "Resume apuntes",
            "tipo": "resumir",
            "instrucciones": "   ",
        },
        "instrucciones",
        id="resumir-instrucciones-vacias",
    ),
    pytest.param(
        {
            "nombre": "clasificar-invalido",
            "descripcion": "Clasifica apuntes",
            "tipo": "clasificar",
            "categorias": ["trabajo", "ocio"],
        },
        "categorias",
        id="clasificar-sin-otros",
    ),
]


def escribir_config(datos: dict[str, Any]) -> Path:
    ruta = Path("acciones.json")
    ruta.write_text(
        json.dumps(datos, ensure_ascii=False), encoding="utf-8"
    )
    return ruta


@pytest.mark.parametrize("accion", CASOS_VALIDOS)
def test_config_acepta_acciones_validas_de_cada_tipo(
    accion: dict[str, Any],
) -> None:
    ruta = escribir_config({"version": 1, "acciones": [accion]})

    assert cargar_acciones(ruta) == [accion]


@pytest.mark.parametrize(("accion", "campo"), CASOS_INVALIDOS)
def test_config_rechaza_acciones_invalidas_con_codigo_3(
    accion: dict[str, Any], campo: str
) -> None:
    ruta = escribir_config({"version": 1, "acciones": [accion]})

    with pytest.raises(TareasError) as info:
        cargar_acciones(ruta)

    assert info.value.codigo == 3
    assert accion["nombre"] in str(info.value)
    assert campo in str(info.value)


@pytest.mark.parametrize(
    ("datos", "campo"),
    [
        pytest.param(
            {"version": 2, "acciones": []}, "version", id="version-incorrecta"
        ),
        pytest.param(
            {"version": 1, "acciones": "no es lista"},
            "acciones",
            id="acciones-no-lista",
        ),
    ],
)
def test_config_rechaza_configuracion_invalida_con_codigo_3(
    datos: dict[str, Any], campo: str
) -> None:
    ruta = escribir_config(datos)

    with pytest.raises(TareasError) as info:
        cargar_acciones(ruta)

    assert info.value.codigo == 3
    assert campo in str(info.value)


def test_config_rechaza_json_roto_con_codigo_3() -> None:
    ruta = Path("acciones.json")
    ruta.write_text("{", encoding="utf-8")

    with pytest.raises(TareasError) as info:
        cargar_acciones(ruta)

    assert info.value.codigo == 3
