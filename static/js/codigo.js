function ajustarEstilo(elementId, estilos) {
    const elemento = document.getElementById(elementId);
    if (elemento) {
        Object.assign(elemento.style, estilos);
    }
}

function mostrarHistorico() {
    ajustarEstilo("exit", { height: "35px", width: "35px" });
    ajustarEstilo("tabelaazul", { width: "130px", marginLeft: "10px" });
    ajustarEstilo("tabela", { width: "180px" });
    ajustarEstilo("input", { width: "150px" });
    ajustarEstilo("input2", { width: "150px" });
    ajustarEstilo("input3", { width: "150px" });
    ajustarEstilo("texto-quadro", { marginLeft: "10px" });
    ajustarEstilo("adicionar", { marginLeft: "10px" });
    ajustarEstilo("c-to-l", { left: "10px" });
    ajustarEstilo("topo_azul", { width: "800px", height: "100px" });
    ajustarEstilo("baixo_branco", { width: "800px", height: "300px" });
}

function fecharHistorico() {
    ajustarEstilo("exit", { height: "0px", width: "0px" });
    ajustarEstilo("tabelaazul", { width: "250px", marginLeft: "0px" });
    ajustarEstilo("tabela", { width: "600px" });
    ajustarEstilo("input", { width: "450px" });
    ajustarEstilo("input2", { width: "450px" });
    ajustarEstilo("input3", { width: "450px" });
    ajustarEstilo("texto-quadro", { marginLeft: "0px" });
    ajustarEstilo("adicionar", { marginLeft: "460px" });
    ajustarEstilo("c-to-l", { left: "345px" });
    ajustarEstilo("topo_azul", { width: "0px", height: "0px" });
    ajustarEstilo("baixo_branco", { width: "0px", height: "0px" });
}
//mudar imagens e cores da tela de inicio

const pessoas = [
    { class: 'pessoa1', image: 'static/img/pessoa1.png', bgColor: 'pessoa1_cor', fundo: 'static/img/fundo1.png' },
    { class: 'pessoa2', image: 'static/img/pessoa2.png', bgColor: 'pessoa2_cor', fundo: 'static/img/fundo2.png' },
    { class: 'pessoa3', image: 'static/img/pessoa3.png', bgColor: 'pessoa3_cor', fundo: 'static/img/fundo3.png' },
    { class: 'pessoa4', image: 'static/img/pessoa4.png', bgColor: 'pessoa4_cor', fundo: 'static/img/fundo4.png' },
];


function escolherPessoaAleatoria() {
    return pessoas[Math.floor(Math.random() * pessoas.length)];
}


function aplicarEstiloAleatorio() {
    
    const pessoaEscolhida = escolherPessoaAleatoria();

    
    const imgElement = document.querySelector('.pessoa4'); 
    const saldoElement = document.querySelector('.saldo_total');
    const fundoSection = document.querySelector('.fundo1');


    pessoas.forEach(pessoa => {
        imgElement.classList.remove(pessoa.class);
        saldoElement.classList.remove(pessoa.bgColor);
        fundoSection.classList.remove(pessoa.bgColor); 
    });


    imgElement.classList.add(pessoaEscolhida.class);
    imgElement.src = pessoaEscolhida.image;
    saldoElement.classList.add(pessoaEscolhida.bgColor);
    fundoSection.classList.add(pessoaEscolhida.bgColor); 

    fundoSection.style.backgroundImage = `url(${pessoaEscolhida.fundo})`;
    fundoSection.style.backgroundSize = 'cover';
}

window.onload = aplicarEstiloAleatorio;

//mudar pergunta da pagina de cadastro


const grupo1 = document.getElementById('grupo1');
const grupo2 = document.getElementById('grupo2');
const btnProximo1 = document.getElementById('btnProximo1');
const btnVoltar = document.getElementById('btnVoltar');

btnProximo1.addEventListener('click', () => {
    grupo1.style.display = 'none';
    grupo2.style.display = 'block';
});

btnVoltar.addEventListener('click', () => {
    grupo2.style.display = 'none';
    grupo1.style.display = 'block';
});

// aparecer as informações do usuario na home

document.getElementById("toggleUser").addEventListener("click", function () {
    const userInfo = document.querySelector(".escuro.mais");
    userInfo.classList.toggle("oculto");
});