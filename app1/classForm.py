class FormInput:
    label = ""
    type = ""
    required = True
    readonly = False

    def __init__(self, label, value="", type="text", required = "True"):
        self.label = label
        self.value = value
        self.type = type
        self.required = required
    def __str__(self):
        antwort = '<label for="'+self.label+'">'+self.label+'</label>\n'
        antwort += '<input type="'+self.type+'" class="form-control" id="'+self.label+'" value="'+self.value
        antwort += '" name="'+self.label+'"'
        if self.required: 
            antwort += " required"
        if self.readonly:
            antwort += " readonly"
        antwort += '>\n'
        return antwort

class FormSlider:
    label = ""
    min = 0
    max = 10
    required = True
    readonly = False

    def __init__(self, label, value="0", required = "True", min=0, max=10):
        self.label = label
        self.value = value
        self.min = min
        self.max
        self.required = required
    def __str__(self):
        antwort = '<label for="'+self.label+'">'+self.label+'</label>\n'
        antwort += '<input type="range" class="form-control" id="'+self.label+'" value="'+str(self.value)
        antwort += '" name="'+self.label+'"'
        antwort += ' min="'+str(self.min)+'"'
        antwort += ' max="'+str(self.max)+'"'
        if self.required: 
            antwort += " required"
        if self.readonly:
            antwort += " readonly"
        antwort += '>\n'
        return antwort

class Btn:
    name = ""
    label = ""
    color = ""
    onClick = ""
    modal = ""
    novaliade = False
    type = ""
    def __init__(self, name, label, color="primary", onClick="", modal="", formnovalidate=False, type="submit"):
        self.name = name
        self.label= label
        self.color = color
        self.onClick = onClick
        self.modal = modal
        self.novaliade = formnovalidate
        self.type = type
    def __str__(self):
        antwort ='<button class="btn btn-'+self.color+'" name="button" value="'+self.label+'" '
        antwort += 'type="'+self.type+'" '
        if self.onClick != "":
            antwort += ' onclick="'+self.onClick+'()" '
        if self.modal != "":
            antwort += 'data-toggle="modal" data-target="#'
            antwort += self.modal
            antwort += '" '
        if self.novaliade:
            antwort += " formnovalidate"
        antwort += ' >'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort

class BtnSave:
    name = "Speichern"
    def __str__(self):
        antwort ='<button type="submit" class="btn btn-primary" name="button" value="save">'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort
        
class BtnCancel:
    name = "Abbruch"
    def __str__(self):
        antwort ='<button type="submit" class="btn btn-primary" name="button" value="cancel" formnovalidate>'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort

class BtnNext:
    name = "Speichern und Nächster"
    def __str__(self):
        antwort ='<button type="submit" class="btn btn-primary" name="button" value="next">'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort

class BtnRemove:
    name = "Löschen"
    def __str__(self):
        antwort ='<button type="submit" class="btn btn-danger" name="button" value="remove" formnovalidate>'
        antwort +=  self.name
        antwort +=  '</button>'
        return antwort

class FormAuswahl:
    liste = ""
    value = ""
    name = ""
    def __init__(self, name, liste, value=0):
           self.liste = liste
           self.value = value
           self.name = name
    def __str__(self):
        daten = self.liste.objects.filter(aktiv=True)
        antwort = '\n<label for="'+self.name+'">'+self.name+': </label>\n'
        antwort += '<select name="'+self.name+'" class="form-control">\n'
        for zeile in daten:
            antwort += '<option value="'+str(zeile.id)+'"'
            if zeile.id == self.value:
                antwort += "selected "
            antwort +='>'+str(zeile)+'</option>\n'
        antwort += '</select>\n'


        return antwort

def formZeile(*liste):
    antwort = '<div class="form-row">\n'
    for element in liste:
        antwort += '<div class="col">' 
        antwort += str(element)
        antwort += '</div>'
    antwort += '\n</div>'
    return antwort