/**
 * Gerenciamento de Responsabilidade de Chromebooks
 */

const API_URL = 'https://controle-ativos.fly.dev/api';

// Elementos do DOM
const form = document.getElementById('responsabilidadeForm');
const professorSelect = document.getElementById('professor_id');
const submitBtn = document.getElementById('submitBtn');
const successAlert = document.getElementById('successAlert');
const errorAlert = document.getElementById('errorAlert');
const successMessage = document.getElementById('successMessage');
const errorMessage = document.getElementById('errorMessage');

/**
 * Carregar lista de professores da API e preencher select
 */
async function carregarProfessores() {
    try {
        const response = await fetch(`${API_URL}/professores`);
        
        if (!response.ok) {
            throw new Error('Erro ao carregar professores');
        }

        const professores = await response.json();
        
        // Limpar options antigos (manter apenas o primeiro)
        professorSelect.innerHTML = '<option value="">-- Selecione um professor --</option>';
        
        // Adicionar cada professor como option
        professores.forEach(prof => {
            const option = document.createElement('option');
            option.value = prof.id;
            option.textContent = prof.nome;
            professorSelect.appendChild(option);
        });

    } catch (error) {
        console.error('Erro ao carregar professores:', error);
        mostrarErro('Erro ao carregar lista de professores. Tente recarregar a página.');
    }
}

/**
 * Validar formulário no cliente
 */
function validarFormulario() {
    const professorId = document.getElementById('professor_id').value;
    const data = document.getElementById('data').value;
    const periodo = document.getElementById('periodo_turma').value;
    const quantidade = document.getElementById('quantidade_chromebooks').value;

    if (!professorId) {
        mostrarErro('Selecione um professor');
        return false;
    }

    if (!data) {
        mostrarErro('Selecione uma data');
        return false;
    }

    if (!periodo) {
        mostrarErro('Selecione o período/turma');
        return false;
    }

    if (!quantidade || quantidade <= 0) {
        mostrarErro('Quantidade deve ser maior que zero');
        return false;
    }

    return true;
}

/**
 * Submeter formulário e criar responsabilidade
 */
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validar formulário cliente
    if (!validarFormulario()) {
        return;
    }

    // Desabilitar submit button
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Registrando...';

    try {
        // Construir payload
        const payload = {
            professor_id: parseInt(document.getElementById('professor_id').value),
            data: document.getElementById('data').value + 'T00:00:00', // Converter para ISO format
            periodo_turma: document.getElementById('periodo_turma').value,
            quantidade_chromebooks: parseInt(document.getElementById('quantidade_chromebooks').value),
            observacoes: document.getElementById('observacoes').value || null,
        };

        // Enviar POST
        const response = await fetch(`${API_URL}/responsabilidades`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            // API retornou erro
            throw new Error(data.detail || 'Erro ao registrar responsabilidade');
        }

        // Sucesso!
        mostrarSucesso(`Responsabilidade registrada com sucesso! (ID: ${data.id})`);
        
        // Limpar form
        form.reset();
        
        // Recarregar professores (em caso de múltiplos registros)
        carregarProfessores();

        // Redirecionar após 2 segundos
        setTimeout(() => {
            window.location.href = 'cronograma.html';
        }, 2000);

    } catch (error) {
        console.error('Erro:', error);
        mostrarErro(error.message || 'Erro ao registrar responsabilidade. Tente novamente.');
    } finally {
        // Reabilitar submit button
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-check-lg"></i> Registrar Responsabilidade';
    }
});

/**
 * Mostrar alerta de sucesso
 */
function mostrarSucesso(mensagem) {
    successMessage.textContent = mensagem;
    successAlert.classList.remove('d-none');
    errorAlert.classList.add('d-none');
    
    // Auto-hide após 5 segundos
    setTimeout(() => {
        successAlert.classList.add('d-none');
    }, 5000);
}

/**
 * Mostrar alerta de erro
 */
function mostrarErro(mensagem) {
    errorMessage.textContent = mensagem;
    errorAlert.classList.remove('d-none');
    successAlert.classList.add('d-none');
}

/**
 * Inicializar quando DOM está pronto
 */
document.addEventListener('DOMContentLoaded', () => {
    carregarProfessores();
});
