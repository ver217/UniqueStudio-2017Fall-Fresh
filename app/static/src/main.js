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
    var line_new=$(line),
        line_team = line_new.children().get()[8].innerHTML;
    if(line_team===team){
        if(line_new.hasClass("hidden")){
            line_new.transition('fly left');
        }
    }else {
        line_new.transition('fly left');
    }
}

function pick_out(event) {
    var lines=$(info_table).children('tbody').children('tr').get(),
        team=event.data.team;
    lines.forEach(function (element) {
        judge(element,team)
    });
}