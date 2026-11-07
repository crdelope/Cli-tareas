# Guía para entender mi proyecto «tareas»

Hecha para mí, que empiezo desde cero. Palabras sencillas y ejemplos de casa.
Este documento explica **qué es cada cosa y para qué sirve**. El `diario.md` cuenta
**qué órdenes escribí y qué pasó**; esta guía cuenta **por qué**.

> Si algo de aquí no se entiende, no es que yo sea torpe: hay muchas cosas nuevas a la vez.
> Marco con ✏️ las dudas que me queden para preguntarlas.

---

## 1. La idea en una frase

Estoy construyendo una **herramienta de terminal** llamada `tareas`. Con una sola orden escrita
hará por mí lo que hoy hago a mano con mis ficheros: mover fotos, renombrarlas con la fecha y
borrar ficheros temporales.

Un ejemplo de casa: **el mando de la tele**. El fabricante programa una vez lo que hace cada
botón, pero qué canal hay en el botón 1 lo decido yo en un menú, sin abrir el aparato.
Con mi herramienta pasa igual:

- El **programa** (el motor) sabe hacer cosas: mover, renombrar, borrar.
- El **menú** es un fichero (`acciones.json`) donde yo apunto qué acciones quiero y con qué ficheros.
- Un **ayudante de IA** me ayuda a escribir el programa, pero **yo decido y reviso todo**.

---

## 2. El mapa: cómo encaja todo

```
 Yo, en la terminal  ──►  programa "tareas"  ──►  lee acciones.json  ──►  toca mis ficheros
 (PowerShell)             (Python + Typer)        (mi menú de acciones)    (primero, los de prueba)

 Alrededor, para trabajar bien:
   git + GitHub  → guardan el historial de mi proyecto (el álbum de fotos)
   OpenCode      → el ayudante de IA que escribe código con mi permiso
   docs/         → mi diario, mis prompts y esta guía
```

Mi herramienta todavía **no está terminada**. Hasta ahora he montado el taller y escrito el menú.

---

## 3. Las herramientas: qué es cada una

| Herramienta | Qué es, con un ejemplo de casa | Para qué la uso |
|---|---|---|
| **Terminal / PowerShell** | Hablar con el ordenador **por escrito** en lugar de con el ratón. Escribo una orden, pulso Intro y me contesta. | Para instalar, crear y probar todo el proyecto. |
| **Comando** | Una orden con nombre (`git`, `uv`, `dir`, `tareas`). | Cada cosa que escribo en la terminal es un comando. |
| **PATH** | La **lista de carpetas** donde Windows busca los comandos. Como la agenda del móvil: si guardas un contacto nuevo, la copia impresa vieja no lo incluye. | Por eso, tras instalar algo hay que **cerrar y abrir PowerShell**. |
| **Python** | El **lenguaje** en el que escribiré mi programa (como el castellano en el que escribes una carta). | Es el idioma del proyecto. Pide la versión 3.12. |
| **uv** | El **gestor del proyecto**: crea la carpeta con su estructura, instala Python 3.12 y las librerías. Como un carpintero que te monta la estantería con todas las baldas. | `uv init`, `uv add`, `uv run`. |
| **Typer** | Una **librería** (código ya hecho que otros escribieron) para crear órdenes de terminal. Genera la ayuda `--help` sola. | Con Typer haré `tareas --help`, `tareas version`... |
| **Node.js y npm** | Un programa y su instalador. Como el repartidor que sabe traer paquetes. | Solo los necesito para **instalar OpenCode**. |
| **git** | Una **máquina del tiempo** para mi proyecto: guarda fotos (commits) de cómo estaba en cada momento. | Para guardar mi trabajo y volver atrás si algo sale mal. |
| **GitHub** | Una web donde se sube mi proyecto. Es el **álbum de fotos en internet**. | Mi repo es **público** (lo pide el proyecto) y lo ve el profesor. |
| **OpenCode** | El **ayudante de IA**, que vive en la terminal. Lee mi proyecto, propone cambios y, si yo le dejo, los hace. | Para escribir el programa con mi supervisión. |

---

## 4. Git y GitHub: el álbum de fotos

Imagina que mi proyecto es mi habitación y git es un fotógrafo que **solo hace fotos cuando se lo
pido**.

