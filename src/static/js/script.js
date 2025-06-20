function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Use csrf token while doing post request, this will prevent 500 Server Error
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
}); 

//All diagnosis API
$.ajax({
    url : "/api/diagnosis/",
    dataType: "json",
    success : function (response) {
        let trHTML = '';
    $.each(response, function (i, item) {
        trHTML += `<tr>
            <td>
                <button class="btn-physics btn-edit update" id="${item.id}" data-toggle="modal" data-target="#editDiagnosisModal" title="Редактировать">
                    <i class="fas fa-pen"></i>
                </button>

                <button class="btn-physics btn-delete delete" id="${item.id}" data-toggle="modal" data-target="#deleteDiagnosis" title="Удалить">
                    <i class="fas fa-trash"></i>
                </button>

            </td>
            <td>${item.fio ?? ''}</td>
            <td>${item.pol ?? ''}</td>
            <td>${item.vozrast ?? ''}</td>
            <td>${item.ves ?? ''}</td>
            <td>${item.rost ?? ''}</td>
            <td>${item.simptomy_dni ?? ''}</td>
            <td>${item.anamnez ?? ''}</td>
            <td>${item.kashel ?? ''}</td>
            <td>${item.mokrota ?? ''}</td>
            <td>${item.odyshka ?? ''}</td>
            <td>${item.temperatura ?? ''}</td>
            <td>${item.pritplenie ?? ''}</td>
            <td>${item.oslablenie ?? ''}</td>
            <td>${item.auskultaciya ?? ''}</td>
            <td>${item.saturaciya ?? ''}</td>
            <td>${item.chss ?? ''}</td>
            <td>${item.ofv1 ?? ''}</td>
            <td>${item.zhel_ofv1 ?? ''}</td>
            <td>${item.limfadenopatiya ?? ''}</td>
            <td>${item.ochagi ?? ''}</td>
            <td>${item.konsolidacii ?? ''}</td>
            <td>${item.fibrozno_kistoznye ?? ''}</td>
            <td>${item.polosti ?? ''}</td>
            <td>${item.fibroz ?? ''}</td>
            <td>${item.plevralnyj_vypot ?? ''}</td>
            <td>${item.leykocity ?? ''}</td>
            <td>${item.palochko ?? ''}</td>
            <td>${item.eozinofily ?? ''}</td>
            <td>${item.soe ?? ''}</td>
            <td>${item.bak_srb ?? ''}</td>
            <td>${item.imt ?? ''}</td>
            <td>${item.created_at?.slice(0, 10) ?? ''}</td>
            <td>${item.updated_at?.slice(0, 10) ?? ''}</td>
        </tr>`;
});
$('#Diagnosis-Records tbody').html(trHTML);

    }
});

$('#create').click(function(){ 
    $("#add-Diagnosis").trigger('reset');
});

//Save New Diagnosis Button
$(function() { 
    $('#addDiagnosis').on('submit', function(e) { 
        e.preventDefault();  
        let myurl = "/api/diagnosis/add/";

        $.ajax({
            type : 'POST',
            url : myurl,
            contentType: "application/json", 
            data :  JSON.stringify( getDiagnosisDataFromForm('#addDiagnosisModal')),
            dataType: "json",
            success: function(data){
                alert("Формула добавлена");
                location.reload();
            },
            error: function(xhr) {
                console.error("Ошибка загрузки данных:", xhr);
            }
        });
    });
});

function getDiagnosisDataFromForm(formSelector) {
    const formData = {};
    $(formSelector + ' [name]').each(function () {
        const name = $(this).attr('name');
        let value = $(this).val();

        // Преобразуем пустую строку в null
        if (value === '') {
            value = null;
        }

        // Автоматическое приведение к числам, если поле типа number
        if (this.type === 'number' && value !== null) {
            value = this.step === 'any' ? parseFloat(value) : parseInt(value);
        }

        formData[name] = value;
    });

    return formData;
}


function fillDiagnosisFormData(formSelector, data) {
    for (const key in data) {
        const $el = $(formSelector + ` [name="${key}"]`);
        if ($el.length) $el.val(data[key]);
    }
}


// Edit
$('#Diagnosis-Records').on('click', '.update', function(e){
    e.preventDefault();
    const id = $(this).attr('id');
    $('#Myid').val(id);
    $.ajax({
        url: `/api/diagnosis/${id}/`,
        method: 'GET',
        success: function(result){
            fillDiagnosisFormData('#editDiagnosis', result);
        },
        error: function(xhr) {
            console.error("Ошибка загрузки данных:", xhr);
        }
    });
});


// Delete
$('#Diagnosis-Records').on('click', '.delete', function(e){
    e.preventDefault();
    const id = $(this).attr('id');
    $('#Myid').val(id);
    $.ajax({
        url: `/api/diagnosis/${id}/`,
        method: 'GET',
        success: function(result){
            fillDiagnosisFormData('#deleteDiagnosis', result); // если ты хочешь отобразить данные
        },
        error: function(xhr) {
            console.error("Ошибка загрузки данных:", xhr);
        }
    });
});


//Save Edited Diagnosis Button
$(function() { 
    $('#editDiagnosis').on('submit', function(e) { 
        e.preventDefault();  

        let id = $("#Myid").attr("value");

        let myurl = `/api/diagnosis/edit/${id}/`;
        $.ajax({
            type : 'PUT',
            url : myurl,
            contentType: "application/json", 
            data : JSON.stringify(getDiagnosisDataFromForm('#editDiagnosisModal')),
            dataType: "json",
            success: function(data){
                alert("Формула обновлена");
                location.reload();
            },
            error: function(xhr) {
                console.error("Ошибка загрузки данных:", xhr);
            }
        });
    });
});


//Save Delete diagnosis Button
$(function() { 
    $('#deleteDiagnosis').on('submit', function(e) { 
        e.preventDefault(); 
        let id = $("#Myid").attr("value");

        let myurl = `/api/diagnosis/delete/${id}/`;

        $.ajax({
            async: true,
            url:myurl,
            method:'DELETE',
            success: function(result){
                location.reload();
            },
            error: function(xhr) {
                console.error("Ошибка загрузки данных:", xhr);
            }
        });

    });
});   