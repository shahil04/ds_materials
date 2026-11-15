// Wait for the page to fully load
window.addEventListener('load', () => {
    // Check if scraping is currently active
    chrome.storage.local.get(['isScraping', 'currentId', 'endId', 'scrapedData'], (result) => {
        if (result.isScraping) {
            scrapeProfilePage(result);
        }
    });
});

function scrapeProfilePage(state) {
    console.log(`[Profile Scraper] Scanning ID ${state.currentId} of target ${state.endId}`);

    // Slight delay (2.5 seconds) to ensure dynamic card content is fully loaded
    setTimeout(() => {

        let studentData = { id: state.currentId };

        // The structure of the page has <p>Label Name</p> and just before it <span class="item-value">Value</span>
        // in most cases. Or inside the same parent div.

        function extractByLabel(labelText, fallback = "N/A") {
            try {
                // Find all <p> elements inside the card-body
                const pElements = Array.from(document.querySelectorAll("div.card-body p"));

                // Find the <p> that contains our exact label text
                const targetP = pElements.find(p => p.innerText.trim().toLowerCase() === labelText.toLowerCase());

                if (targetP) {
                    // Look at the parent element of this <p> (usually a div like col-lg-4 or col-lg-3)
                    const parentDiv = targetP.parentElement;

                    // Inside that parent div, find the item-value span
                    const valueSpan = parentDiv.querySelector(".item-value");

                    if (valueSpan) {
                        // Some spans just have text, some have anchor tags inside
                        // .innerText gets all visible text nicely
                        let textValue = valueSpan.innerText.trim();

                        // Clean up spacing and newlines
                        textValue = textValue.replace(/[\n\r]+/g, " ");

                        return textValue || fallback;
                    }
                }
            } catch (e) {
                console.error(`Error extracting ${labelText}`, e);
            }
            return fallback;
        }

        // Check if page loaded a valid profile (i.e., card-body exists and has data)
        const nameFallback = extractByLabel("Full Name", "");
        if (nameFallback || document.querySelector(".card-body")) {
            studentData.name = extractByLabel("Full Name", "N/A");
            studentData.phone = extractByLabel("Mobile", "N/A");
            studentData.email = extractByLabel("Email", "N/A");
            studentData.resume = extractByLabel("Resume", "N/A");
            studentData.branch = extractByLabel("Branch", "N/A");
            studentData.enrollment_branch = extractByLabel("Enrollment Branch", "N/A");
            studentData.placement = extractByLabel("Placement", "N/A");
            studentData.package = extractByLabel("Package", "N/A");
            studentData.batch = extractByLabel("Batch", "N/A");
            studentData.admission_date = extractByLabel("Admission Date", "N/A");
            studentData.rm = extractByLabel("Relationship Manager", "N/A");
            studentData.alt_phone = extractByLabel("Alternate Number", "N/A");
            studentData.dob = extractByLabel("Date of Birth", "N/A");
            studentData.qualification = extractByLabel("Qualification", "N/A");
            studentData.college = extractByLabel("College Name", "N/A");
            studentData.gender = extractByLabel("Gender", "N/A");
            studentData.address = extractByLabel("Address", "N/A");

            console.log(`[Profile Scraper] Succeeded extracting data for ID: ${state.currentId}`);
        } else {
            console.log(`[Profile Scraper] Warning: ID ${state.currentId} did not render a valid profile.`);
        }

        // Merge newly scraped data
        const currentData = state.scrapedData || [];
        // Push anyway so we maintain ID sequences, or only push if valid
        currentData.push(studentData);

        const nextId = state.currentId + 1;

        chrome.storage.local.set({ scrapedData: currentData }, () => {
            // Check if we have more IDs left to scrape
            if (nextId <= state.endId) {
                chrome.storage.local.set({ currentId: nextId }, () => {
                    // Navigate to the next ID
                    const nextUrl = `https://pulse.itvedant.com/student/update?id=${nextId}`;
                    console.log(`[Profile Scraper] Navigating to next profile: ${nextUrl}`);
                    window.location.href = nextUrl;
                });
            } else {
                // Target ID reached
                finishScraping(true);
            }
        });
    }, 2500); // 2.5 seconds per profile iteration
}

function finishScraping(success = false) {
    chrome.storage.local.set({ isScraping: false }, () => {
        if (success) {
            alert("Profile Scraping completed! Open the extension popup to download your CSV data.");
        }
    });
}