| Palabra | Qué es | Orden |
|---|---|---|
| **Repositorio (repo)** | La carpeta del proyecto **con** su álbum de fotos. | `git init` (lo hizo `uv`) |
| **Commit** | Una **foto** del proyecto en ese momento, con una **etiqueta** que cuenta qué hice. | `git commit -m "mensaje"` |
| **git add** | **Meter en la caja** lo que saldrá en la foto. Aún no está hecha. | `git add fichero` |
| **git status** | **Mirar la caja** antes de cerrar: qué entra, qué no. | `git status` |
| **git log --oneline** | Ver el **álbum**: la lista de fotos con sus etiquetas. | `git log --oneline` |
| **push** | Mandar mis fotos al **álbum de internet** (GitHub). | `git push` |
| **origin** | El **apodo** de la dirección del repo en GitHub. | (se puso una vez) |
| **main** | El nombre de la **línea principal** de mi proyecto. | — |
| **.gitignore** | La lista de cosas que **no se fotografían**. | (es un fichero) |
| **.gitattributes** | Una nota para que Windows y Linux guarden igual los saltos de línea. | (es un fichero) |

**Por qué hace falta un commit para que algo "exista".** Si cambio algo pero no hago foto, ni mi
historial ni GitHub lo saben. Solo existe lo que he guardado con un commit.

**Un buen mensaje de commit** responde a *"¿qué acabo de hacer?"*. Empieza con un verbo
("Añade...", "Crea...", "Corrige...") y se entiende sin ver el código.

**Regla de oro de git:** nunca se reescribe lo que ya está subido. Si me equivoco, lo **arreglo con
un commit nuevo**, y así el historial cuenta lo que pasó de verdad.

---

## 5. Los ficheros de mi proyecto: qué hace cada uno

```
cli-tareas/
├─ acciones.json       ← mi MENÚ de acciones (lo escribo yo)
├─ README.md           ← la portada del proyecto: qué es y cómo se usa
├─ pyproject.toml      ← la ficha del programa: nombre, versión, librerías, comando
├─ uv.lock             ← las versiones EXACTAS de todo lo instalado
├─ .python-version     ← qué Python usa el proyecto (3.12)
├─ .venv/              ← el entorno: Python y librerías de ESTE proyecto (no se sube)
├─ .gitignore          ← lo que git NO debe subir (.venv, .env...)
├─ .gitattributes      ← saltos de línea iguales en todos los sistemas
├─ opencode.json       ← las NORMAS de permisos para el ayudante de IA
├─ AGENTS.md           ← las normas del proyecto que el ayudante lee siempre
├─ src/tareas/
│   └─ __init__.py     ← convierte la carpeta en un paquete; guarda la versión
└─ docs/
    ├─ diario.md       ← qué hice, con qué órdenes
    ├─ prompts.md      ← los mensajes importantes que le doy a la IA
    ├─ guia-conceptos.md ← esta guía
    └─ adr/            ← el ADR (por qué tomé una decisión)
```

Aún **no existen** (los hará el agente o los escribiré después): `cli.py`, `config.py`,
`motor.py`, `acciones.py`, `errores.py`, y la carpeta `.opencode/` con la skill, el comando
y el subagente.

**Dos ficheros "de secretos":**

- **`.env`:** un fichero pequeño donde se guardan **claves** (el PIN del móvil). **Todavía no
  existe**, y está en el `.gitignore` para que **nunca** se suba a GitHub.
- **Variables de entorno:** otra forma de guardar una clave en el ordenador, **sin ponerla en
  ningún fichero del proyecto**.

Por qué tanto cuidado: si una clave llega a un commit, se queda en el historial **aunque la
borre después**. Por eso el proyecto exige que no haya ninguna en el repo ni en su historial.

---

## 6. acciones.json: mi menú

**JSON** es una forma de escribir información en un fichero de texto, con reglas muy estrictas
(como rellenar un formulario). Un ejemplo de mi menú:

```json
{
  "version": 1,
  "acciones": [
    { "nombre": "mover-fotos",
      "descripcion": "Mueve las fotos a la carpeta Fotos2026",
      "tipo": "mover",
      "filtro": { "extensiones": [".jpg", ".jpeg", ".png"] },
      "destino": "~/pruebas-tareas/Fotos2026" }
  ]
}
```

**Qué significa cada campo:**

| Campo | Qué dice | Ejemplo |
|---|---|---|
| `version` | Qué forma tiene el formulario. Si un día cambia, se sube a 2. | `1` |
| `acciones` | La lista de acciones. | `[ ... ]` |
| `nombre` | Cómo la llamo al ejecutarla. Minúsculas y guiones. | `mover-fotos` |
| `descripcion` | Una frase para alguien que no soy yo. | `Mueve las fotos...` |
| `tipo` | El **verbo**: `mover`, `copiar`, `renombrar` o `borrar`. | `mover` |
| `filtro` | **Qué ficheros** se tocan (por extensión, por antigüedad...). | `{ "extensiones": [".jpg"] }` |
| `destino` | **A dónde** van (solo para mover o copiar). | `~/pruebas-tareas/Fotos2026` |
| `plantilla` | Cómo queda el nombre nuevo (solo para renombrar). | `foto-{n:03}_{fecha:%Y-%m-%d}{ext}` |
| `confirmar` | Si pregunta antes de actuar (para acciones que **borran**). | `true` |

