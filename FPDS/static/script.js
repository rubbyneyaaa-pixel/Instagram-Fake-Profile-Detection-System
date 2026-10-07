const images = [

"https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200",

"https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=1200",

"https://images.unsplash.com/photo-1518770660439-4636190af475?w=1200"

];

let current = 0;

function nextSlide(){

    current++;

    if(current >= images.length){
        current = 0;
    }

    document.getElementById("slider-image").src =
    images[current];
}

function previousSlide(){

    current--;

    if(current < 0){
        current = images.length - 1;
    }

    document.getElementById("slider-image").src =
    images[current];
}