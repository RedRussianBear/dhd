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
                    let gap = Math.max(500 - (Date.now() - sent), 0);
                    window.setTimeout(function () {
                        content.html(data);
                        addHooks();
                        content.fadeIn(500);
                    }, gap);
                }
            });

            e.preventDefault();
        }

        function addRow() {
            let template = $(this).closest('table').find('tbody tr:first').clone().wrap('<div/>').parent().html();
            let n = $(this).closest('table').find('tbody tr').length;

            let new_row = template.replace(/0/g, '' + n);
            let n_row = $.parseHTML(new_row,);

            $(n_row).find('input,select').val('');
            $(this).closest('div').find("[id$=TOTAL_FORMS]").val(n + 1);

            $(this).closest('table').find('tbody').append(n_row);

            let delete_hooks = n_row.find('a.delete');
            delete_hooks.unbind();
            delete_hooks.click(deleteRow);
        }

        function renumber(start) {
            let rows = $(start).closest('tr').nextAll('tr');

            for (let i = 0; i < rows.length; i++) {
                let row = $(rows[i]);
                let regexp = /[a-z_]+-([0-9]+)-[a-z_]+/gi;
                let n = parseInt(regexp.exec(row.find('input[type=hidden]').attr('name'))[1]);

                let inputs = row.find('input');
                for (let j = 0; j < inputs.length; j++) {
                    let input = $(inputs[j]);

                    input.attr('name', input.attr('name').replace('' + n, '' + (n - 1)));
                    input.attr('id', input.attr('id').replace('' + n, '' + (n - 1)));
                }
            }

            $(start).closest('div').find("[id$=TOTAL_FORMS]").val(parseInt($(start).closest('div').find("[id$=TOTAL_FORMS]").val()) - 1);
            $(start).closest('tr').remove();
        }

        function deleteRow(e) {
            e.preventDefault();

            let self = this;

            if ($(this).closest('tr').find('input[type=hidden]').val() !== "") {
                $.ajax({
                    type: 'GET',
                    url: '/delete/' + $(this).attr('type') + '/' + $(this).closest('tr').find('input[type=hidden]').val() + '/',
                    success: function () {
                        $(self).closest('div').find("[id$=INITIAL_FORMS]").val(parseInt($(self).closest('div').find("[id$=INITIAL_FORMS]").val()) - 1);
                        renumber(self);
                    }
                });
            }
            else {
                renumber(self);
            }

        }

        function addHooks() {
            $('form').submit(formSubmit);
            $('a').click(linkClick);
            let add = $($.parseHTML('<a style="font-size: 24pt; display: block; text-align: center; width: 100%;">+</a>',));
            add.click(addRow);
            $('table').append(add);

            let delete_hooks = $('a.delete');
            delete_hooks.unbind();
            delete_hooks.click(deleteRow);
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