**Reglas de escritura del JSON** (donde más me he equivocado):

1. Los textos van **entre comillas**.
2. `true` y `false` van **sin comillas**.
3. Entre un campo y el siguiente va una **coma**; en el **último no**.
4. Entre una acción y la siguiente (`},` y `{`) va una **coma**.
5. Una lista lleva los elementos separados por comas: `[".jpg", ".jpeg", ".png"]`.
6. Guardar con **Ctrl+S** antes de comprobar (un fichero sin guardar está vacío para el programa).

**Cómo se comprueba que está bien** (esto es **validar**): 

```
Get-Content acciones.json | ConvertFrom-Json
```

Si no da error y enseña `version` y las acciones, el JSON es válido.

**Esquema:** la lista de campos que acepta el fichero. Como la plantilla de un formulario.

**Por qué las acciones van en un fichero y no dentro del programa:** porque para añadir o
cambiar una acción solo edito una línea, sin tocar el código ni reinstalar. (Es la decisión del
ADR.)

---

## 7. El ayudante de IA (OpenCode)

**Chat o agente.** Un *chat* contesta con texto y yo copio y pego. Un *agente* además puede
**leer mis ficheros, editarlos y ejecutar órdenes**, siempre que yo se lo permita.

**Modelo:** la "inteligencia" a la que habla OpenCode. Puede ser del instituto o uno
**gratuito** (el que uso ahora, `big-pickle`). Ojo: con los modelos gratuitos mis mensajes **se
guardan en un servidor ajeno**. Por eso nunca les paso claves ni datos personales.

**Los dos modos:**

- **plan:** el agente solo **piensa y propone**. No toca ficheros.
- **build:** el agente **hace** los cambios, pidiéndome permiso.

**Mi flujo de trabajo** (siempre el mismo):

1. **Yo** decido qué quiero y cómo sabré que está bien.
2. **plan:** le pido que me explique cómo lo haría.
3. **build:** le digo que lo haga, y **leo cada cambio** antes de aceptarlo.
4. **Yo** pruebo (en `~/pruebas-tareas` y con `--simular`).
5. **Yo** hago el commit (el agente tiene prohibido hacerlos).

**Los permisos** (`opencode.json`): para cada cosa, el agente tiene tres posibilidades.

| Permiso | Significa | Ejemplo en mi proyecto |
|---|---|---|
| `allow` | Lo hace sin preguntar. | Mirar carpetas, `git status`. |
| `ask` | Me pregunta antes. | Editar ficheros. |
| `deny` | Prohibido. | `git push`, `rm`, leer `.env`. |

**Cosas que le enseño al ayudante:**

- **`AGENTS.md`:** las normas del proyecto. Lo lee **siempre**, al empezar. Como la nota pegada
  en la nevera para quien te ayuda en casa.
- **Skill:** un fichero con conocimiento concreto (mi esquema de `acciones.json`) que el agente
  carga **solo cuando lo necesita**.
- **Comando propio** (`/nueva-accion`): un mensaje que repito mucho, guardado con un nombre.
- **Subagente (`revisor`):** otro agente que **solo mira** mi código y señala fallos. No puede editar.

**`/undo`** deshace lo último que hizo el agente, si me equivoco.

**Por qué reviso todo:** si el agente se equivoca y yo lo acepto, el fallo es mío. Lo que no sé
explicar, no lo entrego.

---

## 8. Cómo funcionará mi herramienta por dentro (lo que se construirá)

Cada fichero hará **una sola cosa**:

| Fichero | Su trabajo |
|---|---|
| `cli.py` | **Habla conmigo**: las órdenes (`--help`, `version`, `listar`, `ejecutar`...). |
| `config.py` | **Lee y comprueba** `acciones.json` antes de nada. Desconfía del fichero. |
| `motor.py` | **Elige** los ficheros que cumplen el filtro. |
| `acciones.py` | **Hace** el trabajo de cada tipo (mover, renombrar, borrar). |
| `errores.py` | Mis **errores propios**, con mensajes humanos en lugar de un traceback. |

La orden completa se lee como una frase:

```
tareas ejecutar mover-fotos ~/pruebas-tareas --simular
  │       │          │               │              └─ opción: enseña qué haría, sin tocar nada
  │       │          │               └─ argumento: sobre qué carpeta
  │       │          └─ argumento: qué acción (de acciones.json)
  │       └─ subcomando: qué hacer
  └─ el programa
```

