const createGroupChatBtn = document.getElementById('createGroupChatBtn');
const startChatUserBtn = document.getElementById('startChatUserBtn');
const createGroupChatForm = document.getElementById('createGroupChatForm');
const startChatUserForm = document.getElementById('startChatUserForm');

const createGroupChatOkBtn = document.getElementById('createGroupChatOkBtn');
const startChatUserOkBtn = document.getElementById('startChatUserOkBtn');

document.addEventListener('DOMContentLoaded', async function () {
  createGroupChatBtn.addEventListener('click', function () {
    console.debug(createGroupChatForm.style.display);
    if (createGroupChatForm.style.display == 'block'){
      createGroupChatForm.style.display = 'none';
      startChatUserForm.style.display = 'none';
    }
    else {
      createGroupChatForm.style.display = 'block';
      startChatUserForm.style.display = 'none';
    }
  });

  startChatUserBtn.addEventListener('click', function () {
    if (startChatUserForm.style.display == 'block') {
      startChatUserForm.style.display = 'none';
      createGroupChatForm.style.display = 'none';
    }
    else {
      startChatUserForm.style.display = 'block';
      createGroupChatForm.style.display = 'none';
    }

  });

  createGroupChatOkBtn.addEventListener('click', async function () {
    const chatName = document.getElementById('chatName').value;
    const users = Array.from(document.getElementById('usersSelectMulti').selectedOptions).map(option => option.value);
    // Здесь можно добавить логику создания группового чата с указанными параметрами
    console.debug('Create group chat ', chatName, users);
    await createChat(users, chatName);
  });

  startChatUserOkBtn.addEventListener('click', async function () {
    const user = document.getElementById('userSelect').value;
    // Здесь можно добавить логику начала чата с выбранным пользователем
    console.debug('Create chat ', user);
    await createChat(user);
  });
  await loadUserList();
})

async function loadUserList() {
  fetch('/api/accounts/')
    .then(response => response.json())
    .then(users => {
      const usersListContainer = document.querySelectorAll('.usersSelect');

      usersListContainer.forEach(userList => {
        users.forEach(user => {
          // <option value="user1">User 1</option>
          const userElement = document.createElement('option');
          userElement.value = user.id;
          userElement.text = user.username;

          userList.appendChild(userElement);
        });
      });
    })
    .catch(error => console.error('Error fetching chat list:', error));
}

async function createChat(users, chatName = '') {
  console.debug('createChat');
  const csrfToken = getCookie('csrftoken');

  const request_data = {
    name: chatName,
    members: users,
    type: 'create_chat'
  }
  fetch('/api/chats/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify(request_data),
  })
  .then(response => response.json())
  .then(newChat => {
    // После создания чата, отправьте уведомление через WebSocket
    // const js_data = JSON.stringify({
    //     type: 'chat.created',
    //     name: newChat.name,
    // })
    // socket.send(js_data);
    loadChatList();
    // currentChatId = newChat.id;
    // loadMessages(currentChatId);
  });
}

function loadChatList() {
    // Загружаем список чатов
    fetch('/api/chats/')
        .then(response => response.json())
        .then(chats => {
            const chatListContainer = document.getElementById('chat-list');
            chatListContainer.innerHTML = '';

            chats.forEach(chat => {
                const chatElement = document.createElement('div');
                chatElement.className = 'chat';
                chatElement.textContent = chat.name;

                // Обработчик клика по чату
                chatElement.addEventListener('click', function () {
                    setCurrentChatId(chat.id);
                    loadMessages(chat.id);
                });

                chatListContainer.appendChild(chatElement);
            });
        })
        .catch(error => console.error('Error fetching chat list:', error));
}
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}