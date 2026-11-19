"""Órdenes de la herramienta tareas."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from tareas import __version__, ia, motor
from tareas.config import cargar_acciones
from tareas.errores import TareasError

app = typer.Typer(help="Automatiza tareas repetitivas con ficheros.")
console = Console()


@app.command()
def version() -> None:
    """Muestra la versión instalada de tareas."""
    console.print(__version__)


@app.command("comprobar-ia")
def comprobar_ia() -> None:
    """Comprueba que la IA del centro responde."""
    try:
        proveedor = ia.ProveedorCentro()
        respuesta = proveedor.completar(
            sistema="Responde de forma breve y en español.",
            usuario="Responde solo con la palabra: hola",
            max_tokens=200,
        )
    except TareasError as error:
        console.print(str(error), style="red")
        raise typer.Exit(code=error.codigo)

    console.print("La IA funciona correctamente.", style="green")
    texto = respuesta.texto.strip()
    if texto:
        console.print(f"Respuesta: {texto}")


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
        proveedor: ia.ProveedorIA | None = None
        if accion.get("tipo") == "resumir" and not simular:
            proveedor = ia.ProveedorCentro()
        resultados = motor.ejecutar(
            accion,
            carpeta,
            simular=simular,
            preguntar=lambda mensaje: typer.confirm(mensaje, default=False),
            proveedor=proveedor,
        )
    except TareasError as error:
        console.print(str(error), style="red")
        raise typer.Exit(code=error.codigo)

    _mostrar_resultados(resultados, simular, str(accion.get("tipo", "")))


def _mostrar_resultados(
    resultados: list[motor.Resultado], simular: bool, tipo: str
) -> None:
    es_renombrar = tipo == "renombrar"
    es_borrar = tipo == "borrar"
    es_resumir = tipo == "resumir"

    if simular:
        if es_renombrar:
            mensaje = "SIMULACIÓN: no se ha renombrado nada."
        elif es_borrar:
            mensaje = "SIMULACIÓN: no se ha borrado nada."
        elif es_resumir:
            mensaje = "SIMULACIÓN: no se ha resumido ni creado nada."
        else:
            mensaje = "SIMULACIÓN: no se ha movido ni creado nada."
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
    if not es_borrar:
        if es_renombrar:
            cabecera = "nuevo nombre"
        elif es_resumir:
            cabecera = "resumen"
        else:
            cabecera = "destino"
        tabla.add_column(cabecera)
    tabla.add_column("motivo")
    for resultado in resultados:
        fila = [resultado.estado, resultado.origen.name]
        if not es_borrar:
            fila.append(resultado.destino.name if resultado.destino else "-")
        fila.append(resultado.motivo)
        tabla.add_row(*fila)
    console.print(tabla)

    simulados = sum(1 for r in resultados if r.estado == "simulado")
    movidos = sum(1 for r in resultados if r.estado == "movido")
    renombrados = sum(1 for r in resultados if r.estado == "renombrado")
    borrados = sum(1 for r in resultados if r.estado == "borrado")
    resumidos = sum(1 for r in resultados if r.estado == "resumido")
    saltados = sum(1 for r in resultados if r.estado == "saltado")
    if simular:
        if es_renombrar:
            console.print(
                f"Se renombrarían {simulados} archivo(s); "
                f"saltados: {saltados}."
            )
        elif es_borrar:
            console.print(
                f"Se borrarían {simulados} archivo(s); saltados: {saltados}."
            )
        elif es_resumir:
            console.print(
                f"Se resumirían {simulados} archivo(s); saltados: {saltados}."
            )
        else:
            console.print(
                f"Se moverían {simulados} archivo(s); saltados: {saltados}."
            )
    elif es_renombrar:
        console.print(f"Renombrados: {renombrados}; saltados: {saltados}.")
    elif es_borrar:
        console.print(f"Borrados: {borrados}; saltados: {saltados}.")
    elif es_resumir:
        console.print(f"Resumidos: {resumidos}; saltados: {saltados}.")
    else:
        console.print(f"Movidos: {movidos}; saltados: {saltados}.")
