# ADR-0001: Las acciones viven en acciones.json, no en el código

- Estado: aceptada
- Fecha: 2026-11-06
- Autor: Carlos Ruiz de Lope Clement

## Contexto
Mi herramienta automatiza tareas repetitivas y muy tediosas, algo que no queremos hacer o que en realidad nos dejamos mucho tiempo en hacerlo.
Son acciones como mover ficheros, renombrar archivos, borrar temporales, etc. Mis primeras acciones van a ser eliminar temporales,
renombrar fotos recogidas del móvil a modo de backup, con la fecha de la foto y moverlas a la carpeta Fotos2026.
En el futuro mi mujer y yo vamos a querer tareas nuevas y mi mujer no sabe programar Python.  

## Decisión
Las acciones se describen en un fichero externo (acciones.json). El agente puede consultarlo para realizar las tareas. El código sólo contiene el motor que lo lee y lo ejecuta. Añadir una acción es editar el JSON, se hizo porque así mi mujer puede añadir una acción, editando un texto, sin programar Python.

## Alternativas consideradas

1. Escribir cada acción como una función en Python.
   
   - A favor: Con Python se puede programar más ampliamente sin los límites del JSON.
   - En contra: Hay que saber programar en Python y no todo el mundo sabe, en cada acción nueva hay que tocar el código. 
                
2. Hacer que una IA lo programe por mí.

   - A favor: Me quita un montón de quebraderos de cabeza y el agente automatiza la tarea, es capaz de modificar el JSON y programar todo.
   - En contra: Hace que yo no tenga el control absoluto, el agente toma decisiones a la hora de programar.

## Consecuencias

- Positivas: El archivo acciones.json es el índice de las acciones que quiero realizar, si quiero ampliar sólo implemento aquí.
- Negativas: Las acciones hay que pensarlas bien previamente. Hay que validar el JSON antes de ejecutar, por si me equivoco al escribirlo. Si me olvido de una coma, el JSON no funciona hasta que lo arregle.
 	
- Qué haré si el esquema cambia: Modificar mis acciones y ampliar si es conveniente. Si añado un campo nuevo, tengo que revisar las acciones que ya existen y actualizarlas.
