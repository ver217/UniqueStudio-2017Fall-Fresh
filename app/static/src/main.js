function input_check() {
    return $('#password').val&&$('#id').val
}
function init() {
    $('.ui.accordion').accordion();
    $('table').tablesort();
}