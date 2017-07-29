function input_check() {
    return $('#password').val&&$('#id').val
}
function init() {
    var info_table=$('#info_table');
    $('.ui.accordion').accordion();
    $('table').tablesort();
    $('#pick-out-btn').children().get().forEach(function (element) {
        $(element).bind("click",{team:element.innerHTML},pick_out);
    });
}
function judge(line,team) {
    line=$(line);
    var line_team = line.children().get()[8];
    if(line_team===team){

    }else {
        line.transiton('fly left');
    }
}

function pick_out(event) {
    var lines=$(info_table).children('tbody').children('tr').get(),
        team=event.data.team;
    lines.forEach(function (element) {
        judge(element,team)
    });
}