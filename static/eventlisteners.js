
const aspect_btn = document.querySelector("#view-more")

const eclipse_div = document.getElementById("eclipse-id")

const aspects_div = document.getElementById("aspects-id")


aspect_btn.addEventListener('click', evt => {
        if(evt.target.value == 'View More'){
                eclipse_div.style.display = 'block'
                aspects_div.style.display = 'block'

                } else if(evt.target.value == 'View Less'){
                eclipse_div.style.display = 'none'
                aspects_div.style.display = 'none'
                }
        });

aspect_btn.addEventListener('click', evt => {
        if(aspect_btn.value == 'View More') {
                aspect_btn.value = 'View Less'
        } else {
                aspect_btn.value = 'View More';
        }
});     


function handleClick() {
    if(aspect_btn.innerHTML == 'View More') {
        aspect_btn.innerHTML = 'View Less';
    } else {
        aspect_btn.innerHTML = 'View More'
    }
    
}

aspect_btn.addEventListener('click', handleClick);



const sunscribe_btn = document.getElementById("text-button")

sunscribe_btn.onclick = (evt) => {
        console.log("subscribe for updates")
        //fetch request to user-profile
        fetch('/login')
        .then(response => response.text())
        .then(serverData => serverData.text())
}
