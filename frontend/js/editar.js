/**
 * Edit ativo handler
 */
const API_URL = 'https://controle-ativos.fly.dev/api';

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const ativoId = urlParams.get('id');
    
    if (!ativoId) {
        showError('ID do ativo não fornecido');
        return;
    }
    
    loadAtivo(ativoId);
    
    const form = document.getElementById('ediçãoForm');
    form.addEventListener('submit', (e) => handleFormSubmit(e, ativoId));
});

async function loadAtivo(ativoId) {
    try {
        const response = await fetch(`${API_URL}/ativos/${ativoId}`);
        
        if (!response.ok) {
            throw new Error('Ativo não encontrado');
        }
        
        const ativo = await response.json();
        
        // Populate form
        document.getElementById('id').value = ativo.id;
        document.getElementById('numero_serie').value = ativo.numero_serie;
        document.getElementById('descricao').value = ativo.descricao;
        document.getElementById('localizacao').value = ativo.localizacao;
        document.getElementById('status').value = ativo.status;
        document.getElementById('valor_estimado').value = ativo.valor_estimado;
        
        // Hide spinner and show form
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('ediçãoForm').classList.remove('d-none');
        
    } catch (error) {
        console.error('Error:', error);
        showError('Erro ao carregar ativo: ' + error.message);
    }
}

async function handleFormSubmit(e, ativoId) {
    e.preventDefault();
    
    document.getElementById('successAlert').classList.add('d-none');
    document.getElementById('errorAlert').classList.add('d-none');
    
    const data = {
        descricao: document.getElementById('descricao').value,
        localizacao: document.getElementById('localizacao').value,
        status: document.getElementById('status').value
    };
    
    try {
        const response = await fetch(`${API_URL}/ativos/${ativoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showSuccess(result.message || 'Ativo atualizado com sucesso!');
            setTimeout(() => {
                window.location.href = 'listagem.html';
            }, 2000);
        } else {
            showError(result.detail || 'Erro ao atualizar ativo');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Erro ao conectar com o servidor');
    }
}

function showSuccess(message) {
    const successAlert = document.getElementById('successAlert');
    document.getElementById('successMessage').textContent = message;
    successAlert.classList.remove('d-none');
}

function showError(message) {
    const errorAlert = document.getElementById('errorAlert');
    document.getElementById('errorMessage').textContent = message;
    errorAlert.classList.remove('d-none');
}
