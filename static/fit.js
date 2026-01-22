const form = document.getElementById("formulario");
const resultado = document.getElementById("resultado");

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const dados = {
    idade: document.getElementById("idade").value,
    peso: document.getElementById("peso").value,
    altura: document.getElementById("altura").value,
    genero: document.getElementById("genero").value,
    atividade: document.getElementById("atividade").value
  };

  fetch("/calcular", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados)
  })
  .then(response => response.json())
  .then(resultadoApi => {
    resultado.innerHTML = `
      <p>Sua TMB: <strong>${resultadoApi.tmb} kcal</strong></p>
      <p>Calorias diárias: <strong>${resultadoApi.calorias} kcal</strong></p>
    `;
  });
});
