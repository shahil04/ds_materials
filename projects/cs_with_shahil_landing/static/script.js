
// Simple JS for toggle chatbot modal and menu
document.addEventListener('DOMContentLoaded', function(){
  var chatBtn = document.getElementById('chatbotBtn');
  var chatModal = document.getElementById('chatModal');
  var closeChat = document.getElementById('closeChat');
  var chatForm = document.getElementById('chatForm');
  var chatBody = document.querySelector('.chat-body');

  if(chatBtn){
    chatBtn.addEventListener('click', function(){ chatModal.style.display = 'flex'; });
  }
  if(closeChat){ closeChat.addEventListener('click', function(){ chatModal.style.display = 'none'; }); }
  if(chatForm){
    chatForm.addEventListener('submit', function(e){
      e.preventDefault();
      var input = document.getElementById('chatInput');
      if(!input.value) return;
      var node = document.createElement('div'); node.className='msg user'; node.textContent = input.value;
      chatBody.appendChild(node);
      // simple echo bot
      setTimeout(function(){
        var bot = document.createElement('div'); bot.className='msg bot';
        bot.textContent = 'Thanks for your question! Our counselor will contact you soon.';
        chatBody.appendChild(bot);
        chatBody.scrollTop = chatBody.scrollHeight;
      }, 800);
      input.value='';
    });
  }
});
