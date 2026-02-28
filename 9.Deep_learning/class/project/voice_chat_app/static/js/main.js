// main.js for voice and chat interactions
let recognition = null;
let lastAudio = null;
const v_start = document.getElementById('v_start');
const v_stop = document.getElementById('v_stop');
const v_play = document.getElementById('v_play');
const v_source = document.getElementById('v_source');
const v_target = document.getElementById('v_target');
const v_orig = document.getElementById('v_orig');
const v_trans = document.getElementById('v_trans');

const chatbox = document.getElementById('chatbox');
const chat_input = document.getElementById('chat_input');
const send_chat = document.getElementById('send_chat');
const play_chat = document.getElementById('play_chat');

function supportsSpeech(){ return ('webkitSpeechRecognition' in window) || ('SpeechRecognition' in window); }

function createRec(){
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const r = new SpeechRecognition();
  r.continuous = true; r.interimResults = true; r.lang = v_source.value || 'en-IN';
  r.maxAlternatives = 1;
  r.onresult = (event) => {
    let final=''; let interim='';
    for(let i=event.resultIndex;i<event.results.length;++i){
      const res = event.results[i];
      if(res.isFinal) final += res[0].transcript;
      else interim += res[0].transcript;
    }
    v_orig.textContent = final + (interim? '\n'+interim : '');
    if(final.trim()) sendForTrans(final.trim());
  };
  r.onend = ()=>{ v_start.disabled=false; v_stop.disabled=true; console.log('stopped'); }
  r.onerror = (e)=>{ console.error(e); }
  return r;
}

v_start.onclick = ()=>{
  if(!supportsSpeech()){ alert('Use Chrome for Web Speech API'); return; }
  recognition = createRec();
  recognition.start();
  v_start.disabled=true; v_stop.disabled=false;
};

v_stop.onclick = ()=>{ if(recognition) recognition.stop(); };

v_play.onclick = ()=>{ if(lastAudio) new Audio(lastAudio).play(); };

async function sendForTrans(text){
  v_trans.textContent = 'Translating...';
  try{
    const res = await fetch('/api/translate_text',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text, source_lang:v_source.value.split('-')[0], target_lang:v_target.value})});
    const data = await res.json();
    v_trans.textContent = data.translated || '(no translation)';
    lastAudio = data.audio_url || null;
    v_play.disabled = !lastAudio;
    if(lastAudio){
      try{ const a=new Audio(lastAudio); await a.play(); }catch(e){ console.warn('Autoplay blocked',e); }
    }
  }catch(e){ console.error(e); v_trans.textContent='Error'; }
}

// Chat
send_chat.onclick = async ()=>{
  const msg = chat_input.value.trim(); if(!msg) return;
  appendMessage(msg,'user'); chat_input.value='';
  const history = [...document.querySelectorAll('.message')].map(el=>({role: el.classList.contains('msg-user')? 'user':'assistant', content: el.textContent}));
  try{
    const res = await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg, history})});
    const data = await res.json();
    appendMessage(data.reply || '(no reply)','assistant');
    play_chat.disabled = !data.audio_url;
    if(data.audio_url){ try{ new Audio(data.audio_url).play(); }catch(e){ console.warn('autoplay blocked'); } }
  }catch(e){ console.error(e); appendMessage('Error contacting server','assistant'); }
};

play_chat.onclick = ()=>{ /* not implemented: could store last assistant audio */ };

function appendMessage(text, who){
  const div = document.createElement('div'); div.className = 'message ' + (who==='user'? 'msg-user':'msg-assistant'); div.textContent = text;
  chatbox.appendChild(div); chatbox.scrollTop = chatbox.scrollHeight;
}