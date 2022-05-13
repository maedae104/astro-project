const aspect_btn = document.querySelector("#view-more")

const eclipse_div = document.getElementById("eclipse-id")

const aspects_div = document.getElementById("aspects-id")

const retro_div = document.getElementById("retro-id")


aspect_btn.addEventListener('click', evt => {
        if(evt.target.value == 'View More'){
                eclipse_div.style.display = 'block'
                aspects_div.style.display = 'block'
                retro_div.style.display = 'block'

                } else if(evt.target.value == 'View Less'){
                eclipse_div.style.display = 'none'
                aspects_div.style.display = 'none'
                retro_div.style.display = 'none'
                }
        });

aspect_btn.addEventListener('click', evt => {
        if(aspect_btn.value == 'View More') {
                aspect_btn.value = 'View Less'
        } else {
                aspect_btn.value = 'View More';
        }
});     

function viewChange() {
    if(aspect_btn.innerHTML == 'View More') {
        aspect_btn.innerHTML = 'View Less';
    } else {
        aspect_btn.innerHTML = 'View More'
    }
    
}

aspect_btn.addEventListener('click', viewChange);



