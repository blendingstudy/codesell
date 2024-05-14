document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
  
    // Socket.IO 연결 설정
    const socket = io();
  
    // 채팅방 입장
    function joinRoom(roomId) {
      socket.emit('join_room', { room_id: roomId });
    }
  
    // 채팅방 퇴장
    function leaveRoom(roomId) {
      socket.emit('leave_room', { room_id: roomId });
    }
  
    // 메시지 전송
    function sendMessage(e) {
      e.preventDefault();
      const message = messageInput.value.trim();
      const roomId = chatForm.dataset.roomId;
  
      if (message === '') {
        return;
      }
  
      socket.emit('send_message', {
        room_id: roomId,
        message: message,
      });
  
      messageInput.value = '';
    }
  
    // 메시지 수신
    socket.on('receive_message', (data) => {
      const messageElement = document.createElement('div');
      messageElement.classList.add('chat-message');
      messageElement.innerHTML = `
        <p class="meta">${data.username} <span>${data.timestamp}</span></p>
        <p class="content">${data.message}</p>
      `;
      chatMessages.appendChild(messageElement);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    });
  
    // 채팅방 입장 시 메시지 로드
    socket.on('load_messages', (data) => {
      chatMessages.innerHTML = '';
      data.messages.forEach((message) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message');
        messageElement.innerHTML = `
          <p class="meta">${message.username} <span>${message.timestamp}</span></p>
          <p class="content">${message.message}</p>
        `;
        chatMessages.appendChild(messageElement);
      });
      chatMessages.scrollTop = chatMessages.scrollHeight;
    });
  
    // 채팅 폼 제출 이벤트 리스너 등록
    chatForm.addEventListener('submit', sendMessage);
  });