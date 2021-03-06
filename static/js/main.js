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

$('#login').click(function(){
	var username=$(".login_fields #username").val();
	var password=$(".login_fields #password").val();
    var dataString = 'username='+username+'&password='+password;

    var usuario = {
            username: username,
            password: password
    }

	if($.trim(username).length>0 && $.trim(password).length>0){	
		$.ajax({
	        type: "POST",
	        url: "http://timetable-ttv1.rhcloud.com/auth",//url login -> rhcloud.com
	        data: JSON.stringify(usuario),
	        contentType: "application/json; charset=utf-8",
	        cache: false,
	        beforeSend: function(){ $("#login").val('Connecting...');},
	        success: function(data){
	            if(data){
	                var token = data['token'];
	            	localStorage.setItem('token', token);
	            	//para recuperar el token: var token = localStorage.getItem('token');
	            	$("body").load("login").hide().fadeIn(1500).delay(6000);
	            	window.location.replace("http://timetable-ttv1.rhcloud.com/home");
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
	        method: "POST",
	        dataType: "json",
	        url: "http://timetable-ttv1.rhcloud.com/registration",//url login -> rhcloud.com
	        contentType: "application/json; charset=utf-8",
	        data: JSON.stringify(usuario),//data i'm sending to the login url
	        cache: false,
	        beforeSend: function(){ $("#register").val('Enviando...');},
	        success: function(data){
	            if(data){
                    var code = data['code'];
                    var message = data['message'];
                    if(code==1003){
	            	    $("body").load("home.php").hide().fadeIn(1500).delay(6000);
                        //$('#back-to-login').click()
	            	}
	            	else{
                        $("#register").val('Enviar')
                        $("#error").html("<span style='color:#cc0000'>Error:</span> Se produjo un error, inténtelo más tarde. ");
	            	}
	            }
	            else{
				    $("#register").val('Enviar')
				    $("#error").html("<span style='color:#cc0000'>Error:</span> Se produjo un error, inténtelo más tarde. ");
	            }
	        },
            error:function(){
                 $("#register").val('Enviar')
				 $("#error").html("<span style='color:#cc0000'>Error:</span> Se produjo un error, inténtelo más tarde. ");
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