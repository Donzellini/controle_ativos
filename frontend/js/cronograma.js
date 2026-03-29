/**
 * Gerenciamento de Cronograma de Responsabilidades
 */

const API_URL = 'https://controle-ativos.fly.dev/api';

// Elementos do DOM
const filterProfessor = document.getElementById('filterProfessor');
const filterMes = document.getElementById('filterMes');
const filterAno = document.getElementById('filterAno');
const cronogramaBody = document.getElementById('cronogramaBody');
const cronogramaTable = document.getElementById('cronogramaTable');
const emptyMessage = document.getElementById('emptyMessage');
const loadingAlert = document.getElementById('loadingAlert');
const errorAlert = document.getElementById('errorAlert');
const errorMessage = document.getElementById('errorMessage');
const editModal = document.getElementById('editModal');
const saveEditBtn = document.getElementById('saveEditBtn');

// Estado da aplicação
let responsabilidadeAtual = null;
let todosProfeissores = [];

/**
 * Carregar lista de professores
 */
async function carregarProfessores() {
    try {
        const response = await fetch(`${API_URL}/professores`);
        
        if (!response.ok) {
            throw new Error('Erro ao carregar professores');
        }

        todosProfeissores = await response.json();
        
        // Preencher select de filtro
        filterProfessor.innerHTML = '<option value="">-- Todos os professores --</option>';
        todosProfeissores.forEach(prof => {
            const option = document.createElement('option');
            option.value = prof.id;
            option.textContent = prof.nome;
            filterProfessor.appendChild(option);
        });

    } catch (error) {
        console.error('Erro ao carregar professores:', error);
        mostrarErro('Erro ao carregar lista de professores.');
    }
}

/**
 * Traduzir dia da semana (inglês → português)
 */
function traduzirDiaSemana(dia) {
    const diasSemana = {
        'Monday': 'Segunda',
        'Tuesday': 'Terça',
        'Wednesday': 'Quarta',
        'Thursday': 'Quinta',
        'Friday': 'Sexta',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    };
    return diasSemana[dia] || dia;
}

/**
 * Formatar data (YYYY-MM-DD → DD/MM/YYYY)
 */
function formatarData(dataStr) {
    const [ano, mes, dia] = dataStr.split('-');
    return `${dia}/${mes}/${ano}`;
}

/**
 * Obter badge de status com cor
 */
function obterBadgeStatus(status) {
    const badges = {
        'Pendente': { text: 'Pendente', color: 'primary' },
        'Devolvido': { text: 'Devolvido', color: 'success' },
        'Com falta': { text: 'Com falta', color: 'danger' },
        'Não realizado': { text: 'Não realizado', color: 'secondary' }
    };
    
    const badge = badges[status] || { text: status, color: 'secondary' };
    return `<span class="badge bg-${badge.color}">${badge.text}</span>`;
}

/**
 * Carregar e renderizar cronograma
 */
async function carregarCronograma() {
    try {
        loadingAlert.classList.remove('d-none');
        errorAlert.classList.add('d-none');
        cronogramaBody.innerHTML = '';
        emptyMessage.classList.add('d-none');

        // Construir query string
        const mes = filterMes.value;
        const ano = filterAno.value;
        const professorId = filterProfessor.value;

        let url = `${API_URL}/cronograma?mes=${mes}&ano=${ano}`;
        if (professorId) {
            url += `&professor_id=${professorId}`;
        }

        // Buscar cronograma
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error('Erro ao carregar cronograma');
        }

        const data = await response.json();
        
        // Renderizar responsabilidades
        if (data.dias.length === 0) {
            emptyMessage.classList.remove('d-none');
            loadingAlert.classList.add('d-none');
            return;
        }

        // Renderizar cada responsabilidade
        data.dias.forEach(dia => {
            dia.responsabilidades.forEach(resp => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${formatarData(dia.data)}</td>
                    <td>${traduzirDiaSemana(dia.dia_semana)}</td>
                    <td>${resp.professor}</td>
                    <td>${resp.periodo_turma}</td>
                    <td>${resp.quantidade}</td>
                    <td>${obterBadgeStatus(resp.status)}</td>
                    <td>
                        <button class="btn btn-sm btn-warning" onclick="abrirEditarResponsabilidade(${resp.id})">
                            <i class="bi bi-pencil"></i> Editar
                        </button>
                    </td>
                `;
                cronogramaBody.appendChild(row);
            });
        });

        loadingAlert.classList.add('d-none');

    } catch (error) {
        console.error('Erro:', error);
        mostrarErro(error.message || 'Erro ao carregar cronograma.');
        loadingAlert.classList.add('d-none');
    }
}

/**
 * Abrir modal para editar responsabilidade
 */
async function abrirEditarResponsabilidade(responsabilidadeId) {
    try {
        // Buscar detalhes da responsabilidade
        const response = await fetch(`${API_URL}/responsabilidades/${responsabilidadeId}`);
        
        if (!response.ok) {
            throw new Error('Responsabilidade não encontrada');
        }

        responsabilidadeAtual = await response.json();

        // Preencher modal com dados
        document.getElementById('modalProfessor').textContent = 
            todosProfeissores.find(p => p.id === responsabilidadeAtual.professor_id)?.nome || 'Desconhecido';
        
        document.getElementById('modalData').textContent = formatarData(responsabilidadeAtual.data.split('T')[0]);
        document.getElementById('modalPeriodo').textContent = responsabilidadeAtual.periodo_turma;
        document.getElementById('modalQuantidade').textContent = responsabilidadeAtual.quantidade_chromebooks;
        document.getElementById('editStatus').value = responsabilidadeAtual.status;
        document.getElementById('editObservacoes').value = responsabilidadeAtual.observacoes || '';

        // Mostrar modal
        const modal = new bootstrap.Modal(editModal);
        modal.show();

    } catch (error) {
        console.error('Erro:', error);
        mostrarErro(error.message);
    }
}

/**
 * Salvar edições de responsabilidade
 */
saveEditBtn.addEventListener('click', async () => {
    if (!responsabilidadeAtual) return;

    try {
        // Desabilitar botão
        saveEditBtn.disabled = true;
        saveEditBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Salvando...';

        // Enviar PUT
        const payload = {
            status: document.getElementById('editStatus').value,
            observacoes: document.getElementById('editObservacoes').value || null,
        };

        const response = await fetch(`${API_URL}/responsabilidades/${responsabilidadeAtual.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error('Erro ao atualizar responsabilidade');
        }

        // Sucesso! Fechar modal e recarregar
        const modal = bootstrap.Modal.getInstance(editModal);
        modal.hide();

        // Recarregar cronograma
        setTimeout(() => {
            carregarCronograma();
        }, 500);

    } catch (error) {
        console.error('Erro:', error);
        mostrarErro(error.message);
    } finally {
        saveEditBtn.disabled = false;
        saveEditBtn.innerHTML = 'Salvar Mudanças';
    }
});

/**
 * Filtros disparam recarregamento
 */
filterProfessor.addEventListener('change', carregarCronograma);
filterMes.addEventListener('change', carregarCronograma);
filterAno.addEventListener('change', carregarCronograma);

/**
 * Mostrar alerta de erro
 */
function mostrarErro(mensagem) {
    errorMessage.textContent = mensagem;
    errorAlert.classList.remove('d-none');
}

/**
 * Inicializar quando DOM está pronto
 */
document.addEventListener('DOMContentLoaded', () => {
    carregarProfessores();
    carregarCronograma();
});
