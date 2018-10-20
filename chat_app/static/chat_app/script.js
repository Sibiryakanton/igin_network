var startBadge = function(){
  var newMessLen = 0;
  $('#counter').removeClass('badge-secondary');
  $('#counter').removeClass('badge-success');
  $('#counter').addClass((newMessLen != 0) ? 'badge-success' : 'badge-secondary');
  $('#counter').text(newMessLen);
}
var NewUpdatePlusBadge = function(){
  $('#counter').removeClass('badge-secondary');
  $('#counter').removeClass('badge-success');
  var newMessLen = document.getElementById('counter').innerHTML;
  /*$('#counter').removeClass('badge-secondary');
  $('#counter').removeClass('badge-success'); */
  newMessLen = parseInt(newMessLen) + 1;
  $('#counter').text(newMessLen);
  $('#counter').addClass((newMessLen != 0) ? 'badge-success' : 'badge-secondary');
}
var NewUpdateMinusBadge = function(){
  $('#counter').removeClass('badge-secondary');
  $('#counter').removeClass('badge-success');
  var newMessLen = document.getElementById('counter').innerHTML;
  newMessLen = parseInt(newMessLen) - 1;
  $('#counter').text(newMessLen);
  $('#counter').addClass((newMessLen != 0) ? 'badge-success' : 'badge-secondary');
}

var offset = new Date().getTimezoneOffset();
var hour_diff = offset / 60;
var pathname = document.location.pathname.split('/');
var roomName = pathname[pathname.length-2];

var current_user_id = document.getElementById('current_user_id').innerHTML;

startBadge();
room_socket_url = 'ws://' + window.location.host + '/ws/chat/' + roomName + '/';
var chatSocket = new WebSocket(room_socket_url);
    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message_type = data['message_type'];
        // На данный момент есть два типа сообщения: chat_message (создание сообщения) и update_message_status
        // (обновление статуса существующего сообщения в чате)
        if (message_type === 'create_message') {
            var date_published = data['date_published'];
            var time_published = data['time_published'];
            var author = data['author'];
            var author_id = data['author_id'];
            var message_text = data['message'];
            var read = data['read'];
            var message_id = data['message_id'];

              /* Cборка и добавление сообщения */
              var message = document.createElement('div');
              message.classList.add('col-sm-12');
              var alertBox = document.createElement('div');
              alertBox.classList.add('alert');
              alertBox.id = 'message_' + message_id + '_' + author_id;
              if (read == false){
                  alertBox.classList.add('alert-success');
              } else {
                alertBox.classList.add('alert-light');
              }
              alertBox.setAttribute('role','alert');
              message.append(alertBox);
              var messageText = document.createElement('p');
              messageText.innerText = message_text;
              alertBox.append(messageText);
              alertBox.append(document.createElement('hr'));

              var infoContainer = document.createElement('p');
              infoContainer.classList.add('mb-0');

            // Сборка даты и перевод на локальное время
             date_list = date_published.split('-');
             time_list = time_published.split(':');
             new_date = new Date(date_list[0], date_list[1], date_list[2], time_list[0], time_list[1], time_list[2])
             var hours = new_date.getHours();
             new_date.setHours(hours - hour_diff);
             // конец сборки

              var infoDate = document.createElement('span');
              infoDate.classList.add('small');
              var now = new Date();
              infoDate.innerText = new_date.toLocaleTimeString();;
              var infoAuthor = document.createElement('span');
              infoAuthor.classList.add('small');
              infoAuthor.classList.add('float-right');
              infoAuthor.innerText = author;

              infoContainer.append(infoDate);
              infoContainer.append(infoAuthor);
              alertBox.append(infoContainer);
              $('#messages').prepend(message);
              $('#message_box').val("")
              if (current_user_id != author_id && read==false) {
                NewUpdatePlusBadge();
              }
              /* Конец сборки и добавления сообщения */

            }
         else if (message_type == 'update_message_status'){
            var message_id = data['message_id'];
            var author_id = data['author_id'];

            current_user_id = document.getElementById('current_user_id').innerHTML;
            var updatedElement = document.getElementById('message_' + message_id + '_' + author_id);
            console.error('message_' + message_id + '_' + author_id);
            updatedElement.classList.remove('alert-success');
            updatedElement.classList.add('alert-light');
            if (current_user_id != author_id) {
                NewUpdateMinusBadge();
              }
         }

    };

$(document).on('mouseenter', '.alert-success', function(e){
  var current_user_id = document.getElementById('current_user_id').innerHTML;
  var message_id = $(this).attr('id').split('_')[1] /* Получить id сообщения */
  var author_id = $(this).attr('id').split('_')[2]

  if (current_user_id != author_id){
      chatSocket.send(JSON.stringify({
          'message_id': message_id,
          'type_message': 'update_message_status',
      }));
  }
});

$(document).on('click','#btn_send', function(){
  var messageInputDom = ($('#message_box').val());
  chatSocket.send(JSON.stringify({
      'message': messageInputDom,
      'type_message': 'send_message',
  }));
  messageInputDom.value = '';
})

$(document).on('keydown','#message_box', function(e){
  if(e.keyCode === 13) {
    $('#btn_send').click();
  }
})
