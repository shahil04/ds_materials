let results = []

chrome.runtime.onMessage.addListener(async (msg)=>{

if(msg.action==="startScraping"){

results = []

for(let i=msg.start;i<=msg.end;i++){

let url = `https://pulse.itvedant.com/trainer-metadata/view?id=${i}`

let tab = await chrome.tabs.create({url, active:false})

await new Promise(r=>setTimeout(r,6000))

let response = await chrome.tabs.sendMessage(tab.id,{action:"scrape"})

if(response){

response.id = i

results.push(response)

}

chrome.tabs.remove(tab.id)

}

console.log(results)

}

if(msg.action==="downloadCSV"){

let csv = convertToCSV(results)

let blob = new Blob([csv],{type:"text/csv"})

let url = URL.createObjectURL(blob)

chrome.downloads.download({

url:url,

filename:"trainers.csv"

})

}

})

function convertToCSV(data){

if(!data.length) return ""

const header = Object.keys(data[0]).join(",")

const rows = data.map(o=>Object.values(o).join(","))

return [header,...rows].join("\n")

}