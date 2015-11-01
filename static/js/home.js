$(document).ready(function() {

    var token = localStorage.getItem('token');
    $.ajax({
        type: "GET",
        url: "http://timetable-ttv1.rhcloud.com/users/2",//url login -> rhcloud.com
        contentType: "application/json; charset=utf-8",
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", "Bearer "+token)
        },
        cache: false,
        success: function(data){
            if(data){
                var code = data['code'];
            }
            else{
                var lala="";
            }
        }
    });

});