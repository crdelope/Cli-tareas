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


### Prompt 1 · Crear cli.py con version y listar (8 nov 2026)

Texto redactado con ayuda de Claude

**Agente:** plan (para ver el plan) y luego build
**Prompt:**
> Crea el archivo src/tareas/cli.py con Typer para que exista el comando `tareas`.
> Debe tener: una variable `app` (Typer); el comando `version` (muestra __version__ de src/tareas/__init__.py); el comando `listar` (lee acciones.json y muestra con Rich una tabla con nombre, tipo y descripcion); y `tareas --help` debe funcionar.
> Reglas: respeta AGENTS.md. Usa solo Typer y Rich. Si falta Rich, dímelo antes de instalarlo. No ejecutes ninguna acción sobre archivos todavía, solo listar. No toques ningún otro archivo. Antes de escribir nada, enséñame el plan.

**Qué hizo:** Leer los archivos del proyecto con las directrices de las tareas que queremos crear y hace el archivo cli.py para habilitar los comandos --help y listar.
**Lo que revisé en el diff:** Sólo se edita src/tareas/cli.py, que existe la variable app; que habían dos comandos (version y listar), que no había nada que borrara o moviera archivos. 
**Resultado:** --help, version y listar funcionaron a la primera sin necesidad de cambiar nada. Añade version junto a --help y listar y comprobo que todo funcionara.
**Commit:** Añado cli.py con los comandos version y listar


### Prompt 2 · Crear errores.py y config.py y modifica cli.py (10 nov 2026)

Texto redactado con ayuda de Claude

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


### Prompt 3 · Crear src/tareas/motor.py y añadir el comando `ejecutar` en src/tareas/cli.py (13 nov 2026)

Texto redactado con ayuda de Claude

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


### Prompt 4 · Modificar src/tareas/motor.py y src/tareas/cli.py, para añadir tipo renombrar. (13 nov 2026)

Texto redactado con ayuda de Claude

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


### Prompt 6 · Capa de IA: ia.py y comprobar-ia (15 nov 2026).

Texto redactado con ayuda de Claude

**Agente:** plan (para ver el plan) y luego build
**Prompt:**


> **Qué archivos:** Crea `src/tareas/ia.py` y modifica `src/tareas/errores.py` y `src/tareas/cli.py`. Solo puedes crear `ia.py` y modificar `errores.py` y `cli.py`.

> **Qué debe hacer:** 
> - En `ia.py`, crea la clase `Respuesta`, que guarda el texto que le devuelve el modelo.
> - En `ia.py`, crea la clase base `ProveedorIA`, con un método `completar(sistema, usuario, max_tokens)`, que devuelve una `Respuesta`.
> - En `ia.py`, crea `ProveedorCentro`, que hereda de `ProveedorIA`. Lee la dirección, la clave y el modelo de las variables `CENTRO_IA_URL`, `CENTRO_IA_KEY` y `CENTRO_IA_MODELO`, cargándolas del archivo `.env` con `python-dotenv`. Para llamar al servidor usa `httpx`: hace un POST a `{CENTRO_IA_URL}/chat/completions`, envía la clave en la cabecera `Authorization: Bearer <clave>` y pone un tiempo máximo de espera.
> - En `errores.py`, crea `IANoDisponible`, que hereda de `TareasError` y tiene código de salida 4.
> - En `cli.py`, añade el comando `tareas comprobar-ia`, que hace una pregunta mínima al modelo, con `max_tokens` de 200, y dice si ha funcionado o no.
>
> **Reglas:**
> - Los errores se muestran en español y en rojo, como los demás, con un mensaje claro para cada caso: falta la clave, no hay conexión, el servidor tarda demasiado, la clave es rechazada (401) y hay demasiadas peticiones (429).
> - La clave nunca se imprime, ni en mensajes, ni en errores, ni en el resultado de `comprobar-ia`.
> - Usa un margen de 200 tokens en `comprobar-ia`, porque el modelo piensa antes de contestar y con menos puede devolver vacío.
>
> **Qué NO tocar:**
> - No toques `motor.py`, `config.py` ni `acciones.json`.
> - No abras ni leas el archivo `.env`, ni muestres su contenido.
> - No instales nada: las librerías ya están instaladas.
> - No ejecutes `tareas comprobar-ia`: la prueba con la red la haré yo.


