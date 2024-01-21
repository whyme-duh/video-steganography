

document.addEventListener('DOMContentLoaded', (event) => {
    var element = document.getElementById('card');
    
    document.getElementById('closebtn').addEventListener('click', function(){
        element.style.display = 'none';
        document.getElementById('blur').classList.remove('active');
    });
});