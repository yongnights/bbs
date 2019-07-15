/**
 * Created by sandu .
 * @Project:zhifu
 * @author:sandu
 * @Software: PyCharm
 * @file: captcha_img.js
 * @time: 2018-10-10 0010 下午 15:52
 */

$(function () {
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = zlparam.setParam(src, 'xx', Math.random());
        self.attr('src', newsrc);
    });
});