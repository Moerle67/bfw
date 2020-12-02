class ModTest():
    btn1 = '<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal" data-whatever="@mdo">Open modal for @mdo</button>'
    btn2 = '<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal" data-whatever="@fat">Open modal for @fat</button>'
    btn3 = '<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal" data-whatever="@getbootstrap">Open modal for @getbootstrap</button>'

    modDiv= '<div class="modal fade" id="exampleModal" tabindex="-1"'
    modDiv += 'aria-labelledby="exampleModalLabel" aria-hidden="true">'
    modDiv += '<div class="modal-dialog">'
    modDiv += '<div class="modal-content">'
    modDiv += '<div class="modal-header">'
    modDiv += '        <h5 class="modal-title" id="exampleModalLabel">New message</h5>'
    modDiv += '        <button type="button" class="close" data-dismiss="modal" aria-label="Close" >'
    modDiv += '        <span aria-hidden="true">&times;</span>'
    modDiv += '        </button>'
    modDiv += '    </div>'
    modDiv += '    <div class="modal-body">'
    modDiv += '        <form>'
    modDiv += '        <div class="form-group">'
    modDiv += '            <label for="recipient-name" class="col-form-label">Recipient:</label>'
    modDiv += '            <input type="text" class="form-control" id="recipient-name">'
    modDiv += '        </div>'
    modDiv += '        <div class="form-group">'
    modDiv += '            <label for="message-text" class="col-form-label">Message:</label>'
    modDiv += '            <textarea class="form-control" id="message-text"></textarea>'
    modDiv += '        </div>'
    modDiv += '        </form>'
    modDiv += '    </div>'
    modDiv += '    <div class="modal-footer">'
    modDiv += '        <button type="button" class="btn btn-secondary" data-dismiss="modal" onclick="formularAuswerten()" >Close</button>'
    modDiv += '        <button type="button" class="btn btn-primary" >Send message</button>'
    modDiv += '    </div>'
    modDiv += '    </div>'
    modDiv += '</div>'
    modDiv += '</div>'

    modSrc = '<script>\n'
    modSrc += "$('#exampleModal').on('show.bs.modal', function (event) {\n"
    modSrc += "var button = $(event.relatedTarget) // Button that triggered the modal\n"
    modSrc += "var recipient = button.data('whatever') // Extract info from data-* attributes\n"
    modSrc += "// If necessary, you could initiate an AJAX request here (and then do the updating in a callback).\n"
    modSrc += "// Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.\n"
    modSrc += "var modal = $(this)\n"
    modSrc += "modal.find('.modal-title').text('New message to ' + recipient)\n"
    modSrc += "modal.find('.modal-body input').val(recipient)\n"
    modSrc += "})\n"