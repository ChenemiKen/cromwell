// const socket='';
document.getElementById('switch-on').onclick= ()=>{
    fetch('/app/switchon').then(response =>{
        console.log(response);
    });
        
    const socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + 'roomName'
        + '/'
    );

    socket.onopen=()=>{
        console.log('Wesocket connected');
    }
};

