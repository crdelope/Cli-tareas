# tareas

Mi herramienta de línea de órdenes para automatizar tareas repetitivas con ficheros: mover fotos, renombrar fotos con la fecha del archivo y un formato específico (ejemplo: foto-001_2026-11-13.jpg), borrar temporales y resumir apuntes de texto con una IA, siempre dentro de las carpetas que le indico, y pide permiso para renombrar o borrar archivos.

Las acciones no están en el código, están en el archivo `acciones.json`, que podemos editar y actualizar siempre que queramos.

## Instalación

Necesitas [uv](https://docs.astral.sh/uv/) y Python 3.12.

```powershell
uv tool install git+https://github.com/crdelope/Cli-tareas@v1.0.0
tareas --help
```
Si ves la ayuda con los comandos, está bien instalado. Pendiente: la versión `v1.0.0` aún no está publicada.

> **Windows:** si después de instalar el comando `tareas` no se reconoce, ejecuta `uv tool update-shell` y abre una terminal nueva.

Para desarrollo, desde la carpeta del repositorio:

```powershell
uv tool install --editable .
```

## Configuración de la IA

Las acciones de tipo `resumir` usan un modelo de IA. Las demás (`mover`, `renombrar` y `borrar`) no la necesitan y funcionan sin conexión.

1. Crea un archivo llamado `.env` en la carpeta desde la que ejecutas `tareas`. Puedes copiar el `.env.example` del repositorio.
2. Rellena estas tres variables. Ejemplo con Groq (gratuito, compatible con la API de OpenAI):

   ```
   CENTRO_IA_URL=https://api.groq.com/openai/v1
   CENTRO_IA_KEY=tu-clave-personal
   CENTRO_IA_MODELO=openai/gpt-oss-120b
   ```

   Opcionalmente, `CENTRO_IA_CA` apunta a un certificado propio, solo si tu servidor lo necesita.

3. Comprueba que funciona:

   ```powershell
   tareas comprobar-ia
   ```

El archivo `.env` **no se sube a git**: está en el `.gitignore`. La clave no debe aparecer en ningún otro archivo del repositorio. Usa la IA solo con documentos de prueba.

Con `--simular` nunca se llama a la IA. Si la IA no está disponible (falta la clave, no hay conexión, la clave es rechazada o hay demasiadas peticiones), el programa lo explica en español y termina con el código 4. Las acciones sin IA siguen funcionando.

## Uso

`tareas` busca el archivo `acciones.json` en la **carpeta desde la que ejecutas el comando**. Copia el `acciones.json` del repositorio a tu carpeta de trabajo y ejecútalo desde ahí.

| Comando | Qué hace |
|---|---|
| `tareas --help` | Muestra la ayuda |
| `tareas version` | Muestra la versión |
| `tareas listar` | Lista las acciones de `acciones.json` |
| `tareas ejecutar NOMBRE CARPETA` | Ejecuta la acción NOMBRE sobre CARPETA |
| `tareas ejecutar NOMBRE CARPETA --simular` | Enseña lo que haría, sin cambiar nada |
| `tareas comprobar-ia` | Comprueba que la IA responde y que la clave del `.env` funciona |

Ejemplo, probando primero sin cambiar nada:

```powershell
tareas ejecutar mover-fotos ~/Fotos/Backup --simular
tareas ejecutar mover-fotos ~/Fotos/Backup
```

Y con la IA, para resumir apuntes:

```powershell
tareas ejecutar resumir-apuntes ~/Apuntes --simular
tareas ejecutar resumir-apuntes ~/Apuntes
```

Mira siempre primero con `--simular`.

## Las acciones (`acciones.json`)

Cada acción es una receta y hay que seguirla al pie de la letra: qué hacer, con qué ficheros y adónde. Estructura:

```json
{
  "version": 1,
  "acciones": [
    {
      "nombre": "mover-fotos",
      "descripcion": "mueve las fotos a la carpeta Fotos2026",
      "tipo": "mover",
      "destino": "~/Fotos2026",
      "filtro": { "extensiones": [".jpg", ".jpeg", ".png"] }
    },
    {
      "nombre": "resumir-apuntes",
      "descripcion": "Resume los apuntes de texto de la carpeta indicada",
      "tipo": "resumir",
      "instrucciones": "Resume el texto en cinco líneas, en español sencillo."
    }
  ]
}
```

| Campo | Obligatorio | Qué es |
|---|---|---|
| `nombre` | Sí | Único, en minúsculas y con guiones |
| `descripcion` | Sí | Texto que se ve en `listar`, todas las acciones programadas |
| `tipo` | Sí | `mover`, `renombrar`, `borrar` o `resumir`. `clasificar` se valida pero aún no se ejecuta, y `copiar` está previsto, aún no funciona |
| `destino` | Con `mover` | Carpeta a la que se mueven los ficheros |
| `plantilla` | Con `renombrar` | Nombre nuevo, con huecos `{n:03}`, `{fecha:%Y-%m-%d}`, `{ext}` y `{nombre}` |
| `confirmar` | Con `borrar` | `true` o `false` |
| `instrucciones` | Con `resumir` (con `clasificar`, opcional) | Lo que se le pide a la IA, por ejemplo «Resume el texto en cinco líneas» |
| `max_caracteres` | Opcional, con `resumir` y `clasificar` | Texto máximo que se envía a la IA, entre 500 y 50000. Por defecto, 12000 |
| `categorias` | Con `clasificar` | Lista de al menos dos categorías, que debe incluir `otros` |
| `filtro` | Opcional, **obligatorio con `borrar`** | Qué ficheros cuentan (ver abajo) |

Campos del `filtro` (todos opcionales; si pones varios, se tienen que cumplir **todos**):

- `extensiones`: lista, por ejemplo `[".jpg", ".png"]`. No distingue mayúsculas.
- `patron`: expresión regular sobre el nombre del fichero.
- `mas_antiguo_que_dias`: número de días desde la última modificación.
- `mayor_que_mb`: tamaño mínimo en megas.


### Qué hace cada tipo

- **mover:** mueve los ficheros de la carpeta que cumplan el filtro (sin entrar en subcarpetas) al `destino`. Crea el destino si no existe.
- **renombrar:** renombra en la misma carpeta con la `plantilla`. Numera desde 001 por orden de nombre y usa la fecha de modificación del fichero. Pregunta una sola vez antes de renombrar.
- **borrar:** borra de verdad los ficheros que cumplan el filtro (nunca carpetas). Enseña antes la lista y pregunta siempre.
- **resumir:** lee los ficheros de la carpeta (por defecto `.txt` y `.md`, o los que indique el filtro), manda a la IA el texto con las `instrucciones` de la acción y guarda el resumen en un fichero nuevo junto al original: `apuntes.txt` pasa a `apuntes.resumen.md`.
  - No modifica ni borra nunca el original.
  - Si el resumen ya existe, no lo pisa: crea `apuntes.resumen1.md`.
  - Salta los ficheros que no se pueden leer como UTF-8 y los que ya terminan en `.resumen.md`.
  - Con `--simular` no llama a la IA ni escribe nada: solo indica «enviaría N caracteres».
  - Si la IA falla a mitad, se detiene con el código 4 y conserva los resúmenes ya hechos.
- **clasificar:** el archivo `acciones.json` ya valida este tipo (con `categorias`, que debe incluir `otros`), pero **todavía no se ejecuta**. Se implementará en una versión posterior.

## Seguridad

- Con `--simular` no se cambia nada, no se pregunta y no se llama a la IA.
- **Nunca sobrescribe.** Si ya existe un fichero con ese nombre, al mover pregunta y, si aceptas, le añade un `1` antes de la extensión (`foto.jpg` pasa a `foto1.jpg`, y si también existe, `foto11.jpg` y así sucesivamente hasta resolver el problema).
- `borrar` siempre pide confirmación y no funciona sin filtro, para no vaciar una carpeta por error.
- `resumir` nunca modifica ni borra los ficheros originales.
- No guarda claves ni secretos en el repositorio. La clave de la IA va solo en el `.env`, que git ignora.

## Códigos de salida

| Código | Significado |
|---|---|
| 0 | Todo bien |
| 1 | Fallo al ejecutar (acción o carpeta inexistente, error de plantilla…) |
| 2 | Uso incorrecto (opción que no existe) |
| 3 | Configuración inválida (`acciones.json` mal escrito) |
| 4 | La IA no está disponible (sin clave, sin conexión, clave rechazada o límite de peticiones) |

## Pruebas

El proyecto tiene 29 pruebas con pytest. No usan la red ni tocan tus archivos: cada prueba trabaja en una carpeta temporal y la IA se sustituye por un proveedor falso.

```powershell
uv run pytest -v
```

## Cómo se ha hecho

El código se ha construido con un agente de IA (OpenCode), con prompts escritos por mí y revisando cada cambio antes de aceptarlo.

- `AGENTS.md`: reglas que sigue el agente.
- `docs/prompts.md`: los prompts que he usado y lo que revisé en cada uno.
- `docs/adr/`: decisiones de diseño, por ejemplo por qué las acciones viven en un JSON.
- `docs/diario.md`: el diario del proyecto.
- `.opencode/`: la skill del esquema de `acciones.json` y el comando `/nueva-accion`.
- `tests/`: las pruebas con pytest.


## Spec Original (versión 0 · 01/11/2026)
1. **Problema:** cada semana pierdo tiempo en ordenar las fotos recuperadas del móvil y cambiar el nombre por fecha.
2. **Para quién:** para mí y para mi mujer.
3. **Cómo se usa:** `tareas ejecutar NOMBRE CARPETA [--simular]` desde cualquier terminal.
4. **Órdenes de la semana 1:** `tareas --help`, `tareas version`, `tareas listar [acciones.json]`.
5. **Órdenes previstas:** `tareas acciones`, `tareas validar`, `tareas ejecutar NOMBRE --simular`.
6. **Mis 3 acciones (borrador):** Mover fotos de carpeta Backup Movil a Fotos2026/fecha de cada foto, renombrar las fotos con la fecha de la foto, Borrar los ficheros .tmp de la carpeta que se le indique.
7. **Nunca hará:** borrar sin preguntar ni tocar ficheros fuera de la carpeta que le indique.
8. **Plataformas:** Windows (es el mío); también Linux y macOS.
9. **Códigos de salida:** 0 bien · 1 fallo al ejecutar · 2 uso incorrecto · 3 configuración inválida.
10. **Instalación:** `uv tool install git+https://github.com/crdelope/Cli-tareas@v1.0.0`.