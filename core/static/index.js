

document.addEventListener('DOMContentLoaded', (event) => {
    var element = document.getElementById('card');
    
    document.getElementById('closebtn').addEventListener('click', function(){
        element.style.display = 'none';
        document.getElementById('blur').classList.remove('active');
    });

    function toggleFunction(){
        var topNav = document.getElementById('topNav');
        if (topNav.className == "topNav"){
            topNav.className += 'responsive';
        }
        else{
            topNav.className = "topNav";
        }
    }
});