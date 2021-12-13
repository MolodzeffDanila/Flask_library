function filter(button){
    let id = button.id;
    call_ajax(id, (res) => {
        let books = JSON.parse(res);
        for(let book of books){
            let book_elem = document.getElementById(book.id);
            if(book.status === true){
                book_elem.style.display = 'block';
            }else{
                book_elem.style.display = 'none';
            }
        }
    });
}

function call_ajax(id, callback){
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function (){
        if(this.readyState == 4 && this.status == 200){
            callback(this.responseText);
        }
    }
    xhttp.open("GET", `/filter/${id}`,true);
    xhttp.send();
}