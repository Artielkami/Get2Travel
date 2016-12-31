/**
 * Created by admin on 29/04/2016.
 */

$(document).ready(function(){
    $(".table-result button").click(function(){
        var sid = this.id;
        var target = '#detail_' + sid;
        //alert(target);
        if($(target).hasClass('hidden')){
            $(target).removeClass('hidden');
        }else {
            $(target).addClass('hidden');
        }
    });

    $('.open-sec-btn').click(function () {
        var sid = this.id;
        var target = '.' + sid;
        //alert(target);
        if($(target).hasClass('hidden')){
            $(target).removeClass('hidden');
        }else {
            $(target).addClass('hidden');
        }
    });

    $('.datepicker').pickadate({
        weekdaysShort: ['Chủ Nhật', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7'],
        showMonthsShort: true,
        today: 'Hôm nay',
        clear: 'Xóa lựa chọn',
        close: 'Hủy',
        labelMonthNext: 'Tháng sau',
        labelMonthPrev: 'Tháng trước',
        labelMonthSelect: 'Chọn tháng',
        labelYearSelect: 'Chọn năm',
        selectMonths: true,
        selectYears: true,
        format: 'yyyy-mm-dd',
        formatSubmit: 'yyyy-mm-dd',
    });

    $('select').chosen({
        disable_search_threshold: 10,
        no_results_text: "Không tìm thấy!",
        allow_single_deselect: true,
    });
    $('.a-result-flight').hover(function(){
        $(this).css('background-color', '#C3C9C5');
    }, function () {
        $(this).css('background-color', '#ffffff');
    });

});


$('#way input:radio').change(function(){
    if ($(this).val() == '2') {
        $('#inbound').css('visibility', 'visible');
    } else {
        $('#inbound').css('visibility', 'hidden');
    }
});


/* Sort list result*/

// sort
function sortResults(lst, prop, asc) {
    lst = lst.sort(function(a, b) {
        if (asc) return (a[prop] > b[prop]);
        else return (b[prop] > a[prop]);
    });
    showResults(lst);
}

// show result after sorted
function showResults (lst) {
    //var html = '';
    // for (var i in lst) {
    //     html += '<tr>'
    //         +'<td>'+lst[i].f_name+'</td>'
    //         +'<td>'+lst[i].l_name+'</td>'
    //         +'<td>'+lst[i].age+'</td>'
    //     +'</tr>';
    // }
    //$('#results').html(html);
    alert(lst.length);
}

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