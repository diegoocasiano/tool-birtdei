function showLoader() {
    var button = document.getElementById('sendButton');
    button.innerHTML = '<span class="loader"></span>';
    return true; // Envía el formulario
}