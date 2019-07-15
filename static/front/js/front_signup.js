/**
 * Created by sandu .
 * @Project:zhifu
 * @author:sandu
 * @Software: PyCharm
 * @file: front_signup.js
 * @time: 2018-09-29 0029 下午 16:48
 */


$(function () {
    /**
     * 获取提交的表单数据
     */
    // submit是页面中提交的id值
    $("#submit").click(function (event) {
        // event.preventDefault
        // 是阻止按钮默认的提交表单的事件
        event.preventDefault();

        var emailE = $("input[name=email]");
        var email_captchaE = $("input[name=email_captcha]");
        var passwordE = $("input[name=password]");
        var repeat_passwordE = $("input[name=repeat_password]");
        var graph_captchaE = $("input[name=graph_captcha]");

        var email = emailE.val();
        var email_captcha = email_captchaE.val();
        var password = passwordE.val();
        var repeat_password = repeat_passwordE.val();
        var graph_captcha = graph_captchaE.val();
        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken
        // zlajax是另一个js文件

        zlajax.post({
            'url': '/signup/',
            'data': {
                'email': email,
                'email_captcha': email_captcha,
                'password': password,
                'repeat_password': repeat_password,
                'graph_captcha': graph_captcha,
            },
            'success': function (data) {
                // console.log(data);
                if (data['code'] == 200) {
                    var return_to = $("#return-to-span").text();
                    if (return_to){
                        window.location = return_to;
                    }else {
                        window.location = '/';
                    }
                   } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                zlalert.alertNetworkError('网络错误!')
            }
        })

    });

});