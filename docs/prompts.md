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

## Prompts

### Prompt 2 · Crear errores.py y config.py y modifica cli.py (10 nov 2026)

**Agente:** plan (para ver el plan) y luego build
**Prompt:**

>Escribe en src/tareas un archivo que se llame errores.py y que tenga tres clases, una llamada TareasError que sea la general, un ConfigError(TareasError) para cuando acciones.json esté mal escrito y  AccionNoValida(ConfigError), recibe (accion, campo, motivo) y su mensaje dice en español qué acción, qué campo y por qué falla. `TareasError` tiene un atributo `codigo` (1 por defecto) y `ConfigError` tiene código 3

>Escribe en src/tareas otro archivo llamado config.py con la función `cargar_acciones(ruta)` que lee y valida acciones.json antes de ejecutar nada. Si no existe o el JSON está roto, lanza ConfigError con un mensaje humano. Comprueba: "version" es 1; "acciones" es una lista; cada acción tiene nombre (único, en minúsculas y guiones),  descripcion y tipo (uno de mover, copiar, renombrar, borrar). Mover y copiar exigen destino; renombrar exige plantilla; borrar usa confirmar. Si hay filtro, comprueba extensiones (lista de textos), patron (expresión regular válida), mas_antiguo_que_dias y mayor_que_mb (números). Cada fallo lanza AccionNoValida con la acción, el campo y el motivo. Devuelve la lista de acciones validada.

>Adapta src/tareas/cli.py: el comando `listar` usa cargar_acciones y, si salta una TareasError, muestra el mensaje en rojo y sale con el código de la excepción, sin traceback.


> Reglas: respeta AGENTS.md. Solo la librería estándar de Python (json, re, pathlib). No toques acciones.json ni ningún otro archivo. No ejecutes ninguna acción sobre archivos. Antes de escribir nada, enséñame el plan.

**Qué hizo:** Creó errores.py, config.py y modificó el cli.py adantando listar para validar acciones.json antes de ejecutar.
**Lo que revisé en el diff:** Que sólo tocara esos tres archivos, que config.py sólo usara librería estardard, que no hubiera nada que borrara archivos y que acciones.json no se modificara.
**Resultado:** Bien. 19 casos pasan, probé a mano tareas listar con el archivo bueno (tabla) y con uno malo (mensaje rojo y codigo 3)
**Commit:** Añado errores.py y config.py y modifico cli.py. Guardo el segundo prompt en opencode.

## Prompts

### Prompt 3 · Crear src/tareas/motor.py y añadir el comando `ejecutar` en src/tareas/cli.py (13 nov 2026)

**Agente:** plan (para ver el plan) y luego build
**Prompt:**


> **Qué archivos:** Crea `src/tareas/motor.py` y añade en `src/tareas/cli.py` el comando `ejecutar`. Solo puedes cambiar esos dos archivos.

> **Qué debe hacer:** `tareas ejecutar NOMBRE CARPETA [--simular]` busca la acción NOMBRE en `acciones.json` y la aplica a CARPETA. Por ahora solo el tipo `mover`: mueve los archivos de CARPETA (sin subcarpetas) al `destino` de la acción. Mueve solo los archivos que cumplan el filtro.
> - Con `--simular`, el programa dice qué va a hacer sin hacerlo en realidad (ni siquiera crea la carpeta destino).
> - Si ya existe un archivo con ese nombre en el destino, el programa me lo dice y nunca lo sobrescribe: me pide permiso y, si digo que sí, lo mueve añadiendo un 1 al final del nombre, antes de la extensión. Si sigue existiendo, añade otro 1, hasta que ya no se parezcan. Si digo que no, se salta ese archivo y sigue con los demás.
> - Al terminar, el programa muestra lo que ha hecho y con qué archivos.
> - Si la acción no existe, avisa en rojo y sale con código 1. Si CARPETA no existe, igual.

> **Reglas:** sigue `AGENTS.md`. Solo librería estándar. No instales nada. No borres ninguna foto.

> **Qué NO tocar:** `acciones.json`, `config.py` y `errores.py`. Para probar, usa solo carpetas dentro de `~/pruebas-tareas`.

> **Antes de escribir nada, enséñame el plan.**

**Qué hizo:** Creó los archivos que le pedí motor.py, modificó cli.py para añadir el comando ejecutar
**Lo que revisé en el diff:** Modificaba los archivos pidiéndome autorización, nada de borrar, modifica el cli.py sin perder version ni --listar. 
**Resultado:** Hice varias pruebas metiendo archivos varios foto-a.jpg, foto-b.jpg, foto-c.png, informe.pdf, texto.txt, para ver que movía sólo las fotos y no los .txt y .pdf y comprabar que el filtro funciona bien. 
**Commit:** Añade motor.py y modifica el cli.py para introducir ejecutar con --simular en el código.

