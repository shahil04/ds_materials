chrome.runtime.onInstalled.addListener(() => {

chrome.storage.local.set({
scrapedData: [],
isScraping:false
})

console.log("Trainer Scraper Installed")

})