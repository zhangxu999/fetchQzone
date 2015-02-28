window.onload=initvar;
var result,dui1,dui2;
function initvar (argument) {
	result=document.getElementById('result');
 	dui1=document.getElementById('dui1');
	dui2=document.getElementById('dui2');
}
function cli(arg) {
	var choose;
	if (arg.id==="left") {
	choose="你选了左边";
	dui1.style.opacity="1.0";
	dui2.style.opacity="0";
	getnext();
}
else{
	choose="你选了右边";
	dui2.style.opacity="1.0";
	dui1.style.opacity="0";
	getnext();
}
	result.innerHTML=choose;	
}
function getnext (argument) {
	var i=0;
	var xmlhttp=new XMLHttpRequest();
	xmlhttp.open("GET","http://127.0.0.1:8002/girl/getnext/",true);
	xmlhttp.send();
	xmlhttp.onreadystatechange=function  () {
		if (xmlhttp.readyState===4 && xmlhttp.status==200) {
			result.innerHTML=xmlhttp.responseText;
		};
		
	}
	
}