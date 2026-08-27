document.addEventListener("DOMContentLoaded", () => {
  const botoes = document.querySelectorAll(".botaoMostrarMais");

  botoes.forEach((botao) => {
    // Seleciona o próximo elemento irmão do botão que seja um parágrafo
    let conteudo = botao.parentElement.querySelector(".conteudoOculto");
    if (conteudo) {
      conteudo.style.display = "none";
      botao.textContent = "Mostrar Mais";
      botao.addEventListener("click", () => {
        if (
          conteudo.style.display === "none" ||
          conteudo.style.display === ""
        ) {
          conteudo.style.display = "block";
          botao.textContent = "Mostrar Menos";
        } else {
          conteudo.style.display = "none";
          botao.textContent = "Mostrar Mais";
        }
      });
    }
  });
});
