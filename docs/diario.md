# Diario del proyecto · CLI «tareas con IA»

Mi cuaderno de recetas: qué hice, con qué órdenes, qué pasó y qué he aprendido.
Sistema: Windows 10 + PowerShell. Inicio: 27 oct 2026.

> Regla de oro: aquí **nunca** se escribe una clave ni una contraseña (ni "de ejemplo").

**Cómo leer este diario.** Cada paso tiene siempre las mismas partes:
*Qué quería*, *Órdenes*, *Qué pasó* y *Conclusión*.
Las líneas que empiezan por ✏️ son **mías**: las escribo yo con mis palabras
(2 o 3 líneas bastan). Cuando las rellene, borro el ✏️.

---

## Paso 1 · Comprobar qué tengo instalado (27 oct)

**Qué quería:** saber si mi equipo ya tiene lo necesario antes de instalar nada.

**Órdenes (PowerShell):**

```
python --version
git --version
winget --version
```

**Qué pasó:**

| Orden | Resultado |
|---|---|
| `python --version` | Python 3.15.2 |
| `git --version` | git version 2.56.0.windows.2 |
| `winget --version` | v1.29.380 |

Observación: el curso pide Python 3.12 y yo tengo la 3.15. No hay que desinstalar nada:
`uv` usará la 3.12 solo dentro del proyecto.

**Conclusión:**
Hemos comprobado las versiones con `--version` para saber qué tenemos instalado.
Instalé Python desde python.org y me puso la 3.15 en vez de la 3.12. `uv` me permitirá
ajustar las versiones.

---

## Paso 2 · Instalar uv (27 oct)

**Qué quería:** tener `uv`, la herramienta que crea el proyecto y gestiona Python y las librerías.

**Órdenes:**

```
winget install --id=astral-sh.uv -e
```

**Qué pasó:** me pidió aceptar los términos del origen `msstore` (respondí `Y`).
Instaló uv 0.13.6 y añadió los alias `uv`, `uvx` y `uvw`.
Avisó: *"Variable de entorno PATH modificada; reinicie el shell"*.

**Conclusión:**
✏️ CONCLUSIÓN 2 (escríbela tú): ¿por qué tengo que cerrar y abrir PowerShell después de instalar?
(Pista: piensa en qué es el PATH, la lista de carpetas donde Windows busca los comandos.)

---

## Paso 3 · Comprobar uv (pendiente)

**Qué quería:** confirmar que `uv` funciona en una ventana nueva.

**Órdenes:**

```
uv --version
```

**Qué pasó:** en una ventana nueva de PowerShell, `uv` ya se reconoce:

```
uv 0.13.6 (329bf9448 2026-10-26 x86_64-pc-windows-msvc)
```

**Conclusión:**
✏️ CONCLUSIÓN 3 (escríbela tú): ¿qué ha cambiado respecto a antes de reiniciar PowerShell?
¿Qué me dice este resultado sobre mi instalación?

---

## Paso 4 · Crear el proyecto (pendiente)

**Qué quería:** crear la carpeta `cli-tareas` con la estructura de un programa instalable, usando Python 3.12.

**Órdenes:**

```
cd ~
uv init --package --name tareas --python 3.12 cli-tareas
cd cli-tareas
dir
```

**Qué pasó:** el proyecto ya estaba creado, así que al repetir la orden `uv` me avisó con
`error: Cannot initialize a project ... because pyproject.toml already exists`.
No es un fallo grave: significa que no machaca lo que ya existe.

El `dir` de `C:\Users\crdel\cli-tareas` muestra:

| Nombre | Qué es |
|---|---|
| `src` | carpeta donde irá el código |
| `.gitignore` | lista de cosas que git no debe subir |
| `.python-version` | la versión de Python del proyecto |
| `pyproject.toml` | ficha del proyecto (nombre, versión, dependencias) |
| `README.md` | explicación del proyecto (vacío por ahora) |

**Incidente: carpeta duplicada.** Después repetí `uv init ... cli-tareas` estando *ya dentro*
de `cli-tareas`. Resultado: `uv` creó otra carpeta `cli-tareas` **dentro** de la primera (con su
`src`, `pyproject.toml` y `README.md` vacío) y añadió esto al final del `pyproject.toml`:

