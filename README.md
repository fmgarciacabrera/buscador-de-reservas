# Buscador de reservas

Mi primera aplicación web Django, un pequeño motor de reservas para un hotel imaginario.

## TODO

El tema pendiente más importante es la validación del formulario de reservas: evitar que la fecha de llegada sea posterior a la de salida, la fecha de salida debe ser al menos el día siguiente de la llegada, etcétera.
* validación jQuery en el lado del cliente: en el evento `onSelect` de la fecha de llegada actuar sobre el campo fecha de salida, actualizando su propiedad `minDate`, modificando la fecha seleccionada si fuere menester, ...
* validación del formulario en el servidor: implementar la validación de los datos del formulario recibido utilizando las herramientas que proporciona el framework Django.
