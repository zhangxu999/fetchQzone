window.onload=init;
function init (argument) {
    // body...
    showTime();
}
function showTime (argument) {
    times=document.getElementsByClassName('times');
    now=new Date();
    for(var i=0;i<times.length;i++)
    {
        time=new Date(parseInt(times[i].textContent));
        times[i].textContent=convertTime(now,time);
    }
}
function convertTime (now,time) {
    var daymillisec=86400000;
    cut=now.getTime()-time.getTime();
    hour=time.getHours();
    min=time.getMinutes();
    if(time.getHours()<10)
    {
        hour='0'+time.getHours();
    }
    if (time.getMinutes()<10)
     {
        min='0'+time.getMinutes();
     }
    HourMin=hour+':'+min;
    MonthDayHM=(time.getMonth()+1)+'月'+(time.getDay()+1)+'日  '+HourMin;
    try{
    if(cut<daymillisec)
    {
        if (now.getDay()==time.getDay()) 
            return HourMin;
        else
            return '昨天'+' '+HourMin;
    }
    else if (cut<daymillisec*2) 
    {
        if (now.getDay()-time.getDay()==1) 
            return '昨天'+' '+HourMin;
        else 
            return MonthDayHM;

    }
    else if (now.getFullYear()==time.getFullYear()) 
        {
            return MonthDayHM;
        }
    else
    {
        return time.getFullYear()+"年"+MonthDayHM;
    }
    }
    catch (e)
    {
        return "    ";
    }

}