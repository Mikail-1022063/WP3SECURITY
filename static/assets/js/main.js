// Init AOS
AOS.init({
    duration: 650,
    once: true
});

// Current Page Active
const currentPage = location.pathname;
$('nav a').each(function () {
    const currentHref = $(this).attr('href');
    if (currentHref === currentPage) {
        $(this).addClass("active-nav-link");
    } else {
        $(this).removeClass("active-nav-link");
    }
})