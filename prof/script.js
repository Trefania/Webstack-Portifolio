const sidebar = document.querySelector(".sidebar");
const sidebarClose = document.querySelector("#sidebar-close");
const menu = document.querySelector(".menu-content");
const menuItems = document.querySelectorAll(".submenu-item");
const subMenuTitles = document.querySelectorAll(".submenu .menu-title");

sidebarClose.addEventListener("click", () => sidebar.classList.toggle("close"));

menuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    menu.classList.add("submenu-active");
    item.classList.add("show-submenu");
    menuItems.forEach((item2, index2) => {
      if (index !== index2) {
        item2.classList.remove("show-submenu");
      }
    });
  });
});

subMenuTitles.forEach((title) => {
  title.addEventListener("click", () => {
    menu.classList.remove("submenu-active");
  });
});

const apiKey = "key"
const chatArea = document.querySelector(".chat-area");
const inputArea = document.querySelector(".input-area");
const inputField = inputArea.querySelector("input[type='text']");
const sendButton = inputArea.querySelector("button");

sendButton.addEventListener("click", sendMessage);
inputField.addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    sendMessage();
  }
});

async function sendMessage() {
  const message = inputField.value.trim();

  if (!message) {
    return;
  }

  addMessage(message, "User");
  inputField.value = "";
  inputField.setAttribute("disabled", "disabled");
  sendButton.setAttribute("disabled", "disabled");

  try {
    const response = await fetch(
      `https://api.openai.com/v1/engines/text-davinci-002/jobs`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`,
        },
        body: JSON.stringify({
          prompt: message,
          max_tokens: 100,
        }),
      }
    );

    if (!response.ok) {
      throw new Error("try again");
    }

    const data = await response.json();
    addMessage(data.choices[0].text, "Assist");
  } catch (error) {
    console.error(error);
    addMessage("Something went wrong.", "Assist");
  } finally {
    inputField.removeAttribute("disabled");
    sendButton.removeAttribute("disabled");
  }
}

function addMessage(message, sender) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("chat-message");
  messageElement.innerHTML = `
    <p>${message}</p>
    <span>${sender}</span>
  `;
  chatArea.appendChild(messageElement);
  chatArea.scrollTop = chatArea.scrollHeight;
}
