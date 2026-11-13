"""Órdenes de la herramienta tareas."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from tareas import __version__, motor
from tareas.config import cargar_acciones
from tareas.errores import TareasError

app = typer.Typer(help="Automatiza tareas repetitivas con ficheros.")
console = Console()


@app.command()
def version() -> None:
    """Muestra la versión instalada de tareas."""
    console.print(__version__)


@app.command()
def listar() -> None:
    """Muestra las acciones definidas en acciones.json."""
    try:
        acciones = cargar_acciones(Path("acciones.json"))
    except TareasError as error:
        console.print(str(error), style="red")
        raise typer.Exit(code=error.codigo)

    tabla = Table(title="Acciones")
    tabla.add_column("nombre")
    tabla.add_column("tipo")
    tabla.add_column("descripcion")
    for accion in acciones:
        tabla.add_row(
            str(accion.get("nombre", "")),
            str(accion.get("tipo", "")),
            str(accion.get("descripcion", "")),
        )
    console.print(tabla)


@app.command()
def ejecutar(
    nombre: str = typer.Argument(..., help="Nombre de la acción de acciones.json"),
    carpeta: Path = typer.Argument(..., help="Carpeta de origen"),
    simular: bool = typer.Option(
        False,
        "--simular",
        help="Muestra lo que haría sin mover ni crear nada",
    ),
) -> None:
    """Ejecuta una acción sobre los archivos de una carpeta."""
    try:
        acciones = cargar_acciones(Path("acciones.json"))
        accion = motor.buscar_accion(acciones, nombre)
        resultados = motor.ejecutar(
            accion,
            carpeta,
            simular=simular,
            preguntar=lambda mensaje: typer.confirm(mensaje, default=False),
        )
    except TareasError as error:
        console.print(str(error), style="red")
        raise typer.Exit(code=error.codigo)

    _mostrar_resultados(resultados, simular)


def _mostrar_resultados(
    resultados: list[motor.Resultado], simular: bool
) -> None:
    if simular:
        console.print(
            "SIMULACIÓN: no se ha movido ni creado nada.", style="yellow"
        )

    if not resultados:
        console.print(
            "No hay archivos que cumplan el filtro en la carpeta.",
            style="yellow",
        )
        return

    tabla = Table(title="Resultado de la ejecución")
    tabla.add_column("estado")
    tabla.add_column("archivo")
    tabla.add_column("destino")
    tabla.add_column("motivo")
    for resultado in resultados:
        tabla.add_row(
            resultado.estado,
            str(resultado.origen),
            str(resultado.destino) if resultado.destino else "-",
            resultado.motivo,
        )
    console.print(tabla)

    simulados = sum(1 for r in resultados if r.estado == "simulado")
    movidos = sum(1 for r in resultados if r.estado == "movido")
    saltados = sum(1 for r in resultados if r.estado == "saltado")
    if simular:
        console.print(
            f"Se moverían {simulados} archivo(s); saltados: {saltados}."
        )
    else:
        console.print(f"Movidos: {movidos}; saltados: {saltados}.")