> **Antes de escribir nada, enséñame el plan.**

**Qué hizo:** Creó el archivo ia.py que contiene las clases Respuesta, ProveedorIA y ProveedorCentro y modificó el errores.py y el cli.py, creando el comando comprobar-ia y la clase IANoDisponible (código 4).
**Lo que revisé en el diff:** En el plan vi un fallo: `load_dotenv()` sin más busca el `.env` desde la carpeta donde está `ia.py`. Ahora funciona porque el proyecto está en modo editable, pero si alguien lo instala con `uv tool install`, `ia.py` quedará en otro sitio y no encontrará el `.env` de su carpeta. Es lo mismo que con `acciones.json`, que se lee de la carpeta donde estoy ejecutando el comando. Se arregla con `load_dotenv(find_dotenv(usecwd=True))`, y se lo pedí al pasar a build. Después revisé `ia.py`: están los nombres de clase que pedí, no hay ningún `print` de la clave, los errores de variable dicen el nombre y no el valor, y el cambio de `find_dotenv` está incluido. (Aquí añade lo que veas en el `git diff` de `cli.py` y `errores.py`.). En cli.py solo se añadió el comando comprobar-ia y el import de ia; en errores.py solo IANoDisponible con código 4. No se tocó ningún otro comando.
**Resultado:** Con la clave buena, `comprobar-ia` contesta "hola". Probé los errores: con una clave errónea sale el 401, con una dirección errónea sale "No hay conexión", y quitando el `.env` de su sitio sale "Falta la variable". En todos el código de salida es 4. Probé también con una variable vacía, pero PowerShell la borra, así que esa prueba no sirve.
**Commit:** 05494d5 Añado la capa de la IA: ia.py, IANoDisponible (Codigo 4) y comprobar-ia.


### Prompt 7 · Validar en config.py las acciones resumir y clasificar (15 nov 2026)

Texto redactado con ayuda de Claude

**Agente:** plan (para ver el plan) y luego build
**Prompt:**


> **Qué archivos:** Modifica solo `src/tareas/config.py`.
>
> **Qué debe hacer:** Acepta y valida dos tipos de acción nuevos: `resumir` y `clasificar`.
> - `resumir`:
>   - `instrucciones` es obligatoria y debe ser un texto no vacío.
>   - `max_caracteres` es opcional, un número entero entre 500 y 50000. Si no está, vale 12000.
>   - `filtro` es opcional, igual que en las otras acciones.
> - `clasificar`:
>   - `categorias` es obligatoria, una lista de al menos 2 textos no vacíos, y debe incluir `otros`.
>   - `instrucciones` es opcional, pero si está debe ser un texto no vacío.
>   - `max_caracteres` y `filtro` funcionan igual que en `resumir`.
>
> **Reglas:**
> - Los errores de validación usan los mismos errores y el mismo código de salida (3) que los demás. Los mensajes van en español y dicen qué acción y qué campo falla.
> - Las acciones `mover`, `renombrar` y `borrar` siguen validando exactamente igual que ahora.
> - Los tipos nuevos solo se validan: todavía no se ejecutan.
>
> **Qué NO tocar:**
> - No toques `motor.py`, `cli.py`, `ia.py`, `errores.py` ni `acciones.json`.
> - No abras ni leas el archivo `.env`.
> - No instales nada.
> - No llames a la IA.
>
> **Pruebas:** Haz las pruebas con `uv run python -` en línea, sin crear archivos fuera del proyecto. Enséñame un caso válido y otro inválido de `resumir` y de `clasificar`.
>
> **Antes de escribir nada, enséñame el plan.**

