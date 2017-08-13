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