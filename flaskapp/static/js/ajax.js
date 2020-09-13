const form = document.getElementById('formi');
const spinner = document.getElementById('spin')
let mapNumber = 0;

// To switch to google map:

// let map;

// function initMap(mapa, lati, long) {
// map = new google.maps.Map(document.getElementById(mapa), {
//     center: { lat: lati, lng: long },
//     zoom: 15
// });
// }

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
        let title1 = document.createElement('h2');
        title1.textContent = document.getElementById("question").value;
        questionElt.className = "col-lg-8 box";
        questionElt.appendChild(title1);
        let answerElt = document.createElement('div');
        answerElt.className = "offset-lg-2 col-lg-10";
        let title2 = document.createElement('h2');
        let mapbotElt = document.createElement('div');
        let wikibotElt = document.createElement('div');
        let para = document.createElement('p');
        wikibotElt.appendChild(para);
        let dialog = document.getElementById("dialogBot");
        let firstChild = dialog.firstChild;
        let chatDiv = document.createElement("div");
        dialog.insertBefore(chatDiv, firstChild);
    
        if (response['address']) {

            let mapa = "map" + mapNumber.toString();
            title2.textContent = response['messages'][0] + " " + response['address'];
            answerElt.appendChild(title2);

            mapbotElt.className = "offset-lg-2 col-lg-10 col-md-8 offset-sm-2 col-sm-6 offset-xs-1 col_xs_10";
            mapbotElt.id = mapa;

            if (window.screen.width > 700) {
                mapbotElt.style = 'width: 700px; height: 400px;';
            }
            else {
                mapbotElt.style = 'width: 250px; height: 400px;';
            }


            if (response['summary']) {
                wikibotElt.className = "offset-lg-2 col-lg-10 offset-md-2 col-md-6 offset-sm-2 col-sm-6 col-xs-6";
                para.textContent = response['messages'][1] + " " + response['summary'] + "[";
                let wikilink = document.createElement('a');
                wikilink.textContent = "En savoir plus sur Wikipedia";
                wikilink.href = response['url'];
                para.appendChild(wikilink);
                wikibotElt.appendChild(para);
                let paraending = document.createTextNode("]");
                para.appendChild(paraending);
            }
            else {
                wikibotElt.className = "offset-lg-2 col-lg-10";
                para.textContent = response['messages'][1];
                wikibotElt.appendChild(para);
            }

            chatDiv.appendChild(questionElt)
            chatDiv.appendChild(answerElt)
            chatDiv.appendChild(mapbotElt)
            chatDiv.appendChild(wikibotElt)

            let lati = response['locate'].lat;
            let long = response['locate'].lng;    

            var map = new mapboxgl.Map({
                container: mapa,
                center: [ long, lati ],
                style: 'mapbox://styles/mapbox/streets-v11',
                zoom: 15,
            });

            var marker = new mapboxgl.Marker()
            .setLngLat([ long, lati ])
            .addTo(map);

            // The 'building' layer in the mapbox-streets vector source contains building-height
            // data from OpenStreetMap.
            map.on('load', function () {
                // Insert the layer beneath any symbol layer.
                var layers = map.getStyle().layers;

                var labelLayerId;
                for (var i = 0; i < layers.length; i++) {
                    if (layers[i].type === 'symbol' && layers[i].layout['text-field']) {
                    labelLayerId = layers[i].id;
                    break;
                    }
                }

                map.addLayer(
                    {
                        'id': '3d-buildings',
                        'source': 'composite',
                        'source-layer': 'building',
                        'filter': ['==', 'extrude', 'true'],
                        'type': 'fill-extrusion',
                        'minzoom': 15,
                        'paint': {
                            'fill-extrusion-color': '#aaa',

                            // use an 'interpolate' expression to add a smooth transition effect to the
                            // buildings as the user zooms in
                            'fill-extrusion-height': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                15,
                                0,
                                15.05,
                                ['get', 'height']
                            ],
                            'fill-extrusion-base': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                15,
                                0,
                                15.05,
                                ['get', 'min_height']
                            ],
                            'fill-extrusion-opacity': 0.6
                        }
                    },
                    labelLayerId
                );
            });

            // To init google map:

            // initMap(mapa, lati, long);

            mapNumber++
        }
        else {

            title2.textContent = response['messages'][0];
            answerElt.appendChild(title2);
            mapbotElt.className = "offset-lg-2 col-lg-10";
            wikibotElt.className = "offset-lg-2 col-lg-10";

            chatDiv.appendChild(questionElt)
            chatDiv.appendChild(answerElt)
            chatDiv.appendChild(mapbotElt)
            chatDiv.appendChild(wikibotElt)
        }
    })
    .then(display)
});

function display(){
    spinner.style.visibility="hidden"
}
