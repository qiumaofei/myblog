$('.love').click(function () {
//  添加ajax动作
    comment_id = $(this).attr('tag');
    a_obj = $(this)
    $.getJSON('/article/clove/', {commentid: comment_id}, function (data) {
        console.log(data);
        if (data.status == 200) {

            // console.log(a.prev())
            a_obj.prev().text('(' + data.love + ')');
        } else {
            alert('点赞失败')
        }
    });
});