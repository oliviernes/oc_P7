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
        let questionElt = document.createElement('div');
        questionElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><h1>${ response['question'] }</h1></div>` 
        document.getElementById('questionbot').appendChild(questionElt)
        const mapbotElt = document.getElementById('mapbot');
        const papybotElt = document.getElementById('papybot');
        const wikibotElt = document.getElementById('wikibot');

        if (response['address']) {
            
            mapbotElt.innerHTML = `<div id='map' class="offset-lg-2 col-lg-10" style='width: 1000px; height: 400px;'></div>`;            
            let lati = response['locate'].lat;
            let long = response['locate'].lng;    
            var map = new mapboxgl.Map({
                container: 'map',
                center: [ long, lati ],
                style: 'mapbox://styles/mapbox/streets-v11',
                zoom: 15,
            });
            var marker = new mapboxgl.Marker()
                .setLngLat([ long, lati ])
                .addTo(map);
            
            papybotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><h1>${response['messages'][0]} ${response['address']}</h1></div>`
            if (response['summary']) {
                wikibotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><p>${response['messages'][1]} ${response['summary']} [<a href="${response['url']}">En savoir plus sur Wikipedia</a>]</p></div>` 
            }
            else {
                wikibotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><p>${response['messages'][1]}</p></div>` 
            }
        }
        else {
            mapbotElt.innerHTML = `<div class="offset-lg-2 col-lg-10" ></div>`;
            papybotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><h1>${response['messages']}</h1></div>`;
            wikibotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"></div>`;
        }
    })
    // .then(spinner => {
    //     spinner.style.visibility="hidden"
    // })
    .then(display)
});

function display(){
    spinner.style.visibility="hidden"
}
