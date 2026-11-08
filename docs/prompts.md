# Prompts clave · CLI «tareas con IA»

Aquí guardo solo los prompts importantes que le doy a **OpenCode** (el agente),
con una línea de qué pedí y qué pasó. Los apuntes de aprendizaje van en `diario.md`.

> Regla de oro: nunca pegar claves, contraseñas ni el contenido de `.env`.

## Cómo apuntar cada prompt

Copio esta plantilla por cada prompt importante:

```
### Prompt N · título corto (fecha)

**Agente:** plan / build
**Prompt:**
> (el texto exacto que escribí)

**Qué hizo:** (resumen en 1 o 2 líneas)
**Lo que revisé en el diff:** (qué miré antes de aceptar)
**Resultado:** bien / lo deshice con /undo / lo corregí así: ...
**Commit:** (mensaje del commit que hice yo)
```

---

## Prompts

### Prompt 1 · Crear cli.py con version y listar (8 nov 2026)

**Agente:** plan (para ver el plan) y luego build
**Prompt:**
> Crea el archivo src/tareas/cli.py con Typer para que exista el comando `tareas`.
> Debe tener: una variable `app` (Typer); el comando `version` (muestra __version__ de src/tareas/__init__.py); el comando `listar` (lee acciones.json y muestra con Rich una tabla con nombre, tipo y descripcion); y `tareas --help` debe funcionar.
> Reglas: respeta AGENTS.md. Usa solo Typer y Rich. Si falta Rich, dímelo antes de instalarlo. No ejecutes ninguna acción sobre archivos todavía, solo listar. No toques ningún otro archivo. Antes de escribir nada, enséñame el plan.

**Qué hizo:** Leer los archivos del proyecto con las directrices de las tareas que queremos crear y hace el archivo cli.py para habilitar los comandos --help y listar.
**Lo que revisé en el diff:** Sólo se edita src/tareas/cli.py, que existe la variable app; que habían dos comandos (version y listar), que no había nada que borrara o moviera archivos. 
**Resultado:** --help, version y listar funcionaron a la primera sin necesidad de cambiar nada. Añade version junto a --help y listar y comprobo que todo funcionara.
**Commit:** Añado cli.py con los comandos version y listar
