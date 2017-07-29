function input_check() {
    return $('#password').val&&$('#id').val
}
function init() {
    $('.ui.accordion').accordion();
    $('table').tablesort();
    $('#pick-out-btn').children().get().forEach(function (element) {
        $(element).bind("click",{team:element.innerHTML},pick_out);
    });
}
function judge(line,team) {
    var line_team = line.getElementsByName('td')[-4];
    if(line_team===team){

    }else {
        line.transiton('fly left');
    }
}
var info_table=$('#info_table');
function pick_out(event) {
    var lines=info_table.children('tr').get(),
        team=event.data.team;
    lines.map(judge(team));
}