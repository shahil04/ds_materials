// ─────────────────────────────────────────────────────────────────────────────
// VIDEO EXTENSION PATTERNS
// ─────────────────────────────────────────────────────────────────────────────
const VIDEO_EXT = /\.(mp4|webm|mkv|ogg|ogv|avi|mov|flv|ts|m3u8)(\?.*)?$/i;
const IMAGE_EXT = /\.(jpg|jpeg|png|gif|webp|bmp|svg|avif)(\?.*)?$/i;

// In-memory store: tabId -> Set of detected video URLs
const detectedVideos = {};

// ─────────────────────────────────────────────────────────────────────────────
// NETWORK INTERCEPTION — capture video requests as the page loads them
// ─────────────────────────────────────────────────────────────────────────────
chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    if (details.type === 'media' || VIDEO_EXT.test(details.url)) {
      const tabId = details.tabId;
      if (tabId < 0) return; // background requests
      if (!detectedVideos[tabId]) detectedVideos[tabId] = [];

      // Avoid duplicates
      if (!detectedVideos[tabId].find(v => v.url === details.url)) {
        detectedVideos[tabId].push({
          url: details.url,
          title: getTitleFromUrl(details.url),
          source: 'network',
          type: 'video'
        });
      }
    }
  },
  { urls: ['<all_urls>'] }
);

// Clear captured videos when a tab navigates away
chrome.tabs.onUpdated.addListener((tabId, changeInfo) => {
  if (changeInfo.status === 'loading') {
    detectedVideos[tabId] = [];
  }
});

// Clean up when a tab closes
chrome.tabs.onRemoved.addListener((tabId) => {
  delete detectedVideos[tabId];
});

// ─────────────────────────────────────────────────────────────────────────────
// HELPER
// ─────────────────────────────────────────────────────────────────────────────
function getTitleFromUrl(url) {
  try {
    const urlObj = new URL(url);
    const segments = urlObj.pathname.split('/').filter(Boolean);
    const last = segments[segments.length - 1] || 'video';
    // Remove query string and decode
    return decodeURIComponent(last.split('?')[0]);
  } catch {
    return 'video';
  }
}

function sanitizeFilename(name) {
  return name.replace(/[/\\?%*:|"<>]/g, '-');
}

function getExtension(url) {
  try {
    const pathname = new URL(url).pathname;
    const parts = pathname.split('.');
    if (parts.length > 1) return '.' + parts.pop().split('?')[0].toLowerCase();
  } catch {}
  return '';
}

// ─────────────────────────────────────────────────────────────────────────────
// MESSAGE LISTENER
// ─────────────────────────────────────────────────────────────────────────────
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

  // ── Get detected network videos for a specific tab ──
  if (request.action === 'get_detected_videos') {
    const tabId = request.tabId;
    const videos = detectedVideos[tabId] || [];
    sendResponse({ videos });
    return true;
  }

  // ── Clear detected videos for a tab ──
  if (request.action === 'clear_detected_videos') {
    const tabId = request.tabId;
    detectedVideos[tabId] = [];
    sendResponse({ success: true });
    return true;
  }

  // ── Download a media file ──
  if (request.action === 'download_media') {
    const { url, filename } = request.payload;

    if (!url) {
      sendResponse({ success: false, error: 'No URL provided' });
      return true;
    }

    let cleanName = sanitizeFilename(filename || getTitleFromUrl(url));
    const ext = getExtension(url);

    const knownExts = ['.mp4','.webm','.mkv','.ogg','.avi','.mov','.ts','.m3u8',
                       '.jpg','.jpeg','.png','.gif','.webp','.bmp','.svg','.avif'];
    if (!knownExts.some(e => cleanName.toLowerCase().endsWith(e)) && ext) {
      cleanName += ext;
    }

    chrome.downloads.download({ url, filename: cleanName, saveAs: false }, (downloadId) => {
      if (chrome.runtime.lastError) {
        sendResponse({ success: false, error: chrome.runtime.lastError.message });
      } else {
        sendResponse({ success: true, downloadId });
      }
    });

    return true;
  }
});
