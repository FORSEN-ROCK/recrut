//var selected = []//Global var
var selected_display_left;//Global var
var selected_display_rigth;//Global var

function update_selected(){
    //var target = event.target;
    //console.log(target);
    //if(target.tagName == 'SELECT' && target.id == 'id_vacancy_0'){
    var select_elm = document.body.querySelector("select[id='id_vacancy_1']");
    selected = [];
    var vacancy_var = document.body.querySelector("input[name='select_vacancy']");
    for(var i = 0; i < select_elm.children.length; i++)
        selected.push(select_elm.children[i].value);
        
    vacancy_var.value = selected;
    //}
    //else
    //    return;
}

function creat_option(selected_record){
    var choices = document.body.querySelector("select[id='id_vacancy_0']");
    var selected = document.body.querySelector("select[id='id_vacancy_1']");
    for(var i=0; i < choices.children.length; i++){
        if(choices.children[i].value == selected_record){
            var option = choices.removeChild(choices.children[i]);
            selected.appendChild(option);
        }
    }   
}

function del_option(selected_record){
    var choices = document.body.querySelector("select[id='id_vacancy_0']");
    var selected = document.body.querySelector("select[id='id_vacancy_1']");
    for(var i=0; i < selected.children.length; i++){
        if(selected.children[i].value == selected_record){
            var option = selected.removeChild(selected.children[i]);
            choices.appendChild(option);
        }
    }
}

function choice(event){
    var target = event.target;
    if(target.tagName == 'OPTION'){
        //selected.push(target.value);
        var select_id = target.value;
        creat_option(select_id);
        update_selected();
    }
}

function cancel_choice(event){
    var target = event.target;
    if(target.tagName == 'OPTION'){
        //selected.push(target.value);
        var select_id = target.value;
        del_option(select_id);
        update_selected();
    }
}

function choice_sliding(event){
    var target = event.target;
    if(target.tagName == 'OPTION')
        selected_display_rigth = target.value;
}

function select_sliding(event){
    var target = event.target;
    if(target.tagName == 'OPTION')
        selected_display_left = target.value;
}

function left_button(event){
    if(selected_display_left != undefined){
        del_option(selected_display_left);
        update_selected();
    }
    else
        return;
}

function right_button(event){
    if(selected_display_rigth != undefined){
        creat_option(selected_display_rigth);
        update_selected();
    }
    else
        return;
}

window.onload = function(event){
    var choice_list = document.body.querySelector("select[id='id_vacancy_0']");
    var selected = document.body.querySelector("select[id='id_vacancy_1']");
    var left = document.body.querySelector("button[name='left']");
    var right = document.body.querySelector("button[name='right']");
    document.forms[0].addEventListener("click", function(event){return false})
    
    choice_list.addEventListener("dblclick", choice);
    selected.addEventListener("dblclick", cancel_choice);
    choice_list.addEventListener("click", choice_sliding);
    selected.addEventListener("click", select_sliding);
    //selected.addEventListener("change", update_selected);
    
    left.addEventListener("click", left_button);
    right.addEventListener("click", right_button);
    //console.log(choice_list);
    //console.log(left);
    //console.log(right);
};