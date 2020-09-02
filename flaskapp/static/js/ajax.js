const form = document.getElementById('formi');
const spinner = document.getElementById('spin')
let mapNumber = 0;

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
        questionElt.innerHTML = `<div class="col-lg-8 box"><h2>${ response['question'] }</h2></div>` 

        let answerElt = document.createElement('div');
        let mapbotElt = document.createElement('div');
        let wikibotElt = document.createElement('div');

        let dialog = document.getElementById("dialogBot");
        let firstChild = dialog.firstChild;
        let chatDiv = document.createElement("div");
        dialog.insertBefore(chatDiv, firstChild);
        let chatInsert = dialog.firstChild;
    
        if (response['address']) {
            
            let mapa = "map" + mapNumber.toString();

            console.log(mapa);

            answerElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><h2>${response['messages'][0]} ${response['address']}</h2></div>`

            mapbotElt.innerHTML = `<div id="${mapa}" class="offset-lg-2 col-lg-10 col-md-8 offset-sm-2 col-sm-6 offset-xs-1 col_xs_10" style='width: 600px; height: 400px;'></div>`;
            
            if (response['summary']) {
                wikibotElt.innerHTML = `<div class="offset-lg-2 col-lg-10 offset-md-2 col-md-6 offset-sm-2 col-sm-6 col-xs-6"><p>${response['messages'][1]} ${response['summary']} [<a href="${response['url']}">En savoir plus sur Wikipedia</a>]</p></div>`
            }
            else {
                wikibotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><p>${response['messages'][1]}</p></div>` 
            }

            chatDiv.appendChild(questionElt)
            chatDiv.appendChild(answerElt)
            chatDiv.appendChild(mapbotElt)
            chatDiv.appendChild(wikibotElt)

            let lati = response['locate'].lat;
            let long = response['locate'].lng;    

            console.log(mapa);

            var map = new mapboxgl.Map({
                container: mapa,
                center: [ long, lati ],
                style: 'mapbox://styles/mapbox/streets-v11',
                zoom: 15,
            });    

            var marker = new mapboxgl.Marker()
            .setLngLat([ long, lati ])
            .addTo(map);

            mapNumber++
        }
        else {
            answerElt.innerHTML = `<div class="offset-lg-2 col-lg-10"><h2>${response['messages']}</h2></div>`;
            mapbotElt.innerHTML = `<div class="offset-lg-2 col-lg-10" ></div>`;
            wikibotElt.innerHTML = `<div class="offset-lg-2 col-lg-10"></div>`;

            chatDiv.appendChild(questionElt)
            chatDiv.appendChild(answerElt)
            chatDiv.appendChild(mapbotElt)
            chatDiv.appendChild(wikibotElt)

        }

        // document.getElementById('chatbot').appendChild(questionElt)
        // document.getElementById('chatbot').appendChild(answerElt)
        // document.getElementById('chatbot').appendChild(mapbotElt)
        // document.getElementById('chatbot').appendChild(wikibotElt)

        // let lati = response['locate'].lat;
        // let long = response['locate'].lng;    

        // function initMap(long, lati, mapa) {
        //     var map = new mapboxgl.Map({
        //         container: '${mapa}',
        //         center: [ long, lati ],
        //         style: 'mapbox://styles/mapbox/streets-v11',
        //         zoom: 15,
        //     });
    
        // initMap(long, lati, mapa)

            // new google.maps.Map(document.getElementById(div), {
            //     center: {lat: receiveLat, lng: receiveLng},
            //     zoom: 15
            //     });
        // }
        
        // console.log(mapa);

        // var map = new mapboxgl.Map({
        //     container: mapa,
        //     center: [ long, lati ],
        //     style: 'mapbox://styles/mapbox/streets-v11',
        //     zoom: 15,
        // });
        // var marker = new mapboxgl.Marker()
        // .setLngLat([ long, lati ])
        // .addTo(map);

    })
    .then(display)
});

function display(){
    spinner.style.visibility="hidden"
}
