// static/js/valida_cpf.js
document.addEventListener('DOMContentLoaded', () => {
    const cpfInput     = document.getElementById('id_unique_identifier');
    const submitButton = document.getElementById('submit-button');
  
    function isValidCPF(cpf) {
      cpf = cpf.replace(/\D/g, '');
      if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;
      let soma = 0, resto;
  
      for (let i = 0; i < 9; i++) soma += +cpf[i] * (10 - i);
      resto = soma % 11;
      if ((resto < 2 ? 0 : 11 - resto) !== +cpf[9]) return false;
  
      soma = 0;
      for (let i = 0; i < 10; i++) soma += +cpf[i] * (11 - i);
      resto = soma % 11;
      return (resto < 2 ? 0 : 11 - resto) === +cpf[10];
    }
  
    cpfInput.addEventListener('input', function () {
      let v = this.value.replace(/\D/g, '').slice(0, 11);
  
      // máscara
      if (v.length > 9) v = v.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
      else if (v.length > 6) v = v.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
      else if (v.length > 3) v = v.replace(/(\d{3})(\d{1,3})/, '$1.$2');
      this.value = v;
  
      // validação
      const ok = isValidCPF(v);
      submitButton.disabled = !ok;
  
      this.classList.toggle('is-valid',   ok);
      this.classList.toggle('is-invalid', !ok && v.length === 14); // mostra erro só c/ 11 dígitos
    });
  });
  