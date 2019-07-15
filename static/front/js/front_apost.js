/**
 * Created by sandu .
 * @Project:zhifu
 * @author:sandu
 * @Software: PyCharm
 * @file: front_apost.js
 * @time: 2018-10-15 0015 下午 15:34
 */

// 初始化编辑器
$(function () {
   var ue = UE.getEditor('editor',{
       'serverUrl': '/ueditor/upload/'
   });
   $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $("input[name='title']");
        var boardSelect = $("select[name='board_id']");

        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = ue.getContent();

        zlajax.post({
            'url': '/apost/',
            'data': {
                'title': title,
                'content': content,
                'board_id':board_id,
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertConfirm({
                        'msg': '恭喜,帖子发表成功！',
                        'cancelText': '回到首页',
                        'confirmText': '再发一篇',
                        'cancelCallback': function () {
                            window.location = '/';
                        },
                        'confirmCallback': function () {
                            titleInput.val('');
                            ue.setContent('');
                        }
                    });
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });




   });

});