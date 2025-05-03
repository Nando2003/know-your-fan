document.addEventListener("DOMContentLoaded", function () {
    const rgFront = document.getElementById("id_rg_front");
    const rgBack = document.getElementById("id_rg_back");

    rgFront.addEventListener("change", function () {
        const label = document.getElementById("label-rg-front");
        label.textContent = this.files[0]?.name || "Escolher imagem";
    });

    rgBack.addEventListener("change", function () {
        const label = document.getElementById("label-rg-back");
        label.textContent = this.files[0]?.name || "Escolher imagem";
    });
});