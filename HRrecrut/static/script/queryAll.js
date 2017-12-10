function validURL(){
    var VRegExp = new RegExp(/\/(http.+)/);
    var noValidHref = window.location.href
    var VResult = noValidHref.match(VRegExp); 
    var link = document.body.querySelector("input[name='link']");
    link.value = VResult[1];
    console.log(VResult[1]);
}

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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function complileQueryData(){
    var tbody = document.querySelector("table[class='resume_table']").firstElementChild;
    var entryList = tbody.querySelectorAll("input");
    var VIEW_NAME = document.querySelector("input[name='view_name']").value;
    var dataset = {view : VIEW_NAME}
    for( var i = 0; i < entryList.length; i++){
        dataset[entryList[i].name] = entryList[i].value;
    }
    return dataset;
}

function complileSaveData() {
    var fields = document.body.querySelector('form');
    var VIEW_NAME = document.querySelector("input[name='view_name']").value;
    var linkResume = document.querySelector("input[name='link']").value;
    var fieldsData = {view : VIEW_NAME, link : linkResume};
    for(var i=0; i < fields.elements.length; i++){
        if(fields.elements[i].type != "hidden"){
            fieldsData[fields.elements[i].name] = fields.elements[i].value;
        }
    }
    return fieldsData;
}

function showeStatus(responseMessage){
    var contenerStatus = document.getElementById("status");
    //console.log(contenerStatus);
    //console.log(responseMessage);
    //var message  = JSON.parse(responseMessage);
    var messageElement = document.createElement("div");
    
    if(responseMessage.status == "Success" || responseMessage.status == "Update link"){
        messageElement.className = "alert alert-success";
        messageElement.innerHTML = "Данные сохранены или обновлены";
    }
    else{
        messageElement.className = "alert alert-error";
        messageElement.innerHTML = "Произошла ошибка";
    }
    contenerStatus.appendChild(messageElement);
}
document.addEventListener("DOMContentLoaded", validURL);

document.addEventListener("click",function(event){
            var target = event.target;
            //if((target.dataset.query == undefined)&&(target.dataset.run == undefined)) {
            //    return;
            //}
            if(target.dataset.query){
                table = document.querySelector("table[class='resume_table']");
                tbody = table.firstElementChild;
                for(var i = 0; i < tbody.children.length; i++){
                    if(tbody.children[i] == tbody.firstElementChild){
                        continue;
                    }
                    else{
                        for(var j = 0; j < tbody.children[i].children.length; j++){
                            tbody.children[i].children[j].textContent  = " ";
                            if(i == 1){
                                entry = document.createElement("input");
                                entry.name = tbody.firstElementChild.children[j].dataset.name;
                                tbody.children[i].children[j].appendChild(entry);
                            }
                        }
                        document.querySelector("#run_query").disabled = false;
                    }
                }
            }
            if(target.dataset.run){
                dataset = complileQueryData();
                dataset['command'] = 'run';
                data = JSON.stringify(dataset);
                var csrftoken = getCookie('csrftoken');
                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });
                $.ajax({
                    url: "incoming/",
                    type: "POST",
                    data: data,
                    success: function(response) { console.log('s;lfkd;fl');},
                    dataType: "json"
                });   
            }
            if(target.dataset.save){
                dataset = complileSaveData();
                dataset['command'] = 'save';
                console.log(dataset);
                data = JSON.stringify(dataset);
                var csrftoken = getCookie('csrftoken');
                $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
                });
                $.ajax({
                    url: "incoming/",
                    type: "POST",
                    data: data,
                    success: function(data) { console.log(data); showeStatus(data);},
                    dataType: "json"
                });   
            }
        });