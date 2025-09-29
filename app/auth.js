const URL = 'http://localhost:8080/send_login'

const loginButton = document.getElementById('loginButton')
const loginForm = document.getElementById('loginForm')
let userForm = document.getElementById('user')
let passwordForm = document.getElementById('password')
let confirmPasswordForm = document.getElementById('confirmPassword')


async function login(user, password, confirmPasswordForm){
    try {
        const response = await fetch(URL, { // A variável 'response' aguarda a resposta do servidor para continuar o código atráves do metódo await
            method: "post",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({user, password, confirmPasswordForm})
        });

        if (response.ok){
            console.log("Login bem-sucedido!")
            alert("Login bem-sucedido! Sejá bem vindo nome");
            window.location.href = "http://localhost:8080/filmes_listagem";
        } else if (response.status == 403){
            console.log("Usuário ou senha inválidos.");
            alert("Usuário ou senha inválidos.");
        } else {
            console.log("Foi para o cacete!!!!");
            alert("Erro inesperado no sistema.");
        }
    } catch (error){
        console.log("Erro de conexão: ", error)
    }
}

loginForm.addEventListener('submit', (e) =>{
    e.preventDefault();
    login(userForm.value, passwordForm.value, confirmPasswordForm.value);
})