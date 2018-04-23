// Bar chart
let linechart = new Chart(document.getElementById("line-chart"), {
    type: 'line',
    data: {
      labels: initiate_labels(),
      datasets: []
    },
    scales: {
      yAxes: [{
        ticks: {min: 0, max:100}
      }]
        },
    options: {
      legend: {display: true}
    }
});


function initiate_labels(){
  let dt = new Date();
  let stop = dt.getSeconds() + (60 * dt.getMinutes());
  let start = stop - 60;

  let labels = [];
  for (let i = start; i <= stop; i++) {
     labels.push(i);
  }
  return labels
}

let labels_todelete = [];
function deleteDataset(chart, label) {
  chart.data.datasets.forEach(function (dataset, index, datasets) {
    if (dataset.label == label) {
      datasets.splice(index, 1);
    }
  })
  labels_todelete.splice(labels_todelete.indexOf(label), 1);
}

function updateChart(chart, data) {
  let dt = new Date();
  let now = dt.getSeconds() + (60 * dt.getMinutes());
  chart.data.labels.push(now);
  chart.data.labels.shift();

  let label = ""
  chart.data.datasets.forEach(function(dataset, index, datasets) {
    label = dataset.label

    if (label in data) {
      dataset.data.push(data[label]);
      dataset.data.shift();
      delete data[label];
    } else {
      dataset.data.push(0);
      dataset.data.shift();
      dataset.borderColor = '#ff0000';
      if (!(label in labels_todelete)){
        setTimeout(deleteDataset, 5000, chart, label);
        labels_todelete.push(label);
      }
    }
  })

  for (let label in data){
    _data = new Array(60).fill(0);
    _data[60] = data[label];

    dataset = {
      "label": label,
      "data": _data
    }
    chart.data.datasets.push(dataset);
  }

  chart.update();
}

function WebSocketTest() {
  if ("WebSocket" in window) {
     console.log("WebSocket is supported by your Browser!");

     // Let us open a web socket
     let ws = new WebSocket("ws://localhost:8899/socket");

     ws.onopen = function(){
        // Web Socket is connected, send data using send()
        console.log("Connection is open");
     };

     ws.onmessage = function (evt) {
        let data = JSON.parse(evt.data);
        updateChart(linechart, data);
     };

     ws.onclose = function() {
        // websocket is closed.
        console.log("Connection is closed");
     };

     window.onbeforeunload = function(event) {
        socket.close();
     };
  }
  else {
     // The browser doesn't support WebSocket
     alert("WebSocket NOT supported by your Browser!");
  }
}

$(function() {
  WebSocketTest();
});



// function updateData(chart, label, data) {
//     chart.data.labels.push(label);
//     chart.data.labels.shift();
//     chart.data.datasets[0].data.push(data);
//     chart.data.datasets[0].data.shift();
//     chart.update();
// }
// function addRandomData() {
//   let dt = new Date();
//   let now = dt.getSeconds() + (60 * dt.getMinutes());
//
//   data = Math.floor(Math.random() * 100);
//   updateData(linechart, now, data);
// }
//
// setInterval(addRandomData, 1000);
