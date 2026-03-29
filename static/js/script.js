// script.js
function sendMessage() {
    const inputField = document.getElementById("input-field");
    const chatBox = document.getElementById("chatBox");
    const message = inputField.value.trim();
    
   if (message === "") return;

   // 1. Display User Message
    //chatBox.innerHTML += `<div class="user-msg"><strong>You:</strong> ${message}</div>`;
    chatBox.innerHTML += `<div class="item right"><div class="user-msg"><p> ${message}</p></div>&nbsp;<div class="icon_user"><i class="fa fa-user"></i></div></div>`;
    inputField.value = ""; // Clear input

    // 2. Send Message to Flask Backend
    fetch("/chat", { // Ensure this matches your Flask route
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // 3. Display Bot Response
        //chatBox.innerHTML += `<div class="bot-msg"><strong>Bot:</strong> ${data.answer}</div>`;
        chatBox.innerHTML += `<div class="item"><div class="icon"><i class="fa fa-user-md"></i></div>&nbsp; <div class="bot-msg"><p> ${data.answer} </p></div> </div><br clear="both">`;
        // Auto-scroll to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);
        chatBox.innerHTML += `<div class="error">Error: Could not reach server.</div>`;
    });
}

// Event listener for Send button
sendBtn.addEventListener('click', sendMessage);

// Allow sending with 'Enter' key
document.getElementById("user-input").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});