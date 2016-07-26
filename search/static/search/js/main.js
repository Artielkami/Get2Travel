/**
 * Created by admin on 29/04/2016.
 */
$('#way input:radio').change(function(){
    if ($(this).val() == '2') {
        $('#inbound').css('visibility', 'visible');
    } else {
        $('#inbound').css('visibility', 'hidden');
    }
});

function rt_day() {
    var d = new Date();
    d.setDate(d.getDate() + 3);
    var day = d.getDate();
    var year = d.getYear() + 1900;
    var mon = d.getMonth() + 1;
    if (day == 1 || day == 2 || day == 3) {
        mon += 1;
    }
    var time;
    if (day < 10 && mon < 10) {
        time = year + '-0' + mon + '-0' + day;
        $('#return').val(time);
        return false;
    }
    else if (day < 10 && mon > 10) {
        time = year + '-' + mon + '-0' + day;
        $('#return').val(time);
        return false;
    }
    else if (day > 10 && mon < 10) {
        time = year + '-0' + mon + '-' + day;
        $('#return').val(time);
        return false;
    }
    else {
        time = year + '-' + mon + '-' + day;
        $('#return').val(time);
        return false;
    }
}
function test() {
    var d = new Date();
    var day = d.getDate() + 1;
    var year = d.getYear() + 1900;
    var mon = d.getMonth() + 1;
    var time;
    if (day < 10 && mon < 10) {
        time = year + '-0' + mon + '-0' + day;
        $('#outbound').val(time);
        return false;
    }
    else if (day < 10 && mon > 10) {
        time = year + '-' + mon + '-0' + day;
        $('#outbound').val(time);
        return false;
    }
    else if (day > 10 && mon < 10) {
        time = year + '-0' + mon + '-' + day;
        $('#outbound').val(time);
        return false;
    }
    else {
        time = year + '-' + mon + '-' + day;
        $('#outbound').val(time);
        return false;
    }
}
function makeday(d, id) {
    var day = d.getDate();
    var year = d.getYear() + 1900;
    var mon = d.getMonth() + 1;
    var time;
    if (day < 10 && mon < 10) {
        time = year + '-0' + mon + '-0' + day;
        $(id).val(time);
        return false;
    }
    else if (day < 10 && mon > 10) {
        time = year + '-' + mon + '-0' + day;
        $(id).val(time);
        return false;
    }
    else if (day > 10 && mon < 10) {
        time = year + '-0' + mon + '-' + day;
        $(id).val(time);
        return false;
    }
    else {
        time = year + '-' + mon + '-' + day;
        $(id).val(time);
        return false;
    }
}