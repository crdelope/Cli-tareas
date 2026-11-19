from pathlib import Path
from typing import Callable

from typer.testing import CliRunner

from tareas.cli import app

runner = CliRunner()


def test_help_y_listar_terminan_con_codigo_cero(
    acciones_json: Callable[..., Path],
) -> None:
    acciones_json()

    ayuda = runner.invoke(app, ["--help"])
    listado = runner.invoke(app, ["listar"])

    assert ayuda.exit_code == 0, ayuda.output
    assert listado.exit_code == 0, listado.output
    assert "mover-prueba" in listado.output
    assert "resumir-prueba" in listado.output


def test_ejecutar_accion_inexistente_devuelve_codigo_1(
    acciones_json: Callable[..., Path],
) -> None:
    acciones_json()
    Path("carpeta").mkdir()

    resultado = runner.invoke(app, ["ejecutar", "no-existe", "carpeta"])

    assert resultado.exit_code == 1, resultado.output
    assert "No existe ninguna acción" in resultado.output


def test_listar_con_json_invalido_devuelve_codigo_3(
    acciones_json: Callable[..., Path],
) -> None:
    acciones_json({"version": 2, "acciones": []})

    resultado = runner.invoke(app, ["listar"])

    assert resultado.exit_code == 3, resultado.output
    assert "version" in resultado.output


def test_resumir_sin_variables_de_ia_devuelve_codigo_4(
    acciones_json: Callable[..., Path],
) -> None:
    acciones_json()
    carpeta = Path("carpeta")
    carpeta.mkdir()
    (carpeta / "apuntes.txt").write_text("texto de prueba", encoding="utf-8")

    resultado = runner.invoke(app, ["ejecutar", "resumir-prueba", "carpeta"])

    assert resultado.exit_code == 4, resultado.output
    assert "CENTRO_IA_URL" in resultado.output
    assert not (carpeta / "apuntes.resumen.md").exists()
