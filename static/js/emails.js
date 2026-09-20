const emailField = document.querySelector("#emailField");
const EmailfeedBackArea = document.querySelector(".invalidEmailfeedback");
const emailSuccessOutput = document.querySelector(".EmailSuccessOutput");


emailField.addEventListener("keyup", (e)=>{
    
    emailVal = e.target.value;
    emailSuccessOutput.style.display = "block";

    emailSuccessOutput.textContent = "Checking '" + emailVal + "'";

    emailField.classList.remove("is-invalid");
    EmailfeedBackArea.style.display = "none";
    

if(emailVal.length > 0){
    fetch("/email-validate/", {
        body:JSON.stringify({email:emailVal}),
        method:"POST",
    })
    .then((res)=>res.json())
    .then((data)=>{
        console.log("data", data);
        emailSuccessOutput.style.display = "none";
        if(data.email_error){
            let p = data.email_error;
            emailField.classList.add("is-invalid");
            EmailfeedBackArea.style.display = "block";
            EmailfeedBackArea.innerHTML = p;
            
        }
    });
}
});