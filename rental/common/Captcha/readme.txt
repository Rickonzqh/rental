调用方式：
	1、增加 url(r'^captcha/', include('Captcha.urls')), 
	2、在前端放img控件指向 captcha
	
	3、验证码存储在session中，后端获取当前验证码值：request.session['captcha_code']
		