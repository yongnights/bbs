/**
 * Created by sandu .
 * @Project:zhifu
 * @author:sandu
 * @Software: PyCharm
 * @file: resetemail.js
 * @time: 2018-09-25 0025 下午 19:08
 */

$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var captchaE = $("input[name='captcha']");

        var email = emailE.val();
        var captcha = captchaE.val();

        zlajax.post({
            'url': '/cms/resetemail/',
            'data': {
                'email': email,
                'captcha': captcha
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    emailE.val("");
                    captchaE.val("");
                    zlalert.alertSuccessToast('恭喜！邮箱修改成功！');
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                zlalert.alertNetworkError();
            }
        });
    });
});