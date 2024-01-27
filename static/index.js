

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('myform').addEventListener('submit', function(){
        document.getElementById('spinner').style.display = 'block';
        console.log('loading');
    });
    var element = document.getElementById('card');
    
    document.getElementById('closebtn').addEventListener('click', function(){
        element.style.display = 'none';
        document.getElementById('card-container').style.display = 'none';
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