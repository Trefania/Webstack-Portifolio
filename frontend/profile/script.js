function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  sidebar.style.left = sidebar.style.left === '0px' ? '-250px' : '0px';
}

function sendMessage() {
  const userInput = document.getElementById('userInput');
  const message = userInput.value;
  if (message.trim() !== '') {
    const chatBody = document.getElementById('chatBody');
    const newMessage = document.createElement('div');
    newMessage.classList.add('message', 'sent');
    newMessage.innerHTML = `<p>${message}</p>`;
    chatBody.appendChild(newMessage);
    userInput.value = '';
    chatBody.scrollTop = chatBody.scrollHeight;

    // Simulate bot response
    setTimeout(() => {
      const botMessage = document.createElement('div');
      botMessage.classList.add('message', 'received');
      botMessage.innerHTML = '<p>Thank you for your message. How can I help you further?</p>';
      chatBody.appendChild(botMessage);
      chatBody.scrollTop = chatBody.scrollHeight;
    }, 1000);
  }
}