const jahr = parseInt(document.getElementById("hidden_year").innerHTML);
const monat = parseInt(document.getElementById("hidden_month").innerHTML);
const tag = parseInt(document.getElementById("hidden_day").innerHTML);
const stunde = parseInt(document.getElementById("hidden_hour").innerHTML);
const minute = parseInt(document.getElementById("hidden_minutes").innerHTML);

var startDateTime = new Date(jahr, monat-1, tag, stunde, minute, 0, 0);
console.log(jahr, monat-1, tag, stunde, minute, startDateTime)
var startStamp = startDateTime.getTime();

let timer, diff;

function updateClock() {
    newDate = new Date();
    newStamp = newDate.getTime();
    var element = document.getElementById("time-elapsed");
    if (newStamp > startStamp) {
        diff = Math.round((newStamp-startStamp)/1000);
        element.className="rot";
    } else {
        diff = Math.round((startStamp-newStamp)/1000);
        element.className="gruen";
    }    
    let d = Math.floor(diff/(24*60*60));
    diff = diff-(d*24*60*60);
    let h = Math.floor(diff/(60*60));
    diff = diff-(h*60*60);
    let m = Math.floor(diff/(60));
    diff = diff-(m*60);
    let s = diff;
    
    document.getElementById("time-elapsed").innerHTML = d+" Tage, "+h+" Stunden, "+m+" Minuten, "+s+" Sekunden";
}

timer = setInterval(updateClock, 1000);