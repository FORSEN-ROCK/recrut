/*
document.addEventListener("click", function() {
    checkList = document.body.querySelectorAll("input[name='sourse']");
    conteiner = document.body.querySelector("input[name='sourseList']");
    listCheck = [];
    for(var item in checkList) {
        if(item.checked == true){
            listCheck.push(item.value);
        }
    }
    listCheck.value=listCheck;
});
*/
document.addEventListener("submit", function() {
    var checkList = document.body.querySelectorAll("input[type='checkbox']");
    var listCheck = [];
    console.log(checkList)
    for(var i = 0; i < checkList.length; i++) {
        if(checkList[i].checked == true){
            listCheck.push(checkList[i].value);
            console.log(checkList[i].value)
        }
    }
    listCheck.value=listCheck;
    var ls = document.createElement('input');
    ls.name = "sourseList";
    ls.type = "hidden";
    ls.value = listCheck;
    document.forms[0].appendChild(ls);
});