javascript:(function (){
    var  mode=0,times=0,unZan=[];
    function letterInWord(letter,string){
        console.log("in letterInWord");
        if (letter==null||string==null)
            {return false;}
        for (var i = 0; i < string.length; i++) {
            if(letter[0]==string[i])
                return true;
        };
        return false;
    };
    function main () {
        var unZanTimes=0;
        console.log("in main!"+"unZanTimes:"+unZanTimes);
        for(var i=0;i<all.length;i++){
         if (letterInWord("取",all[i].text)){

         } 
         else{
            all[i].click();
            times++;
            var content="###第"+i+"个";
            all[i].innerText+=content;
        } if(i==all.length-1) {
            unZanTimes=0;
            console.log(i);
             for (var i = 0; i < all.length; i++) 
                { 
                    if (!letterInWord("取",all[i].text)) 
                     {
                        unZan[unZan.length]=i;unZanTimes++;
                    }; 
                }; 
                if(unZanTimes==0)
                    {
                        return;
                    } 
                else{
                    console.log("unZanTimes:"+unZanTimes);main();} }; }} var all=document.getElementsByClassName("qz_like_btn_v3"); main(); mode==0?(alert("赞了"+times+"次！")):(alert("取消赞"+times+"次！"));} )();