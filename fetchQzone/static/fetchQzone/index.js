var ctx = document.getElementById("myChart").getContext("2d");
var user=document.getElementById("user");
//var myNewChart = new Chart(ctx).PolarArea(data);

var data = {
    labels: [ "1:00", "2:00", "3:00", "4:00", "5:00", "6:00","7:00","8:00","9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00","24:00"],
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
function reqtianaly () {
    console.log("request timeanalysis----");

    var xmlhttp=new XMLHttpRequest();
    var host="http://127.0.0.1:8000";
    xmlhttp.open("GET",host+"/fetchQzone/timeanaly/?user="+user.getAttribute("value"),true);
//xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.setRequestHeader("HTTP_X_REQUESTED_WITH","XMLHttpRequest");
    xmlhttp.setRequestHeader("Access-Control-Allow-Origin","*");
    xmlhttp.send('user='+738285867);
    
    xmlhttp.onreadystatechange=function  () {
        if (xmlhttp.readyState===4 && xmlhttp.status==200) {
         result=eval(xmlhttp.responseText);
        data.datasets[0].data=result;
        console.log(data.datasets[0].data)
        c=new Chart(ctx).Line(data);
        //,{bezierCurve: false}
        }
};
}

reqtianaly();
console.log(result);
