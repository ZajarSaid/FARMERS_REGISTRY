const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid_feedback");
const usernameSuccessOutput = document.querySelector(".UsernameSuccessOutput");


usernameField.addEventListener("keyup", (e)=>{
    
    usernameVal = e.target.value;
    usernameSuccessOutput.style.display = "block";

    usernameSuccessOutput.textContent = "Checking '" + usernameVal + "'";

    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display = "none";
    

if(usernameVal.length > 0){
    fetch("/validate-username/", {
        body:JSON.stringify({username:usernameVal}),
        method:"POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log("data", data);
        usernameSuccessOutput.style.display = "none";
        if(data.username_error){
            let p = data.username_error;
            usernameField.classList.add("is-invalid");
            feedBackArea.style.display = "block";
            feedBackArea.innerHTML = p;
            
        }
    });
}
});


