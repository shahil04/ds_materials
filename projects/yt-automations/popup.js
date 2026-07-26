document.addEventListener('DOMContentLoaded', () => {
  const urlInput = document.getElementById('yt-url');
  const clearBtn = document.getElementById('clear-btn');
  const previewContainer = document.getElementById('preview-container');
  const videoCard = previewContainer.querySelector('.video-card');
  const emptyState = previewContainer.querySelector('.empty-state');
  const thumbnail = document.getElementById('video-thumbnail');
  const videoTitleEl = document.getElementById('video-title');
  const transcribeBtn = document.getElementById('transcribe-btn');
  
  // Provider elements
  const comRadio = document.querySelector('input[value="com"]');
  const ioRadio = document.querySelector('input[value="io"]');
  const comLabel = document.getElementById('provider-com-label');
  const ioLabel = document.getElementById('provider-io-label');

  // Set up provider radio selection styling
  function updateProviderUI() {
    if (comRadio.checked) {
      comLabel.classList.add('active');
      ioLabel.classList.remove('active');
    } else {
      ioLabel.classList.add('active');
      comLabel.classList.remove('active');
    }
  }

  comRadio.addEventListener('change', updateProviderUI);
  ioRadio.addEventListener('change', updateProviderUI);

  // Helper to extract YouTube Video ID
  function extractVideoId(url) {
    if (!url) return null;
    try {
      const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|live\/)([^#\&\?]*).*/;
      const match = url.match(regExp);
      return (match && match[2].length === 11) ? match[2] : null;
    } catch (e) {
      return null;
    }
  }

  // Helper to check if a URL is a valid YouTube URL
  function isValidYouTubeUrl(url) {
    return !!extractVideoId(url);
  }

  // Update preview card based on URL
  function updatePreview(url, tabTitle = '') {
    const videoId = extractVideoId(url);
    
    if (videoId) {
      // Input has a valid YouTube URL
      thumbnail.src = `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
      
      // Attempt to clean up tab title if provided, otherwise show generic title
      let displayTitle = 'YouTube Video Detected';
      if (tabTitle) {
        displayTitle = tabTitle.replace(/ - YouTube$/i, '');
      } else {
        displayTitle = `Video ID: ${videoId}`;
      }
      
      videoTitleEl.textContent = displayTitle;
      
      // Update visibility states
      emptyState.classList.add('hidden');
      videoCard.classList.remove('hidden');
      previewContainer.classList.remove('empty');
      
      // Enable Action Button
      transcribeBtn.disabled = false;
      transcribeBtn.classList.remove('disabled');
    } else {
      // Input is empty or invalid
      emptyState.classList.remove('hidden');
      videoCard.classList.add('hidden');
      previewContainer.classList.add('empty');
      
      // Disable Action Button
      transcribeBtn.disabled = true;
      transcribeBtn.classList.add('disabled');
    }

    // Toggle clear button visibility
    if (url.length > 0) {
      clearBtn.classList.remove('hidden');
    } else {
      clearBtn.classList.add('hidden');
    }
  }

  // Auto-detect YouTube tab on popup load
  if (chrome && chrome.tabs) {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs && tabs[0]) {
        const activeTab = tabs[0];
        const activeUrl = activeTab.url || '';
        
        if (isValidYouTubeUrl(activeUrl)) {
          urlInput.value = activeUrl;
          updatePreview(activeUrl, activeTab.title);
        }
      }
    });
  }

  // Listen to input typing changes
  urlInput.addEventListener('input', (e) => {
    const value = e.target.value.trim();
    updatePreview(value);
  });

  // Clear button click handler
  clearBtn.addEventListener('click', () => {
    urlInput.value = '';
    updatePreview('');
    urlInput.focus();
  });

  // Action Button (Transcribe) Click handler
  transcribeBtn.addEventListener('click', () => {
    const url = urlInput.value.trim();
    if (!isValidYouTubeUrl(url)) return;

    const provider = document.querySelector('input[name="provider"]:checked').value;
    let targetBaseUrl = 'https://youtubetotranscript.com/';
    
    if (provider === 'io') {
      targetBaseUrl = 'https://youtubetotranscript.io/';
    }

    // Embed URL as a hash parameters to prevent search logs on the transcribers 
    // and let the content script extract it cleanly.
    const finalUrl = `${targetBaseUrl}#auto_yt_url=${encodeURIComponent(url)}`;
    
    if (chrome && chrome.tabs) {
      chrome.tabs.create({ url: finalUrl });
      window.close(); // Close the extension popup
    } else {
      // Fallback for debugging in regular tab
      window.open(finalUrl, '_blank');
    }
  });
});
