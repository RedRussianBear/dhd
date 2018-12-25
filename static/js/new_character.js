let c = 1;
let sections = ['name', 'description', 'characteristics', 'skills_powers', 'talents_traits_mutations', 'weapons', 'inventory', 'details'];
let next_part = $('#next');

function next() {
    let section = "#" + sections[c];
    $(section).css('opacity', 0)
        .slideDown({
            duration: 800,
            start: function () {
                $(this).css({
                    display: "flex"
                })
            }
        })
        .animate(
            {opacity: 1}, 800
        );
    if (c + 1 < sections.length) c++;
    else {
        next_part.hide();
        $('#save').fadeIn(500);
    }
}


next_part.unbind();
next_part.click(next);