const URL = 'http://localhost:8000/send_filmes';

const postFilmsForm = document.getElementById('postFilmsForm');
const filmsFormInputs = postFilmsForm.querySelectorAll('.siteInput');

function get_films_data() {
    let filmsData = {};
    filmsFormInputs.forEach(input => {
        filmsData[input.id] = input.value;
    });
    return filmsData;
}

async function post_films(data) {
    try {
        const response = await fetch(URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data) 
        });

        if (response.ok) {
            console.log('Filme cadastrado com sucesso.')
            alert("Filme cadastrado com sucesso!")
             window.location.href = "/filmes_listagem"
        }
    } catch(error){
        console.error("Erro de conexão: ", error);
    }
}

postFilmsForm.addEventListener('submit', (e) => {
    e.preventDefault(); 
    const filmsData = get_films_data();
    post_films(filmsData); 
});