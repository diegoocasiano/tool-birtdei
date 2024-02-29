var password = sessionStorage.getItem('password');
if (!password) {
    password = prompt("Enter password");
    if (password === "Mc1107#2002") {
        sessionStorage.setItem('password', password);
    } else {
        document.write('<p>:(</p>');
    }
}

if (password === "Mc1107#2002"){
    document.getElementById("content").style.display = "block";
    } else {
        document.write('<p>Password incorrect</p>');
    }

function showLoader() {
    var button = document.getElementById('sendButton');
    button.innerHTML = '<span class="loader"></span>';
    return true; // Envía el formulario
}