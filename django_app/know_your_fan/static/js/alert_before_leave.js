document.addEventListener("DOMContentLoaded", function () {

    const leaveBtn = document.getElementById("leave_button_id");

    function showAlert(e) {
        const confirmationMessage = "Você tem certeza que deseja sair?";

        if (!confirm(confirmationMessage)) {
            e.preventDefault();
        }
    }

    if (leaveBtn) {
        leaveBtn.addEventListener("click", showAlert);
    }

});