```
[tool.uv.workspace]
members = [
    "cli-tareas",
]
```

Cómo lo arreglé (sin ningún commit hecho todavía, así que sin riesgo):

1. Miré antes de borrar: `dir -Force cli-tareas` y `Get-Content pyproject.toml`.
2. Comprobé con `pwd` que estaba en la carpeta correcta y borré la sobrante:
   `Remove-Item -Recurse -Force .\cli-tareas`
3. Abrí `notepad pyproject.toml` y quité el bloque `[tool.uv.workspace]`.
4. Comprobé con `Get-Content pyproject.toml` que terminaba en `build-backend = "uv_build"`.

**Conclusión:**
✏️ CONCLUSIÓN 4 (escríbela tú): ¿qué hace `uv init --package`? ¿Qué significa el error de
"already exists" y por qué es bueno que `uv` no sobrescriba? ¿Qué lección te llevas del incidente
(dónde tenía que estar antes de ejecutar una orden, y por qué conviene mirar antes de borrar)?

---

## Paso 5 · Añadir `.env` al `.gitignore` (27 oct)

**Qué quería:** que git nunca suba el fichero `.env`, donde irá la clave de los modelos,
**antes** del primer commit.

**Órdenes:**

```
notepad .gitignore
git check-ignore -v .env
```

En el Bloc de notas añadí al final:

```
# Secretos
.env
```

**Qué pasó:** `git check-ignore -v .env` respondió `.gitignore:13:.env      .env`.
Eso significa que la línea 13 del `.gitignore` bloquea el fichero `.env`.
También comprobé con `dir` que la carpeta duplicada ya no existe.

**Conclusión:**
Si `.env` no estuviera en el `.gitignore`, git lo guardaría todo sin restricciones y acabaría
publicándose en GitHub. Con el `.gitignore` le decimos a git que ese fichero no lo queremos
publicado y que se quede guardado solo en mi ordenador.

---

## Paso 6 · Mi primer commit (1 nov)

**Qué quería:** guardar la primera "foto" del proyecto en git, con una etiqueta que cuente lo que hice.

**Órdenes:**

```
git add .
git commit -m "Primer commit: Proyecto tareas con uv y .env en .gitignore"
git log --oneline
```

**Qué pasó:**

- `git add .` metió los 5 ficheros en la "caja". Salieron avisos de `LF will be replaced by CRLF`:
  son normales en Windows (cambia el modo de acabar las líneas) y no hay que hacer nada.
- `git status` mostró los 5 ficheros en `Changes to be committed`: `.gitignore`, `.python-version`,
  `README.md`, `pyproject.toml` y `src/tareas/__init__.py`. No había ninguna carpeta duplicada ni `.venv`.
- `git commit` creó el commit `7594b35` y `git log --oneline` mostró una sola línea con mi mensaje.
- Llevo **1 commit de los 10** que pide el proyecto.

**Conclusión:**
✏️ CONCLUSIÓN 6 (escríbela tú): ¿qué es un commit y para qué sirve la etiqueta (`-m`)?
¿Qué diferencia hay entre `git add` y `git commit`?

---

## Paso 7 · Subir el repo a GitHub (1 nov)

**Qué quería:** poner mi proyecto en internet, en un repositorio **público** (lo exige el proyecto).

**Qué hice:**

1. En github.com creé el repositorio `Cli-tareas`, público y **vacío** (sin README, sin `.gitignore`
   y sin licencia, para que no choquen con los de mi carpeta).
2. En PowerShell, dentro de `cli-tareas`:

```
git remote add origin https://github.com/crdelope/Cli-tareas.git
git remote -v
git push -u origin main
```

**Qué pasó:** `git remote -v` mostró la URL dos veces (`fetch` y `push`). El `git push` subió
9 objetos y terminó con `main -> main` y `branch 'main' set up to track 'origin/main'`.
El repo queda en: https://github.com/crdelope/Cli-tareas

**Conclusión:**
✏️ CONCLUSIÓN 7 (escríbela tú): ¿qué diferencia hay entre `git commit` y `git push`?
¿Para qué sirve `origin`? ¿Por qué se crea el repo vacío en GitHub?

