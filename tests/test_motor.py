from pathlib import Path
from typing import Any

import pytest

from tareas import motor
from tareas.errores import IANoDisponible, TareasError


def crear_archivos(carpeta: Path, nombres: list[str]) -> dict[str, str]:
    carpeta.mkdir(parents=True, exist_ok=True)
    textos: dict[str, str] = {}
    for nombre in nombres:
        texto = f"contenido de {nombre}"
        (carpeta / nombre).write_text(texto, encoding="utf-8")
        textos[nombre] = texto
    return textos


def no_debe_preguntar(_mensaje: str) -> bool:
    pytest.fail("No se debe pedir confirmación durante la simulación")


def accion_mover() -> dict[str, Any]:
    return {
        "nombre": "mover-prueba",
        "tipo": "mover",
        "destino": "~/destino",
        "filtro": {"extensiones": [".jpg"]},
    }


def accion_renombrar() -> dict[str, Any]:
    return {
        "nombre": "renombrar-prueba",
        "tipo": "renombrar",
        "plantilla": "foto-{n:03}{ext}",
        "filtro": {"extensiones": [".jpg"]},
    }


def accion_borrar() -> dict[str, Any]:
    return {
        "nombre": "borrar-prueba",
        "tipo": "borrar",
        "filtro": {"extensiones": [".tmp"]},
    }


def accion_resumir() -> dict[str, Any]:
    return {
        "nombre": "resumir-prueba",
        "tipo": "resumir",
        "instrucciones": "Resume en una línea.",
        "filtro": {"extensiones": [".txt"]},
    }


def test_mover_simular_no_mueve_ni_crea_destino() -> None:
    origen = Path("origen")
    crear_archivos(origen, ["foto.jpg", "nota.txt"])
    destino = Path("~/destino").expanduser()

    resultados = motor.ejecutar(
        accion_mover(), origen, simular=True, preguntar=no_debe_preguntar
    )

    assert [resultado.estado for resultado in resultados] == ["simulado"]
    assert (origen / "foto.jpg").exists()
    assert (origen / "nota.txt").exists()
    assert not destino.exists()


def test_mover_real_mueve_solo_los_archivos_del_filtro() -> None:
    origen = Path("origen")
    crear_archivos(origen, ["foto.jpg", "nota.txt"])
    destino = Path("~/destino").expanduser()

    resultados = motor.ejecutar(accion_mover(), origen)

    assert [resultado.estado for resultado in resultados] == ["movido"]
    assert not (origen / "foto.jpg").exists()
    assert (origen / "nota.txt").exists()
    assert (destino / "foto.jpg").read_text(encoding="utf-8") == "contenido de foto.jpg"


def test_renombrar_simular_no_cambia_nombres_ni_pregunta() -> None:
    origen = Path("origen")
    crear_archivos(origen, ["b.jpg", "a.jpg"])

    resultados = motor.ejecutar(
        accion_renombrar(), origen, simular=True, preguntar=no_debe_preguntar
    )

    assert [resultado.estado for resultado in resultados] == ["simulado", "simulado"]
    assert [resultado.destino.name for resultado in resultados] == [
        "foto-001.jpg",
        "foto-002.jpg",
    ]
    assert (origen / "a.jpg").exists()
    assert (origen / "b.jpg").exists()
    assert not (origen / "foto-001.jpg").exists()


def test_renombrar_real_pregunta_una_sola_vez_y_renombra() -> None:
    origen = Path("origen")
    crear_archivos(origen, ["b.jpg", "a.jpg"])
    preguntas: list[str] = []

    def preguntar(mensaje: str) -> bool:
        preguntas.append(mensaje)
        return True

    resultados = motor.ejecutar(accion_renombrar(), origen, preguntar=preguntar)

    assert [resultado.estado for resultado in resultados] == [
        "renombrado",
        "renombrado",
    ]
    assert len(preguntas) == 1
    assert "2 archivo" in preguntas[0]
    assert (origen / "foto-001.jpg").exists()
    assert (origen / "foto-002.jpg").exists()
    assert not (origen / "a.jpg").exists()


def test_borrar_simular_no_borra_ni_pregunta() -> None:
    origen = Path("origen")
    crear_archivos(origen, ["viejo.tmp", "nota.txt"])

    resultados = motor.ejecutar(
        accion_borrar(), origen, simular=True, preguntar=no_debe_preguntar
    )

    assert [resultado.estado for resultado in resultados] == ["simulado"]
    assert (origen / "viejo.tmp").exists()
    assert (origen / "nota.txt").exists()


