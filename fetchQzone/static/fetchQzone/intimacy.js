var ctx = document.getElementById("myChart").getContext("2d");
var canvas=document.getElementById("myChart")
var user=document.getElementById("user");
//var myNewChart = new Chart(ctx).PolarArea(data);

var data = {
    labels: [],
    //   labels: [ "0:00", "2:00",  "4:00",  "6:00","8:00","10:00","12:00","14:00","16:00","18:00","20:00","22:00","24:00"],
    datasets: [
    /*    {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [65, 59, 80, 81, 56, 55, 40,23]
        },
*/
        {
            user:[],
            label: "My Second dataset",
            fillColor: "rgba(151,187,205,0.2)",
            strokeColor: "rgba(151,187,205,1)",
            pointColor: "rgba(151,187,205,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(151,187,205,1)",
            data: [28, 48, 40, 19, 86, 27, 90,40]
        }
    ]
};
var result="ss";
var acbar="";
var c="";
function reqtianaly () {
    console.log("request timeanalysis----");

    var xmlhttp=new XMLHttpRequest();
    var host="http://127.0.0.1:8000";
    xmlhttp.open("GET",host+"/fetchQzone/intimacy/?user="+user.getAttribute("value"),true);
//xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.setRequestHeader("HTTP_X_REQUESTED_WITH","XMLHttpRequest");
    xmlhttp.setRequestHeader("Access-Control-Allow-Origin","*");
    xmlhttp.send('user='+738285867);
    
    xmlhttp.onreadystatechange=function  () {
        if (xmlhttp.readyState===4 && xmlhttp.status==200) {
         result=eval(xmlhttp.responseText);
         for(var i=0;i<result.length;i++)
         {
            data.labels[i]=result[i][2];
            data.datasets[0].data[i]=result[i][1];
            data.datasets[0].user[i]=result[i][0];

         }
       // data.datasets[0].data=result;
        console.log(data.datasets[0].data)
        c=new Chart(ctx).Bar(data);
        //,{bezierCurve: false}
        canvas.onclick = function(evt){
            console.log("dddd");
    acbar = c.getBarsAtEvent(evt);
    window.open("http://127.0.0.1:8000/fetchQzone/?user="+user.getAttribute("value")+"&friend="+acbar[0].user);
    // => activeBars is an array of bars on the canvas that are at the same position as the click event.
};
        }
};
}

reqtianaly();
console.log(result);
