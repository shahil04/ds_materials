

// let content =
// document.querySelector('body').innerHTML;
// const emailPattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,7}/g;
// const emailAddresses = content.match(emailPattern) || [];
// let unique = new Set(emailAddresses);
// let email = [...unique];
// console.log(email);


const http = require("http");
const nodemailer = require("nodemailer");

const server = http.createServer((request, response) => {
    const auth = nodemailer.createTransport({
        service: "gmail",
        secure: true,
        port: 465,
        auth: {
            user: "maarish441@gmail.com",
            pass: "doav dxnm mpeg jupv"
        }
    });
    

 
    const recipients = [
        'ingale.su@talentxo.co', 
        'anil@techsarasolutions.com', 
        'ahil.prashanth@shadowfax.in', 
        'communication@probo.com'
    ];
    
    

    // Function to send emails to each recipient
    const sendEmailToRecipient = (recipientIndex) => {
        if (recipientIndex >= recipients.length) {
            console.log("All emails sent!");
            response.end();
            return;
        }

        const recipient = recipients[recipientIndex];
        if (!recipient) {
            console.log(`Invalid recipient at index ${recipientIndex}`);
            sendEmailToRecipient(recipientIndex + 1); // Skip invalid email
            return;
        }

        const receiver = {
            from: "easy4solution1@gmail.com",
            to: recipient,
            subject: "Application for Data Science Position",
            text: `Dear Hiring Manager,
    
I am excited to apply for the Data Scientist position at your organization. With hands-on experience in Python, SQL, Power BI, Machine Learning, and tools like Pandas, scikit-learn, Flask, and Streamlit,
I have led several end-to-end data science projects and trained over 200 students in core analytics skills.

Please find my resume attached for your review.
I look forward to the opportunity to contribute to your data-driven team.

Thank you for your time and consideration.

Sincerely, 
MD Shahil Ansari
mohammadshahil4u@gmail.com | +91 9708549289
`,
            attachments: [
                {
                    filename: "Resume.pdf", // Name of your PDF file in the project directory
                    path: "Resume.pdf", // Directly use the file name if it's in the same directory
                    contentType: "application/pdf" // Content type for PDF
                }
            ]
        };

        auth.sendMail(receiver, (error, emailResponse) => {
            if (error) {
                console.error(`Error sending email to ${recipient}: ${error}`);
                throw error;
            }
            console.log(`Email sent to ${recipient}`);
            sendEmailToRecipient(recipientIndex + 1); // Move to the next recipient
        });
    };

    sendEmailToRecipient(0); // Start the loop from the first recipient
});

server.listen(8080);







// const http = require("http");
// const nodemailer = require("nodemailer");

// const server = http.createServer((request, response) => {
//     const auth = nodemailer.createTransport({
//         service: "gmail",
//         secure: true,
//         port: 465,
//         auth: {
//             user: "maarish441@gmail.com",
//             pass: "doav dxnm mpeg jupv"
//         }
//     });

//     const recipients = [
//         "careers.india@tnpconsultants.com",
//         "monica.sharma@ltimindtree.com",
//         "sapna.purohit@we3.tech",
//         "hr@openxcell.com",
//         "athulyad@spanidea.com",
//         "shwetaz@zimetrics.com",
//         "swetha.sv@resourcetree.co.in",
//         "diamondhr2015@gmail.com",
//         "diksha.tiwari@infogain.com",
//         "himanshu@dmsvisions.com",
//         "Sakshi.bansal@codersbrain.com",
//         "greeshma.velivela@quesscorp.com",
//         "aishwarya.p@twsol.com",
//         "amitsaini615@gmail.com",
//         "Shannon@openkyber.com",
//         "nayan@sidinformation.com",
//         "nithya@sanengineeringsolutions.com",
//         "charvi.srivastava@techmahindra.com",
//         "taikhums@mindlance.com",
//         "sravani.k@valuesoftinfo.com",
//         "shradha.a@growelsoftech.com",
//         "nkaran@datamaxis.net",
//         "sumanth.vm@teamlease.com",
//         "dipali.polkade@eclerx.com",
//         "arunarani@vysystems.com"
//     ];
    
    
    
//     // Function to send emails to each recipient
//     const sendEmailToRecipient = (recipientIndex) => {
//         if (recipientIndex >= recipients.length) {
//             console.log("All emails sent!");
//             response.end("All emails sent!");
//             return;
//         }

//         const recipient = recipients[recipientIndex];
//         if (!recipient) {
//             console.log(`Invalid recipient at index ${recipientIndex}`);
//             sendEmailToRecipient(recipientIndex + 1); // Skip invalid email
//             return;
//         }

//         const receiver = {
//             from: "maarish441@gmail.com",
//             to: recipient,
//             subject: "Application for Data Analyst Position",
//             text: `Dear Hiring Manager,
    
// I am excited to apply for the Data Analyst position at your organization. With expertise in data science, analytics, and training, I am eager to contribute my skills to your team.
    
// As a Data Analyst Trainer, I design and deliver programs on Python, SQL, and data visualization, helping individuals build analytical capabilities. Additionally, I have worked on predictive modeling, machine learning, and data visualization projects, including a soil quality analysis system using Random Forest and Django, and an NLP-based duplicate question detection system.
    
// My proficiency in Python (pandas, NumPy, scikit-learn), SQL, Tableau, and Streamlit, along with my ability to translate data into actionable insights, aligns well with your organization’s data-driven approach.
    
// I welcome the opportunity to discuss how my skills can benefit your team. Thank you for your time and consideration.
    
// Sincerely,
// Mohammad Aarish`,
//             attachments: [
//                 {
//                     filename: "Resume.pdf", // Name of your PDF file in the project directory
//                     path: "Resume.pdf", // Directly use the file name if it's in the same directory
//                     contentType: "application/pdf" // Content type for PDF
//                 }
//             ]
//         };

//         auth.sendMail(receiver, (error, emailResponse) => {
//             if (error) {
//                 console.error(`Error sending email to ${recipient}: ${error}`);
//                 response.end(`Error sending email to ${recipient}: ${error}`);
//                 return;
//             }
//             console.log(`Email sent to ${recipient}`);
//             sendEmailToRecipient(recipientIndex + 1); // Move to the next recipient
//         });
//     };

//     sendEmailToRecipient(0); // Start the loop from the first recipient
// });

// server.listen(8080, () => {
//     console.log("Server is listening on port 8080");
// });
