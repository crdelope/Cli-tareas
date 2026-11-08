---
name: acciones-json
description: Reglas para escribir o modificar acciones en acciones.json. Úsala siempre que se añada o cambie una acción.
---

## Campos de cada acción
- `nombre`: el nombre de la acción se escribe sin espacios, solo se separa con un guión. Por ejemplo, `borrar-temporales`. Obligatorio.
- `descripcion`: define qué se va a hacer con los archivos. Obligatorio.
- `tipo`: lo que hace la acción. Solo puede valer una de estas palabras, en minúsculas: `mover`, `copiar`, `renombrar` o `borrar`. Obligatorio.
- `filtro`: elige qué archivos se tocan. Opcional. Puede llevar: 
    - `extensiones`: lista de extensiones, con el punto y entre comillas, por ejemplo `[".jpeg", ".png"]`.
    - `mas_antiguo_que_dias`: Archivos con más de N días de antigüedad, por ejemplo `30`.
    - `patron`: El nombre del archivo debe encajar con esta expresión regular, por ejemplo: `"^captura.*\\.png$"`.
    - `mayor_que_mb`: El archivo debe de pesar más que N MB, por ejemplo `2`.

## Campos según el tipo
- `destino`: la carpeta a la que van los archivos, por ejemplo `"~/pruebas-tareas/Fotos2026"`. Obligatorio si el tipo es `mover` o `copiar`. No se usa en los otros tipos.
- `plantilla`: cómo queda el nombre nuevo del archivo, por ejemplo `"foto-{n:03}_{fecha:%Y-%m-%d}{ext}"`. Obligatorio si el tipo es `renombrar`. Lleva estos huecos:
    - `{fecha:%Y-%m-%d}`: ...
    - `{n:03}`: ...
    - `{ext}`: ...
    - `{nombre}`: ...
- `confirmar`: ...

## Reglas del JSON
- Los textos van entre comillas.
- `true` y `false` van sin comillas.
- Entre un campo y el siguiente va una coma; en el último no.
- Entre una acción y la siguiente va una coma.
- Una lista lleva los elementos separados por comas: `[".jpg", ".jpeg", ".png"]`.
- Los nombres de los campos se escriben exactamente como en esta lista, sin tildes.

## Ejemplo
```json
{
  "nombre": "mover-fotos",
  "descripcion": "mueve las fotos a la carpeta Fotos2026",
  "tipo": "mover",
  "filtro": { "extensiones": [".jpg", ".jpeg", ".png"] },
  "destino": "~/pruebas-tareas/Fotos2026"
}
```