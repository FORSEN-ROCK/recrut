//alert("It's worck!");

window.onload = function(){
    var sourceWin = document.getElementById('sourceWin');
    //console.log(sourceWin);
    var sourceLink = sourceWin.src;
    //window.open(sourceLink);
    sourceWin.contentWindow.location.href = 'https://hh.ru/resume/e9bb81ccff0337fea50039ed1f577a68444648';//'' + sourceLink;
    sourceWin.onload = null;
    //console.log('ghfh');
    //alert("it's worck!");
    //request = new XMLHttpRequest();
    //request.open("GET", sourceLink, false);
    //request.withCredentials = true;
    //request.send(null);
    //if(request.readyState == 4 && request.status == 200){
    //    console.log(request);
    //    sourceWin.innerHTML = request.responseText;;
    //}
};

    