const form = document.getElementById('formi');
const spinner = document.getElementById('spin')
let count = 0;
let lastquestion = ""
let div = document.createElement('div');

form.addEventListener('submit', function(event){
    event.preventDefault();
    spinner.style.visibility="visible";
    fetch("/ajax/", {
        method: "POST",
        body: new FormData(form)
    })
    .then(response => response.json())
    .then(response => {
        let questionlastElt = document.createElement('div');
        
        if ( count == 1 ) {
            let previous1 = `<div class="col-lg-8 box"><p id="recherches"> Recherche précédente: </p></div>`
            let div1 = document.querySelector('#question-bar');
            div.innerHTML = previous1;
            div1.parentNode.insertBefore(div.firstChild, div1.nextSibling);
        }
        else if ( count == 2 ) {
            let previous2 = document.createTextNode("Recherches précédentes:");
            let recherche = document.getElementById("recherches");
            recherche.replaceChild(previous2, recherche.firstChild);
        }

        if ( count > 0 ) {
            questionlastElt.innerHTML = `<div class="col-lg-8 box"><p>${ lastquestion }</p></div>` 
            document.getElementById('question-last-bot').appendChild(questionlastElt)
        }

        let questionElt = document.getElementById('questionbot');
        questionElt.innerHTML = `<div class="col-lg-8"><h2>${ response['question'] }</h2></div>`
        
        lastquestion = response['question']

        count += 1;
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
            
            papybotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><h2>${response['messages'][0]} ${response['address']}</h2></div>`
            if (response['summary']) {
                wikibotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><p>${response['messages'][1]} ${response['summary']} [<a href="${response['url']}">En savoir plus sur Wikipedia</a>]</p></div>` 
            }
            else {
                wikibotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><p>${response['messages'][1]}</p></div>` 
            }
        }
        else {
            mapbotElt.innerHTML = `<div class="offset-lg-2 col-lg-10" ></div>`;
            papybotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><h2>${response['messages']}</h2></div>`;
            wikibotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"></div>`;
        }
    })
    .then(display)
});

function display(){
    spinner.style.visibility="hidden"
}
