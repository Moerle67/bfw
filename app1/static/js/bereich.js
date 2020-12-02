function OnClickBereich() {
    var deineValue = document.getElementById("auswahlBereich").value;
    var send = "/pr1/kanban/all?bereich="+deineValue
    window.location=send
}