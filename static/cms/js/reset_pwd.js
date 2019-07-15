/**
 * Created by Sandu on 2018/09/12.
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

        var old_passwordE = $("input[name=old_password]");
        var new_passwordE = $("input[name=new_password]");
        var confirm_new_passwordE = $("input[name=confirm_new_password]");

        var old_password = old_passwordE.val();
        var new_password = new_passwordE.val();
        var confirm_new_password = confirm_new_passwordE.val();

        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken

        // zlajax是另一个js文件

        zlajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'old_password': old_password,
                'new_password': new_password,
                'confirm_new_password': confirm_new_password
            },
            'success': function (data) {
                // console.log(data);
                if (data['code'] == 200){
                    zlalert.alertSuccessToast('恭喜,修改密码成功!');
                    old_passwordE.val('');
                    new_passwordE.val('');
                    confirm_new_passwordE.val('');
                }else {
                    var message = data['message'];
                    zlalert.alertInfo(message);
                }
            },
            'fail': function () {
                // console.log(error);
                zlalert.alertNetworkError('网络错误!')
            }
        })

    });

});