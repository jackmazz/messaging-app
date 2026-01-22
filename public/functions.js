const ws = true;
let socket = null;
let chatMessages = {};

function welcome() {
    document.addEventListener("keypress", function (event) {
        if (event.code === "Enter") {
            sendChat();
        }
    });
    document.getElementById("paragraph").innerHTML += "<br/>This text was added by JavaScript 😀";
    document.getElementById("chat-text-box").focus();
    updateChat();
    if (ws) {
        initWS();
    } else {
        setInterval(updateChat, 3000);
    }
}

function sendChat() {
    const chatTextBox = document.getElementById("chat-text-box");
    const message = chatTextBox.value;
    const xsrf_token = document.getElementById("xsrf_token").value;
    chatTextBox.value = "";
    if (ws) {
        socket.send(JSON.stringify({'messageType': 'chatMessage', 'message': message, "xsrf_token": xsrf_token}));
    } else {
        const request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                console.log(this.response);
            }
        }
        const messageJSON = {"message": message, "xsrf_token": xsrf_token};
        request.open("POST", "/chat-messages");
        request.send(JSON.stringify(messageJSON));
    }
    chatTextBox.focus();
}

function deleteMessage(messageId) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    request.open("DELETE", "/chat-messages/" + messageId);
    request.send();
}

function updateChat() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            updateChatMessages(JSON.parse(this.response));
        }
    }
    request.open("GET", "/chat-messages");
    request.send();
}

function updateChatMessages(serverMessages) {
    let serverIndex = 0
    let localIndex = 0;
    while (serverIndex < serverMessages.length && localIndex < chatMessages.length) {
        let fromServer = serverMessages[serverIndex];
        let localMessage = chatMessages[localIndex];
        if (fromServer["id"] !== localMessage["id"]) {
            const messageElem = document.getElementById("message_" + localMessage["id"]);
            messageElem.parentNode.removeChild(messageElem);
            localIndex++;
        } else {
            serverIndex++;
            localIndex++;
        }
    }
    while (localIndex < chatMessages.length) {
        let localMessage = chatMessages[localIndex];
        const messageElem = document.getElementById("message_" + localMessage["id"]);
        messageElem.parentNode.removeChild(messageElem);
        localIndex++;
    }
    const postIds = getPostIds()
    while (serverIndex < serverMessages.length) {
        addMessageToChat(serverMessages[serverIndex], postIds);
        serverIndex++;
    }
    chatMessages = serverMessages;
}

function addMessageToChat(messageJSON, postIds) {
    const chatMessages = document.getElementById("chat-messages");
    const isUserPost = postIds.includes(messageJSON.id);
    chatMessages.insertAdjacentHTML("beforeend", chatMessageHTML(messageJSON, isUserPost));
    chatMessages.scrollIntoView(false);
    chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
}

function chatMessageHTML(messageJSON, isUserPost) {
    const username = messageJSON.username;
    const message = messageJSON.message;
    const messageId = messageJSON.id;
    let messageHTML = "<b>" + username + ":</b><br>" + message + "<br><br>";
    console.log("message_length: " + message.length)
    if(isUserPost) {
        messageHTML = "<font color=\"#FFFF00\">" + messageHTML + "</font>"
    }
    messageHTML = "<div id='message_" + messageId + "'><button onclick='deleteMessage(\"" + messageId + "\")'>X</button> " + messageHTML + "</div>";
    return messageHTML;
}

function initWS() {
    socket = new WebSocket('wss://' + window.location.host + '/websocket');
    socket.onmessage = function (ws_message) {
        const message = JSON.parse(ws_message.data);
        const messageType = message.messageType
        if (messageType === 'chatMessage') {
            addMessageToChat(message, getPostIds());
        } else {
            processMessageAsWebRTC(message, messageType);
        }
    }
}

function getCookie(name) {
    let cookies = decodeURIComponent(document.cookie);
    for(const element of cookies.split(";")) {
        let split = element.split("=", 2);
        if(split.length == 2) {
            let key = split[0].trim()
            let value = split[1].trim()
            if(key == name) {
                return value
            }
        }
    }
}

function getPostIds() {
    let post_ids = getCookie("post_ids")
    if(post_ids == null) {
        return []
    }
    return JSON.parse(post_ids);
}