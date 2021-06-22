
/*
var options = {
  chart: {
    type: 'line'
  },
  series: [{
    name: 'temperature',
    data: [30,40,35,50,49,60,70,91,125]
  }],
  xaxis: {
    categories: [1991,1992,1993,1994,1995,1996,1997, 1998,1999]
  }
}

var chart = new ApexCharts(document.querySelector(".chart"), options);

chart.render();
*/




const drawChart = function (labels, data) {
    let ctx = document.querySelector(".js-chart-temperature").getContext("2d");

    let config = {
        type: "line", //geeft de soort grafiek
        data: {
            labels: labels, //al de labels die worden getoond aan de onderkant vd grafiek
            datasets: [
                {
                    label: "Temperature(°C)", //label vanboven
                    backgroundColor: "white", // styling
                    borderColor: "#2969FF", // styling
                    data: data, // we voegen de data toe om de grafiek te vormen
                    fill: "#2969FF" //styling
                }
            ]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: "Chart.js Line Chart"
            },
            tooltips: {
                mode: "index",
                intersect: true
            },
            hover: {
                mode: "nearest",
                intersect: true
            },
            scale: {
                xAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: "Temperatuur"
                        }
                    }
                ],
                yAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: "Tijd"
                        }
                    }
                ]
            }
        }
    };
    if (window.myChart) window.myChart.destroy();
    window.myChart = new Chart(ctx, config);

};

const drawChart_humidity = function (labels, data) {
    let ctx = document.querySelector(".js-chart-humidity").getContext("2d");

    let config = {
        type: "line", //geeft de soort grafiek
        data: {
            labels: labels, //al de labels die worden getoond aan de onderkant vd grafiek
            datasets: [
                {
                    label: "Humidity(%)", //label vanboven
                    backgroundColor: "white", // styling
                    borderColor: "#2969FF", // styling
                    data: data, // we voegen de data toe om de grafiek te vormen
                    fill: "#2969FF" //styling
                }
            ]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: "Chart.js Line Chart"
            },
            tooltips: {
                mode: "index",
                intersect: true
            },
            hover: {
                mode: "nearest",
                intersect: true
            },
            scale: {
                xAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: "Vochtigheid"
                        }
                    }
                ],
                yAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: "Tijd"
                        }
                    }
                ]
            }
        }

    };
    if (window.myChart2) window.myChart2.destroy();
    window.myChart2 = new Chart(ctx, config);

};

const drawChart_light = function (labels, data) {
    let ctx = document.querySelector(".js-chart-light").getContext("2d");

    let config = {
        type: "line", //geeft de soort grafiek
        data: {
            labels: labels, //al de labels die worden getoond aan de onderkant vd grafiek
            datasets: [
                {
                    label: "Light", //label vanboven
                    backgroundColor: "white", // styling
                    borderColor: "#2969FF", // styling
                    data: data, // we voegen de data toe om de grafiek te vormen
                    fill: "#2969FF" //styling
                }
            ]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: "Chart.js Line Chart"
            },
            tooltips: {
                mode: "index",
                intersect: true
            },
            hover: {
                mode: "nearest",
                intersect: true
            },
            scale: {
                xAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: "Licht"
                        }
                    }
                ],
                yAxes: [
                    {
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: "Tijd"
                        }
                    }
                ]
            }
        }
    };
    if (window.myChart3) window.myChart3.destroy();
    window.myChart3 = new Chart(ctx, config);

};



showTemperatureData = function (data) {
    console.log(data) //data = jsonobject bij script.js
    console.log("Temperatuur data is geladen!")

    let converted_labels_temperature = [];
    let converted_data_temperature = [];

    // console.log(data.read_alle_metingen) 

    data = data.read_alle_metingen

    for (const temp of data) {
        converted_labels_temperature.push(temp.EindDatum)
        converted_data_temperature.push(temp.GemetenWaarde)
    }
    //console.log(converted_data_temperature)
    //console.log(converted_labels_temperature)



    //push data to Chart
    drawChart(converted_labels_temperature, converted_data_temperature)
}

//#region ***********  Callback - Vizualisation // show________

showHumidityData = function (data) {

    //console.log(jsonObject.read_alle_metingen)
    console.log(data)
    console.log("Vochtigheid data is geladen!")

    let converted_labels_humidity = [];
    let converted_data_humidity = [];



    data = data.read_alle_metingen

    for (const humidity of data) {
        converted_labels_humidity.push(humidity.EindDatum)
        converted_data_humidity.push(humidity.GemetenWaarde)

        // console.log(converted_data_humidity)

        //   console.log(converted_humidity)

        drawChart_humidity(converted_labels_humidity, converted_data_humidity)

    }

}


showLightData = function (data) {
    console.log("Light data geladen!");

    let converted_labels_light = [];
    let converted_data_light = [];

    data = data.read_alle_metingen

    for (const light of data) {
        converted_labels_light.push(light.EindDatum)
        converted_data_light.push(light.GemetenWaarde)



        drawChart_light(converted_labels_light, converted_data_light)

    }
};


//humidities = jsonObject.read_alle_metingen
//console.log(humidities)
//yHumidity.push(converted_humidity)



//#region ***********  Data Access ***********// get_______


const getHumidityData = handleData("http://127.0.0.1:5000/api/v1/metingen/1", showHumidityData)

const getTemperatureData = handleData("http://127.0.0.1:5000/api/v1/metingen/2", showTemperatureData)

const getLightData = handleData("http://127.0.0.1:5000/api/v1/metingen/3", showLightData)


//#endregion