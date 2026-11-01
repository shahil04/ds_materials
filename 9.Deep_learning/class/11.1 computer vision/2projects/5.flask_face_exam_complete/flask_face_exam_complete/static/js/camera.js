// static/js/camera.js - Advanced Proctored Assessment Controller
(function () {
  'use strict';

  // DOM Elements
  const video = document.getElementById('video');
  const statusBadge = document.getElementById('statusBadge');
  const statusDot = document.getElementById('statusDot');
  const faultsCountEl = document.getElementById('faultsCount');
  const faultsBar = document.getElementById('faultsBar');
  const tickerText = document.getElementById('tickerText');
  const cameraCard = document.getElementById('proctorCameraCard');
  const timerDisplay = document.getElementById('timerDisplay');
  const examForm = document.getElementById('examForm');
  const answeredProgressFill = document.getElementById('answeredProgressFill');
  const answeredBadge = document.getElementById('answeredBadge');

  // Modals
  const welcomeModal = document.getElementById('welcomeModal');
  const startExamBtn = document.getElementById('startExamBtn');
  const confirmModal = document.getElementById('confirmModal');
  const confirmSummaryText = document.getElementById('confirmSummaryText');
  const cancelSubmitBtn = document.getElementById('cancelSubmitBtn');
  const finalSubmitBtn = document.getElementById('finalSubmitBtn');
  const tabWarningModal = document.getElementById('tabWarningModal');
  const dismissTabWarnBtn = document.getElementById('dismissTabWarnBtn');
  const autoSubmitModal = document.getElementById('autoSubmitModal');

  // Hidden canvas for frame capture
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');

  // State
  let currentQIndex = 0;
  const questionPanels = document.querySelectorAll('.question-panel');
  const totalQuestions = questionPanels.length;
  const paletteButtons = document.querySelectorAll('.palette-btn');
  const markedForReview = new Set();
  let maxFaults = 10;
  let examRunning = false;
  let tabSwitchCount = 0;
  let lastViolationReason = "";

  // Audio Context for subtle proctor alert chimes
  let audioCtx = null;
  function playAlertBeep(isDanger) {
    try {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.type = isDanger ? 'sawtooth' : 'sine';
      osc.frequency.setValueAtTime(isDanger ? 380 : 540, audioCtx.currentTime);
      gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.35);
    } catch (e) {
      // Audio autoplay policy fallback
    }
  }

  // ==========================================
  // Toast Notification System
  // ==========================================
  const toastContainer = document.getElementById('toastContainer');
  function showToast(message, type = 'info') {
    if (!toastContainer) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      <span style="font-size:1.1rem">${type === 'danger' ? '⛔' : (type === 'warn' ? '⚠️' : 'ℹ️')}</span>
      <span>${message}</span>
    `;
    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(30px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 4000);
  }

  // ==========================================
  // Webcam Initialization & Streaming
  // ==========================================
  async function startWebcam() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' },
        audio: false
      });
      video.srcObject = stream;
      await video.play();
      showToast('AI Proctoring Camera Connected', 'info');
      // Begin frame analysis loop
      setTimeout(sendFrameLoop, 1200);
    } catch (err) {
      console.error('Camera access error:', err);
      if (statusBadge) statusBadge.innerText = 'Camera Error';
      if (statusDot) statusDot.className = 'status-indicator-dot danger';
      showToast('Camera access denied. Please allow webcam permissions.', 'danger');
    }
  }

  async function sendFrameLoop() {
    if (!examRunning) {
      setTimeout(sendFrameLoop, 800);
      return;
    }

    if (video.readyState < 2) {
      setTimeout(sendFrameLoop, 500);
      return;
    }

    // Capture current frame from video stream
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/jpeg', 0.75);

    try {
      const resp = await fetch('/monitor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ frame: dataUrl })
      });
      const result = await resp.json();

      if (result.error) {
        console.warn('Proctor server error:', result.error);
      } else {
        updateProctorUI(result);

        if (result.submit) {
          handleMaxFaultsReached();
          return;
        }
      }
    } catch (e) {
      console.error('Monitor request failure:', e);
    }

    // Interval between proctor frames: 1200ms
    setTimeout(sendFrameLoop, 1200);
  }

  function updateProctorUI(result) {
    const status = result.status || 'Face OK';
    const faults = result.faults || 0;
    maxFaults = result.max_faults || 10;
    const severity = result.severity || (status === 'Face OK' ? 'ok' : 'warning');

    // Status Badge & Dot
    if (statusBadge) {
      if (status === 'Face OK') {
        statusBadge.innerText = 'Face Verified';
      } else {
        statusBadge.innerText = status;
      }
    }

    if (statusDot) {
      statusDot.className = `status-indicator-dot ${severity}`;
    }

    // Camera Card Glow Effect
    if (cameraCard) {
      cameraCard.classList.remove('status-ok', 'status-warning', 'status-danger');
      cameraCard.classList.add(`status-${severity}`);
    }

    // Faults Counter & Bar
    if (faultsCountEl) {
      faultsCountEl.innerText = `${faults} / ${maxFaults}`;
    }

    if (faultsBar) {
      const pct = Math.min(100, Math.round((faults / maxFaults) * 100));
      faultsBar.style.width = `${pct}%`;
      faultsBar.className = 'faults-bar-fill';
      if (pct >= 70) {
        faultsBar.classList.add('crit');
      } else if (pct >= 30) {
        faultsBar.classList.add('warn');
      }
    }

    // Violation Trigger & Sound
    if (status !== 'Face OK') {
      if (status !== lastViolationReason) {
        lastViolationReason = status;
        playAlertBeep(severity === 'danger');
        showToast(`Proctor Warning: ${status}`, severity === 'danger' ? 'danger' : 'warn');
      }
      if (tickerText) {
        tickerText.innerText = `[${new Date().toLocaleTimeString()}] Warning: ${status}`;
      }
    } else {
      lastViolationReason = "";
      if (tickerText && faults === 0) {
        tickerText.innerText = 'Monitoring active: No violations registered.';
      }
    }
  }

  function handleMaxFaultsReached() {
    examRunning = false;
    if (autoSubmitModal) {
      autoSubmitModal.classList.add('active');
    }
    let countdown = 4;
    const countdownEl = document.getElementById('autoSubmitCountdown');
    const interval = setInterval(() => {
      countdown -= 1;
      if (countdownEl) countdownEl.innerText = countdown;
      if (countdown <= 0) {
        clearInterval(interval);
        examForm.submit();
      }
    }, 1000);
  }

  // ==========================================
  // Question Navigation & Form Controls
  // ==========================================
  function showQuestion(index) {
    if (index < 0 || index >= totalQuestions) return;
    currentQIndex = index;

    // Hide all question panels and show active
    questionPanels.forEach((p, idx) => {
      p.classList.toggle('active', idx === index);
    });

    // Update Palette Buttons
    updatePaletteDisplay();

    // Enable / Disable Prev & Next buttons
    const prevBtn = document.getElementById('prevQuestionBtn');
    const nextBtn = document.getElementById('nextQuestionBtn');
    if (prevBtn) prevBtn.disabled = (index === 0);
    if (nextBtn) {
      if (index === totalQuestions - 1) {
        nextBtn.innerHTML = `Review Complete <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
      } else {
        nextBtn.innerHTML = `Save & Next <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>`;
      }
    }

    // Update "Mark for Review" button style for current question
    const reviewBtn = document.getElementById('markReviewBtn');
    if (reviewBtn) {
      if (markedForReview.has(index)) {
        reviewBtn.classList.add('marked');
        reviewBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg> Marked for Review`;
      } else {
        reviewBtn.classList.remove('marked');
        reviewBtn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg> Mark for Review`;
      }
    }
  }

  function getAnsweredCount() {
    let count = 0;
    questionPanels.forEach((panel) => {
      const selected = panel.querySelector('input[type="radio"]:checked');
      if (selected) count++;
    });
    return count;
  }

  function updatePaletteDisplay() {
    let answeredCount = 0;

    paletteButtons.forEach((btn) => {
      const qIdx = parseInt(btn.getAttribute('data-qindex'), 10);
      const panel = questionPanels[qIdx];
      const selectedRadio = panel ? panel.querySelector('input[type="radio"]:checked') : null;

      btn.classList.remove('current', 'answered', 'review');

      if (selectedRadio) {
        answeredCount++;
        btn.classList.add('answered');
      }

      if (markedForReview.has(qIdx)) {
        btn.classList.add('review');
      }

      if (qIdx === currentQIndex) {
        btn.classList.add('current');
      }
    });

    // Update Progress bar & badge
    if (answeredProgressFill) {
      const pct = Math.round((answeredCount / totalQuestions) * 100);
      answeredProgressFill.style.width = `${pct}%`;
    }
    if (answeredBadge) {
      answeredBadge.innerText = `${answeredCount} / ${totalQuestions} Answered`;
    }
  }

  // Option Card selection binding
  document.querySelectorAll('.option-card').forEach((card) => {
    card.addEventListener('click', function (e) {
      const radio = this.querySelector('input[type="radio"]');
      if (!radio) return;

      radio.checked = true;

      // Update styling inside the current question panel
      const parentPanel = this.closest('.question-panel');
      if (parentPanel) {
        parentPanel.querySelectorAll('.option-card').forEach((c) => c.classList.remove('selected'));
        this.classList.add('selected');
      }

      updatePaletteDisplay();
    });
  });

  // Palette button direct clicks
  paletteButtons.forEach((btn) => {
    btn.addEventListener('click', function () {
      const qIdx = parseInt(this.getAttribute('data-qindex'), 10);
      showQuestion(qIdx);
    });
  });

  // Previous & Next navigation buttons
  const prevBtn = document.getElementById('prevQuestionBtn');
  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      if (currentQIndex > 0) showQuestion(currentQIndex - 1);
    });
  }

  const nextBtn = document.getElementById('nextQuestionBtn');
  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (currentQIndex < totalQuestions - 1) {
        showQuestion(currentQIndex + 1);
      } else {
        openSubmitModal();
      }
    });
  }

  // Clear Response Button
  const clearBtn = document.getElementById('clearResponseBtn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      const activePanel = questionPanels[currentQIndex];
      if (activePanel) {
        activePanel.querySelectorAll('input[type="radio"]').forEach((r) => (r.checked = false));
        activePanel.querySelectorAll('.option-card').forEach((c) => c.classList.remove('selected'));
        updatePaletteDisplay();
        showToast('Selection cleared for this question', 'info');
      }
    });
  }

  // Mark for Review Button
  const reviewBtn = document.getElementById('markReviewBtn');
  if (reviewBtn) {
    reviewBtn.addEventListener('click', () => {
      if (markedForReview.has(currentQIndex)) {
        markedForReview.delete(currentQIndex);
      } else {
        markedForReview.add(currentQIndex);
      }
      showQuestion(currentQIndex);
    });
  }

  // ==========================================
  // Submit Confirmation Modal
  // ==========================================
  function openSubmitModal() {
    const answered = getAnsweredCount();
    const unanswered = totalQuestions - answered;
    if (confirmSummaryText) {
      confirmSummaryText.innerHTML = `
        You have answered <b>${answered}</b> out of <b>${totalQuestions}</b> questions.
        ${unanswered > 0 ? `<br><span style="color:#ef4444; font-weight:600">Note: ${unanswered} question(s) remain unanswered!</span>` : ''}
      `;
    }
    if (confirmModal) confirmModal.classList.add('active');
  }

  const triggerFinishBtns = document.querySelectorAll('.trigger-finish-exam');
  triggerFinishBtns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      openSubmitModal();
    });
  });

  if (cancelSubmitBtn) {
    cancelSubmitBtn.addEventListener('click', () => {
      if (confirmModal) confirmModal.classList.remove('active');
    });
  }

  if (finalSubmitBtn) {
    finalSubmitBtn.addEventListener('click', () => {
      examRunning = false;
      examForm.submit();
    });
  }

  // ==========================================
  // Tab Switch & Visibility Change Detection
  // ==========================================
  document.addEventListener('visibilitychange', () => {
    if (!examRunning) return;
    if (document.hidden) {
      handleTabSwitchViolation('Tab switch or window minimized detected!');
    }
  });

  window.addEventListener('blur', () => {
    if (!examRunning) return;
    handleTabSwitchViolation('Window lost focus!');
  });

  function handleTabSwitchViolation(reason) {
    tabSwitchCount++;
    playAlertBeep(true);
    showToast(`⚠️ Security Alert: ${reason}`, 'danger');
    if (tabWarningModal) {
      tabWarningModal.classList.add('active');
    }
    if (tickerText) {
      tickerText.innerText = `[${new Date().toLocaleTimeString()}] Violation: ${reason}`;
    }
  }

  if (dismissTabWarnBtn) {
    dismissTabWarnBtn.addEventListener('click', () => {
      if (tabWarningModal) tabWarningModal.classList.remove('active');
    });
  }

  // ==========================================
  // Fullscreen Helper
  // ==========================================
  const fullscreenToggleBtn = document.getElementById('fullscreenToggleBtn');
  if (fullscreenToggleBtn) {
    fullscreenToggleBtn.addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch((err) => {
          console.warn('Fullscreen request failed:', err);
        });
        fullscreenToggleBtn.title = 'Exit Fullscreen';
      } else {
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
        fullscreenToggleBtn.title = 'Enter Fullscreen';
      }
    });
  }

  // ==========================================
  // Live Countdown Timer (15 Minutes)
  // ==========================================
  let totalSeconds = 15 * 60; // 15 mins default
  function startTimer() {
    const timerInterval = setInterval(() => {
      if (!examRunning) {
        clearInterval(timerInterval);
        return;
      }
      totalSeconds -= 1;
      if (totalSeconds <= 0) {
        clearInterval(timerInterval);
        showToast('Time is up! Submitting examination...', 'warn');
        examForm.submit();
        return;
      }

      const mins = Math.floor(totalSeconds / 60);
      const secs = totalSeconds % 60;
      const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

      if (timerDisplay) {
        timerDisplay.innerText = formatted;
        if (totalSeconds <= 120) {
          timerDisplay.className = 'timer-display timer-danger';
        } else if (totalSeconds <= 300) {
          timerDisplay.className = 'timer-display timer-warning';
        }
      }
    }, 1000);
  }

  // ==========================================
  // Start Exam Trigger (From Calibration Modal)
  // ==========================================
  if (startExamBtn) {
    startExamBtn.addEventListener('click', () => {
      if (welcomeModal) welcomeModal.classList.remove('active');
      examRunning = true;
      startWebcam();
      startTimer();
      showQuestion(0);
    });
  } else {
    // Fallback if modal omitted
    examRunning = true;
    startWebcam();
    startTimer();
    showQuestion(0);
  }

  // Show calibration modal on initial page load
  if (welcomeModal) {
    welcomeModal.classList.add('active');
  }
})();
