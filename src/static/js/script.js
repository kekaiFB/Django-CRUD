const only_diagnosis = !!document.querySelector('.only_diagnosis');


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
        trHTML += `<tr>`;

        // коллонка действий: кнопки или пустая ячейка
        if (!only_diagnosis) {
        trHTML += `<td>
            <button class="btn-physics btn-edit update" id="${item.id}" data-toggle="modal" data-target="#editDiagnosisModal" title="Редактировать">
              <i class="fas fa-pen"></i>
            </button>
            <button class="btn-physics btn-delete delete" id="${item.id}" data-toggle="modal" data-target="#deleteDiagnosis" title="Удалить">
              <i class="fas fa-trash"></i>
            </button>
          </td>
        `;
        }
        
        trHTML += `
          <td>${item.fio ?? ''}</td>
          <td>
            ${item.diagnosis ?? ''}
            <button class="btn-diagnosis-edit btn-edit update-diagnosis-only" id="${item.id}" data-toggle="modal" data-target="#editDiagnosisOnlyModal" title="Редактировать диагноз">
              <i class="fas fa-pen"></i>
            </button>
          </td>
        `;
        
        // далее — блоки по режимам
        if (only_diagnosis) {
          trHTML += `<td>${item.recomendation_healing ?? ''}</td>`;
        } else {
          trHTML += `
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
            <td>${item.chs ?? ''}</td>
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
          `;
        }
        
        trHTML += `</tr>`;
        
});
$('#Diagnosis-Records tbody').html(trHTML);
        // Инициализация DataTable после загрузки данных
        initializeDataTable();
    }
});


let columnDefs = [];

if (only_diagnosis) {
    columnDefs = [];
} else {
    columnDefs = [
        {
            targets: 0, // действия
            orderable: false,
            searchable: false,
            width: '100px',
            className: 'text-center actions-column'
        },
        {
            targets: 1, // ФИО
            width: '180px',
            className: 'text-center fio-column'
        },
        {
            targets: 2, // Диагноз
            width: '200px',
            className: 'text-center diagnosis-column'
        },
        {
            targets: 3, // Пол
            width: '80px',
            className: 'text-center gender-column'
        },
        {
            targets: 4, // Возраст
            width: '80px',
            className: 'text-center age-column'
        },
        {
            targets: 5, // Вес
            width: '80px',
            className: 'text-center weight-column'
        },
        {
            targets: 6, // Рост
            width: '80px',
            className: 'text-center height-column'
        },
        {
            targets: 7, // Дата
            width: '120px',
            className: 'text-center date-column'
        }
    ];
}


// Функция инициализации DataTable
function initializeDataTable() {
    let table = $('#Diagnosis-Records').DataTable({
        responsive: true,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.13.7/i18n/ru.json'
        },
        pageLength: 25,
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "Все"]],
        dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>' +
             '<"row"<"col-sm-12"tr>>' +
             '<"row"<"col-sm-12 col-md-5"i><"col-sm-12 col-md-7"p>>',
        columnDefs: columnDefs,
        scrollX: true,
        scrollCollapse: true,
        autoWidth: false,
        initComplete: function () {
            // Добавляем фильтры для каждого столбца
            this.api().columns().every(function () {
                let column = this;
                let title = column.header().textContent;
                
                // Пропускаем столбец с действиями
                if (column.index() === 0) return;
                
                // Создаем input для фильтрации
                let input = $('<input class="form-control form-control-sm column-filter" type="text" placeholder="Фильтр ' + title + '" />')
                    .appendTo($(column.header()))
                    .on('keyup change', function () {
                        if (column.search() !== this.value) {
                            column.search(this.value).draw();
                        }
                    });
            });
        }
    });
    
    // Обработчики для кнопок экспорта
    $('#copyBtn').on('click', function() {
        table.buttons.exportData({
            modifier: {
                search: 'applied',
                order: 'applied'
            }
        });
        // Простое копирование в буфер обмена
        let data = table.buttons.exportData({
            modifier: {
                search: 'applied',
                order: 'applied'
            }
        });
        
        let csvContent = "data:text/csv;charset=utf-8,";
        data.body.forEach(function(rowArray) {
            let row = rowArray.join(",");
            csvContent += row + "\r\n";
        });
        
        let encodedUri = encodeURI(csvContent);
        let link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "diagnosis_data.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    
    $('#csvBtn').on('click', function() {
        let data = table.buttons.exportData({
            modifier: {
                search: 'applied',
                order: 'applied'
            }
        });
        
        let csvContent = "data:text/csv;charset=utf-8,";
        data.body.forEach(function(rowArray) {
            let row = rowArray.join(",");
            csvContent += row + "\r\n";
        });
        
        let encodedUri = encodeURI(csvContent);
        let link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "diagnosis_data.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    
    $('#excelBtn').on('click', function() {
        let data = table.buttons.exportData({
            modifier: {
                search: 'applied',
                order: 'applied'
            }
        });
        
        // Создаем HTML таблицу для Excel
        let htmlContent = '<table>';
        data.body.forEach(function(rowArray) {
            htmlContent += '<tr>';
            rowArray.forEach(function(cell) {
                htmlContent += '<td>' + cell + '</td>';
            });
            htmlContent += '</tr>';
        });
        htmlContent += '</table>';
        
        let blob = new Blob([htmlContent], {type: 'application/vnd.ms-excel'});
        let url = window.URL.createObjectURL(blob);
        let link = document.createElement("a");
        link.href = url;
        link.download = "diagnosis_data.xls";
        link.click();
        window.URL.revokeObjectURL(url);
    });
    
    $('#printBtn').on('click', function() {
        let data = table.buttons.exportData({
            modifier: {
                search: 'applied',
                order: 'applied'
            }
        });
        
        let printWindow = window.open('', '_blank');
        printWindow.document.write('<html><head><title>Диагнозы</title>');
        printWindow.document.write('<style>table { border-collapse: collapse; width: 100%; } th, td { border: 1px solid black; padding: 8px; text-align: center; } th { background-color: #f2f2f2; }</style>');
        printWindow.document.write('</head><body>');
        printWindow.document.write('<h2>Список диагнозов</h2>');
        printWindow.document.write('<table>');
        
        // Заголовки
        printWindow.document.write('<tr>');
        data.header.forEach(function(header) {
            printWindow.document.write('<th>' + header + '</th>');
        });
        printWindow.document.write('</tr>');
        
        // Данные
        data.body.forEach(function(rowArray) {
            printWindow.document.write('<tr>');
            rowArray.forEach(function(cell) {
                printWindow.document.write('<td>' + cell + '</td>');
            });
            printWindow.document.write('</tr>');
        });
        
        printWindow.document.write('</table></body></html>');
        printWindow.document.close();
        printWindow.print();
    });
    
    return table;
}

// Обработчики для закрытия модальных окон
$(document).ready(function() {
    // При закрытии модального окна добавления
    $('#addDiagnosisModal').on('hidden.bs.modal', function () {
        $('#add-Diagnosis').trigger('reset');
    });
    
    // При закрытии модального окна редактирования
    $('#editDiagnosisModal').on('hidden.bs.modal', function () {
        $('#editDiagnosis').trigger('reset');
    });
    
    // При закрытии модального окна редактирования диагноза
    $('#editDiagnosisOnlyModal').on('hidden.bs.modal', function () {
        $('#editDiagnosisOnly').trigger('reset');
    });
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
                refreshDataTable();
            },
            error: function(xhr) {
                console.error("Ошибка загрузки данных:", xhr);
            }
                });
    });
});   

