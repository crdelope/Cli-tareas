# tareas

Mi herramienta de línea de órdenes para automatizar tareas repetitivas con ficheros.

## Spec (versión 0 · 01/11/2026)
1. **Problema:** cada semana pierdo tiempo en ordenar las fotos recuperadas del móvil y cambiar el nombre por fecha.
2. **Para quién:** para mí y para mi mujer.
3. **Cómo se usa:** `tareas ORDEN [CARPETA] [opciones]` desde cualquier terminal.
4. **Órdenes de la semana 1:** `tareas --help`, `tareas version`, `tareas listar [CARPETA]`.
5. **Órdenes previstas:** `tareas acciones`, `tareas validar`, `tareas ejecutar NOMBRE --simular`.
6. **Mis 3 acciones (borrador):** Mover fotos de carpeta Backup Movil a Fotos2026/fecha de cada foto, renombrar las fotos con la fecha de la foto, Borrar los ficheros .tmp de la carpeta que se le indique.
7. **Nunca hará:** borrar sin preguntar ni tocar ficheros fuera de la carpeta que le indique.
8. **Plataformas:** Windows (es el mío); también Linux y macOS.
9. **Códigos de salida:** 0 bien · 1 fallo al ejecutar · 2 uso incorrecto · 3 configuración inválida.
10. **Instalación:** `uv tool install --editable .` (lo completo en la semana 4).