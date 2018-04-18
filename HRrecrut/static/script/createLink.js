function create_link_pg(){ 
    var url = window.location.href;
    var container_page = document.querySelector("div[class='pagination']");
    var links = container_page.querySelectorAll("a");
    var index = url.length
    var pattern = url.slice(0, index - 1)
    console.log(links)
    for(var i=0; i < links.length; i++){
        links[i].href = pattern + links[i].dataset.num
        
        if(url == links[i].href){
            links[i].classList.add("active");
        }
    }
    if(links.length > 25){
    
    }
}
window.onload = create_link_pg;