---

## Paso 8 · Instalar Node.js y abrir el candado de npm (1 nov)

**Qué quería:** tener Node.js y `npm`, necesarios para instalar OpenCode en Windows.

**Órdenes:**

```
node --version
winget install --id OpenJS.NodeJS.LTS -e
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
npm --version
```

**Qué pasó:**

- `node --version` dio error: no estaba instalado.
- `winget install Node.js` encontró **dos** paquetes con ese nombre y no eligió ninguno; con
  `--id OpenJS.NodeJS.LTS -e` (id exacto) sí se instaló la versión estable (LTS). Quedó `v26.13.0`.
- `npm --version` falló: *la ejecución de scripts está deshabilitada en este sistema*.
  Es el candado de seguridad de PowerShell. Lo abrí **solo para mi usuario** con
  `RemoteSigned`, y entonces `npm --version` dio `11.20.0`.

**Conclusión:**
✏️ CONCLUSIÓN 8 (escríbela tú): ¿para qué necesito Node.js y npm en este proyecto?
¿Qué hace `-Scope CurrentUser` y por qué es mejor que abrir el candado para todo el ordenador?

---

## Paso 9 · Instalar OpenCode 1.18.35 (1 nov)

**Qué quería:** tener OpenCode, el agente de IA, en la **versión exacta del curso**.

**Órdenes:**

```
npm install -g opencode-ai@1.18.35
opencode --version
```

**Qué pasó:** tras cerrar y abrir PowerShell, `opencode --version` respondió `1.18.35`.
Todavía **no** lo he abierto: aún falta la conexión a los modelos del centro.

**Conclusión:**
✏️ CONCLUSIÓN 9 (escríbela tú): ¿por qué fijo la versión con `@1.18.35` en vez de instalar la última?
¿Qué significa `-g`?

---

## Paso 10 · Permisos del proyecto y segundo commit (1 nov)

**Qué quería:** dejar escritas las normas de OpenCode para este repo (qué puede hacer solo,
qué me pregunta y qué tiene prohibido). Ese fichero **no lleva claves**, así que se sube a git.

**Órdenes:**

```
notepad opencode.json
git add opencode.json
git commit -m "Añade opencode.json con los permisos del proyecto"
git push
git log --oneline
```

**Qué pasó:** `git status` mostró `ahead of 'origin/main' by 1 commit` (mi ordenador iba un commit
por delante de GitHub). Tras `git push`, el log mostró `(HEAD -> main, origin/main)` en `3af269e`.
Llevo **2 commits de los 10** que pide el proyecto.

Reglas principales del `opencode.json`: `edit` y `webfetch` preguntan siempre; no puede leer `.env`;
`git push`, `git reset`, `rm` y `sudo` están prohibidos; `git commit` pregunta.

**Conclusión:**
✏️ CONCLUSIÓN 10 (escríbela tú): ¿por qué es buena idea que el agente tenga `git push` y `rm` prohibidos
y que no pueda leer el `.env`? ¿Qué diferencia hay entre `ask`, `allow` y `deny`?

---

## Paso 11 · Typer, ajustes del proyecto y tercer commit (1 nov)

**Qué quería:** dejar el proyecto preparado para que OpenCode construya las órdenes, siguiendo la
página de la Sesión 1 del curso.

**Órdenes y cambios:**

```
uv add typer
notepad pyproject.toml        # description y tareas = "tareas.cli:app"
notepad src\tareas\__init__.py  # solo la versión
notepad .gitattributes        # una línea: * text=auto
git add pyproject.toml uv.lock src/tareas/__init__.py .gitattributes
git commit -m "..."
git push
```

**Qué pasó:** `uv` creó el entorno `.venv` con Python 3.12 e instaló Typer 0.27.3 y Rich 15.0.0.
El `git status` mostró 4 cambios y **no** mostró `.venv` (el `.gitignore` lo esconde).
El push subió el commit `211181d`. Llevo **3 commits de los 10** que pide el proyecto.

Nota para la próxima vez: mi mensaje tenía una errata (`.gitattibutes`) y estaba en pasado.
Como ya está subido, no lo toco; en los siguientes empiezo con un verbo: «Añade...», «Configura...».

