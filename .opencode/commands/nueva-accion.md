---
description: Añade una acción nueva a acciones.json
agent: plan
---

Quiero añadir esta acción a acciones.json: $ARGUMENTS

Sigue estos pasos:
1. Lee acciones.json y la skill acciones-json.
2. Propón la acción nueva con todos sus campos, sin escribir nada todavía.
3. Muéstrame cómo quedaría el JSON y espera a que yo diga que sí.
4. Cuando yo lo apruebe, añádela a acciones.json y valida el archivo con: Get-Content acciones.json | ConvertFrom-Json
5. No borres ningún archivo ni carpeta sin pedirme permiso antes.
6. No toques ningún otro archivo ni el código de src/.