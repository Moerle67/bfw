$('#exampleModal').on('show.bs.modal', function (event) {

    var button = $(event.relatedTarget) // Button that triggered the modal
    var recipient = button.data('whatever') // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('.modal-title').text('New message to ' + recipient)
    test = modal.find('.modal-body input').val(recipient)

  })

function formularAuswerten() {
    var deineValue = document.getElementById("message-text").value;
    var send = "/pr1/kanban/test?var1="+deineValue
    window.location=send
}

function onNeuKanbanBereich() {
  var bezeichnung=document.getElementById("mod_bezeichnung").value
  var slug=document.getElementById("mod_slug").value
  var kommentar=document.getElementById("mod_kommentar").value

  var name = document.getElementById("Name").value
  var beschreibung = document.getElementById("Kommentar").value
  var send = "/pr1/kanban/onNeu?bezeichnung="+bezeichnung
  send += "&slug="+slug
  send += "&kommentar="+kommentar
  send += "&name="+name
  send += "&beschreibung="+beschreibung
  window.location=send
}

function add_comment(question, id, name, gruppe) {
  let comment = prompt(question+ " zu "+name, "Anmerkung");
  // comment = comment.replaceAll(" ","_");
  var send = "/pr1/anwesenheit/add_comment/"+id+"/"+comment+"/"+gruppe
  
  window.location=send
}