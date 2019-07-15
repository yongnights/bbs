/**
 * Created by sandu .
 * @Project:zhifu
 * @author:sandu
 * @Software: PyCharm
 * @file: banners.js
 * @time: 2018-10-11 0011 下午 16:23
 */

$(function () {
    $("#save-banner-btn").click(function (event) {
        // 阻止按钮默认的提交表单的事件
        event.preventDefault();
        var self = $(this);
        // 获取模态框内的元素，跟之前的不一样
        var dialogE = $("#banner-dialog");
        var nameE = $("input[name=name]");
        var image_urlE = $("input[name=image_url]");
        var link_urlE = $("input[name=link_url]");
        var priorityE = $("input[name=priority]");

        var name = nameE.val();
        var image_url = image_urlE.val();
        var link_url = link_urlE.val();
        var priority = priorityE.val();
        var submitType = self.attr('data-type');
        var bannerId = self.attr("data-id");

        // 判断用户是否输入相关数值
        if (!name || !image_url || !link_url || !priority) {
            zlalert.alertInfoToast('请输入完整的轮播图数据');
            return;
        }

        var url = '';
        if (submitType == 'update') {
            url = '/cms/ubanner/';
        } else {
            url = '/cms/abanner/';
        }
        // zlajax是另一个js文件

        zlajax.post({
            'url': url,
            'data': {
                'name': name,
                'image_url': image_url,
                'link_url': link_url,
                'priority': priority,
                'banner_id': bannerId
            },
            'success': function (data) {
                // console.log(data);
                if (data['code'] == 200) {
                    // dialog.modal("hide");
                    zlalert.alertSuccessToast('保存成功!');
                    nameE.val('');
                    image_urlE.val('');
                    link_urlE.val('');
                    priorityE.val('');
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
    $(".edit-banner-btn").click(function (event) {
        // 获取模态框内的元素，跟之前的不一样
        var self = $(this);
        var dialog = $("#banner-dialog");
        dialog.modal('show'); //显示模态框
        //获取绑定的标签上的值
        var tr = self.parent().parent();
        var name = tr.attr('data-name');
        var image_url = tr.attr('data-image');
        var link_url = tr.attr('data-link');
        var priority = tr.attr('data-priority');

        var nameE = dialog.find("input[name=name]");
        var image_urlE = dialog.find("input[name=image_url]");
        var link_urlE = dialog.find("input[name=link_url]");
        var priorityE = dialog.find("input[name=priority]");
        var saveBtn = dialog.find("#save-banner-btn");

        // console.log(saveBtn);
        // return;

        nameE.val(name);
        image_urlE.val(image_url);
        link_urlE.val(link_url);
        priorityE.val(priority);
        saveBtn.attr("data-type", "update");
        saveBtn.attr('data-id', tr.attr('data-id'));
    });
});



$(function () {
    $(".delete-banner-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var banner_id = tr.attr("data-id");

        zlalert.alertConfirm({
            "msg":"您确定要删除这个轮播图么？",
            'confirmCallback':function () {
                zlajax.post({
                    'url':'/cms/dbanner/',
                    'data':{
                        'banner_id':banner_id,
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

$(function(){
    zlqiniu.setUp({
        'domain': 'http://pgmhjjvoy.bkt.clouddn.com/',
        // 绑定按钮id,以后点击这个按钮就可以上传文件
        'browse_btn': 'upload-btn',
        // 后台写好的获取uptoken的接口地址
        'uptoken_url': '/common/uptoken/',
        // 文件上传成功后的回调信息
        'success': function (up, file, info) {
            var imageInput = $("input[name=image_url]"); //获取上传的图片链接
            imageInput.val(file.name); //把图片链接填充到输入框里
        }
    });
});

