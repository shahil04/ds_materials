document.getElementById("start").onclick = async () => {

    const start = parseInt(document.getElementById("startId").value);
    const end = parseInt(document.getElementById("endId").value);

    chrome.runtime.sendMessage({
        action: "startScraping",
        start,
        end
    });

};

document.getElementById("download").onclick = () => {
    chrome.runtime.sendMessage({
        action: "downloadCSV"
    });
};