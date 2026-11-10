"""Excepciones de la herramienta tareas."""


class TareasError(Exception):
    """Error general de la herramienta."""

    codigo = 1


class ConfigError(TareasError):
    """Error de configuración de acciones.json."""

    codigo = 3


class AccionNoValida(ConfigError):
    """Una acción de acciones.json no cumple las reglas."""

    def __init__(self, accion: str, campo: str, motivo: str) -> None:
        self.accion = accion
        self.campo = campo
        self.motivo = motivo
        super().__init__(
            f"Acción '{accion}': el campo '{campo}' no es válido: {motivo}"
        )
