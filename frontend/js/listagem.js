/**
 * Listagem (list ativos)
 */
const API_URL = 'http://localhost:8000/api';
let allAtivos = [];
let filteredAtivos = [];
let currentPage = 1;
const itemsPerPage = 20;

document.addEventListener('DOMContentLoaded', function() {
    loadAtivos();
    
    // Search and filter listeners
    document.getElementById('searchInput').addEventListener('input', filterAtivos);
    document.getElementById('statusFilter').addEventListener('change', filterAtivos);
});

async function loadAtivos() {
    try {
        document.getElementById('loadingSpinner').style.display = 'block';
        document.getElementById('emptyMessage').classList.add('d-none');
        document.getElementById('errorMessage').classList.add('d-none');
        
        const response = await fetch(`${API_URL}/ativos?skip=0&limit=1000`);
        
        if (!response.ok) {
            throw new Error('Erro ao carregar ativos');
        }
        
        allAtivos = await response.json();
        filteredAtivos = [...allAtivos];
        currentPage = 1;
        
        if (allAtivos.length === 0) {
            document.getElementById('emptyMessage').classList.remove('d-none');
            document.getElementById('loadingSpinner').style.display = 'none';
        } else {
            renderTable();
            document.getElementById('loadingSpinner').style.display = 'none';
        }
    } catch (error) {
        console.error('Error loading ativos:', error);
        document.getElementById('errorMessage').classList.remove('d-none');
        document.getElementById('loadingSpinner').style.display = 'none';
    }
}

function filterAtivos() {
    const searchValue = document.getElementById('searchInput').value.toLowerCase();
    const statusValue = document.getElementById('statusFilter').value;
    
    filteredAtivos = allAtivos.filter(ativo => {
        const matchSearch = ativo.numero_serie.toLowerCase().includes(searchValue) ||
                          ativo.descricao.toLowerCase().includes(searchValue);
        const matchStatus = !statusValue || ativo.status === statusValue;
        
        return matchSearch && matchStatus;
    });
    
    currentPage = 1;
    renderTable();
}

function renderTable() {
    const tbody = document.getElementById('ativosTableBody');
    tbody.innerHTML = '';
    
    if (filteredAtivos.length === 0) {
        document.getElementById('emptyMessage').classList.remove('d-none');
        document.getElementById('ativosTable').style.display = 'none';
        return;
    }
    
    document.getElementById('ativosTable').style.display = 'table';
    document.getElementById('emptyMessage').classList.add('d-none');
    
    // Pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedAtivos = filteredAtivos.slice(startIndex, endIndex);
    
    paginatedAtivos.forEach(ativo => {
        const row = document.createElement('tr');
        const statusBadgeClass = `badge-${ativo.status.toLowerCase().replace(' ', '-')}`;
        
        row.innerHTML = `
            <td><strong>#${ativo.id}</strong></td>
            <td>${escapeHtml(ativo.descricao)}</td>
            <td><code>${escapeHtml(ativo.numero_serie)}</code></td>
            <td>
                <span class="badge ${statusBadgeClass}">
                    ${escapeHtml(ativo.status)}
                </span>
            </td>
            <td>${escapeHtml(ativo.localizacao)}</td>
            <td>R$ ${formatCurrency(ativo.valor_estimado)}</td>
            <td>
                <button class="btn btn-sm btn-info" onclick="viewDetails(${ativo.id})">
                    <i class="bi bi-eye"></i> Ver
                </button>
                <a href="editar.html?id=${ativo.id}" class="btn btn-sm btn-warning">
                    <i class="bi bi-pencil"></i> Editar
                </a>
            </td>
        `;
        
        tbody.appendChild(row);
    });
    
    // Update pagination info
    const totalPages = Math.ceil(filteredAtivos.length / itemsPerPage);
    document.getElementById('paginationInfo').textContent = 
        `Página ${currentPage} de ${totalPages} (${filteredAtivos.length} ativo${filteredAtivos.length !== 1 ? 's' : ''})`;
}

function viewDetails(ativoId) {
    const ativo = allAtivos.find(a => a.id === ativoId);
    if (!ativo) return;
    
    const detailsBody = document.getElementById('detailsModalBody');
    const criadoEm = new Date(ativo.criado_em).toLocaleDateString('pt-BR');
    const atualizadoEm = new Date(ativo.atualizado_em).toLocaleDateString('pt-BR');
    const dataAquisicao = new Date(ativo.data_aquisicao).toLocaleDateString('pt-BR');
    const statusBadgeClass = `badge-${ativo.status.toLowerCase().replace(' ', '-')}`;
    
    detailsBody.innerHTML = `
        <div class="row mb-3">
            <div class="col-md-6">
                <p><strong>ID:</strong> #${ativo.id}</p>
                <p><strong>Descrição:</strong> ${escapeHtml(ativo.descricao)}</p>
                <p><strong>Número de Série:</strong> <code>${escapeHtml(ativo.numero_serie)}</code></p>
                <p><strong>MAC Address:</strong> ${ativo.mac_address ? `<code>${ativo.mac_address}</code>` : 'N/A'}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Tipo ID:</strong> ${ativo.tipo_id}</p>
                <p><strong>Status:</strong> <span class="badge ${statusBadgeClass}">${escapeHtml(ativo.status)}</span></p>
                <p><strong>Localização:</strong> ${escapeHtml(ativo.localizacao)}</p>
                <p><strong>Valor Estimado:</strong> R$ ${formatCurrency(ativo.valor_estimado)}</p>
            </div>
        </div>
        <hr>
        <div class="row">
            <div class="col-md-6">
                <p><strong>Data de Aquisição:</strong> ${dataAquisicao}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Criado em:</strong> ${criadoEm}</p>
                <p><strong>Atualizado em:</strong> ${atualizadoEm}</p>
            </div>
        </div>
    `;
    
    document.getElementById('editButton').href = `editar.html?id=${ativoId}`;
    
    const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
    modal.show();
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value).replace('R$', '').trim();
}
