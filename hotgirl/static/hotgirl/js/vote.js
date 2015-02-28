window.onload=initvar;
var result,dui1,dui2,leftimg,leftvote,rightvote,rightimg,imgid,votescore,leftscore,rightscore;
function initvar (argument) {
	result=document.getElementById('result');
 	dui1=document.getElementById('dui1');
	dui2=document.getElementById('dui2');
	leftimg=document.getElementById('leftimg');
	rightimg=document.getElementById('rightimg');
	leftvote=document.getElementById('leftvote');
	rightvote=document.getElementById('rightvote');
	//votescore=document.getElementByClassName('votescore');
	leftscore=leftimg.getAttribute("vote");
	rightscore=rightimg.getAttribute("vote");
}
//处理照片层点击
function cli(arg) {
	
	if (arg.id==="left") {
	changeopacity(1.0,0);
	getnext(arg);
}
else{
	changeopacity(0,1.0);
	getnext(arg);
}	
}
//改变对勾透明度
function changeopacity (left,right) {
	dui1.style.opacity=left;
	dui2.style.opacity=right;
}
//更改分数
function changescore (argument) {
	// body...
	leftvote.innerHTML=leftscore;
	rightvote.innerHTML=rightscore;
}
//点击照片请求下一组图片信息
function getnext (arg) {
	changescore();
	var xmlhttp=new XMLHttpRequest();
	//搞不明白为什么是第三个？？？？？？？
	var imgid=arg.childNodes.item(3).getAttribute("imgid");
	xmlhttp.open("GET","http://127.0.0.1:8002/girl/getnext/?imgid="+imgid,true);
	xmlhttp.send();
	xmlhttp.onreadystatechange=function  () {
		if (xmlhttp.readyState===4 && xmlhttp.status==200) {
			//result.innerHTML=xmlhttp.responseText;
			respjson=eval('('+xmlhttp.responseText+')');
			leftscore=respjson.img[0].vote;
			rightscore=respjson.img[1].vote;
			//votescore.style.font-size=40;
			leftimg.setAttribute('imgid',respjson.img[0].imgid);
			rightimg.setAttribute('imgid',respjson.img[1].imgid);
			
			setTimeout(function  () {
				leftimg.src=respjson.img[0].src;
				rightimg.src=respjson.img[1].src;
				changeopacity(0.5,0.5);
				leftvote.innerHTML='点击查看得分';
				rightvote.innerHTML='点击查看得分';
			},1000);
			//pause(1000);
			
		};
		
	}
	
}