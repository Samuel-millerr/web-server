/* Arquivo utilizado para buscar o filme armazenado no local storage. É realizado um fetch para enviar os dados editados do formulário para o servidor,
onde é realizado um substituição do filme antes armazenado no id para o novo filme */

const URL_UPDATE = 'http://localhost:8000/update_movie';

const film_id = localStorage.getItem('id');
const filme = JSON.parse(localStorage.getItem('filme'))

document.getElementById('title').value = filme.title || '';
document.getElementById('actor').value = filme.actor || '';
document.getElementById('director').value = filme.director || '';
document.getElementById('year').value = filme.year || '';
document.getElementById('genre').value = filme.genre || '';
document.getElementById('producer').value = filme.producer || '';
document.getElementById('summary').value = filme.summary || '';

async function update_movie(updated_data) {
    try {
        const response = await fetch(`${URL_UPDATE}/${film_id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updated_data)
        })

        const data = await response.json(); 
        
        if (response.ok) {
            alert('Filme atualizado com sucesso.');
            window.location.href = "/filmes_listagem"
        } else {
            alert("Falha ao atualizar filme.");
            console.error('Deu pau total.')
        }
    } catch (error) {
        console.error("Erro de conexão durante o update: ", error);
    }
} 

const postMoviesForm = document.getElementById('putMovieForm')
postMoviesForm.addEventListener('submit', (e) => {
    e.preventDefault()
    moviesData = {}
    const moviesFormInputs = postMoviesForm.querySelectorAll('.siteInput');
    moviesFormInputs.forEach(input => {
        moviesData[input.id] = input.value;
    });
    console.log(moviesData)
    update_movie(moviesData)
})