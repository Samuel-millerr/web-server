/* Os dados do formulário são enviados para o servidor atráves do fetch e após isso sçao inseridos no 'movies.json' */

const URL = 'http://localhost:8000/send_movie';

const postMoviesForm = document.getElementById('postMoviesForm');
const moviesFormInputs = postMoviesForm.querySelectorAll('.siteInput');

function get_movies_data() {
    let moviesData = {};
    moviesFormInputs.forEach(input => {
        moviesData[input.id] = input.value;
    });
    return moviesData;
}

async function post_film(data) {
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
        } else {
            console.error("Deu pau total.")
        }
    } catch(error){
        console.error("Erro de conexão: ", error);
    }
}

postMoviesForm.addEventListener('submit', (e) => {
    e.preventDefault(); 
    const moviesData = get_movies_data();
    post_film(moviesData); 
});