**Conclusión:**
✏️ CONCLUSIÓN 11 (escríbela tú): ¿qué es Typer y para qué lo necesito?
¿Qué dice la línea `tareas = "tareas.cli:app"` del `pyproject.toml`?
¿Para qué sirve el `.gitattributes`?

---

## Paso 12 · Carpeta de pruebas (1 nov)

**Qué quería:** tener ficheros de mentira para probar la herramienta sin tocar mis ficheros reales.

**Qué hice:** copié en PowerShell el bloque de la página de la Sesión 1 que crea `~\pruebas-tareas`
con 3 PDF (uno con espacios), un `.docx`, 5 `.tmp` (dos con fecha de septiembre), 3 imágenes en
`fotos` y un `notas.txt` en `docs`. Está **fuera** del repo.

**Qué pasó:** el `Get-ChildItem` mostró todos los ficheros esperados.

**Conclusión:**
✏️ CONCLUSIÓN 12 (escríbela tú): ¿por qué se prueba siempre en `~\pruebas-tareas` y con `--simular`,
y nunca con mis carpetas reales?

---

## Paso 13 · La spec en el README y cuarto commit (1 nov)

**Qué quería:** escribir yo, sin IA, qué herramienta quiero, para que el agente construya lo mío.

**Qué hice:** rellené los huecos de la plantilla: mi problema (ordenar las fotos recuperadas del
móvil y renombrarlas por fecha), para quién (para mí y para mi mujer) y mis 3 acciones
(mover fotos de `Backup Movil` a `Fotos2026/fecha`, renombrar con la fecha, borrar `.tmp` de la
carpeta indicada). Corregí con ayuda: una errata, una acción demasiado peligrosa (borrar en la
carpeta de Windows) y el "lugar", que dejé fuera por ser difícil de sacar.

**Qué pasó:** mi primer intento de commit falló: escribí `git add readme.md` (minúsculas) y el
fichero se llama `README.md`. **Git distingue mayúsculas** aunque Windows no, así que no añadió nada
(`no changes added to commit`) y `git push` dijo `Everything up-to-date`. Repetí con el nombre exacto.
Commit `adcf612`, subido. Llevo **4 commits de los 10**.

**Conclusión:**
✏️ CONCLUSIÓN 13 (escríbela tú): ¿por qué es importante escribir yo la spec y no el agente?
¿Qué me enseñó el error de `readme.md` frente a `README.md`?

---

## Paso 14 · Los documentos entran en el repo (1 nov)

**Qué quería:** que `docs/prompts.md` (lo pide el profesor) y este diario viajen con el repo.

**Qué hice:** descargué los dos ficheros, creé la carpeta `docs` y los moví ahí. Antes del commit
comprobé que no tenían ninguna clave. Commit `67a401c`, subido.

**Qué pasó:** en git solo existe lo que se guarda con un commit. Mientras no lo hice, los ficheros
estaban en mi carpeta pero ni en el historial ni en GitHub. Llevo **5 commits de los 10**.

**Conclusión:**
✏️ CONCLUSIÓN 14 (escríbela tú): ¿por qué hay que hacer un commit para que algo "exista" en git?
¿Por qué no hace falta un commit por cada fichero?

---

## Paso 15 · El `AGENTS.md`: las normas del agente (1 nov)

**Qué quería:** dejar escritas, para OpenCode, las normas del proyecto. Lo lee al empezar cada sesión.

**Qué hice:** creé `AGENTS.md` en la raíz con la plantilla del curso (stack, órdenes y normas), la
leí línea a línea y añadí una norma mía sobre no borrar fotos sin permiso. Commit `f0980c2`,
subido. Llevo **6 commits de los 10**.

**Conclusión:**
✏️ CONCLUSIÓN 15 (escríbela tú): ¿qué es `AGENTS.md` y qué diferencia hay con `opencode.json`?
¿Qué norma he añadido yo y por qué?

---

## Paso 16 · Sin agente del instituto: modelo gratuito (2 nov)

**Qué quería:** poder usar OpenCode aunque el profesor no pueda darme acceso a los modelos del centro.

