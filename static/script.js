async function extractText(){

    const fileInput = document.getElementById("imageInput");
    const output = document.getElementById("output");

    if(!fileInput.files.length){
        alert("Select image");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    output.innerText = "Processing...";

    const response = await fetch("/extract-text", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    if(data.error)
        output.innerText = data.error;
    else
        output.innerText = data.text;
}