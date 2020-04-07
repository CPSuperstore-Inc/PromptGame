function isGameRunningCheck(gameId){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if(this.responseText == "false"){
                window.location.replace("/gameEnded/" + gameId);
            }
        }
    };
    xhttp.open("GET", "/api/is-running/" + gameId, true);
    xhttp.send();
}

function startGameRunningCheckThread(gameId){
    window.setInterval(function(){
        isGameRunningCheck(gameId)
    }, 2000);
}