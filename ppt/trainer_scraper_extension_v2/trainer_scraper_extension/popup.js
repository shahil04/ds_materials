document.addEventListener('DOMContentLoaded',()=>{

const startBtn=document.getElementById("startBtn")
const downloadBtn=document.getElementById("downloadBtn")
const startId=document.getElementById("startId")
const endId=document.getElementById("endId")

startBtn.addEventListener("click",()=>{

let start=parseInt(startId.value)
let end=parseInt(endId.value)

if(!start||!end){

alert("Enter valid ID range")

return

}

let ids=[]

for(let i=start;i<=end;i++){

ids.push(i)

}

chrome.storage.local.set({

isScraping:true,
targetIds:ids,
idsScraped:0

},()=>{

window.open(
`https://pulse.itvedant.com/trainer-metadata/view?id=${start}`
)

})

})

downloadBtn.addEventListener("click",()=>{

chrome.storage.local.get(['scrapedData'],(result)=>{

const data=result.scrapedData||[]

if(!data.length){

alert("No data scraped")

return

}

const headers=Object.keys(data[0])

let csv=[headers.join(",")]

data.forEach(row=>{

csv.push(
headers.map(h=>`"${row[h]||""}"`).join(",")
)

})

const blob=new Blob([csv.join("\n")],{type:"text/csv"})

const url=URL.createObjectURL(blob)

chrome.downloads.download({

url:url,
filename:"trainer_data.csv",
saveAs:true

})

})

})

})