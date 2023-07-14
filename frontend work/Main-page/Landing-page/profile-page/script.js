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

    // Send user message to the server and receive JSON response
    $.ajax({
      url: '/profile/chat/chat_id',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({ message }),
      success: function(jsonResponse) {
        const botMessage = document.createElement('div');
        botMessage.classList.add('message', 'received');
        botMessage.innerHTML = `<p>${jsonResponse.message}</p>`;
        chatBody.appendChild(botMessage);
        chatBody.scrollTop = chatBody.scrollHeight;
      },
      error: function(xhr, status, error) {
        // Handle server error
        console.error('Error:', error);
      }
    });
  }
}
