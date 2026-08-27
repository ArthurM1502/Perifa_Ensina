window.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".imagens");
  const imgs = container.querySelectorAll("img");

  imgs.forEach((img) => {
    const clone = img.cloneNode(true);
    container.appendChild(clone);
  });
});

function startProgress() {
  atualizarBarra("progressbar", 100);
  atualizarBarra("progressbar2", 100);
  atualizarBarra("progressbar3", 100);
  atualizarBarra("progressbar4", 100);
  atualizarBarra("progressbar5", 100);
  atualizarBarra("progressbar6", 100);
}

function atualizarBarra(id, valor) {
  const barra = document.getElementById(id);
  if (!barra) return;

  valor = Math.max(0, Math.min(100, valor));
  // Garante que a barra está visível e animada
  barra.style.display = "block";
  barra.style.transition = "width 1s";
  setTimeout(function () {
    barra.style.width = valor + "%";
  }, 10);
  // Atualiza o texto de porcentagem imediatamente
  var textoId = "porcentagem" + id.replace(/[^0-9]/g, "");
  var texto = document.getElementById(textoId);
  if (texto) {
    texto.style.display = "inline";
    texto.textContent = valor + "%";
  }
  // Se valor 100, adiciona classe verde; senão, remove
  if (valor === 100) {
    barra.classList.add("barra-concluida");
  } else {
    barra.classList.remove("barra-concluida");
  }
  // Envia conclusão do módulo ao backend
  if (valor === 100) {
    var moduloNome = "";
    switch (id) {
      case "progressbar":
        moduloNome = "Introducao";
        break;
      case "progressbar2":
        moduloNome = "DesignThinking";
        break;
      case "progressbar3":
        moduloNome = "Gamificacao";
        break;
      case "progressbar4":
        moduloNome = "SalaDeAulaInvertida";
        break;
      case "progressbar5":
        moduloNome = "EstudoDeCasos";
        break;
      case "progressbar6":
        moduloNome = "SeminariosDebates";
        break;
      default:
        moduloNome = id;
    }
    fetch("/concluir_modulo", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: "modulo=" + encodeURIComponent(moduloNome),
    })
      .then((response) => response.text())
      .then((text) => {
        // Supondo que o backend retorna 'ok' para sucesso
        if (text.trim() === "ok") {
          alert("Módulo concluído com sucesso!");
        } else {
          alert("Erro ao registrar conclusão do módulo.");
        }
      })
      .catch(() => {
        alert("Erro de conexão ao registrar conclusão do módulo.");
      });
  }
}
