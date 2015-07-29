/**
 * Created by collegian on 4/30/2015.
 */
    var b = document.querySelector("#sub");
b.addEventListener("click",function(e) {

        var error1=document.querySelectorAll("span");
        var username=document.getElementById("username");
        var mail=document.getElementById("email");
        var nickname=document.getElementById("name");
        var pwd=document.getElementById("pwd");
        var cpwd=document.getElementById("cpwd");
        var birthday=document.getElementById("birthday");
        var location=document.getElementById("location");
        var items = document.querySelectorAll("input");
        var numberitems = 7;
        var error =["","","","","","",""];
        for( var i=0 ; i<numberitems ; i++){
            if(items[i].value ==""){
                items[i].style.border="2px solid red";
                error1[i].innerHTML= "required!";
                error1[i].style.color = "red";
                error[i] = true;
            }else{
                items[i].style.border="2px solid green";
                error1[i].innerHTML= "";
                error[i]=false;
            }
        }

        var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
        if(!error[0] && !mail.value.match(mailformat)){
            items[0].style.border="2px solid red";
            error1[0].innerHTML= "please inter the correct mail";
            error1[0].style.color = "red";

        }else if(!error[0]){
            items[0].style.border="2px solid green";
            error1[0].innerHTML= "";
            error[0]=false;
        }
        var pass_len = pwd.value.length;
        if (!error[3]&&  pass_len < 6){
            items[3].style.border="2px solid red";
            error1[3].innerHTML= "password lenght must be 6 character at least ";
            error1[3].style.color = "red";
            error[3]=true;
        }else if(!error[3]){
            items[3].style.border="2px solid green";
            error1[3].innerHTML= "";
            error[3]=false;
        }
        if (!error[4] && pwd.value !== cpwd.value){
            items[4].style.border="2px solid red";
            error1[4].innerHTML= "passwords  doesn't match ";
            error1[4].style.color = "red";
            error[4]=true;
        }else if(!error[4]){
            items[4].style.border="2px solid green";
            error1[4].innerHTML= "";
            error[4]=false;
        }

        var dateformat = /^([0-9]{2})\/([0-9]{2})\/([0-9]{4})$/;
        //var dateformat = /^\d{2}/\\d{2}/\\d{4}$/;
        if(!error[5] && !birthday.value.match(dateformat) ){
            console.log("error");
            error[5] =true;
            items[5].style.border="2px solid red";
            error1[5].innerHTML= " ilegal date format ";
            error1[5].style.color = "red";
        }

        else if(!error[5] && birthday.value.match(dateformat)){
            var regs = birthday.value.match(dateformat);
            if(regs[1] < 1 || regs[1] > 31) {
              error[5] =true;
            }
            // month value between 1 and 12
            if(regs[2] < 1 || regs[2] > 12) {
              error[5] =true;
            }
            // year value between 1902 and 2015
            if(regs[3] < 1902 || regs[3] > (new Date()).getFullYear()) {
              error[5] =true;
            }
            if(error[5]){
                items[5].style.border="2px solid red";
                error1[5].innerHTML= " wrong date ";
                error1[5].style.color = "red";
            }
        }
        else if(!error[5]){
            items[5].style.border="2px solid green";
            error1[5].innerHTML= "";
            error[5]= false;
        }
        var complete = true;
        for( var i=0 ; i<numberitems ; i++){
            if(error[i] == true){
                complete = false;
            }
        }
        if(complete){
            var c = document.getElementById("confirm");
            c.setAttribute("class","col-md-12 , success_payam");
            c.style.display = "block";
        }


    });
