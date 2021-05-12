$(document).ready(centerme);
$(window).resize(centerme);


function centerme() {
boiheight = $(".center-meh-boi").height();
middle = boiheight / 2;
$(".center-meh-boi").css("margin-top","-" + middle + "px");
console.log(boiheight);
}
