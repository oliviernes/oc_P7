const form = document.getElementById('formi');
const spinner = document.getElementById('spin')

form.addEventListener('submit', function(event){
    event.preventDefault();
    spinner.style.display == 'block';
    fetch("/ajax/", {
        method: "POST",
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(response => {
        alert(response['locate'].lat);
    })
    console.log("Ajax fonctionne");
});

// let map = document.createElement("div")

// function initMap() {
//     map = new google.maps.Map(document.getElementById("map"), {
//       center: {
//         lat: -34.397,
//         lng: 150.644
//       },
//       zoom: 8
//     });
//   }
