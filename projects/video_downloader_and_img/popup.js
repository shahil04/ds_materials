document.addEventListener('DOMContentLoaded', async () => {

    // ── Helpers ────────────────────────────────────────────────────────────
    async function getCurrentTab() {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        return tab;
    }

    async function injectContentScript(tabId) {
        await chrome.scripting.executeScript({
            target: { tabId },
            files: ['content.js']
        }).catch(() => {}); // ignore if already injected
    }

    function downloadMedia(url, filename) {
        return new Promise((resolve) => {
            chrome.runtime.sendMessage(
                { action: 'download_media', payload: { url, filename } },
                resolve
            );
        });
    }

    function showStatus(el, msg, ok) {
        el.textContent = msg;
        el.className = ok ? 'status-success' : 'status-error';
        setTimeout(() => { el.textContent = ''; el.className = ''; }, 3000);
    }

    function flashDone(btn) {
        btn.classList.add('done');
        setTimeout(() => btn.classList.remove('done'), 1500);
    }

    // ── Tab Switching ──────────────────────────────────────────────────────
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.add('active');
        });
    });

    // ══════════════════════════════════════════════════════════════════════
    // VIDEOS TAB
    // ══════════════════════════════════════════════════════════════════════
    const videoResults    = document.getElementById('video-results');
    const scanVideosBtn   = document.getElementById('scan-videos-btn');
    const clearVideosBtn  = document.getElementById('clear-videos-btn');
    const dlAllBtn        = document.getElementById('download-all-videos-btn');

    let videoItems = []; // currently displayed video list

    // Load network-detected videos whenever popup opens
    (async () => {
        const tab = await getCurrentTab();
        if (!tab) return;
        await loadNetworkVideos(tab.id);
    })();

    async function loadNetworkVideos(tabId) {
        const resp = await chrome.runtime.sendMessage({ action: 'get_detected_videos', tabId });
        const networkVideos = resp?.videos || [];
        networkVideos.forEach(v => {
            if (!videoItems.find(x => x.url === v.url)) {
                videoItems.push(v);
            }
        });
        renderVideoList();
    }

    // Scan page DOM for videos
    scanVideosBtn.addEventListener('click', async () => {
        scanVideosBtn.classList.add('scanning');
        scanVideosBtn.textContent = 'Scanning…';

        try {
            const tab = await getCurrentTab();
            await injectContentScript(tab.id);

            await new Promise((resolve, reject) => {
                chrome.tabs.sendMessage(tab.id, { action: 'scan_page' }, (response) => {
                    if (chrome.runtime.lastError) { reject(chrome.runtime.lastError); return; }

                    const domVideos = (response?.items || []).filter(i => i.type === 'video');
                    domVideos.forEach(v => {
                        if (!videoItems.find(x => x.url === v.url)) {
                            videoItems.push({ ...v, source: 'dom' });
                        }
                    });

                    // Also refresh network-detected
                    chrome.runtime.sendMessage({ action: 'get_detected_videos', tabId: tab.id }, (r) => {
                        const net = r?.videos || [];
                        net.forEach(v => {
                            if (!videoItems.find(x => x.url === v.url)) videoItems.push(v);
                        });
                        renderVideoList();
                        resolve();
                    });
                });
            });
        } catch (e) {
            videoResults.innerHTML = `<div class="empty-state"><p>Cannot scan this page. Try a regular website.</p></div>`;
        } finally {
            scanVideosBtn.classList.remove('scanning');
            scanVideosBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg> Scan Page Videos`;
        }
    });

    // Clear list
    clearVideosBtn.addEventListener('click', async () => {
        videoItems = [];
        const tab = await getCurrentTab();
        if (tab) chrome.runtime.sendMessage({ action: 'clear_detected_videos', tabId: tab.id });
        renderVideoList();
        dlAllBtn.style.display = 'none';
    });

    // Download All
    dlAllBtn.addEventListener('click', async () => {
        for (const item of videoItems) {
            await downloadMedia(item.url, item.title);
            await new Promise(r => setTimeout(r, 300)); // small delay between downloads
        }
    });

    function renderVideoList() {
        if (videoItems.length === 0) {
            videoResults.innerHTML = `
                <div class="empty-state">
                    <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/></svg>
                    <p>Play a video on the page first,<br>then scan or it appears here.</p>
                </div>`;
            dlAllBtn.style.display = 'none';
            return;
        }

        videoResults.innerHTML = '';
        videoItems.forEach((item, i) => {
            videoResults.appendChild(createVideoCard(item, i));
        });
        dlAllBtn.style.display = videoItems.length > 1 ? 'block' : 'none';
    }

    function createVideoCard(item, index) {
        const isNetwork = item.source === 'network';
        const div = document.createElement('div');
        div.className = 'media-item';

        const ext = getExt(item.url);
        const sourceClass = isNetwork ? 'network' : 'dom';
        const sourceLabel = isNetwork ? 'Network' : 'DOM';
        const thumbClass = isNetwork ? 'video-thumb-network' : 'video-thumb';

        div.innerHTML = `
            <div class="media-thumb ${thumbClass}">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/>
                </svg>
            </div>
            <div class="media-info">
                <div class="media-title" title="${item.title}">${item.title}</div>
                <div class="media-meta">
                    <span class="source-tag ${sourceClass}">${sourceLabel}</span>
                    ${ext ? `<span class="source-tag dom">${ext.toUpperCase()}</span>` : ''}
                </div>
            </div>
            <button class="dl-btn" title="Download">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
            </button>`;

        div.querySelector('.dl-btn').addEventListener('click', async (e) => {
            const btn = e.currentTarget;
            await downloadMedia(item.url, item.title);
            flashDone(btn);
        });

        return div;
    }

    // ══════════════════════════════════════════════════════════════════════
    // IMAGES TAB
    // ══════════════════════════════════════════════════════════════════════
    const imageResults  = document.getElementById('image-results');
    const scanImagesBtn = document.getElementById('scan-images-btn');

    scanImagesBtn.addEventListener('click', async () => {
        scanImagesBtn.classList.add('scanning');
        scanImagesBtn.textContent = 'Scanning…';
        imageResults.innerHTML = '';

        try {
            const tab = await getCurrentTab();
            await injectContentScript(tab.id);

            chrome.tabs.sendMessage(tab.id, { action: 'scan_page' }, (response) => {
                if (chrome.runtime.lastError) {
                    imageResults.innerHTML = `<div class="empty-state"><p>Cannot scan this page.</p></div>`;
                    return;
                }
                const images = (response?.items || []).filter(i => i.type === 'image');
                if (images.length === 0) {
                    imageResults.innerHTML = `<div class="empty-state"><p>No images found.</p></div>`;
                } else {
                    images.forEach(item => imageResults.appendChild(createImageCard(item)));
                }
                scanImagesBtn.classList.remove('scanning');
                scanImagesBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg> Scan Page Images`;
            });
        } catch (e) {
            imageResults.innerHTML = `<div class="empty-state"><p>Error scanning page.</p></div>`;
            scanImagesBtn.classList.remove('scanning');
        }
    });

    function createImageCard(item) {
        const div = document.createElement('div');
        div.className = 'media-item';
        const ext = getExt(item.url);

        div.innerHTML = `
            <div class="media-thumb">
                <img src="${item.url}" alt="${item.title}" class="thumb-img"
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                <div class="thumb-fallback" style="display:none">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2"/>
                        <circle cx="8.5" cy="8.5" r="1.5"/>
                        <polyline points="21 15 16 10 5 21"/>
                    </svg>
                </div>
            </div>
            <div class="media-info">
                <div class="media-title" title="${item.title}">${item.title}</div>
                <div class="media-meta">
                    <span class="source-tag image">Image</span>
                    ${ext ? `<span class="source-tag dom">${ext.toUpperCase()}</span>` : ''}
                </div>
            </div>
            <button class="dl-btn" title="Download">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
            </button>`;

        div.querySelector('.dl-btn').addEventListener('click', async (e) => {
            const btn = e.currentTarget;
            await downloadMedia(item.url, item.title);
            flashDone(btn);
        });

        return div;
    }

    // ══════════════════════════════════════════════════════════════════════
    // PASTE URL TAB
    // ══════════════════════════════════════════════════════════════════════
    const urlInput      = document.getElementById('url-input');
    const filenameInput = document.getElementById('filename-input');
    const dlUrlBtn      = document.getElementById('download-url-btn');
    const pasteStatus   = document.getElementById('paste-status');

    dlUrlBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        const filename = filenameInput.value.trim();
        if (!url) { showStatus(pasteStatus, 'Please enter a URL.', false); return; }
        try { new URL(url); } catch { showStatus(pasteStatus, 'Invalid URL format.', false); return; }

        await downloadMedia(url, filename || undefined);
        showStatus(pasteStatus, '✓ Download started!', true);
    });

    // ── Utility ────────────────────────────────────────────────────────────
    function getExt(url) {
        try {
            const path = new URL(url).pathname;
            const seg = path.split('/').pop();
            if (seg.includes('.')) return seg.split('.').pop().split('?')[0].toLowerCase();
        } catch {}
        return '';
    }
});
