document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const clearBtn = document.getElementById('clearBtn');
    const statusDiv = document.getElementById('status');
    const startIdInput = document.getElementById('startId');
    const endIdInput = document.getElementById('endId');

    // Function to update the popup status text
    function updateStatus() {
        chrome.storage.local.get(['scrapedData', 'isScraping', 'currentId', 'endId'], (result) => {
            const count = result.scrapedData ? result.scrapedData.length : 0;
            if (result.isScraping) {
                statusDiv.innerHTML = `⏳ Scanning ID: ${result.currentId} (Target: ${result.endId})<br><br>✅ Saved: <b>${count}</b> profiles`;
                startBtn.disabled = true;
            } else {
                statusDiv.innerHTML = `✅ Ready.<br>Total saved profiles: <b>${count}</b>`;
                startBtn.disabled = false;
            }
        });
    }

    updateStatus();
    setInterval(updateStatus, 1000);

    // Start scraping button
    startBtn.addEventListener('click', () => {
        const startId = parseInt(startIdInput.value, 10);
        const endId = parseInt(endIdInput.value, 10);

        if (!startId || !endId || startId > endId) {
            alert("Please enter a valid start and end ID (Start must be less than or equal to End).");
            return;
        }

        chrome.storage.local.set({
            isScraping: true,
            currentId: startId,
            endId: endId
        }, () => {
            // Initiate the very first page navigation
            const firstUrl = `https://pulse.itvedant.com/student/update?id=${startId}`;

            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                if (tabs.length > 0) {
                    chrome.tabs.update(tabs[0].id, { url: firstUrl });
                } else {
                    chrome.tabs.create({ url: firstUrl });
                }
            });
        });
    });

    // Download CSV button
    downloadBtn.addEventListener('click', () => {
        chrome.storage.local.get(['scrapedData'], (result) => {
            const data = result.scrapedData || [];
            if (data.length === 0) {
                alert("No data available to download! Please scrape some profiles first.");
                return;
            }

            const headers = [
                "ID", "Name", "Phone", "Email", "Resume", "Branch",
                "Enrollment Branch", "Placement", "Package", "Batch",
                "Admission Date", "Relationship Manager", "Alternate Number",
                "Date of Birth", "Qualification", "College Name", "Gender"
            ];

            const csvRows = [headers.join(',')];

            for (const row of data) {
                const values = [
                    `"${(row.id || '').toString().replace(/"/g, '""')}"`,
                    `"${(row.name || '').replace(/"/g, '""')}"`,
                    `"${(row.phone || '').replace(/"/g, '""')}"`,
                    `"${(row.email || '').replace(/"/g, '""')}"`,
                    `"${(row.resume || '').replace(/"/g, '""')}"`,
                    `"${(row.branch || '').replace(/"/g, '""')}"`,
                    `"${(row.enrollment_branch || '').replace(/"/g, '""')}"`,
                    `"${(row.placement || '').replace(/"/g, '""')}"`,
                    `"${(row.package || '').replace(/"/g, '""')}"`,
                    `"${(row.batch || '').replace(/"/g, '""')}"`,
                    `"${(row.admission_date || '').replace(/"/g, '""')}"`,
                    `"${(row.rm || '').replace(/"/g, '""')}"`,
                    `"${(row.alt_phone || '').replace(/"/g, '""')}"`,
                    `"${(row.dob || '').replace(/"/g, '""')}"`,
                    `"${(row.qualification || '').replace(/"/g, '""')}"`,
                    `"${(row.college || '').replace(/"/g, '""')}"`,
                    `"${(row.gender || '').replace(/"/g, '""')}"`
                ];
                csvRows.push(values.join(','));
            }

            const csvString = csvRows.join('\n');
            const blob = new Blob([csvString], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);

            chrome.downloads.download({
                url: url,
                filename: `student_profiles_${Date.now()}.csv`,
                saveAs: true
            });
        });
    });

    // Clear Data button
    clearBtn.addEventListener('click', () => {
        if (confirm("Are you sure you want to delete all scraped data?")) {
            chrome.storage.local.set({ scrapedData: [], isScraping: false }, () => {
                updateStatus();
            });
        }
    });
});
