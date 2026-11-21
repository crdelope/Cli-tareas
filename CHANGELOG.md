# Cambios

Todos los cambios importantes de este proyecto se anotan aquí. El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [1.0.0] - 2026-11-21

Primera versión completa.

### Añadido

- Comando `tareas` con `--help`, `version`, `listar`, `ejecutar NOMBRE CARPETA` y `comprobar-ia`.
- Acciones definidas en `acciones.json`, validadas al cargar, con mensajes de error en español.
- Acción `mover`: mueve los ficheros que cumplen el filtro y nunca sobrescribe.
- Acción `renombrar`: renombra con una plantilla (`{n:03}`, `{fecha:%Y-%m-%d}`, `{ext}`, `{nombre}`) y pregunta una sola vez.
- Acción `borrar`: exige un filtro, enseña la lista y pregunta siempre antes de borrar.
- Acción `resumir`: resume ficheros de texto con una IA y guarda el resumen junto al original, sin pisar nada.
- Opción `--simular`: enseña lo que haría sin cambiar nada y sin llamar a la IA.
- Capa de IA con configuración en variables de entorno (`.env`, con `.env.example` como plantilla) y errores claros con el código de salida 4.
- Códigos de salida: 0 todo bien, 1 fallo al ejecutar, 2 uso incorrecto, 3 configuración inválida, 4 IA no disponible.
- 29 pruebas con pytest que no usan la red ni tocan los archivos del usuario.
- Documentación: `README.md`, decisión de diseño en `docs/adr/`, prompts y diario del proyecto.

### Pendiente para versiones futuras

- La acción `clasificar` ya se valida en `acciones.json`, pero todavía no se ejecuta.
- El tipo `copiar` está previsto y aún no funciona.