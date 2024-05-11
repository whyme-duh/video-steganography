

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('myform').addEventListener('submit', function clicked(){
        document.getElementById('spinner-container').style.display = 'block';
        console.log('loading');
        document.getElementsByTagName('body').classList.add('stop-scrolling');
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