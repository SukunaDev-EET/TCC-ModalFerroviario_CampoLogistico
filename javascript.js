
// =================================
// FERROLOG - ANIMAÇÕES
// =================================

// OBSERVAR ELEMENTOS DURANTE A ROLAGEM

const elementos = document.querySelectorAll(".reveal");

const observador = new IntersectionObserver((entradas) => {

    entradas.forEach((entrada) => {

        if (entrada.isIntersecting) {
            entrada.target.classList.add("active");
            observador.unobserve(entrada.target);
        }

    });

}, {
    threshold: 0.12
});

elementos.forEach((elemento) => {
    observador.observe(elemento);
});


// EFEITO NO MENU AO ROLAR

const header = document.querySelector(".header");

window.addEventListener("scroll", () => {

    if (header) {
        if (window.scrollY > 50) {
            header.style.boxShadow = "0 5px 25px rgba(0,229,255,0.12)";
        } else {
            header.style.boxShadow = "none";
        }
    }

});


// DESTAQUE DO LINK ATIVO

const links = document.querySelectorAll(".menu a");

links.forEach((link) => {

    link.addEventListener("click", () => {

        links.forEach((item) => {
            item.style.color = "";
        });

        link.style.color = "#00e5ff";

    });

});


// CARROSSEL AUTOMÁTICO

const slides = document.querySelectorAll(".imagens .slide");

let atual = 0;

function passarSlide() {

    if (slides.length === 0) return;

    slides[atual].classList.remove("active");

    atual++;

    if (atual >= slides.length) {
        atual = 0;
    }

    slides[atual].classList.add("active");

}

if (slides.length > 1) {
    setInterval(passarSlide, 3000);
}
