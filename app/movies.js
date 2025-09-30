const URL = 'http://localhost:8000/get_filmes'

document.addEventListener('DOMContentLoaded', function() {
    fetch(URL)
        .then(response => response.json()) 
        .then(data => {
            console.log(data)
            const filmesContainer = document.getElementById('film');
            
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
                    <div class="sinopse">
                        <strong>Sinopse:</strong>
                        <p>${filme.summary}</p>
                    </div>
                    <button type='submmit' class='deleteButton' data-id=${filme.id}> Deletar </button>
                `;
                
                filmesContainer.appendChild(card);

                const deleteButton = card.querySelector('.deleteButton');
                deleteButton.addEventListener('click', () => {
                    const filmId = deleteButton.dataset.id;
                    deleteFilm(filmId, card);
                });
            }
        }).catch(error => console.error('Erro ao buscar filmes:', error));
});

async function deleteFilm(id, element) {
    try {
        const response = await fetch(`/delete_filme`, {
            method: 'DELETE',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(id)
        });

        if (response.ok) {
            console.log(`Filme com ID ${id} deletado com sucesso.`);
            element.remove();
        } else {
            console.error('Falha ao deletar o filme.');
        }
    } catch (error) {
        console.error('Erro ao deletar o filme:', error);
    }
}
