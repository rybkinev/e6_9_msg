
let currentChatId = null;  // Переменная для хранения ID текущего чата
let socket;

document.addEventListener('DOMContentLoaded', function () {
    // Подключаемся к WebSocket
    socket = new WebSocket(`ws://${window.location.host}/ws/chat/`);

    console.debug('Create WebSocket')
    console.debug(socket);

    socket.addEventListener('open', function (event) {
        console.debug('WebSocket connection opened:', event);
        loadChatList();
    });

    socket.addEventListener('message', function (event) {
        console.debug("WebSocket message");

        const data = JSON.parse(event.data);

        console.debug(data.type)
        if (data.type === 'chat-list') {
            // Обновляем список чатов при получении сообщения о новом чате
            loadChatList();
        } else if (data.type === 'message') {
            // Обновляем список сообщений при получении нового сообщения
            loadMessages(data.chat_id);
        }
    });

    socket.addEventListener('close', function (event) {
        if (event.wasClean) {
            console.debug('Соединение закрыто чисто');
        } else {
            console.debug('Обрыв соединения'); // например, "убит" процесс сервера
        }
            console.debug('Код: ' + event.code + ' причина: ' + event.reason);

    });

    socket.addEventListener('error', function (event) {
        console.error('WebSocket error:', event);
    });
});

function setCurrentChatId(chatId) {
    currentChatId = chatId;
}

function getCurrentChatId() {
    return currentChatId;
}

function loadMessages(chatId) {
    // Загружаем сообщения для выбранного чата
    fetch(`/api/chats/${chatId}/messages/`)
        .then(response => response.json())
        .then(messages => {
            const messagesContainer = document.getElementById('messages');
            messagesContainer.innerHTML = '';

            messages.forEach(message => {
                const messageElement = document.createElement('div');
                messageElement.className = 'message';
                messageElement.textContent = `${message.sender_username}: ${message.text}`;
                messagesContainer.appendChild(messageElement);
            });
        })
        .catch(error => console.error('Error fetching messages:', error));
}

// function createChat() {
//     const chatName = document.getElementById('chatName').value;
//
//     const js_data = JSON.stringify({
//         type: 'chat.created',
//         name: chatName,
//     })
//     socket.send(js_data);
//     loadChatList();
//     // currentChatId = newChat.id;
//     // loadMessages(currentChatId);
//
//     // var csrfToken = getCookie('csrftoken');
//
//     // fetch('/api/chats/', {
//     //     method: 'POST',
//     //     headers: {
//     //         'Content-Type': 'application/json',
//     //         'X-CSRFToken': csrfToken,
//     //     },
//     //     body: JSON.stringify({ name: chatName, type: 'create_chat' }),
//     // })
//     // .then(response => response.json())
//     // .then(newChat => {
//     //     // После создания чата, отправьте уведомление через WebSocket
//     //     const js_data = JSON.stringify({
//     //         type: 'chat.created',
//     //         name: newChat.name,
//     //     })
//     //     socket.send(js_data);
//     //     loadChatList();
//     //     // currentChatId = newChat.id;
//     //     // loadMessages(currentChatId);
//     // });
// }

function sendMessage() {
    const messageText = document.getElementById('message-text').value;

    socket.send(JSON.stringify({
            type: 'chat.message',
            text: messageText,
            chatId: currentChatId,
        }));
    document.getElementById('message-text').value = '';
    loadMessages(currentChatId);
}

// function getCookie(name) {
//     var value = "; " + document.cookie;
//     var parts = value.split("; " + name + "=");
//     if (parts.length == 2) return parts.pop().split(";").shift();
// }
