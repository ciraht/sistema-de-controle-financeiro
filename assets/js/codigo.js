function mostrarHistorico() {
    const historico = document.getElementById("historico");
    if (historico.style.display === "none" || historico.style.display === "") {
        historico.style.display = "block";
    } else {
        historico.style.display = "none";
    }
}
