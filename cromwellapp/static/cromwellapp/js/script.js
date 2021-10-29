// const socket='';
const yesNotificationBtn = document.getElementById('yesNotification');
const noNotificationBtn = document.getElementById('noNotification');

noNotificationBtn.onclick = ()=>{askNotificationPermission()}
yesNotificationBtn.onclick = sendNotification
handlePermission()
document.getElementById('pph-switch-on').onclick= ()=>{
    fetch('/app/pphswitchon').then(response =>{
        // console.log(response);
    });
        
    const socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/cromwell/'
        + 'app'
        + '/'
    );

    socket.onopen=()=>{
        console.log('Wesocket connected');
    }
    socket.onmessage=(event)=>{
        console.log(event.data);
        sendNotification();
        // if (!('Notification' in window)) {
        //     // set the button to shown or hidden, depending on what the user answers
        //     if(Notification.permission === 'default') {
        //         askNotificationPermission();
        //         // send notification
        //         sendNotification();
        //     } else if(Notification.permission === 'granted'){
        //         // send notification
        //         sendNotification();
        //     }
        // }
    }
        
    socket.onclose=()=>{
        console.log('socket closed.')
    }
};

function sendNotification(){
    // if(Notification.permission === 'granted'){
        var text = 'HEY! Your task is now overdue.';
        var notification = new Notification('To do list', { body: text});
    // }
}


function askNotificationPermission() {
  // function to actually ask the permissions
  // Let's check if the browser supports notifications
  if (!('Notification' in window)) {
    console.log("This browser does not support notifications.");
    alert('This browser does not support notifications')
  } else {
    if(checkNotificationPromise()) {
      Notification.requestPermission()
      .then((permission) => {
        handlePermission(permission);
      })
    } else {
      Notification.requestPermission(function(permission) {
        handlePermission(permission);
      });
    }
  }
}

// Handles notification permissions
function handlePermission(permission) {
    if ('Notification' in window) {
        // set the button to shown or hidden, depending on what the user answers
        if(Notification.permission === 'denied' || Notification.permission === 'default') {
            yesNotificationBtn.style.display = 'none';
            noNotificationBtn.style.display = 'block';
        } else {
            yesNotificationBtn.style.display = 'block';
            noNotificationBtn.style.display = 'none';
        }
    } else{
        yesNotificationBtn.style.display = 'none';
        noNotificationBtn.style.display = 'block';
    }
}

// to check if the browser supports the promise version of requestPermission.
// We basically try to see if the .then() method is available on requestPermission().
function checkNotificationPromise() {
    try {
      Notification.requestPermission().then();
    } catch(e) {
      return false;
    }

    return true;
  }

