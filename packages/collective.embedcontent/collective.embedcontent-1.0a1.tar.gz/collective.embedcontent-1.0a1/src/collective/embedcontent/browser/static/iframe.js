 $(document).ready(function () {
        $("iframe.embed-content-frame").load(function () {
            $(this).height($(this).contents().find("html").height());
        });
    });
