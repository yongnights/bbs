// 允许/禁止用户登录
$(function () {
    $(".highlight-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var cuser_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if (highlight == 1) {
            url = "/cms/uhcuser/";
        } else {
            url = "/cms/hcuser/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'cuser_id': cuser_id,
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    zlalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {
                        window.location.reload();
                    }, 500);
                } else {
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});

$(function () {
    $("#save-cuser-btn").click(function (event) {
        // 阻止按钮默认的提交表单的事件
        event.preventDefault();
        var self = $(this);
        // 获取模态框内的元素，跟之前的不一样
        var dialogE = $("#cuser-dialog");
        var nameE = $("input[name=name]");
        var emailE = $("input[name=email]");
        var passwordE = $("input[name=password]");
        var roleE = $("select[name=role] option:selected");

        var name = nameE.val();
        var email = emailE.val();
        var password = passwordE.val();
        var role = roleE.val();
        var submitType = self.attr('data-type');
        var cuserId = self.attr("data-id");

        // 判断用户是否输入相关数值
        if (!name || !email || !role) {
            zlalert.alertInfoToast('请输入用户数据');
            return;
        }

        var url = '';
        var data = {
            'name': name,
            'email': email,
            'role': role,
            'cuser_id': cuserId
        }
        if (submitType == 'update') {
            url = '/cms/ucusers/';

        } else {
            url = '/cms/acusers/';
            data.password = password;
        }
        // zlajax是另一个js文件

        zlajax.post({
            'url': url,
            'data': data,
            'success': function (data) {
                // console.log(data);
                if (data['code'] == 200) {
                    // dialog.modal("hide");
                    zlalert.alertSuccessToast('保存成功!');
                    nameE.val('').removeAttr('readonly');
                    emailE.val('').removeAttr('readonly');
                    passwordE.val('');
                    roleE.val('');
                    passwordE.parent().parent().show();
                    window.location.reload(); //重新加载这个页面
                } else {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                // console.log(error);
                zlalert.alertNetworkError('网络错误!')
            }
        })

    });

});

$(function () {
    $(".edit-cuser-btn").click(function (event) {
        // 获取模态框内的元素，跟之前的不一样
        var self = $(this);
        var dialog = $("#cuser-dialog");
        dialog.modal('show'); //显示模态框
        //获取绑定的标签上的值
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var email = tr.attr('data-email');
        var password = tr.attr('data-pwd');
        var role = tr.attr('data-role');

        var nameE = dialog.find("input[name=name]");
        var emaillE = dialog.find("input[name=email]");
        var passwordE = dialog.find("input[name=password]");
        var roleE = dialog.find("select[name=role] option:contains('"+role+"')");
        var saveBtn = dialog.find("#save-cuser-btn");

        nameE.val(name).attr("readonly", "readonly");
        emaillE.val(email).attr("readonly", "readonly");
        passwordE.val(password);
        passwordE.parent().parent().hide();
        roleE[0].selected=true;
        console.log(role);
        saveBtn.attr("data-type", "update");
        saveBtn.attr('data-id', tr.attr('data-id'));
    });
});

