const URL = 'http://localhost:8000/send_login';

const loginForm = document.getElementById('loginForm');
const userForm = document.getElementById('user');
const passwordForm = document.getElementById('password');

async function login(user, password){
    try {
        const response = await fetch(URL, { // A variável 'response' aguarda a resposta do servidor para continuar o código atráves do metódo await
            method: "post",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({user, password})
        });

        if (response.ok){
            console.log("Login bem-sucedido!");
            alert("Login bem-sucedido! Seja bem vindo " + userForm.value);
            window.location.href = "/filmes_listagem";
        } else if (response.status == 403){
            console.log("Usuário ou senha inválidos.");
            alert("Usuário ou senha inválidos.");
        } else {
            console.log("Foi para o cacete!!!!");
            alert("Erro inesperado no sistema.");
        }
    } catch(error){
        console.error("Erro de conexão: ", error);
    }
}

loginForm.addEventListener('submit', (e) =>{
    e.preventDefault();
    login(userForm.value, passwordForm.value);
})