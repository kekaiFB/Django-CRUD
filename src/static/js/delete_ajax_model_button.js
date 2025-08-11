// Пример вызова функции:
// {% if 'table.change_schedulenotjob' in perms %}
//     {% del_button_ajax_model 'ScheduleNotJob' elem.id %} 
// {% endif %}

// Пример инициализации в js: delete_ajax_model(datatable=current_datatable) 
 
// В переборе строк обращаемся к обьекту, передаем название модели и ебрем его id, так же важно чтобы моедль присутствовала в словаре в функции Timetable.views.delete_ajax_model
// Функцию импортировать как скрипт после тостов и jquery, то есть можно в конце импортируемых скриптов .js

delete_ajax_model = function deleteAxajEventbuttonFunction (datatable,) {
    $(document).off('click', '.delete_ajax_model').on('click', '.delete_ajax_model', function() {
     Swal.fire({
         title: 'Удалить?',
         icon: 'warning',
         showCancelButton: true,
         confirmButtonColor: '#d33',
         cancelButtonColor: '',
         confirmButtonText: 'Да, удалить!',
         cancelButtonText: 'Отмена',
       }).then((result) => {
         if (result.isConfirmed) {
             var formData = {
                'model': $(this).data("model"),
                'id': $(this).data("model-id"),
                 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
             };                    
            toastr.info(`Инфомрация`, 'Пожалуйста подождите', { timeOut: 3000 });
            $('body').addClass('body-loading');
            $.ajax({
                url: "/timetable/delete_ajax_model", 
                data: formData,
                success: function(data) {
                    if (data.status != 'ok') {
                    toastr.error(`Ошибка`, 'Ошибка', { timeOut: 3000 });
                    $('body').removeClass('body-loading');
                    } else {
                        var id = data.id;

                        // Удаляем эту строку из таблицы
                        var rowToDelete = $('[data-model-id="' + id + '"]').closest('tr');
                        datatable.row(rowToDelete).remove().draw();

                        toastr.success(`Успешно`, 'Операция выполнена успешно', { timeOut: 3000 });
                        $('body').removeClass('body-loading');

                        // pagination_ajax(datatable, window.datatable_name_global, $(datatable.table().node()),);
                    }
                },
                error: function(error) {
                toastr.error(`Ошибка`, 'Ошибка на стороне сервера', { timeOut: 3000 });
                $('body').removeClass('body-loading');

                }
            });
         }
       }) 

    }); 
}    