**Qué pasó:** el profesor me contestó que no hay VPN a los servidores de IA (prohibido por ley) y que
desde casa se usa OpenCode con modelos *free* (o el Copilot de Conselleria, que es solo para consultas).
`opencode models` me listó los modelos `opencode/...-free`. Probé:

```
opencode run --model opencode/big-pickle "Responde solo: hola"
```

y contestó `hola`. Después puse `opencode/big-pickle` como modelo por defecto en mi config global
(`%USERPROFILE%\.config\opencode\opencode.json`, que está **fuera** del repo).

Importante: con los modelos gratuitos mis mensajes se guardan en un servidor de terceros, así que
nunca les paso claves ni datos personales.

**Conclusión:**
✏️ CONCLUSIÓN 16 (escríbela tú): ¿qué diferencia hay entre el modelo del centro y uno gratuito?
¿Qué cuidados tengo con los datos?

---

## Paso 17 · acciones.json: mis dos primeras acciones (2 nov)

**Qué quería:** escribir yo, sin IA, las acciones de mi herramienta.

**Qué hice:** creé `acciones.json` con `borrar-temporales` (tipo `borrar`, `.tmp` de más de 30 días,
`confirmar: true`) y `renombrar-fotos` (tipo `renombrar`, con una `plantilla` con contador y fecha).
Fui corrigiendo: dos puntos que faltaban, `true` sin comillas, nombres en minúsculas con guion,
el `tipo` en español y la `plantilla` obligatoria en `renombrar`.

**Qué pasó:** subí `acciones.json` con un fallo: faltaban comas entre los elementos de la lista de
extensiones. Lo detecté con `Get-Content acciones.json | ConvertFrom-Json` (daba *Se esperaba ','*).
Lo corregí en un commit nuevo (`1ff9728`) sin tocar el historial. Llevo **9 commits de los 10**.
Otra vez me pasó que el fichero estaba **sin guardar** (Ctrl+S) y por eso daba error.

**Conclusión:**
✏️ CONCLUSIÓN 17 (escríbela tú): ¿por qué hay que comprobar el JSON antes del commit?
¿Qué cosas pasan con las comas y las comillas en JSON?

---

## Paso 18 · La tercera acción y el undécimo commit (6 nov)

**Qué quería:** tener mis tres acciones escritas en `acciones.json`.

**Qué hice:** escribí `mover-fotos` (tipo `mover`, con `filtro` de extensiones y `destino`).
Al principio copié campos de `renombrar-fotos` que sobraban: `plantilla` es solo para `renombrar`
y `confirmar` solo para acciones que borran. Mover necesita `destino`.

**Qué pasó:** otra vez faltaba una **coma** entre dos acciones (`},` y `{`) y la comprobación
dio *Se esperaba ','*. La puse, comprobé de nuevo y subí el commit `450ddb3`.
Llevo **11 commits**.

**Conclusión:**
✏️ CONCLUSIÓN 18 (escríbela tú): ¿qué campos necesita cada tipo de acción
(`mover`, `renombrar`, `borrar`)? ¿Por qué `confirmar` solo va en las que borran?

---

## Paso 19 · El ADR y esta guía (7 nov)

**Qué quería:** escribir mi primer ADR y entender los conceptos que me faltaban.

**Qué hice:** escribí un borrador del ADR-0001 en `docs/adr/`. Me señalaron que el contexto debe
hablar de mis fotos, que las alternativas se comparan por *dónde viven las acciones* y que
las consecuencias deben incluir lo que me pasó con las comas. Aún lo estoy corrigiendo.
Además tengo una guía nueva, `docs/guia-conceptos.md`, que explica cada herramienta y cada
fichero con palabras sencillas.

**Conclusión:**
✏️ CONCLUSIÓN 19 (escríbela tú): ¿qué es un ADR y por qué es **uno** y no uno por acción?

---

## Lo que viene después

- Corregir y subir el ADR (commit)
- Skill `acciones-json` y comando `/nueva-accion` en `.opencode/` (commits)
- Subagente `revisor` (cuando el profesor aclare la versión de OpenCode)
- Que el agente construya `cli.py` (`--help`, `version`, `listar`) y yo audite cada cambio
- Validación y motor con `--simular`
- Preguntar al profesor qué versión de OpenCode hay que usar (1.18.35 o la 2)
