const URL = 'http://localhost:8000/get_movies';
const URL_DELETE = 'http://localhost:8000/delete_movie';

async function delete_movie(film_id) {
    try {
        const response = await fetch(`${URL_DELETE}/${film_id}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            alert('Filme deletado com sucesso.');
        } else {
            alert("Falha ao deletar filme.");
            console.error('Deu pau total.')
        }
    } catch (error) {
        console.error("Erro de conexão durante o delete: ", error);
    }
} 

document.addEventListener('DOMContentLoaded', function() {
    fetch(URL)
        .then(response => response.json()) 
        .then(data => {
            console.log(data)
            const filmesContainer = document.getElementById('movies');
            
            for (const id in data) {
                const filme = data[id];
                
                const card = document.createElement('div');
                card.classList.add('movieCard');
                
                card.innerHTML = `
                    <h2>${filme.title} (${filme.year})</h2>
                    <p><strong>Gênero:</strong> ${filme.genre}</p>
                    <p><strong>Diretor:</strong> ${filme.director}</p>
                    <p><strong>Atores:</strong> ${filme.actor}</p>
                    <p><strong>Produtora:</strong> ${filme.producer}</p>
                    <p><strong>Sinopse:</strong> ${filme.summary}</p>
                    <div>
                        <button type='button' class='updateButton' data-id=${filme.id}> Editar </button>
                        <button type='button' class='deleteButton' data-id=${filme.id}> Deletar </button>
                    </div>
                    `;
                
                filmesContainer.appendChild(card);

                const updateButton = card.querySelector('.updateButton');
                updateButton.addEventListener('click', (e) => { 
                    const id = updateButton.dataset.id;
                    localStorage.setItem('id', id);
                    localStorage.setItem('filme', JSON.stringify(filme))
                    window.location.href = "/filmes_edicao";
                    // update_movie();
                    // e.preventDefault()
                });

                const deleteButton = card.querySelector('.deleteButton');
                deleteButton.addEventListener('click', () => {
                    const id = deleteButton.dataset.id;
                    delete_movie(id);
                    location.reload();
                });
            }
        }).catch(error => console.error('Erro ao buscar filmes:', error));
});

