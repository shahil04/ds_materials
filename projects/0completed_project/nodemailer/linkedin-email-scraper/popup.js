document.getElementById("scrapeBtn").addEventListener("click", () => {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.scripting.executeScript(
            {
                target: { tabId: tabs[0].id },
                function: scrapeEmails,
            },
            (results) => {
                const emails = results[0].result;
                document.getElementById("results").value = emails.join("\n");
            }
        );
    });
});

function scrapeEmails() {
    let content = document.body.innerHTML;
    const emailPattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,7}/g;
    const emailAddresses = content.match(emailPattern) || [];
    let unique = new Set(emailAddresses);
    return [...unique];
}

// Copy button
document.getElementById("copyBtn").addEventListener("click", () => {
    const text = document.getElementById("results");
    text.select();
    document.execCommand("copy");
});

// Download CSV
document.getElementById("downloadBtn").addEventListener("click", () => {
    const emails = document.getElementById("results").value;
    const blob = new Blob([emails], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "mails.csv";
    a.click();

    URL.revokeObjectURL(url);
});