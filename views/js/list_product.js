let slideIndex = 1;
showSlides(slideIndex);

// Function to automatically advance slides every 2 seconds
setInterval(function() {
    plusSlides(1);
}, 2000); // 1000 milliseconds = 2 seconds

function plusSlides(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("Slides");
    let dots = document.getElementsByClassName("dot");

    if (n > slides.length) {
        slideIndex = 1;  // Reset to the first slide if n exceeds the total number of slides
    }
    if (n < 1) {
        slideIndex = slides.length;  // Set to the last slide if n is less than 1
    }

    // Hide all slides
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    // Remove the "active" class from all dots
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }

    // Show the current slide and add the "active" class to the corresponding dot
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}
