

let content =
document.querySelector('body').innerHTML;
const emailPattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,7}/g;
const emailAddresses = content.match(emailPattern) || [];
let unique = new Set(emailAddresses);
let email = [...unique];
console.log(email);