// Функция для обновления DataTable без перезагрузки страницы
function refreshDataTable() {
    $.ajax({
        url: "/api/diagnosis/",
        dataType: "json",
        success: function(response) {
            let trHTML = '';
            $.each(response, function (i, item) {
                trHTML += `<tr>`;

// коллонка действий: кнопки или пустая ячейка
trHTML += only_diagnosis ? `<td></td>` : `
  <td>
    <button class="btn-physics btn-edit update" id="${item.id}" data-toggle="modal" data-target="#editDiagnosisModal" title="Редактировать">
      <i class="fas fa-pen"></i>
    </button>
    <button class="btn-physics btn-delete delete" id="${item.id}" data-toggle="modal" data-target="#deleteDiagnosis" title="Удалить">
      <i class="fas fa-trash"></i>
    </button>
  </td>
`;

trHTML += `
  <td>${item.fio ?? ''}</td>
  <td>
    ${item.diagnosis ?? ''}
    <button class="btn-diagnosis-edit btn-edit update-diagnosis-only" id="${item.id}" data-toggle="modal" data-target="#editDiagnosisOnlyModal" title="Редактировать диагноз">
      <i class="fas fa-pen"></i>
    </button>
  </td>
`;

// далее — блоки по режимам
if (only_diagnosis) {
  trHTML += `<td>${item.recomendation_healing ?? ''}</td>`;
} else {
  trHTML += `
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
    <td>${item.chs ?? ''}</td>
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
  `;
}

trHTML += `</tr>`;

            });
            
            // Очищаем и пересоздаем DataTable
            if ($.fn.DataTable.isDataTable('#Diagnosis-Records')) {
                $('#Diagnosis-Records').DataTable().destroy();
            }
            
            $('#Diagnosis-Records tbody').html(trHTML);
            // initializeDataTable();
        },
        error: function(xhr) {
            console.error("Ошибка загрузки данных:", xhr);
        }
    });
}

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
                refreshDataTable();
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
                refreshDataTable();
            },
            error: function(xhr) {
                console.error("Ошибка загрузки данных:", xhr);
            }
        });

    });
});   

// Обработчик для редактирования только диагноза
$('#Diagnosis-Records').on('click', '.update-diagnosis-only', function(e){
    e.preventDefault();
    const id = $(this).attr('id');
    $('#DiagnosisId').val(id);
    
    // Получаем текущий диагноз для отображения в форме
    $.ajax({
        url: `/api/diagnosis/${id}/`,
        method: 'GET',
        success: function(result){
            $('#diagnosisText').val(result.diagnosis || '');
        },
        error: function(xhr) {
            console.error("Ошибка загрузки данных:", xhr);
        }
    });
});

// Сохранение отредактированного диагноза
$(function() { 
    $('#editDiagnosisOnly').on('submit', function(e) { 
        e.preventDefault(); 
        
        let id = $("#DiagnosisId").attr("value");
        let diagnosisText = $('#diagnosisText').val();
        
        let myurl = `/api/diagnosis/edit/${id}/`;
        
        $.ajax({
            type: 'PUT',
            url: myurl,
            contentType: "application/json", 
            data: JSON.stringify({
                diagnosis: diagnosisText
            }),
            dataType: "json",
            success: function(data){
                alert("Диагноз обновлен");
                refreshDataTable();
            },
            error: function(xhr) {
                console.error("Ошибка обновления диагноза:", xhr);
            }
        });
    });
});   