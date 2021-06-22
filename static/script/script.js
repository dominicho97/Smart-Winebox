
//handleData (script) werkt precies niet => dus functie hier geplaatst:

const handleData = function (url, callbackFunctionName, callbackErrorFunctionName = null, method = "GET", body = null) {
    fetch(url, {
        method: method,
        body: body,
        headers: {
            "content-type": "application/json",
        },
    })
        .then(function (response) {
            if (!response.ok) {
                console.warn(`>> Probleem bij de fetch(). Statuscode: ${response.status}`);
                if (callbackErrorFunctionName) {
                    console.warn(`>> Callback errorfunctie ${callbackErrorFunctionName.name}(response) wordt opgeroepen`);
                    callbackErrorFunctionName(response);
                } else {
                    console.warn(">> Er is geen callback errorfunctie meegegeven als parameter");
                }
            } else {
                console.info(">> Er is een response teruggekomen van de server");
                return response.json();
            }
        })
        .then(function (jsonObject) {
            if (jsonObject) {
                console.info(">> JSONobject is aangemaakt");
                console.info(`>> Callbackfunctie ${callbackFunctionName.name}(response) wordt opgeroepen`);
                callbackFunctionName(jsonObject);
            }
        });
}















//DATA VAN SENSORS TONEN OP WEBSERVER

//#region ***********  DOM references ***********
let html_temperature, html_humidity, html_light;

let html_cta_button

let kistStatus = 0;

const lanIP = `${window.location.hostname}:5000`;  //http://127.0.0.1:5000
const socket = io(lanIP);

//#endregion




//#region ***********  Callback - Vizualisation // show________

showLight = function (jsonObject) {
    console.log(jsonObject)
    let htmlstring_light = "";
    //gemetenwaarde met sensorid2
    console.log(jsonObject.read_alle_metingen[jsonObject.read_alle_metingen.length - 1].GemetenWaarde)
    htmlstring_light = `<h2 class="lead-data">
    Light: ${jsonObject.read_alle_metingen[jsonObject.read_alle_metingen.length - 1].GemetenWaarde} 
    </h2>`
    html_light.innerHTML = htmlstring_light

}



showTemperature = function (jsonObject) {
    //console.log(jsonObject)
    let htmlstring_temperature = "";
    //gemetenwaarde met sensorid2
    console.log(jsonObject.read_alle_metingen[jsonObject.read_alle_metingen.length - 1].GemetenWaarde)
    htmlstring_temperature = `<h2 class="lead-data" >
    Temperature: ${jsonObject.read_alle_metingen[jsonObject.read_alle_metingen.length - 1].GemetenWaarde} °C
    </h2>`

    html_temperature.innerHTML = htmlstring_temperature
}




showHumidity = function (jsonObject) {
    console.log(jsonObject)
    let htmlstring_humidity = "";
    //gemetenwaarde met sensorid1
    console.log(jsonObject.read_alle_metingen[jsonObject.read_alle_metingen.length - 1].GemetenWaarde)
    htmlstring_humidity = `<h2 class=" lead-data ">
    Humidity: ${jsonObject.read_alle_metingen[jsonObject.read_alle_metingen.length - 1].GemetenWaarde} %
</h2>`

    html_humidity.innerHTML = htmlstring_humidity
}

//#endregion

//#region ***********  Callback - HTML Generation (After select) ***********
// show________


//#endregion

//#region ***********  Callback - (After update/delete/insert) ***********
// callback______

//#endregion


//#region ***********  Data Access ***********/ 


const getHumidity = handleData(`http://${lanIP}/api/v1/metingen/1`, showHumidity)

const getTemperature = handleData(`http://${lanIP}/api/v1/metingen/2`, showTemperature)

const getLight = handleData(`http://${lanIP}/api/v1/metingen/3`, showLight)

//#endregion

//#region ***********  Event Listeners ***********
// listenTo________________

const listenToUI = function () {
    console.log("listenToUI werkt");

    html_cta_button.addEventListener("click", function () {
        console.log("cta clicked")
        socket.send('F2B_open_kist');
    });
    // const buttons = document.querySelectorAll(".js-kist-btn")
    // for (const button of buttons){
    //     button.addEventListener("click", function(){
    //         console.log("kist geopend")
    //     })
    // }

}

const listenToSocket = function () {
    socket.on("connected", function () {
        console.log("Verbonden met de socket")
    })
};


//#endregion

//#region ***********  INIT / DOMContentLoaded ***********
const init = function () {
    console.log('DOMContentLoaded')
   


    html_temperature = document.querySelector('.js-temperature');
    html_humidity = document.querySelector('.js-humidity');
    html_light = document.querySelector('.js-light');

    html_cta_button = document.querySelector(".js-kist-btn");

    listenToUI();
    listenToSocket();

    //showHumidity()
    //showTemperature()

};


document.addEventListener('DOMContentLoaded', init);

//#endregion