def test_borrar_real_pregunta_una_sola_vez_y_borra_solo_el_filtro() -> None:
    origen = Path("origen")
    crear_archivos(origen, ["viejo.tmp", "nota.txt"])
    preguntas: list[str] = []

    def preguntar(mensaje: str) -> bool:
        preguntas.append(mensaje)
        return True

    resultados = motor.ejecutar(accion_borrar(), origen, preguntar=preguntar)

    assert [resultado.estado for resultado in resultados] == ["borrado"]
    assert len(preguntas) == 1
    assert "viejo.tmp" in preguntas[0]
    assert not (origen / "viejo.tmp").exists()
    assert (origen / "nota.txt").exists()


def test_borrar_sin_filtro_no_borra_y_devuelve_codigo_1() -> None:
    origen = Path("origen")
    crear_archivos(origen, ["viejo.tmp"])
    accion = accion_borrar()
    accion.pop("filtro")

    with pytest.raises(TareasError) as info:
        motor.ejecutar(accion, origen, preguntar=lambda _mensaje: True)

    assert info.value.codigo == 1
    assert (origen / "viejo.tmp").exists()


def test_resumir_simular_no_llama_a_la_ia_ni_escribe(
    proveedor_falso: type,
) -> None:
    origen = Path("origen")
    textos = crear_archivos(origen, ["apuntes.txt"])
    proveedor = proveedor_falso()

    resultados = motor.ejecutar(
        accion_resumir(), origen, simular=True, proveedor=proveedor
    )

    assert [resultado.estado for resultado in resultados] == ["simulado"]
    assert resultados[0].motivo == (
        f"enviaría {len(textos['apuntes.txt'])} caracteres"
    )
    assert proveedor.llamadas == 0
    assert not (origen / "apuntes.resumen.md").exists()


def test_resumir_real_guarda_el_resumen_sin_tocar_el_original(
    proveedor_falso: type,
) -> None:
    origen = Path("origen")
    textos = crear_archivos(origen, ["apuntes.txt"])
    proveedor = proveedor_falso(texto="resumen fijo")

    resultados = motor.ejecutar(accion_resumir(), origen, proveedor=proveedor)

    assert [resultado.estado for resultado in resultados] == ["resumido"]
    assert (origen / "apuntes.resumen.md").read_text(encoding="utf-8") == "resumen fijo"
    assert (origen / "apuntes.txt").read_text(encoding="utf-8") == textos["apuntes.txt"]
    assert proveedor.llamadas == 1


def test_resumir_real_no_pisa_un_resumen_existente(
    proveedor_falso: type,
) -> None:
    origen = Path("origen")
    crear_archivos(origen, ["apuntes.txt"])
    (origen / "apuntes.resumen.md").write_text("resumen antiguo", encoding="utf-8")
    proveedor = proveedor_falso(texto="resumen nuevo")

    resultados = motor.ejecutar(accion_resumir(), origen, proveedor=proveedor)

    assert resultados[0].destino.name == "apuntes.resumen1.md"
    assert (origen / "apuntes.resumen.md").read_text(encoding="utf-8") == "resumen antiguo"
    assert (origen / "apuntes.resumen1.md").read_text(encoding="utf-8") == "resumen nuevo"


def test_resumir_real_salta_archivo_no_utf8(
    proveedor_falso: type,
) -> None:
    origen = Path("origen")
    crear_archivos(origen, ["apuntes.txt"])
    (origen / "malo.txt").write_bytes(b"\xff\xfe")
    proveedor = proveedor_falso(texto="resumen fijo")

    resultados = motor.ejecutar(accion_resumir(), origen, proveedor=proveedor)

    estados = {resultado.origen.name: resultado for resultado in resultados}
    assert estados["apuntes.txt"].estado == "resumido"
    assert estados["malo.txt"].estado == "saltado"
    assert "UTF-8" in estados["malo.txt"].motivo
    assert not (origen / "malo.resumen.md").exists()
    assert proveedor.llamadas == 1


def test_resumir_real_con_fallo_de_ia_conserva_resumenes_hechos(
    proveedor_falso: type,
) -> None:
    origen = Path("origen")
    crear_archivos(origen, ["a.txt", "b.txt"])
    proveedor = proveedor_falso(texto="resumen fijo", fallar_en=2)

    with pytest.raises(IANoDisponible) as info:
        motor.ejecutar(accion_resumir(), origen, proveedor=proveedor)

    assert info.value.codigo == 4
    assert (origen / "a.resumen.md").read_text(encoding="utf-8") == "resumen fijo"
    assert not (origen / "b.resumen.md").exists()
    assert proveedor.llamadas == 2
