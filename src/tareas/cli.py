"""Órdenes de la herramienta tareas."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from tareas import __version__
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
