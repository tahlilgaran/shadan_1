/**
 * Created by collegian on 4/30/2015.
 */
function add(button){

    //var selector = "#comment"+button.name;
    //var comment = document.querySelector(selector);
    var table = button.parentNode.parentNode.parentNode.parentNode;
    var comment = table.parentNode.querySelector(".comment");
    //console.log(table.type);
    //var length = table.getElementsByTagName("tr").length;
    var newrow = table.insertRow(0);
    //console.log(newrow.type);
    //var cell = newrow.insertCell(0);
    //<img class="small_img , col-md-2" src="img/currentUser.jpg" />

    var elements = [];
    elements[0] = document.createElement("img");
    elements[0].setAttribute("class","small_img , col-md-2");
    elements[0].setAttribute("src","img/currentUser.jpg");

    //<div class="writer , col-md-8"><strong>Current User</strong></div>
    elements[1] = document.createElement("div");
    elements[1].setAttribute("class","writer , col-md-8");
    elements[1].innerHTML="<strong>Current User</strong>";

    //<div class="date , col-md-2"><strong>2-03-2015</strong></div>
    elements[2] = document.createElement("div");
    elements[2].setAttribute("class","date , col-md-2");
    elements[2].innerHTML="<strong>this-time</strong>";

    //<div class="text , col-md-10">
    elements[3] = document.createElement("div");
    elements[3].setAttribute("class","text , col-md-10");
    elements[3].innerHTML=comment.value;

    //var newrow =  document.createElement("tr");
    for(var i=0 ; i<4 ; i++){
        newrow.appendChild(elements[i]);
    }
    comment.value = "";
    //var selector2 = "#numcomment"+button.name;
    var td = table.parentNode.parentNode.querySelector(".numcomment");
        var val = parseInt(td.innerHTML);
        td.innerHTML = val + 1;
}
function jlike(button){
    if(button.name == "like") {
        button.setAttribute("class", "btn btn-xs btn-danger , col-md-2 , pull-right");
        button.innerHTML = "unlike!";
        //var selector = "#numlike"+button.id;
        var td = button.parentNode.querySelector(".numlike");
        var val = parseInt(td.innerHTML);
        td.innerHTML = val + 1;
        button.name = "dislike";
    }else{
        button.setAttribute("class", "btn btn-xs btn-success , col-md-2 , pull-right");
        button.innerHTML = "like!";
        //var selector = "#numlike"+button.id;
        var td = button.parentNode.querySelector(".numlike");
        var val = parseInt(td.innerHTML);
        td.innerHTML = val - 1;
        button.name = "like";
    }
}
function voting(button){
    var select = document.querySelectorAll(".radio");
    var vote;
    for( var i=0 ; i<select.length ; i++){
        if(select[i].checked){
            vote = 10-i;
        }
    }
    var svote = document.querySelector("#vote");
    svote.innerHTML = vote;
    var rvote = document.querySelector("#vote_result")
    rvote.value = vote;

}
function edit(button){
    var e = document.querySelector("#edit");
    e.setAttribute("class","info , col-md-12");
    e.style.display = "block";
}
function hiding2(button){
    var e = document.querySelector("#edit");
    e.setAttribute("class","info , col-md-12 ,hidden");
    console.log("done");
    console.log(e.className);
    e.style.display = "none";

}
function hiding(button){
    var v = document.querySelector("#v");
    v.setAttribute("class","posts , col-md-12 ,hidden");
    console.log("done");
    console.log(v.className);
    v.style.display = "none";

}
//function following(button){
//    if(button.name == "follow") {
//        button.setAttribute("class", "col-md-6 , btn btn-danger btn-lg");
//        button.innerHTML = "unfollow";
//        var numf = document.querySelector("#numf");
//        var val = parseInt(numf.innerHTML);
//        numf.innerHTML = val + 1;
//        button.name = "unfollow";
//    }else{
//        button.setAttribute("class", "col-md-6 , btn btn-success btn-lg");
//        button.innerHTML = "follow";
//        var td = document.querySelector("#numf");
//        var val = parseInt(td.innerHTML);
//        td.innerHTML = val - 1;
//        button.name = "follow";
//    }
//}


function search(){
    var value = document.querySelector('#search_value');
    var link = document.querySelector('#search_link');
    link.href = '/search/film/value';

}