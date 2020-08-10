const form = document.getElementById('formi');

form.addEventListener('submit', function(event){
    event.preventDefault();
    fetch("/ajax/", {
        method: "POST",
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(response => {
        alert(response.lat);
    })
    console.log("Ajax fonctionne");
});
