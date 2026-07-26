(function() {
  // Check if we have an automation URL in the hash
  const hash = window.location.hash;
  if (!hash.includes('auto_yt_url=')) {
    return; // Normal site visit, do not automate
  }

  // Parse the YouTube URL from the hash
  const match = hash.match(/auto_yt_url=([^&]*)/);
  if (!match) return;
  const youtubeUrl = decodeURIComponent(match[1]);

  // Clean the address bar hash immediately so user has a clean URL
  try {
    history.replaceState(
      null, 
      document.title, 
      window.location.pathname + window.location.search
    );
  } catch (e) {
    console.error('[YT Auto-Transcriber] Failed to clean hash:', e);
  }

  console.log('[YT Auto-Transcriber] Starting automation for:', youtubeUrl);

  // Helper to wait for an element to exist and be visible in the DOM
  function waitForElement(selectorGetter, timeoutMs = 8000) {
    return new Promise((resolve, reject) => {
      // Check if it already exists
      const el = selectorGetter();
      if (el) {
        return resolve(el);
      }

      const interval = 100;
      let elapsed = 0;

      const timer = setInterval(() => {
        const target = selectorGetter();
        if (target) {
          clearInterval(timer);
          resolve(target);
        } else {
          elapsed += interval;
          if (elapsed >= timeoutMs) {
            clearInterval(timer);
            reject(new Error(`Timeout waiting for element`));
          }
        }
      }, interval);
    });
  }

  // Helper to dispatch React/Vue/standard event triggers
  function simulateInput(inputEl, value) {
    inputEl.focus();
    inputEl.value = value;
    
    // Dispatch standard input events to make sure reactive forms register the input
    inputEl.dispatchEvent(new Event('input', { bubbles: true }));
    inputEl.dispatchEvent(new Event('change', { bubbles: true }));
    
    // Blur to trigger potential blur-related validations
    inputEl.blur();
  }

  // Determine site selectors and run automation
  const hostname = window.location.hostname;

  if (hostname.includes('youtubetotranscript.com')) {
    // ---- Automating youtubetotranscript.com ----
    
    // Input element getter
    const getInput = () => document.querySelector('input[placeholder*="Paste YouTube URL"]') || 
                           document.querySelector('.input-bordered');
    
    // Button element getter
    const getButton = () => {
      // Try class first
      const btn = document.querySelector('button.btn-secondary');
      if (btn) return btn;
      
      // Fallback: search buttons containing specific text
      const buttons = Array.from(document.querySelectorAll('button'));
      return buttons.find(b => b.textContent.toLowerCase().includes('get free transcript'));
    };

    Promise.all([
      waitForElement(getInput),
      waitForElement(getButton)
    ]).then(([input, button]) => {
      console.log('[YT Auto-Transcriber] Elements found. Typing URL...');
      simulateInput(input, youtubeUrl);
      
      // Small timeout to allow potential reactive framework validation
      setTimeout(() => {
        console.log('[YT Auto-Transcriber] Clicking submit button...');
        button.click();
      }, 400);
    }).catch(err => {
      console.error('[YT Auto-Transcriber] Automation failed:', err);
    });

  } else if (hostname.includes('youtubetotranscript.io')) {
    // ---- Automating youtubetotranscript.io ----
    
    const getInput = () => document.querySelector('input#youtube-url');
    
    // On youtubetotranscript.io, the button might not exist or be disabled initially, 
    // but let's locate it by finding a button containing "Generate Transcript"
    const getButton = () => {
      const buttons = Array.from(document.querySelectorAll('button'));
      return buttons.find(b => b.textContent.toLowerCase().includes('generate transcript'));
    };

    waitForElement(getInput)
      .then((input) => {
        console.log('[YT Auto-Transcriber] Input found. Typing URL...');
        simulateInput(input, youtubeUrl);

        // Wait for the button to appear or become enabled
        return waitForElement(getButton);
      })
      .then((button) => {
        // Small delay to ensure click registers
        setTimeout(() => {
          console.log('[YT Auto-Transcriber] Clicking submit button...');
          button.click();
        }, 500);
      })
      .catch(err => {
        console.error('[YT Auto-Transcriber] Automation failed:', err);
      });
  }
})();