## Prompts

### Prompt 4 · Modificar src/tareas/motor.py y src/tareas/cli.py, para añadir tipo renombrar. (13 nov 2026)

**Agente:** plan (para ver el plan) y luego build
**Prompt:**


> **Qué archivos:** Modifica `src/tareas/motor.py` y `src/tareas/cli.py`. No cambies cómo funciona mover. Solo puedes cambiar esos dos archivos.
>
> **Qué debe hacer:** 
>– En la tabla de resultados, muestra solo el nombre de cada archivo, no la ruta entera, para que no salga cortado.
>– Añade el tipo renombrar. Debe mirar los archivos de CARPETA (sin subcarpetas) que cumplan el filtro de la acción y renombrarlos en la misma carpeta con la plantilla de la acción. La fecha es la de modificación del archivo. Se numeran desde 001 por orden de nombre.
>– Antes de cambiar nada, pídeme confirmación una sola vez, diciendo cuántos archivos vas a renombrar.
>– Si el nombre nuevo ya existe, añade un 1 al nombre antes de la extensión. Si sigue existiendo, añade otro 1, hasta que se resuelva.
>– Con --simular, muestra nombre antiguo -> nombre nuevo sin renombrar nada y sin preguntar.
>– Si la plantilla no se puede aplicar, avisa en rojo y sale con código 1.


> **Reglas:** sigue `AGENTS.md`. Solo librería estándar. No instales nada. No borres ninguna foto.

> **Qué NO tocar:** `acciones.json`, `config.py` y `errores.py`. Para probar, usa solo carpetas dentro de `~/pruebas-tareas`. Pruebas sólo con --simular; Las pruebas reales las hago yo.

> **Antes de escribir nada, enséñame el plan.**

**Qué hizo:** Modificó motor.py y cli.py para añadir el tipo renombrar sin cambiar mover, y para que la tabla muestre solo el nombre del archivo.
**Lo que revisé en el diff:** Revisé el resultado de Opencode y probé el resultado yo mismo.
**Resultado:**  Probé renombrar con fotos que había incluido en la carpeta y con --simular no cambió nada, sin --simular renombró los archivos.
**Commit:** Añade tipo renombrar y simplifica tabla de resultados.

## Prompts

### Prompt 5 · Modificar src/tareas/motor.py y src/tareas/cli.py, para añadir tipo borrar. (13 nov 2026)

Texto redactado con ayuda de Claude

**Agente:** plan (para ver el plan) y luego build
**Prompt:**


> **Qué archivos:** Modifica `src/tareas/motor.py` y, si hace falta, `src/tareas/cli.py`. No cambies cómo funcionan `mover` ni `renombrar`. Solo puedes cambiar esos dos archivos.

> **Qué debe hacer:** Añade el tipo `borrar`. Debe mirar los archivos de CARPETA (sin subcarpetas) que cumplan el filtro de la acción, y nunca debe borrar carpetas.
> - Si la acción no tiene filtro, no borra nada: avisa en rojo y sale con código 1, para no vaciar una carpeta por error.
> - Antes de borrar, enséñame cuántos archivos son y sus nombres, y pídeme confirmación una sola vez. Pregunta siempre, aunque `confirmar` sea `false` o no esté en la acción. Si digo que no, no se borra nada.
> - Si digo que sí, borra los archivos de verdad (no los mandes a ninguna papelera).
> - Con `--simular`, muestra qué archivos se borrarían, sin borrar nada y sin preguntar.
> - Al terminar, muestra qué archivos se han borrado. Si algo falla, avisa en rojo y sale con código 1.

> **Reglas:** sigue `AGENTS.md`. Solo librería estándar. No instales nada. Tú no ejecutes ningún borrado real: prueba solo con `--simular`.

> **Qué NO tocar:** `acciones.json`, `config.py` y `errores.py`. Para probar, usa solo carpetas dentro de `~/pruebas-tareas`. Las pruebas reales las hago yo.

> **Antes de escribir nada, enséñame el plan.**

**Qué hizo:** Modificó Motor.py y cli.py para añadir tipo borrar y borrar pide confirmación antes de borrar y no borra si la acción no tiene filtro.
**Lo que revisé en el diff:** Modificó los archivos pidiendo autorización, no borró nada, pidió hacer cambios fuera de la carpeta del proyecto y lo rechacé, ya que le pedí que no hiciera modificaciones fuera.
**Resultado:**  Motor.py actualizado con el tipo borrar y renombrar y mover intactos. Probé en prueba-borrar con archivos falsos: con --simular no borró nada; con y borró solo los .tmp de más de 30 días; con n no borró nada; y si no había archivos que cumplieran el filtro, avisó.
**Commit:** Añade tipo borrar y actualiza cli.py y motor.py

