/**
 * Created by sandu .
 * @Project:zhifu
 * @author:sandu
 * @Software: PyCharm
 * @file: front_signin.js
 * @time: 2018-10-09 0009 下午 18:39
 */

$(function(){
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var email_input = $("input[name='email']");
        var password_input = $("input[name='password']");
        var graph_captcha_input = $("input[name='graph_captcha']");
        var remember_input = $("input[name='remember']");

        var email = email_input.val();
        var password = password_input.val();
        var graph_captcha = graph_captcha_input.val();
        var remember = remember_input.checked ? 1 : 0;

        zlajax.post({
            'url': '/signin/',
            'data': {
                'email': email,
                'password': password,
                'graph_captcha':graph_captcha,
                'remember': remember
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var return_to = $("#return-to-span").text();
                    if(return_to){
                        window.location = return_to;
                    }else{
                        window.location = '/';
                    }
                }else{
                    zlalert.alertInfo(data['message']);
                    email_input.val('');
                    password_input.val('');
                    graph_captcha_input.val('');
                    remember_input.val('');
                }
            }
        });
    });
});