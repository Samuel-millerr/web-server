const URL = 'http://localhost:8000/send_cadastro';

const singUpForm = document.getElementById('singUpForm');
const userForm = document.getElementById('user');
const passwordForm = document.getElementById('password');
const confirmPasswordForm = document.getElementById('confirmPassword');

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