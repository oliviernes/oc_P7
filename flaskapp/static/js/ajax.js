const form = document.getElementById('formi');
const spinner = document.getElementById('spin')

form.addEventListener('submit', function(event){
    event.preventDefault();
    spinner.style.visibility="visible";
    fetch("/ajax/", {
        method: "POST",
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(response => {
        // alert(response['locate'].lat);
        const papybotElt = document.getElementById('papybot');
        papybotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><h1>${response['messages'][0]} ${response['address']}</h1></div>` 
        const mapbotElt = document.getElementById('mapbot');
        mapbotElt.innerHTML = `<div id='map' class="offset-lg-2 col-lg-10" style='width: 1000px; height: 300px;'></div>`;            
        const wikibotElt = document.getElementById('wikibot');
        wikibotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><p>${response['messages'][1]} ${response['summary']}</p></div>` 
        let lati = response['locate'].lat;
        let long = response['locate'].lng;
        var map = new mapboxgl.Map({
            container: 'map',
            center: [ long, lati ],
            style: 'mapbox://styles/mapbox/streets-v11',
            zoom: 15,
        }); 
    })
    // .then(spinner => {
    //     spinner.style.visibility="hidden"
    // })
    .then(display)
});

function display(){
    spinner.style.visibility="hidden"
    console.log("Ajax fonctionne");
}















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
