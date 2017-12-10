/*
    Функция собирающая сообщение для отправки на сервер
    в формате json
*/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function complileMessage() {
    var fieldsData = {};
    //var fields = document.forms[0];//querySelectorAll('input');
    var fields = document.body.querySelector('form');
    //console.log(fields.elements);
    for(var i=0; i < fields.elements.length; i++){
        if(fields.elements[i].type != "hidden"){
            fieldsData[fields.elements[i].name] = fields.elements[i].value;
            //console.log(fields.elements[i]);
        }
    }
    /*
    for(var item in fields.elements) {
        if(item.required_id){
            fieldsData[item.name] = item.value;
            console.log(item.value);
        }
        console.log(item.name);
        console.log(item.value);
    }
    */
    return JSON.stringify(fieldsData);
};

//function 
/*
    Передача данных POST - запросом на сервер по адресу /resume/add/
    в формате json, в синхронном режиме, блокиру¤ интерфейс до ответа 
    сервера;
    кбработчик вешаетс¤ на кнопку с data-set = "add"
*/

document.addEventListener("click", function(event) {//click
    target = event.target;
    //console.log('Work!');
    if(target.dataset.addResume){
        //modal();
        var csrftoken = getCookie('csrftoken');
        alert(csrftoken);
        console.log(complileMessage);
        var csrftoken = document.body.querySelector("input[name='csrfmiddlewaretoken']");
        //console.log(csrftoken);
        var bodyRequest = 'test_data'//complileMessage();
        var request = new XMLHttpRequest();

        //request.setDisableHeaderCheck(true);
        //withCredentials = true;
        request.withCredentials = true;
        request.open("POST", '/resume/add/', true);
        request.setRequestHeader("X-CSRFToken", csrftoken);
        //bodyRequest.csrfmiddlewaretoken = csrftoken;
        console.log(bodyRequest);

        //request.setRequestHeader('Cookie','csrfmiddlewaretoken=' + csrftoken);
        request.send(bodyRequest);  
    }
});

/*
$(document).ready(function() {
       $("#test").click(function(event){
       event.preventDefault();
            $.ajax({
                 type:"POST",
                 url:"/resume/add/",//"/edit_favorites/",
                 data: {
                        'video': $('#test').val() // from form
                        },
                 success: function(){
                     $('#message').html("<h2>Contact Form Submitted!</h2>") 
                    }
            });
            return false;
       });

    });
*//*
<script type="text/javascript">
// using jQuery
var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
</script>
*/
/*
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
       $("#push").click(function(event){
       event.preventDefault();
            $.ajax({
                 type:"POST",
                 url:"/resume/add/",//"/edit_favorites/",
                 data: {
                        'video': 'test_data'//$('#test').val() // from form
                        },
                 success: function(){
                     $('#message').html("<h2>Contact Form Submitted!</h2>") 
                    }
            });
            return false;
       });

    });
    */