/**
 * Created by sandu .
 * @Project:zhifu
 * @author:sandu
 * @Software: PyCharm
 * @file: boards.js
 * @time: 2018-10-11 0011 下午 16:23
 */

$(function () {
    $("#add-board-btn").click(function (event) {
        event.preventDefault();
        zlalert.alertOneInput({
            'title':'请输入新版块名称',
            'text':'',
            'placeholder': '版块名称',
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/aboard/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            zlalert.alertSuccessToast('添加成功!');
                            window.location.reload();
                        }else{
                            zlalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $(".edit-board-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var board_id = tr.attr("data-id");

        zlalert.alertOneInput({
            'title':'请输入新版块名称',
            'text':'',
            'placeholder': name,
            'confirmCallback': function (inputValue) {
                zlajax.post({
                    'url': '/cms/uboard/',
                    'data': {
                        'board_id': board_id,
                        'name': inputValue
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            zlalert.alertSuccessToast('修改成功!');
                            window.location.reload();
                        }else{
                            zlalert.alertInfo(data['message']);
                        }
                    }
                });
            }
        });
    });
});

$(function () {
    $(".delete-board-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var board_id = tr.attr("data-id");

        zlalert.alertConfirm({
            "msg":"您确定要删除这个版块么？",
            'confirmCallback':function () {
                zlajax.post({
                    'url':'/cms/dboard/',
                    'data':{
                        'board_id':board_id,
                    },
                    'success':function (data) {
                        if(data['code'] == 200){
                            zlalert.alertSuccessToast('删除成功!');
                            window.location.reload();
                        }else {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                })
            }

        })
    });
});
