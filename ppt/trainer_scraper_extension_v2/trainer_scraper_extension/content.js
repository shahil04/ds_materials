window.addEventListener('load', () => {

chrome.storage.local.get(
['isScraping','targetIds','idsScraped','scrapedData'],
(result)=>{

if(result.isScraping){

scrapeTrainer(result)

}

})

})

function scrapeTrainer(state){

const currentIdIndex = state.idsScraped

const ids = state.targetIds

const currentId = ids[currentIdIndex]

console.log("Scraping trainer id:",currentId)

setTimeout(()=>{

const data = extractTrainer()

if(data){

let currentData = state.scrapedData || []

currentData.push(data)

chrome.storage.local.set({

scrapedData:currentData,
idsScraped:currentIdIndex+1

},()=>{

if(currentIdIndex+1 < ids.length){

let nextId = ids[currentIdIndex+1]

window.location.href =
`https://pulse.itvedant.com/trainer-metadata/view?id=${nextId}`

}
else{

finishScraping(true)

}

})

}

},2500)

}

function extractTrainer(){

function getValue(label){

const details = document.querySelectorAll(".detail")

for(let d of details){

const labelText =
d.querySelector("p:last-child")?.innerText?.trim()

if(labelText===label){

return d.querySelector(".item-value")?.innerText?.trim() || ""

}

}

return ""

}

function getBadges(label){

const details = document.querySelectorAll(".detail")

for(let d of details){

const labelText =
d.querySelector("p:first-child")?.innerText?.trim()

if(labelText===label){

return [...d.querySelectorAll(".badge")]
.map(x=>x.innerText.trim())
.join("|")

}

}

return ""

}

return{

employee_code:getValue("Employee Code"),
employee_name:getValue("Employee Name"),
email:getValue("Employee Email"),
official_number:getValue("Official Number"),
emergency_number:getValue("Emergency Number"),
joining_date:getValue("Joining Date"),
branch:getValue("Branch"),
cost_per_hour:getValue("Cost (Per Hour)"),
availability:getBadges("Availibility"),
teaching_mode:getBadges("Teaching Mode"),
time_slots:getBadges("Time Slots"),
technologies:getBadges("Technologies"),

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

function finishScraping(success=false){

chrome.storage.local.set({isScraping:false},()=>{

if(success){

alert("Trainer scraping completed! Download CSV from extension.")

}

})

}