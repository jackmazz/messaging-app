const iceConfig = {
    'iceServers': [{'urls': ['stun:stun2.1.google.com:19302']}]
};

let webRTCConnection = new RTCPeerConnection(iceConfig);

function processMessageAsWebRTC(message, messageType) {
    switch (messageType) {
        case 'webRTC-offer':
            void webRTCConnection.setRemoteDescription(new RTCSessionDescription(message.offer));
            webRTCConnection.createAnswer().then(answer => {
                void webRTCConnection.setLocalDescription(answer);
                socket.send(JSON.stringify({'messageType': 'webRTC-answer', 'answer': answer}));
            });
            break;
        case 'webRTC-answer':
            void webRTCConnection.setRemoteDescription(new RTCSessionDescription(message.answer));
            break;
        case 'webRTC-candidate':
            void webRTCConnection.addIceCandidate(new RTCIceCandidate(message.candidate));
            break;
        default:
            console.log("received an invalid WS messageType");
    }
}

function startVideo() {
    const constraints = {video: true, audio: true};
    navigator.mediaDevices.getUserMedia(constraints).then((myStream) => {
        const elem = document.getElementById("myVideo");
        elem.srcObject = myStream;
        webRTCConnection.addStream(myStream);
        webRTCConnection.onaddstream = function (data) {
            const remoteVideo = document.getElementById('otherVideo');
            remoteVideo.srcObject = data.stream;
        };
        webRTCConnection.onicecandidate = function (data) {
            if (data.candidate) {
                socket.send(JSON.stringify({'messageType': 'webRTC-candidate', 'candidate': data.candidate}));
            }
        };
    })
}

function connectWebRTC() {
    webRTCConnection.createOffer().then(webRTCOffer => {
        socket.send(JSON.stringify({'messageType': 'webRTC-offer', 'offer': webRTCOffer}));
        void webRTCConnection.setLocalDescription(webRTCOffer);
    });
}
