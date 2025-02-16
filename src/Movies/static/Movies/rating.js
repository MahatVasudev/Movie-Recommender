var modal = document.getElementById("myModal") 

var btn = document.getElementById("popup");

var span = document.getElementsByClassName("close")[0];
var close_btn = document.getElementById("close");
// var remove_btn = document.getElementById("popup_pop");
var remove_mov = document.getElementById("myModal_remove");
var rate_value = document.getElementById("rating_value")

var rate = document.getElementById("rate")

rate_value.innerHTML = rate.value

// remove_btn.onclick = function(){
//     remove_mov.style.display = 'block'
// }

rate.oninput = function(){
    if (this.value > 5){
        rate_value.style.color = 'green';
    }else if(this.value == 5){
        rate_value.style.color = 'yellow';
    }else{
        rate_value.style.color = 'red';
    }
    rate_value.innerHTML = this.value
}

openRater = function(){
    modal.style.display="block"
}

OpenRaterClose = () => {
    modal.style.display = "none"
}

RemoveRater = function(){
    remove_mov.style.display = "block"
}

RemoveRaterClose = () =>{
    remove_mov.style.display = "none"
}


window.onclick = function(event){
    if (event.target == modal){
        modal.style.display = "none"
    }else if (event.target == remove_mov){
        remove_mov.style.display = 'none'
    }
}