**Qué hizo:** Modificó el archivo config.py para incluir dos acciones nuevas: resumir y clasificar.
**Lo que revisé en el diff:** Que solo modificó config.py, que las ramas mover, renombrar y borrar no han sido tocadas, que los mensajes de error están en español y dicen acción y campo, que el valor por defecto 12000 no se escribe en ningún sitio. comprobamos una línea que se repetía en el diff pero era sólo cosa del visor lo comprobamos con Select-string.
**Resultado:** Opencode ejecutó 40 pruebas en línea y pasaron todas. Todo los errores nuevos aparecen con código 3. uv run tareas listar sigue enseñando mis tres acciones. y las pruebas no se guardaron en ningún archivo: más adelante las convertiremos en pytest.
**Commit:** Valido en config.py las acciones resumir y clasificar.

### Prompt 8 · Que resumir funcione (19 nov 2026)

Texto redactado con ayuda de Claude

**Agente:** plan (para ver el plan) y luego build
**Prompt:**

> **Qué archivos:** Modifica solo `src/tareas/motor.py` y `src/tareas/cli.py`.
>
> **Qué debe hacer:** Implementa la acción de tipo `resumir`.
> - Para cada archivo de la carpeta que cumpla el filtro, lee el texto y se lo manda a la IA con las `instrucciones` de la acción.
> - Si el filtro no indica extensiones, usa `.txt` y `.md`. Ignora los archivos que ya terminan en `.resumen.md`.
> - Envía como mucho `max_caracteres` del texto (12000 si la acción no lo indica: el valor por defecto se aplica aquí).
> - Guarda el resumen en un archivo nuevo junto al original: `apuntes.txt` pasa a `apuntes.resumen.md`. Si ya existe, no lo pisa: añade un `1` como en `mover`.
> - Con `--simular` no llama a la IA ni escribe nada: muestra "enviaría N caracteres" por cada archivo.
> - `ejecutar` recibe el proveedor de IA desde fuera (como ya recibe `preguntar`), para poder probarlo con uno falso. En `cli.py`, `ProveedorCentro` solo se crea si la acción es de tipo `resumir` y no es `--simular`.
> - Pide a la IA 1500 `max_tokens`, porque el modelo piensa antes de contestar.
> - Si la IA devuelve un texto vacío, salta ese archivo y explica el motivo.
> - La tabla de resultados añade un contador de "Resumidos".
>
> **Reglas:**
> - Si la IA falla, la acción se para con `IANoDisponible` (código 4). Los resúmenes ya hechos se quedan.
> - Nunca se modifica ni se borra un archivo original.
> - `mover`, `renombrar` y `borrar` no cambian. El tipo `clasificar` sigue sin ejecutarse y da el error de siempre.
>
> **Qué NO tocar:**
> - No toques `config.py`, `ia.py`, `errores.py` ni `acciones.json`.
> - No abras ni leas el archivo `.env`.
> - No instales nada.
> - No llames a la IA con red: la prueba real la haré yo.
>
> **Pruebas:** Haz las pruebas con `uv run python -` en línea, con un `ProveedorIA` falso que devuelva un texto fijo, y solo dentro de una carpeta temporal o de `~/pruebas-tareas/`. Prueba `--simular` y comprueba que no se crea ningún archivo.
>
> **Antes de escribir nada, enséñame el plan.**

**Qué hizo:** Modificó `motor.py`, donde añadió la acción de tipo `resumir` (lee los archivos de texto, los manda a la IA, guarda el resumen en un archivo `.resumen.md` junto al original y no pisa archivos existentes), y `cli.py`, donde crea el proveedor de IA solo cuando hace falta y añade el mensaje de simulación y el contador "Resumidos".
**Lo que revisé en el diff:** Comprobé en `cli.py` que `ProveedorCentro()` solo se crea si la acción es `resumir` y no hay `--simular`, y que está dentro del `try`, así que un fallo de la IA sale en rojo con código 4. Comprobé que solo había cambios para `resumir` y que `mover`, `renombrar` y `borrar` no se tocaron. Además, `config.py`, `ia.py`, `errores.py` y `.env` no se modificaron. Después añadí yo la acción `resumir-apuntes` a `acciones.json`.
**Resultado:** OpenCode hizo pruebas con un proveedor falso: simulación sin escribir nada ni llamar a la IA, truncamiento a `max_caracteres`, nombre `apuntes.resumen1.md` si ya existe, archivo no UTF-8 saltado con motivo, respuesta vacía saltada y fallo de la IA con código 4 conservando los resúmenes ya hechos. Yo probé `resumir-apuntes` con un texto de prueba: con `--simular` dijo "enviaría 220 caracteres" y no creó nada, y sin `--simular` Groq devolvió un resumen de cinco líneas guardado en `prueba.resumen.md`. Las tildes mal en PowerShell son un problema de visualización, no del archivo.
**Commit:** Añado la acción de resumir que ya funciona y he añadido la acción a acciones.json, modifico motor.py y cli.py donde crea el proveedor de IA.

