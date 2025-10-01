/* Aqui consiste uma lógica para permitir a passagem de dados do 'movies.js' para o html, a principio é realizado um get em um endpoin feito pelo server, onde se localizam os filmes
armazenados pelo 'movies.json', e os redenrizam na tela, além disso na passagem de dados par ao html é inserido dois botões enos cards dos filmes onde cada um possui uma função.
As funções dos botões são definidas logo após as inserção dos dados dos filmes na tela, quando forem clicados, eles realizaram uma ação.*/

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
                
                // Evento do botão de update
                const updateButton = card.querySelector('.updateButton');
                updateButton.addEventListener('click', () => { 
                    /* Para a edição dos filmes é necessário renderizar outra tela, por conta disso o metódo escolhido para a passagem de dados para a tela de edição foi o
                    local storage, para evitar a necessidade de mais uma requisição GET para o servidor. Os dados do filme são recolhidos ao clicar no botão, onde são identificados pelo
                    data-id definido na inserção de dados na tela. */
                    const id = updateButton.dataset.id;
                    localStorage.setItem('id', id);
                    localStorage.setItem('filme', JSON.stringify(filme))
                    window.location.href = "/filmes_edicao";
                });
                
                // Evento do botão de delete
                const deleteButton = card.querySelector('.deleteButton');
                deleteButton.addEventListener('click', () => {
                    const id = deleteButton.dataset.id;
                    delete_movie(id);
                    location.reload();
                });
            }
        }).catch(error => console.error('Erro ao buscar filmes:', error));
});

