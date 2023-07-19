// Mapping of questions and responses
// const responses = {
//   "hi": "Hello there!",
//   "how are you?": "Unfortunately I don't have feelings, but thank you for asking! I'm here to assist you with any further questions you have.",
//   "Thank you!": "You're Welcome!, Anything Else?",
//   "what is assist.ai?": "Assist.AI is a smart chatbot that can have conversations with people.      It is designed to understand your questions and provide intelligent responses, meaning it can understand the context of the conversation and give relevant responses. Assist.ai is built using advanced technology called 'natural language processing' and 'machine learning'. These techniques help the chatbot understand what you're saying and respond in a way that makes sense.",
//   "what's your name?": "I am Assist.AI, nice to meet you!",
//   "okay": "Great! Anything else, l can help you with?",
//   "America's Independence?": "America gained independence on 4 July 1776. This date is celebrated as Independence Day in the United States and marks the adoption of the Declaration of Independence, which declared the thirteen American colonies free and independent from British rule.",
//   "what is it designed to do?": "It is designed to understand human languges and provide intelligent responses, meaning it can understand the context of the conversation and give relevant responses.",
//   // Add more question-response pairs as needed
// };

function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  sidebar.style.left = sidebar.style.left === '0px' ? '-250px' : '0px';
}

function getResponse(message) {
  
}

function appendMessage(sender, message) {
  const chatBody = document.getElementById('chatBody');
  const newMessage = document.createElement('div');
  newMessage.classList.add('message', sender);
  newMessage.innerHTML = `<p>${message}</p>`;
  chatBody.appendChild(newMessage);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function sendMessage() {
  const userInput = document.getElementById('userInput');
  const userMessage = userInput.value.trim();
  if (userMessage !== '') {
    appendMessage('sent', userMessage);
    userInput.value = '';

    // Simulate bot response
    setTimeout(() => {
      const botResponse = getResponse(userMessage);
      appendMessage('received', botResponse);
    }, 2000);
  }
}
