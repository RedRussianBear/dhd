$(document).ready(function () {
        const content = $('#content');


        function formSubmit(e) {
            content.fadeOut(500);

            $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                data: $(this).serialize(),
                success: function (data) {
                    window.setTimeout(function () {
                        content.html(data);
                        $('form').submit(formSubmit);
                        $('a').click(linkClick);
                        content.fadeIn(500);
                    }, 500);
                }
            });

            e.preventDefault();
        }

        function linkClick(e) {
            content.fadeOut(500);

            $.ajax({
                type: 'GET',
                url: $(this).attr('href'),
                success: function (data) {
                    window.setTimeout(function () {
                        content.html(data);
                        $('form').submit(formSubmit);
                        $('a').click(linkClick);
                        content.fadeIn(500);
                    }, 500);
                }
            });

            e.preventDefault();
        }


        $.get('/login', function (data) {
            content.fadeOut(500, function () {
                content.html(data);
                $('form').submit(formSubmit);
                $('a').click(linkClick);
                content.fadeIn(500);
            });

        });


    }
);
