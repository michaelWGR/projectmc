!function ($) {
    //分页
    $(".form-page-size").submit(function (e) {
        e.preventDefault();
        var pageSize = $.trim($('.input-page-size').val());
        window.location.href = $.query.set('page_num', 1).set('page_size', pageSize);
    });

    $('.pagination li > a').click(function (e) {
        e.preventDefault();
        var pageNum = $(this).attr('data-page');
        window.location.href = $.query.set('page_num', pageNum);
    });

    $(".form-page-num").submit(function (e) {
        e.preventDefault();
        var pageSize = $.trim($('.input-page-size').val());
        var pageNum = $.trim($('.input-page-num').val());
        window.location.href = $.query.set('page_num', pageNum).set('page_size', pageSize);
    });

    $("#checked-filter").change(function (e){
        e.preventDefault()
        var checked = $.trim($('#checked-filter').val())
        window.location.href = $.query.set('checked', checked).set('page_num', 1)
    })

}(jQuery);

