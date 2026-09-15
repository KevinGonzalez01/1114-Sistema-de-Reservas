#Sistema de Reservas — Hotel 5 Estrellas

## 1. Resumen y objetivo

Diseñar e implementar un sistema de reservas para un hotel de 5 estrellas que permita a los huéspedes:
- Consultar disponibilidad y tarifas en tiempo real.
- Reservar habitaciones, paquetes y servicios adicionales (spa, restaurante, eventos).
- Gestionar su reserva desde un portal de cliente (modificar, cancelar, ver historial).

Debe integrarse con el sitio ya existente (`Index.html`, `Habitaciones.html`, `Portal_de_clientes.html`, `biniestar_index.html`, `gastronomia_index.html`, `eventos_index.html`), manteniendo la identidad visual negro + dorado (`#aa7c11`).

## 2. Alcance

**Incluye:**
- Motor de disponibilidad y tarifas por tipo de habitación.
- Flujo de reserva (búsqueda → selección → datos del huésped → pago → confirmación).
- Gestión de reservas desde el Portal de Clientes.
- Panel administrativo interno (staff) para gestionar inventario, tarifas y reservas.
- Notificaciones por correo (confirmación, recordatorio, cancelación).

**Fuera de alcance (fase 1):**
- Integración con channel managers externos (Booking.com, Expedia) — se deja como fase 2.
- App móvil nativa.
- Sistema de fidelización/puntos (fase 2).

## 3. Actores del sistema

| Actor | Descripción |
|---|---|
| Huésped (guest) | Usuario que busca y reserva habitaciones/servicios |
| Cliente registrado | Huésped con cuenta en el Portal de Clientes |
| Recepción / Staff | Gestiona reservas, check-in/check-out, disponibilidad |
| Administrador | Configura tarifas, tipos de habitación, promociones, reportes |
| Pasarela de pago | Sistema externo que procesa el cobro |

## 4. Tipos de habitación y tarifas

Cada tipo de habitación debe modelarse con:
- `id`, `nombre` (ej. Suite Presidencial, Junior Suite, Deluxe, Estándar Superior)
- `capacidad_max` (adultos/niños)
- `descripcion`, `amenidades` (lista)
- `galeria_imagenes`
- `precio_base_noche`
- `inventario_total` (número de unidades)

**Tarifas dinámicas:**
- Tarifa por temporada (alta/media/baja), definida por rangos de fecha.
- Tarifas especiales por evento o promoción (código de descuento).
- Recargos por ocupación extra (huésped adicional, cama extra).
- Moneda base + posible multi-moneda (COP, USD) para huéspedes internacionales.

## 5. Flujo de reserva (huésped)

1. **Búsqueda:** fecha de llegada, fecha de salida, número de huéspedes (adultos/niños), tipo de habitación (opcional).
2. **Resultados:** lista de habitaciones disponibles con precio total, fotos, amenidades y política de cancelación.
3. **Selección:** el huésped elige habitación(es) y, opcionalmente, agrega servicios (desayuno, spa, transporte aeropuerto, decoración especial).
4. **Datos del huésped:** nombre completo, email, teléfono, país, solicitudes especiales (ej. piso alto, luna de miel).
5. **Pago:**
   - Opción de pago total o depósito (ej. 30% para garantizar reserva).
   - Integración con pasarela de pago (Wompi, PayU o Stripe — a definir según mercado colombiano).
   - Captura segura de tarjeta (nunca almacenar datos de tarjeta en el propio servidor; usar tokenización de la pasarela).
6. **Confirmación:** pantalla de confirmación + correo con número de reserva, resumen y política de cancelación/modificación.

### Validaciones clave
- Fecha de salida > fecha de llegada.
- No permitir reservar si no hay disponibilidad real (control de concurrencia para evitar overbooking).
- Ocupación no debe superar la capacidad máxima de la habitación seleccionada.
- Reintentar/expirar el "hold" de inventario si el pago no se completa en X minutos (ej. 15 min).

## 6. Modelo de datos (entidades principales)

