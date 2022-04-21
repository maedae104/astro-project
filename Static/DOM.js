function generateDate(){
    const currentTime = new Date();                
    const curdate = currentTime.getDate();
    document.getElementbyId("dateHidden").value = curdate;
    return true;
}

form.getElementbyId("date-submit").addEventListener("click", generateDate())
