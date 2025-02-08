document.getElementById("send-btn").addEventListener("click", handleSendMessage);
document.getElementById("user-input").addEventListener("keypress", (event) => {
  if (event.key === "Enter") handleSendMessage();
});

function handleSendMessage() {
  const userInput = document.getElementById("user-input").value.trim();

  if (!userInput) {
    displayMessage("Please type a question.", "bot-message");
    return;
  }

  // Display the user's query
  displayMessage(userInput, "user-message");
  document.getElementById("user-input").value = "";

  // Show loading indicator
  showLoadingIndicator();

  // Send the query to the Flask backend
  fetch("/question", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: userInput }),
  })
    .then((response) => response.json())
    .then((data) => {
      hideLoadingIndicator();
      if (data.error) {
        displayMessage(data.error, "bot-message");
      } else {
        displayMessage(data.ai_answer, "bot-message");
        if (data.nasa_data) {
          displayMessage(
            `NASA Info: ${data.nasa_data.explanation || "No additional data."}`,
            "bot-message"
          );
        }
      }
    })
    .catch((error) => {
      hideLoadingIndicator();
      console.error("Error:", error);
      displayMessage("Something went wrong. Please try again.", "bot-message");
    });
}

function displayMessage(message, className) {
  const chatOutput = document.getElementById("chat-output");
  const newMessage = document.createElement("p");
  newMessage.textContent = message;
  newMessage.classList.add(className);
  chatOutput.appendChild(newMessage);
  chatOutput.scrollTop = chatOutput.scrollHeight;
}

function showLoadingIndicator() {
  const chatOutput = document.getElementById("chat-output");
  const loadingIndicator = document.createElement("p");
  loadingIndicator.textContent = "Bot is typing...";
  loadingIndicator.id = "loading-indicator";
  loadingIndicator.classList.add("bot-message");
  chatOutput.appendChild(loadingIndicator);
}

function hideLoadingIndicator() {
  const loadingIndicator = document.getElementById("loading-indicator");
  if (loadingIndicator) loadingIndicator.remove();
}
