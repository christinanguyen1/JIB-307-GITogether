var cName = document.getElementById("cName");
var about = document.getElementById("about");
var recruit = document.getElementById("recruit");

var editButton = document.getElementById("edit");
var saveButton = document.getElementById("save");
editButton.addEventListener("click", function() {
    document.getElementById('edit').hidden = true;
    document.getElementById('save').hidden = false;
    cName.contentEditable = true;
    cName.style.backgroundColor = "#bebebe";
    about.contentEditable = true;
    about.style.backgroundColor = "#bebebe";
    recruit.contentEditable = true;
    recruit.style.backgroundColor = "#bebebe";
} );

saveButton.addEventListener("click", function() {
    document.getElementById('edit').hidden = false;
    document.getElementById('save').hidden = true;
    cName.contentEditable = false;
    var newName= cName.innerHTML;
    localStorage.userEdits = newName;
    cName.style.backgroundColor = "white";

    var newAbout = cName.innerHTML;
    localStorage.userEdits = newAbout;
    about.contentEditable = false;
    about.style.backgroundColor = "white";

    var newRecruit = cName.innerHTML;
    localStorage.userEdits = newRecruit;
    recruit.contentEditable = false;
    recruit.style.backgroundColor = "white";
} )
