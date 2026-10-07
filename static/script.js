// Cuando el cliente elige la fecha de entrada, la salida
// no puede ser igual ni anterior a esa fecha.
const entrada = document.getElementById("entrada");
const salida = document.getElementById("salida");

function actualizarSalida() {
  if (!entrada.value) return;

  const minima = new Date(entrada.value + "T00:00:00");
  minima.setDate(minima.getDate() + 1);
  const minimaTexto = minima.toISOString().split("T")[0];

  salida.min = minimaTexto;
  if (!salida.value || salida.value < minimaTexto) {
    salida.value = minimaTexto;
  }
}

if (entrada && salida) {
  entrada.addEventListener("change", actualizarSalida);
}
