function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  sidebar.style.left = sidebar.style.left === '0px' ? '-250px' : '0px';
}

async function sendMessage() {
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

    // Send user message to the server and receive JSON response
    var chatid = '';
    const response = await fetch('/path-to-your-server-endpoint', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });

    if (response.ok) {
      const jsonResponse = await response.json();
      const botMessage = document.createElement('div');
      botMessage.classList.add('message', 'received');
      botMessage.innerHTML = `<p>${jsonResponse.message}</p>`;
      chatBody.appendChild(botMessage);
      chatBody.scrollTop = chatBody.scrollHeight;
    } else {
      // Handle server error
      console.error('Error:', response.status);
    }
  }
}
