const subscribe_btn = document.getElementById("text-button")

function textRequest() {
        if(subscribe_btn.innerHTML == 'Send me a text update!') {
            subscribe_btn.innerHTML = 'Text sent!'
            subscribe_btn.disabled = true;
        } 
    }

    subscribe_btn.addEventListener('click', textRequest);

subscribe_btn.onclick = (evt) => {
        console.log("subscribe for updates")
        //fetch request to user-profile
        fetch('/updates')
        .then(response => response.text())
        .then(serverData => serverData.text())
}