```
Habitacion
- id, tipo_id, numero, piso, estado (disponible/mantenimiento/ocupada)

TipoHabitacion
- id, nombre, capacidad_max, precio_base, amenidades[], inventario_total

Tarifa
- id, tipo_habitacion_id, fecha_inicio, fecha_fin, precio_noche, motivo (temporada/promo)

Reserva
- id, codigo_reserva, cliente_id, tipo_habitacion_id, fecha_checkin, fecha_checkout,
  num_adultos, num_ninos, estado (pendiente/confirmada/cancelada/completada),
  monto_total, monto_pagado, servicios_adicionales[], solicitudes_especiales,
  fecha_creacion

Cliente
- id, nombre, email, telefono, pais, documento_identidad, historial_reservas[]

ServicioAdicional
- id, nombre, descripcion, precio, categoria (spa/restaurante/eventos/transporte)

Pago
- id, reserva_id, monto, metodo, estado, referencia_pasarela, fecha
```

## 7. Panel de administración (staff)

- **Calendario de disponibilidad:** vista tipo calendario/grid por tipo de habitación y fecha.
- **Gestión de reservas:** buscar, ver detalle, modificar fechas, cambiar de habitación, cancelar, marcar check-in/check-out.
- **Gestión de tarifas:** crear/editar rangos de temporada y precios.
- **Gestión de inventario:** poner habitaciones en mantenimiento (bloquear fechas).
- **Reportes:** ocupación (%), ingresos por periodo, ADR (tarifa promedio diaria), RevPAR.
- **Códigos promocionales:** crear descuentos por porcentaje o monto fijo, con fechas de validez.

## 8. Portal de clientes (`Portal_de_clientes.html`)

- Login/registro (email + contraseña, o magic link).
- Ver reservas activas y pasadas.
- Modificar fechas (sujeto a disponibilidad y política).
- Cancelar reserva (mostrar política de cancelación y posible penalidad).
- Descargar comprobante/factura en PDF.
- Agregar servicios adicionales a una reserva existente.

## 9. Notificaciones

| Evento | Canal | Contenido |
|---|---|---|
| Reserva confirmada | Email | Código, resumen, política |
| Recordatorio pre-llegada | Email (48h antes) | Info check-in, upgrades opcionales |
| Cancelación | Email | Confirmación y reembolso si aplica |
| Pago fallido | Email | Reintentar pago, link |

## 10. Políticas de negocio a definir con el hotel

- Política de cancelación (gratuita hasta X días antes, penalidad después).
- Edad mínima para reservar sin acompañante adulto.
- Política de niños (edad para "gratis" o tarifa reducida).
- Depósito de garantía vs pago total anticipado.
- Horarios de check-in/check-out y costos por early check-in / late check-out.

## 11. Requisitos técnicos

- **Frontend:** consistente con el sitio actual (HTML/CSS/JS plano), con el motor de reservas como módulo independiente que se pueda integrar en `Index.html` y `Habitaciones.html` vía JS (fetch a una API backend).
- **Backend:** API REST (o similar) que exponga endpoints de disponibilidad, creación de reserva, pagos y gestión de cliente.
- **Base de datos:** relacional (PostgreSQL/MySQL) por la naturaleza transaccional de reservas e inventario.
- **Concurrencia:** bloqueo temporal de inventario ("hold") al iniciar el checkout para evitar doble reserva.
- **Seguridad:** HTTPS obligatorio, tokenización de pagos (PCI-DSS vía la pasarela, nunca almacenar número de tarjeta), protección contra bots en el formulario de reserva (captcha/rate limiting).
- **Responsive:** el flujo de reserva debe funcionar bien en móvil, ya que gran parte del tráfico hotelero es móvil.

## 12. Métricas de éxito

- Tasa de conversión búsqueda → reserva completada.
- Tasa de abandono en el paso de pago.
- Tiempo promedio para completar una reserva.
- % de reservas con servicios adicionales agregados (upsell).
- Reducción de overbooking / errores de disponibilidad a 0.

## 13. Fases sugeridas

1. **Fase 1 (MVP):** búsqueda de disponibilidad, reserva de habitación, pago, confirmación por email, portal de cliente básico.
2. **Fase 2:** panel admin completo, reportes, códigos promocionales, servicios adicionales.
3. **Fase 3:** integración con channel managers externos, programa de fidelización, multi-idioma/multi-moneda avanzado.
