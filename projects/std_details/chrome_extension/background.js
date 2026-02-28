// background.js

// Initialize storage when the extension is installed or updated
chrome.runtime.onInstalled.addListener(() => {
    chrome.storage.local.set({ scrapedData: [], isScraping: false });
    console.log("Student Details Scraper Extension Installed!");
});
