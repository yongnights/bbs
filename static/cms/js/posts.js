/**
 * Created by sandu .
 * @Project:zhifu
 * @author:sandu
 * @Software: PyCharm
 * @file: banners.js
 * @time: 2018-10-11 0011 下午 16:23
 */


// 帖子加精,取消加精
$(function () {
    $(".highlight-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if(highlight){
            url = "/cms/uhpost/";
        }else{
            url = "/cms/hpost/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'post_id': post_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});

//删除(隐藏)帖子
$(function () {
    $(".delete-post-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");

        zlalert.alertConfirm({
            "msg":"您确定要删除这篇帖子么？",
            'confirmCallback':function () {
                zlajax.post({
                    'url':'/cms/dpost/',
                    'data':{
                        'post_id':post_id,
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
