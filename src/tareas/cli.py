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

    _mostrar_resultados(resultados, simular, str(accion.get("tipo", "")))


def _mostrar_resultados(
    resultados: list[motor.Resultado], simular: bool, tipo: str
) -> None:
    es_renombrar = tipo == "renombrar"

    if simular:
        mensaje = (
            "SIMULACIÓN: no se ha renombrado nada."
            if es_renombrar
            else "SIMULACIÓN: no se ha movido ni creado nada."
        )
        console.print(mensaje, style="yellow")

    if not resultados:
        console.print(
            "No hay archivos que cumplan el filtro en la carpeta.",
            style="yellow",
        )
        return

    tabla = Table(title="Resultado de la ejecución")
    tabla.add_column("estado")
    tabla.add_column("archivo")
    tabla.add_column("nuevo nombre" if es_renombrar else "destino")
    tabla.add_column("motivo")
    for resultado in resultados:
        tabla.add_row(
            resultado.estado,
            resultado.origen.name,
            resultado.destino.name if resultado.destino else "-",
            resultado.motivo,
        )
    console.print(tabla)

    simulados = sum(1 for r in resultados if r.estado == "simulado")
    movidos = sum(1 for r in resultados if r.estado == "movido")
    renombrados = sum(1 for r in resultados if r.estado == "renombrado")
    saltados = sum(1 for r in resultados if r.estado == "saltado")
    if simular:
        if es_renombrar:
            console.print(
                f"Se renombrarían {simulados} archivo(s); "
                f"saltados: {saltados}."
            )
        else:
            console.print(
                f"Se moverían {simulados} archivo(s); saltados: {saltados}."
            )
    elif es_renombrar:
        console.print(f"Renombrados: {renombrados}; saltados: {saltados}.")
    else:
        console.print(f"Movidos: {movidos}; saltados: {saltados}.")
