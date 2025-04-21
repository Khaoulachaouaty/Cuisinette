document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll(".slide");
    let currentIndex = 0;

    function changeSlide() {
        slides[currentIndex].classList.remove("active");
        currentIndex = (currentIndex + 1) % slides.length;
        slides[currentIndex].classList.add("active");
    }

    setInterval(changeSlide,3000); // Change toutes les 3 secondes

    // Met à jour l'année dans le footer
    document.getElementById("year").textContent = new Date().getFullYear();
});