**`--simular`** es mi red de seguridad: me enseña lo que haría **sin tocar ningún fichero**.
Siempre primero con `--simular`, y siempre en `~/pruebas-tareas`, nunca en mis fotos reales.

**Códigos de salida:** al terminar, el programa devuelve un número. `0` es que fue bien; otro
número es que falló: `1` error al ejecutar, `2` mal uso, `3` configuración inválida. Los scripts
deciden con eso si algo funcionó.

---

## 9. El ADR

**ADR** = *Architecture Decision Record*, un "registro de decisión". Es una nota corta que cuenta
**por qué** tomé **una** decisión importante. Sirve para quien llegue dentro de seis meses (a
veces, yo mismo) y se pregunte "¿por qué está hecho así?".

Mi decisión: **las acciones viven en `acciones.json`, no en el código**. Lleva cuatro partes:

1. **Contexto:** qué problema tengo.
2. **Decisión:** lo que decidí.
3. **Alternativas:** qué otras opciones había y qué tenían de bueno y de malo.
4. **Consecuencias:** lo bueno y lo malo que traerá mi decisión.

Es **un solo documento**, no uno por acción. Y lo escribo yo, porque en la defensa me
preguntarán por él.

---

## 10. Seguridad: mis cuatro normas

1. **Ninguna clave en el repo ni en el historial.** Van en variables de entorno o en `.env`.
2. **Probar siempre en `~/pruebas-tareas`**, con ficheros de mentira.
3. **Siempre `--simular` antes de ejecutar de verdad.**
4. **Copia de seguridad de mis fotos reales** antes de usar la herramienta con ellas.

---

## 11. Chuleta: las órdenes que ya uso

```
cd ~\cli-tareas                                  # ir a mi proyecto
dir                                              # ver qué hay en la carpeta
git status                                       # ver qué ha cambiado
git add fichero                                  # meter en la caja
git commit -m "Verbo + qué hice"                 # hacer la foto
git push                                         # subir a GitHub
git log --oneline                                # ver el álbum
Get-Content acciones.json | ConvertFrom-Json    # comprobar el JSON
uv add typer                                     # añadir una librería
opencode models                                  # ver los modelos
opencode run "texto"                             # probar el agente
```

---

## 12. Dónde estoy (7 de noviembre)

**Hecho:**
- El taller: `uv`, git, Node, OpenCode funcionando con un modelo gratuito.
- El proyecto en GitHub, público, con 11 commits.
- `.gitignore` con `.env`, `.gitattributes`, `opencode.json`, `AGENTS.md`, spec en el README.
- Mis **tres acciones** en `acciones.json` (borrar-temporales, renombrar-fotos, mover-fotos).
- Un borrador del ADR.

**Por hacer** (en este orden):
1. Terminar y subir el ADR.
2. La skill, el comando `/nueva-accion` y el subagente `revisor`.
3. El comando `tareas` con `--help`, `version` y `listar` (con el agente, revisando yo).
4. La validación y el motor con `--simular`.
5. Después: la capa de IA, las pruebas, el README de instalación y la versión 1.0.

**Pendiente de preguntar al profesor:** qué versión de OpenCode usar (1.18.35 o la 2).

---

## 13. Palabras raras, de la A a la Z

| Palabra | Quiere decir |
|---|---|
| **Argumento** | Un dato que le das a una orden (qué acción, qué carpeta). |
| **CLI** | Programa que se maneja escribiendo órdenes, sin ventanas. |
| **Diff** | Lo que cambia entre dos versiones: líneas añadidas y quitadas. Lo leo antes de aceptar. |
| **Entry point** | La línea de `pyproject.toml` que dice "cuando escriban `tareas`, ejecuta esto". |
| **Entorno virtual (`.venv`)** | Carpeta con Python y librerías solo de este proyecto. |
| **Flag / opción** | Un ajuste de una orden, como `--simular`. |
| **Librería** | Código ya hecho por otros que puedo usar (Typer). |
| **Markdown (`.md`)** | Texto con marcas sencillas (`#` para títulos). Lo usan README, diario y ADR. |
| **Motor** | La parte del programa que ejecuta las acciones. |
| **Paquete** | Una carpeta de código que Python puede instalar y usar. |
| **Prompt** | El mensaje que le escribo a la IA. |
| **Regex / patrón** | Una forma de describir nombres de fichero ("los que acaben en `.tmp`"). |
| **Spec** | La descripción de qué quiero construir, antes de construirlo. |
| **Traceback** | El mensaje feo de Python cuando algo falla. Mi herramienta no debe enseñarlo. |
| **Variable de entorno** | Un valor guardado en el ordenador (como una clave), fuera de los ficheros. |
