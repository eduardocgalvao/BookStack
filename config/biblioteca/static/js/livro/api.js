// api.js - FUNÇÕES DE API E COMUNICAÇÃO COM BACKEND
console.log("api.js carregado");

// ========== FUNÇÕES AJAX ==========
async function fetchLivro(id) {
    console.log(`Buscando livro ID: ${id}`);
    try {
        const url = `/api/livro/${id}/`;
        console.log("URL:", url);
        
        const response = await fetch(url, {
            headers: {
                'X-CSRFToken': window.csrftoken,
                'Accept': 'application/json'
            }
        });
        
        console.log("Status:", response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Erro HTTP ${response.status}:`, errorText);
            throw new Error(`Erro ${response.status}: Não foi possível carregar o livro`);
        }
        
        const data = await response.json();
        console.log("Dados recebidos:", data);
        console.log("Status ID recebido:", data.status_id);
        console.log("Status texto recebido:", data.status);
        
        return data;
        
    } catch (error) {
        console.error('Erro ao buscar livro:', error);
        alert('Erro ao carregar dados do livro: ' + error.message);
        return null;
    }
}
window.fetchLivro = fetchLivro;

async function updateLivro(id, data, isFormData = false) {
    console.log(`Atualizando livro ID: ${id}`);
    
    try {
        const metodoEnvio = isFormData ? 'POST' : 'PUT';
        const url = `/api/livro/${id}/update/`;
        console.log("URL:", url);
        
        let requestOptions = {
            method: metodoEnvio,
            headers: {
                'X-CSRFToken': window.csrftoken,
            }
        };
        
        if (isFormData) {
            requestOptions.body = data;
            console.log("Enviando FormData com arquivo");
        } else {
            requestOptions.headers['Content-Type'] = 'application/json';
            requestOptions.headers['Accept'] = 'application/json';
            requestOptions.body = JSON.stringify(data);
            console.log("Enviando JSON:", data);
        }
        
        const response = await fetch(url, requestOptions);
        console.log("Status:", response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Erro HTTP ${response.status}:`, errorText);
            throw new Error(`Erro ${response.status}: Não foi possível atualizar o livro`);
        }
        
        return await response.json();
        
    } catch (error) {
        console.error('Erro ao atualizar livro:', error);
        return { 
            success: false, 
            error: error.message || 'Erro desconhecido ao atualizar' 
        };
    }
}
window.updateLivro = updateLivro;

async function deleteLivro(id) {
    console.log(`Excluindo livro ID: ${id}`);
    try {
        const url = `/api/livro/${id}/delete/`;
        console.log("URL:", url);
        
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': window.csrftoken,
                'Accept': 'application/json'
            }
        });
        
        console.log("Status:", response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`Erro HTTP ${response.status}:`, errorText);
            throw new Error(`Erro ${response.status}: Não foi possível excluir o livro`);
        }
        
        return await response.json();
        
    } catch (error) {
        console.error('Erro ao excluir livro:', error);
        return { 
            success: false, 
            error: error.message || 'Erro desconhecido ao excluir' 
        };
    }
}
window.deleteLivro = deleteLivro;