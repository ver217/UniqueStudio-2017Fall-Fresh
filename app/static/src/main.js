function input_check() {
    return $('#password').val&&$('#id').val
}
function init() {
    $('.ui.accordion').accordion();
    $('table').tablesort();
}
function judge(line) {
    var line_team = line.getElementsByName(td)[-4];
    if(line_team===team){

    }else {
        line.transiton('toggle');
    }
}
var info_table=$('#info_table');
function pick_out(team) {
    var lines=info_table.getElementsByName(tr);
    lines.map(judge);
}