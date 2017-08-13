var selection = ""; // голобальный объект
document.addEventListener("click",function(event){
            var target = event.target;
            if(target.dataset.comand == undefined) {
                return;
            }
            switch(target.dataset.comand) {
                case "parse":
                    var textContain = document.querySelector("textarea");
                    var dataString = textContain.value;
                    if(dataString == "") {
                        return;
                    }
                    var parserForm = document.forms[0];
                    for(var key in parser){
                        var itemParse = parser[key].exec(dataString);
                        if(itemParse.length != 0){
                            parserForm[key].value = itemParse[1];//dataString.match(parser[key][1]);
                            //console.log(''+ key + ' => ' + parser[key].exec(dataString));
                        }
                    }
                    break;
                    
                case "textField":
                    selection = "";//глобальный объект
                    var currentActionElem = document.activeElement;
                    if(currentActionElem.tagName == "TEXTAREA"){
                        selection = currentActionElem.value.substring(currentActionElem.selectionStart, currentActionElem.selectionEnd);
                    }
                    break;
                    
                case "fillField":
                    if(!event.ctrlKey){
                        return;
                    }
                    event.target.value = selection;
                    break;

                case "experienceField":
                    var listExperience =  document.querySelector("select[name='experience']");
                    if(event.target.value == "true"){
                        listExperience.disabled = false;
                    }
                    else{
                        listExperience.disabled = true;
                        listExperience.value = "";
                    }
                    break;
                    
                case "parseField":
                    var parserForm = document.forms[0];
                    var fieldKey = event.target.dataset.name;
                    parserForm[fieldKey].value = selection;
                    break;
                 
            }
        });
        //document.addEventListener("click",handlerClick);