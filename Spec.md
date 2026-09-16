#Sistema de Reservas para Hotel

## 1. ¿Qué es esto?

Un sistema para que las personas puedan reservar una habitación de hotel desde la página web, ver si hay disponibilidad y pagar.

## 2. ¿Qué debe poder hacer? (Requisitos funcionales)

1. El usuario elige fecha de entrada y fecha de salida.
2. El sistema muestra qué habitaciones están disponibles en esas fechas.
3. El usuario elige una habitación y ve el precio total.
4. El usuario llena un formulario con sus datos (nombre, correo, teléfono).
5. El usuario confirma la reserva.
6. El sistema guarda la reserva y muestra un mensaje de "reserva exitosa" con un número de confirmación.
7. (Opcional) El sistema envía un correo de confirmación.

## 3. ¿Qué NO va a hacer?

- No va a procesar pagos reales con tarjeta.
- No va a tener panel de administrador.
- No va a manejar varios idiomas.

## 4. Tipos de habitación

| Tipo | Precio por noche | Capacidad |
|---|---|---|
| Sencilla | $150.000 | 2 personas |
| Doble | $220.000 | 3 personas |
| Suite | $400.000 | 4 personas |

## 5. Datos que necesito guardar

**Habitación:** id, tipo, precio, disponible (sí/no)

**Reserva:** id, nombre del cliente, correo, fecha de entrada, fecha de salida, habitación elegida, precio total

## 6. Pasos del usuario 

1. Inicio
2. Elegir fechas
3. Ver habitaciones disponibles
4. Elegir una habitación
5. Llenar formulario con datos personales
6. Confirmar reserva
7. Mostrar mensaje de éxito

## 7. Reglas simples que debe cumplir

- La fecha de salida tiene que ser después de la fecha de entrada.
- No se puede reservar una habitación que ya está ocupada en esas fechas.
- Todos los campos del formulario son obligatorios.

## 8. Con qué lo voy a construir

- HTML
- CSS
- JavaScript
- SQLite

## 9. Ideas para mejorar después
- Agregar login de usuario.
- Agregar panel para que el hotel vea todas las reservas.
- Conectar con una pasarela de pago real.
