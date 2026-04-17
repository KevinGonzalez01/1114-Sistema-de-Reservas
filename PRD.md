# Sistema de Reservas
Proyecto: Sistema de Reservas
---
Equipo: 
- Lider: Kevin Gonzalez
- Colaborador 1: Alejandro Lopez
- Colaborador 2: David Cuero
- Fecha: 16/04/2026 
- Grupo: 1114
---
1. Descripción del Proyecto

¿Cuál es el problema?

Un pequeño hotel necesita un sistema para controlar las reservas.

¿Quién lo tiene?

Gerente de reservas

¿Por qué es importante?

- Un sistema de reservas es fundamental para el buen funcionamiento de un hotel.

- Permite organizar la disponibilidad de habitaciones y evitar errores como sobreventas.

- Ayuda a maximizar los ingresos al gestionar mejor la ocupación.

- Facilita a los clientes reservar de forma rápida y segura, incluso en línea.

- Mejora la experiencia del huésped desde el primer contacto con el hotel.

- Proporciona datos útiles para la toma de decisiones estratégicas.

En general, aumenta la eficiencia, competitividad y rentabilidad del hotel.

---
2. Roles y Responsabilidades
- Lider: Une los trabajos de los colaboradores a la rama principal y crea el python
- Colaborador 1: Crea el css y el java script
- Colaborador 2: Crea el HTML
---
3. Requisitos Funcionales
- Registrar una reserva (cliente, fecha, hora, duración)
- Ver qué horarios están disponibles
- Impedir doble-booking
- Cancelar una reserva
- Ver todas las reservas del día
- Buscar reserva por cliente o fecha
---
4. Requisitos No Funcionales
- Facil de usar: Un gerente en computadora debe entender
- Seguro: Información no se pierde si apagamos la computadora
- Organizado: Se organiza por año, mes, dia y hora de llegada y salida
- Rapido: Registrar una reserva en menos de 5 min
- Confiable: No permite errores de fechas ni de pagos
---
5. Casos de Uso

Caso 1: Reserva al contado:

El cliente reserva una habitación por $100.000 la noche.

El sistema registra el pago inmediato y confirma la reserva.

No se genera ninguna deuda pendiente.

Caso 2: Reserva fiada:

El cliente reserva 2 noches a $80.000 cada una.

El sistema calcula el total: $160.000 y lo deja como saldo por pagar.

La reserva queda confirmada, pero con deuda registrada.

Caso 3: Pago de reserva: El cliente realiza un abono de $60.000.

El sistema actualiza el saldo pendiente a $100.000.

---
6. Datos Principales


| DATO | TIPO | EJEMPLO |
| :--- | :---: | ---: |
| Habitacion | Texto | Habitacion VIP |
| Cantidad | Número | 2 |
| Precio | Numero | $ 500.000 |
| Cliente | Texto | David Esteba |
| Tipo de pago | Opciones | Efectivo o Tarjeta |

---
7. Criterios de Éxito

