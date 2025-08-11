function get_toast(
    title = '',
    text = '',
    status = '',
    timer = '',
    elem = ''
) {
    var $toastContainer = $('#toast-container');

    // Если контейнер отсутствует, создаем его
    if ($toastContainer.length === 0) {
        $('body').append('<div id="toast-container"></div>');
        $toastContainer = $('#toast-container');
        $toastContainer.css({
            position: 'fixed',
            top: '10px',
            right: '10px',
            width: '300px',
            maxHeight: '200px', // Максимальная высота контейнера
            overflowY: 'auto', // Включаем скролл
            zIndex: 9999
        });
    }

    title = String(title);
    text = String(text);

    // Формируем уникальный идентификатор тоста по содержимому
    var toastId = btoa(unescape(encodeURIComponent(title + text))); // Создаем уникальный ID из title + text

    // Проверяем, есть ли уже такой же тост
    var existingToast = $toastContainer.find(`[data-toast-id="${toastId}"]`);
    if (existingToast.length) {
        existingToast.remove(); // Удаляем старый дубликат перед созданием нового
    }

    // Определяем таймер по статусу
    timer = timer === '' ? (status === 'error' ? 10000 : 5000) : timer;

    // Генерируем новый тост
    var $toast;
    if (status === 'success' || title.toLowerCase().includes('успе') || text.toLowerCase().includes('успе')) {
        $toast = toastr.success(text, title, { timeOut: timer });
    } else if (status === 'info' || title.toLowerCase().includes('инф') || text.toLowerCase().includes('инф')) {
        $toast = toastr.info(text, title, { timeOut: timer });
    } else if (status === 'warning') {
        $toast = toastr.warning(text, title, { timeOut: timer });
    } else if (status === 'error' || title.toLowerCase().includes('ошибк') || text.toLowerCase().includes('ошибк')) {
        $toast = toastr.error(text, title, { timeOut: timer });
    } else {
        $toast = toastr.success(text, title, { timeOut: timer });
    }

    // Добавляем атрибут с уникальным ID, чтобы отслеживать дубликаты
    $($toast).attr('data-toast-id', toastId);


    // Если передан элемент, встраиваем его в тост
    if (elem) {
        $($toast).append(elem);
    }
}
