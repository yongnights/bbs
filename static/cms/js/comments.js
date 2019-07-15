/**
 * Created by sandu .
 * @Project:zhifu
 * @author:sandu
 * @Software: PyCharm
 * @file: banners.js
 * @time: 2018-10-11 0011 下午 16:23
 */


// 评论置顶,取消置顶
$(function () {
    $(".highlight-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var comment_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if(highlight){
            url = "/cms/uhcomment/";
        }else{
            url = "/cms/hcomment/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'comment_id': comment_id
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

//删除(隐藏)帖子,恢复显示帖子
$(function () {
    $(".delete-comment-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var comment_id = tr.attr("data-id");
        var data_display = parseInt(tr.attr("data-display"));
        var url = "";
        if(data_display){
            url = "/cms/dcomments/";
        }else{
            url = "/cms/udcomments/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'comment_id': comment_id
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