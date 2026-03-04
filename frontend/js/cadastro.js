/**
 * Cadastro form handler
 */
const API_URL = 'http://localhost:8000/api';

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('cadastroForm');
    
    // Set today's date as max date for input
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('data_aquisicao').setAttribute('max', today);
    
    form.addEventListener('submit', handleFormSubmit);
    form.addEventListener('input', function(e) {
        // Bootstrap validation
        if (e.target.classList.contains('form-control') || 
            e.target.classList.contains('form-select')) {
            if (e.target.value) {
                e.target.classList.remove('is-invalid');
            }
        }
    });
});

async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Clear previous alerts
    document.getElementById('successAlert').classList.add('d-none');
    document.getElementById('errorAlert').classList.add('d-none');
    
    // Validate form
    if (!validateForm()) {
        return;
    }
    
    // Get form data
    const formData = new FormData(document.getElementById('cadastroForm'));
    const data = Object.fromEntries(formData);
    
    // Client-side validations
    const validation = validateClientSide(data);
    if (!validation.valid) {
        showError(validation.message);
        return;
    }
    
    // Convert data to proper format
    const submitData = {
        descricao: data.descricao,
        tipo_id: parseInt(data.tipo_id),
        numero_serie: data.numero_serie,
        mac_address: data.mac_address || null,
        valor_estimado: parseFloat(data.valor_estimado),
        data_aquisicao: `${data.data_aquisicao}T00:00:00`,
        localizacao: data.localizacao
    };
    
    try {
        const response = await fetch(`${API_URL}/ativos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(submitData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            console.log('Ativo created successfully:', result);
            showSuccess(`${result.message} (ID: ${result.id})`);
            document.getElementById('cadastroForm').reset();
            
            // Redirect after 2 seconds
            setTimeout(() => {
                window.location.href = 'listagem.html';
            }, 2000);
        } else {
            // Handle error response
            const errorMessage = result.detail?.error || result.detail || 'Erro ao cadastrar ativo';
            showError(errorMessage);
            
            // Mark invalid field
            if (result.detail?.field) {
                const field = document.getElementById(result.detail.field);
                if (field) {
                    field.classList.add('is-invalid');
                }
            }
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Erro ao conectar com o servidor. Verifique se o backend está rodando.');
    }
}

function validateForm() {
    const form = document.getElementById('cadastroForm');
    let isValid = true;
    
    // Check required fields
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        if (!field.value) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

function validateClientSide(data) {
    // Validate numero_serie is not empty
    if (!data.numero_serie || data.numero_serie.trim() === '') {
        return { valid: false, message: 'Número de série é obrigatório' };
    }
    
    // Validate valor_estimado is positive
    const valor = parseFloat(data.valor_estimado);
    if (valor < 0) {
        return { valid: false, message: 'Valor deve ser positivo' };
    }
    
    // Validate data is not in the future
    const data_aquisicao = new Date(data.data_aquisicao);
    const today = new Date();
    if (data_aquisicao > today) {
        return { valid: false, message: 'Data não pode ser no futuro' };
    }
    
    return { valid: true };
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
