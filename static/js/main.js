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
                        addHooks();
                        content.fadeIn(500);
                    }, 500);
                }
            });

            e.preventDefault();
        }

        function linkClick(e) {
            content.fadeOut(500);

            let sent = Date.now();
            $.ajax({
                type: 'GET',
                url: $(this).attr('href'),
                success: function (data) {
                    let gap = Math.max(Date.now() - sent, 0);
                    window.setTimeout(function () {
                        content.html(data);
                        addHooks();
                        content.fadeIn(500);
                    }, gap);
                }
            });

            e.preventDefault();
        }

        function addRow(e) {
            let template = $(this).closest('table').find('tbody tr:first').clone().wrap('<div/>').parent().html();
            let n = $(this).closest('table').find('tbody tr').length;

            let new_row = template.replace(/0/g, '' + n);
            let n_row = $.parseHTML(new_row,);

            $(n_row).find('input,select').val('');
            $(this).closest('div.section').find("[id$=TOTAL_FORMS]").val(n + 1);

            $(this).closest('table').find('tbody').append(n_row);
        }

        function addHooks() {
            $('form').submit(formSubmit);
            $('a').click(linkClick);
            let add = $($.parseHTML('<a style="font-size: 24pt; display: block; text-align: center;">+</a>',));
            add.click(addRow);
            $('table').append(add);
        }


        $.get('/login', function (data) {
            content.fadeOut(500, function () {
                content.html(data);
                addHooks();
                content.fadeIn(500);
            });

        });


    }
);
