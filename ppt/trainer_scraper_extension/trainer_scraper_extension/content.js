function getValue(label){

    const details = document.querySelectorAll(".detail");

    for(let d of details){

        const labelText = d.querySelector("p:last-child")?.innerText?.trim();

        if(labelText === label){

            return d.querySelector(".item-value")?.innerText?.trim() || "";
        }
    }

    return ""
}

function getBadges(label){

    const details = document.querySelectorAll(".detail");

    for(let d of details){

        const labelText = d.querySelector("p:first-child")?.innerText?.trim();

        if(labelText === label){

            return [...d.querySelectorAll(".badge")]
                .map(x=>x.innerText.trim())
                .join("|")
        }
    }

    return ""
}

function getLedgerData(){

return {

ledger_name:
document.querySelector(".card-custom p")?.innerText || "",

debit_transactions:
document.querySelector("#total_num_tr_dr")?.innerText || "",

credit_transactions:
document.querySelector("#total_num_tr_cr")?.innerText || "",

total_debit_amount:
document.querySelector("#total_debit_atm")?.innerText || "",

total_credit_amount:
document.querySelector("#total_credit_amt")?.innerText || "",

balance:
document.querySelector("#balanec_amount_ladger")?.innerText || ""

}

}

function scrapeTrainer(){

const ledger = getLedgerData()

return {

employee_code: getValue("Employee Code"),

employee_name: getValue("Employee Name"),

email: getValue("Employee Email"),

official_number: getValue("Official Number"),

emergency_number: getValue("Emergency Number"),

joining_date: getValue("Joining Date"),

branch: getValue("Branch"),

cost_per_hour: getValue("Cost (Per Hour)"),

availability: getBadges("Availibility"),

teaching_mode: getBadges("Teaching Mode"),

time_slots: getBadges("Time Slots"),

technologies: getBadges("Technologies"),

ledger_name: ledger.ledger_name,

debit_transactions: ledger.debit_transactions,

credit_transactions: ledger.credit_transactions,

total_debit_amount: ledger.total_debit_amount,

total_credit_amount: ledger.total_credit_amount,

balance: ledger.balance

}

}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse)=>{

if(msg.action==="scrape"){

const data = scrapeTrainer()

sendResponse(data)

}

})