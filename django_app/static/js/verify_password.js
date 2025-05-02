document.addEventListener("DOMContentLoaded", function () {
    const username = document.getElementById("id_username");
    const email = document.getElementById("id_email");
    const password1 = document.getElementById("id_password1");
    const password2 = document.getElementById("id_password2");
    const errorDiv = document.getElementById("password-error");
    const submitBtn = document.getElementById("submit-button");

    let password2Touched = false;

    function validarCampos() {
        const valUsername = username.value.trim();
        const valEmail = email.value.trim();
        const val1 = password1.value.trim();
        const val2 = password2.value.trim();

        const camposPreenchidos = valUsername && valEmail && val1 && val2;
        const senhasIguais = val1 === val2;

        // Mostrar erro só se password2 foi tocado e as senhas não batem
        if (password2Touched && (!senhasIguais || !val2)) {
            password2.classList.add("is-invalid");
            errorDiv.style.display = "block";
        } else {
            password2.classList.remove("is-invalid");
            errorDiv.style.display = "none";
        }

        // Habilita o botão só se tudo estiver ok
        submitBtn.disabled = !(camposPreenchidos && senhasIguais);
    }

    // Listeners para atualizar dinamicamente
    username.addEventListener("input", validarCampos);
    email.addEventListener("input", validarCampos);
    password1.addEventListener("input", validarCampos);
    password2.addEventListener("input", function () {
        password2Touched = true;
        validarCampos();
    });

    validarCampos(); // Verificação inicial
});