### Prompt 9 · Pruebas con pytest (19 nov 2026)

Texto redactado con ayuda de Claude

**Agente:** plan (para ver el plan) y luego build
**Prompt:**

> **Qué archivos:** Crea la carpeta `tests/` con `conftest.py`, `test_config.py`, `test_motor.py` y `test_cli.py`. No modifiques ningún archivo de `src/`.
>
> **Qué debe hacer:** Escribe pruebas con pytest, ya instalado.
> - `conftest.py`: un fixture automático que antes de cada prueba cambie a una carpeta temporal (`tmp_path`), apunte `HOME` y `USERPROFILE` a esa carpeta y quite las variables `CENTRO_IA_URL`, `CENTRO_IA_KEY`, `CENTRO_IA_MODELO` y `CENTRO_IA_CA`. Un `ProveedorFalso` que devuelva un texto fijo. Un fixture que escriba un `acciones.json` en la carpeta actual.
> - `test_config.py`: acciones válidas e inválidas de cada tipo (`mover`, `renombrar`, `borrar`, `resumir`, `clasificar`), con `pytest.mark.parametrize`. Comprueba que los errores tienen código 3.
> - `test_motor.py`: `mover`, `renombrar`, `borrar` y `resumir` con `--simular` (no cambia nada) y sin simular. En `resumir`, usa el `ProveedorFalso`, comprueba `apuntes.resumen1.md` si ya existe, que se salta un archivo no UTF-8 y que, si la IA falla, se conservan los resúmenes ya hechos y el error tiene código 4.
> - `test_cli.py`: con `CliRunner` de Typer, comprueba los códigos de salida 0, 1, 3 y 4, y que `--help` y `listar` funcionan.
>
> **Reglas:**
> - Todas las pruebas usan solo `tmp_path`. Nunca tocan `~/pruebas-tareas` ni el `acciones.json` real.
> - Ninguna prueba usa la red.
> - Cada prueba tiene un nombre que explique qué comprueba.
> - Si una prueba descubre un fallo del programa, no lo arregles: dímelo.
>
> **Qué NO tocar:**
> - No toques nada de `src/`, ni `acciones.json`, ni `.env`.
> - No abras ni leas `.env`.
> - No instales nada.
>
> **Pruebas:** Ejecuta `uv run pytest -v` y enséñame el resultado.
>
> **Antes de escribir nada, enséñame el plan.**

**Qué hizo:** Creó la carpeta `tests/` con cuatro archivos: `conftest.py` (aísla cada prueba en una carpeta temporal, quita las variables de la IA y define un `ProveedorFalso`), `test_config.py` (acciones válidas e inválidas de cada tipo, con código 3), `test_motor.py` (`mover`, `renombrar`, `borrar` y `resumir`, con y sin `--simular`) y `test_cli.py` (códigos de salida 0, 1, 3 y 4).
**Lo que revisé en el diff:** Comprobé que solo se habían creado archivos nuevos dentro de `tests/` y que `src/`, `acciones.json` y `.env` no se tocaron. Vi que `conftest.py` cambia a `tmp_path` antes de cada prueba y anula `load_dotenv`, así que ninguna prueba toca mis carpetas reales ni usa la clave. Y que ninguna prueba usa la red.
**Resultado:** Ejecuté `uv run pytest -v` y pasaron las 29 pruebas en menos de un segundo. Comprobé con `git status` que solo se subían `tests/` y `prompts.md`.
**Commit:** `594fb67`Añado pruebas con pytest de config, motor y cli.
