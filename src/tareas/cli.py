"""Órdenes de la herramienta tareas."""

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from tareas import __version__

app = typer.Typer(help="Automatiza tareas repetitivas con ficheros.")
console = Console()


@app.command()
def version() -> None:
    """Muestra la versión instalada de tareas."""
    console.print(__version__)


@app.command()
def listar() -> None:
    """Muestra las acciones definidas en acciones.json."""
    ruta = Path("acciones.json")
    if not ruta.is_file():
        console.print(f"[red]No se encuentra el fichero {ruta.resolve()}[/red]")
        raise typer.Exit(code=3)

    try:
        datos = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        console.print(f"[red]No se puede leer acciones.json: {error}[/red]")
        raise typer.Exit(code=3)

    acciones = datos.get("acciones") if isinstance(datos, dict) else None
    if not isinstance(acciones, list):
        console.print("[red]acciones.json no contiene una lista de acciones[/red]")
        raise typer.Exit(code=3)

    tabla = Table(title="Acciones")
    tabla.add_column("nombre")
    tabla.add_column("tipo")
    tabla.add_column("descripcion")
    for accion in acciones:
        if not isinstance(accion, dict):
            console.print("[red]Cada acción debe ser un objeto JSON[/red]")
            raise typer.Exit(code=3)
        tabla.add_row(
            str(accion.get("nombre", "")),
            str(accion.get("tipo", "")),
            str(accion.get("descripcion", "")),
        )
    console.print(tabla)
