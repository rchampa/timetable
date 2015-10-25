$('input[type="text"],input[type="password"]').focus(function(){
  $(this).prev().animate({'opacity':'1'},200)
});
$('input[type="text"],input[type="password"]').blur(function(){
  $(this).prev().animate({'opacity':'.5'},200)
});
$('input[type="email"]').focus(function(){
  $(this).prev().animate({'opacity':'1'},200)
});
$('input[type="email"]').blur(function(){
  $(this).prev().animate({'opacity':'.7'},200)
});

$('input[type="text"],input[type="password"]').keyup(function(){
  if(!$(this).val() == ''){
    $(this).next().animate({'opacity':'1','right' : '30'},200)
  } else {
    $(this).next().animate({'opacity':'0','right' : '20'},200)
  }
});

$('.login_fields').click(function(){
	var username=$(".login_fields #username").val();
	var password=$(".login_fields #password").val();
    var dataString = 'username='+username+'&password='+password;

	if($.trim(username).length>0 && $.trim(password).length>0){	
		$.ajax({
	        type: "POST",
	        url: "http://timetable-ttv1.rhcloud.com/auth",//url login -> rhcloud.com
	        data: dataString,//data i'm sending to the login url
	        cache: false,
	        beforeSend: function(){ $("#login").val('Connecting...');},
	        success: function(data){
	            if(data){
	            	$("body").load("home.php").hide().fadeIn(1500).delay(6000);
	            	localStorage.setItem('token', JSON.stringify(data));
	            }
	            else{
	             $('#box').shake();
				 $("#login").val('Acceder')
				 $("#error").html("<span style='color:#cc0000'>Error:</span> datos incorrectos. ");
	            }
	        }
	    });
	}
	
	return false;
});

$('#register').click(function(){
	var username=$(".register_fields #username").val();
	var password=$(".register_fields #password").val();
	var email=$(".register_fields #mail").val();
    var dataString = 'username='+username+'&password='+password+'&mail='+mail;

    var usuario = {
            email: email,
            password: password
    }

	if($.trim(username).length>0 && $.trim(password).length>0 && $.trim(email).length>0){	
		$.ajax({
	        type: "POST",
	        url: "http://timetable-ttv1.rhcloud.com/registration",//url login -> rhcloud.com
	        dataType: 'jsonp',//croos domain
	        contentType: "application/json; charset=utf-8",
	        data: usuario,//data i'm sending to the login url
	        cache: false,
	        beforeSend: function(){ $("#register").val('Enviando...');},
	        success: function(data){
	            if(data){

	            	$("body").load("home.php").hide().fadeIn(1500).delay(6000);
	            }
	            else{
				 $("#register").val('Enviar')
				 $("#error").html("<span style='color:#cc0000'>Error:</span> Se produjo un error, inténtelo más tarde. ");
	            }
	        },
            error:function(){
                 alert("Error");
            }
	    });
	}
	
	return false;
});

$('#register, #back-to-login').click(function(){

	if($('.login_fields').css('display')=='none'){
		$('.register_fields').hide();	
		$('#go-to-register').show();
		$('#back-to-login').hide();				
		$('.login_fields').fadeIn(800);	

	}
	else{
		$('.login_fields').hide();	
		$('#go-to-register').hide();
		$('#back-to-login').show();	
		$('.register_fields').fadeIn(800);		
	}



	  	
	return false;
});	