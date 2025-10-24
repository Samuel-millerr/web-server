const URL = 'http://localhost:8000/send_login';

const loginForm = document.getElementById('loginForm');
const userForm = document.getElementById('user');
const passwordForm = document.getElementById('password');

/* Fetch utilizado para passar os dados digitados para o server, caso estejam corretos e de acordo com os dados armazenados no users.json é retornado
um código 200 e o acesso do usuário é liberado */

async function login(user, password){
    try {
        // A variável 'response' aguarda a resposta do servidor para continuar o código atráves do metódo await
        const response = await fetch(URL, { 
            method: "post",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({user, password})
        });
        
        // Condição para avaliar qual código foi recibido e qual deve ser a ação do javascript
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