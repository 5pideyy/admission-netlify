document.getElementById("admissionForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const formObject = formDataToObject(formData);

    const response = await fetch("https://unicornfastapi.onrender.com/submit_admission/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(formObject),
    });

    if (response.ok) {
        alert("Admission form submitted successfully!");
        form.reset(); // Reset the form
    } else {
        alert("Error submitting the form.");
    }
});

// Function to convert FormData to an object
function formDataToObject(formData) {
    const obj = {};
    formData.forEach((value, key) => {
        obj[key] = value;
    });
    return obj;
}
