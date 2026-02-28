document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const clearBtn = document.getElementById('clearBtn');
    const statusDiv = document.getElementById('status');
    const pagesInput = document.getElementById('pages');
    const urlInput = document.getElementById('customUrl');

    // Function to update the popup status text
    function updateStatus() {
        chrome.storage.local.get(['scrapedData', 'isScraping', 'pagesScraped', 'targetPages'], (result) => {
            const count = result.scrapedData ? result.scrapedData.length : 0;
            if (result.isScraping) {
                statusDiv.innerHTML = `⏳ Scraping Page ${result.pagesScraped + 1} of ${result.targetPages}...<br><br>✅ Saved: <b>${count}</b> students`;
                startBtn.disabled = true;
            } else {
                statusDiv.innerHTML = `✅ Ready.<br>Total saved: <b>${count}</b> students`;
                startBtn.disabled = false;
            }
        });
    }

    // Periodically update the status while the popup is open
    updateStatus();
    setInterval(updateStatus, 1000);

    // Start scraping button
    startBtn.addEventListener('click', () => {
        const pagesToScrape = parseInt(pagesInput.value, 10);
        const customUrl = urlInput.value.trim();

        if (!pagesToScrape || pagesToScrape < 1) {
            alert("Please enter a valid number of pages.");
            return;
        }

        chrome.storage.local.set({
            isScraping: true,
            targetPages: pagesToScrape,
            pagesScraped: 0
        }, () => {
            if (customUrl) {
                // If a custom URL is provided, open/update a tab with it
                chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                    if (tabs.length > 0) {
                        chrome.tabs.update(tabs[0].id, { url: customUrl });
                    } else {
                        chrome.tabs.create({ url: customUrl });
                    }
                });
            } else {
                // If no custom URL is provided, try to use the existing active tab Context
                chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                    if (tabs.length > 0) {
                        if (tabs[0].url.includes("pulse.itvedant.com")) {
                            // Reload current tab; logic inside content.js will trigger automatically
                            chrome.tabs.reload(tabs[0].id);
                        } else {
                            if (confirm("You are not on pulse.itvedant.com.\nClick OK to open the generic Active Learners page and begin scraping (Please ensure you are already logged in).")) {
                                const url = `http://pulse.itvedant.com/student/active-learners?page=1&per-page=10`;
                                chrome.tabs.create({ url: url });
                            } else {
                                // Cancel scraping if they didn't want to navigate
                                chrome.storage.local.set({ isScraping: false });
                            }
                        }
                    }
                });
            }
        });
    });

    // Download CSV button
    downloadBtn.addEventListener('click', () => {
        chrome.storage.local.get(['scrapedData'], (result) => {
            const data = result.scrapedData || [];
            if (data.length === 0) {
                alert("No data available to download! Please scrape some pages first.");
                return;
            }

            // Convert JSON array to CSV format
            const headers = ["Name", "Phone Number", "Branch", "Courses (Degree)"];
            const csvRows = [headers.join(',')];

            for (const row of data) {
                const values = [
                    `"${(row.name || '').replace(/"/g, '""')}"`,
                    `"${(row.phone || '').replace(/"/g, '""')}"`,
                    `"${(row.branch || '').replace(/"/g, '""')}"`,
                    `"${(row.courses || '').replace(/"/g, '""')}"`
                ];
                csvRows.push(values.join(','));
            }

            const csvString = csvRows.join('\n');
            const blob = new Blob([csvString], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);

            chrome.downloads.download({
                url: url,
                filename: 'student_details_extension.csv',
                saveAs: true
            });
        });
    });

    // Clear Data button
    clearBtn.addEventListener('click', () => {
        if (confirm("Are you sure you want to delete all scraped data from the extension's memory?")) {
            chrome.storage.local.set({ scrapedData: [], isScraping: false, pagesScraped: 0 }, () => {
                updateStatus();
            });
        }
    });
});
