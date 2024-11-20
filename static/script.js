$(document).ready(function() {

    // Menu toggle functionality
    $('#menu').click(function() {
        $(this).toggleClass('fa-times');
        $('.navbar').toggleClass('nav-toggle');
    });

    // Scroll and window load handling
    $(window).on('load scroll', function() {
        $('#menu').removeClass('fa-times');
        $('.navbar').removeClass('nav-toggle');

        $('section').each(function() {
            let top = $(window).scrollTop();
            let height = $(this).height();
            let offset = $(this).offset().top - 200;
            let id = $(this).attr('id');

            if(top > offset && top < offset + height) {
                $('.navbar ul li a').removeClass('active');
                $('.navbar').find(`[href="#${id}"]`).addClass('active');
            }
        });
    });

    // AJAX for form submission without reloading page
    $('#classifierForm').on('submit', function(e) {
        e.preventDefault(); // Prevent form from submitting normally

        const message = $('#message').val(); // Get the textarea value
        $('.result').removeClass('hide');
        $.ajax({
            url: '/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: message }),
            success: function(response) {
                // Display the result dynamically
                $('#result').html(`<h4>Prediction Result:</h4><p>${response.prediction}</p>`);
            },
            error: function() {
                $('#result').html('<p style="color: red;">An error occurred. Please try again.</p>');
            }
        });
    });

});
