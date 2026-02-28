// Wait for the page to fully load
window.addEventListener('load', () => {
    // Check if scraping is currently active
    chrome.storage.local.get(['isScraping', 'targetPages', 'pagesScraped', 'scrapedData'], (result) => {
        if (result.isScraping) {
            scrapeCurrentPage(result);
        }
    });
});

function scrapeCurrentPage(state) {
    const currentPageNum = state.pagesScraped + 1;
    console.log(`[Student Scraper Extension] Scraping page ${currentPageNum} of ${state.targetPages}`);

    // Slight delay (2.5 seconds) to ensure dynamic table content is rendered
    setTimeout(() => {
        const rows = document.querySelectorAll("table.table-bordered tbody tr");
        if (rows.length === 0) {
            console.log("[Student Scraper Extension] No table rows found, stopping.");
            finishScraping();
            return;
        }

        let newData = [];
        rows.forEach(row => {
            try {
                // Name string parsing
                let name = "";
                const nameEl = row.querySelector("td.fullname_column h5");
                if (nameEl) {
                    // Extract name and strip possible premium icons / labels
                    name = nameEl.innerText.replace("premium", "").replace(/[\n\r]/g, " ").trim();
                }

                // Phone extraction
                let phone = "";
                const phoneEl = row.querySelector("td.fullname_column p");
                if (phoneEl) {
                    phone = phoneEl.innerText.trim();
                }

                // Branch / College Location
                let branch = "";
                const branchEl = row.querySelector("td.branch_column");
                if (branchEl) {
                    branch = branchEl.innerText.trim();
                }

                // Courses / Degree extraction
                let courses = "";
                const courseEls = row.querySelectorAll("td.courses_column ul li");
                if (courseEls.length > 0) {
                    let courseList = [];
                    courseEls.forEach(li => {
                        const text = li.innerText.trim();
                        // Ignore the "Show More..." / "Show Less..." buttons
                        if (text && text !== "Show More..." && text !== "Show Less...") {
                            courseList.push(text);
                        }
                    });
                    courses = courseList.join(" | ");
                }

                if (name || phone) {
                    newData.push({ name, phone, branch, courses });
                }
            } catch (e) {
                console.error("[Student Scraper Extension] Error scraping row", e);
            }
        });

        console.log(`[Student Scraper Extension] Succeeded extracting ${newData.length} rows.`);

        // Merge newly scraped data with existing data
        const currentData = state.scrapedData || [];
        const mergedData = currentData.concat(newData);

        const newPagesScraped = state.pagesScraped + 1;

        chrome.storage.local.set({ scrapedData: mergedData, pagesScraped: newPagesScraped }, () => {
            // Check if we have more pages left to scrape
            if (newPagesScraped < state.targetPages) {
                // Dynamically navigate to the next page
                let currentUrl = window.location.href;
                let urlObj = new URL(currentUrl);

                // Get current 'page' parameter if it exists, default to 1 (or matching the original page logic)
                let currentPageParam = urlObj.searchParams.get('page');
                let currentPageNumActual = currentPageParam ? parseInt(currentPageParam, 10) : 1;
                let nextPageIndexActual = currentPageNumActual + 1;

                // Set the incremented page parameter
                urlObj.searchParams.set('page', nextPageIndexActual);

                const nextUrl = urlObj.toString();
                console.log(`[Student Scraper Extension] Navigating to next page: ${nextUrl}`);
                window.location.href = nextUrl;
            } else {
                // Target pages reached
                finishScraping(true);
            }
        });
    }, 2500); // Wait 2.5 seconds per page iteration
}

function finishScraping(success = false) {
    chrome.storage.local.set({ isScraping: false }, () => {
        if (success) {
            alert("Scraping completed! Open the extension popup to download your CSV data.");
        }
    });
}
