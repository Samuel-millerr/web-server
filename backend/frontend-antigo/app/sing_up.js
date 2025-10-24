const URL = 'http://localhost:8000/send_cadastro';

const singUpForm = document.getElementById('singUpForm');
const userForm = document.getElementById('user');
const passwordForm = document.getElementById('password');
const confirmPasswordForm = document.getElementById('confirmPassword');

/* Fetch utilizado para passar os dados digitados para o server, caso as credenciais para o cadastro estejam de acordo com as regras definidas pelo server,
o cadastro é liberado e o usuário é direcionado para a tela de login */
async function singUp(user, password, confirmPassword){
    try {
        const response = await fetch(URL, {
            method: "post",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({user, password, confirmPassword})
        });

        if (response.ok) {
            console.log("Cadastro realizado com sucesso.");
            alert("Cadastro realizado com sucesso!");
            window.location.href = "/login";
        } else {
            console.log('Cadastro negado!');
            alert("Credenciais para cadastro inválidas, por gentileza digite novamente.");
        }
    } catch(error){
        console.error("Erro de conexão: ", error);
    }
}

singUpForm.addEventListener('submit', (e) => {
    e.preventDefault();
    singUp(userForm.value, passwordForm.value, confirmPasswordForm.value);
})