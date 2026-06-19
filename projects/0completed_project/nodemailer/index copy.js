const http = require("http");
const nodemailer = require("nodemailer");

const server = http.createServer((request, response) => {
    const auth = nodemailer.createTransport({
        service: "gmail",
        secure: true,
        port: 465,
        auth: {
            user: "mohammadshahil4u@gmail.com",
            pass: "frim jsfm nwwu lhyj"
        }
    });
    

 
const recipients = [
    "abhishek.m@livecjobs.com",
    "shireesha@clouddatavision.com",
    "hiring@statglow.com",
    "vgarg1601994@gmail.com",
    "Nagendra@wavesoftsol.com",
    "tirtha.chovatia@bacancy.com",
    "karthikt@flairtechsolutions.com",
    "diligencetechnologieshyd@gmail.com",
    "pradeep.k@testyantra.co.uk",
    "nagesh@global-tech.co.in",
    "bhulakshmi@wavesoftsol.com",
    "pragya.srivastava@velocis.co.in",
    "navya@fusionhiretech.com",
    "mita.chatterjee@optimumdataanlytics.com",
    "lavanya@fusionhiretech.com",
    "esther.m@twsol.com",
    "pavankumar.s@vdartinc.com",
    "mathan@sstech-llc.com",
    "srigouri.d@trysol.co.in",
    "radhika@fusionhiretech.com",
    "a.aditi@anjusmriti.com",
    "shalu@voltoconsulting.com",
    "mohammad_a@tekwissen.com",
    "David@lakshya-tech.com",
    "vamsi@neurasol.com",
    "shweta@qchrservices.com",
    "rlodhi@sagaciousminds.com",
    "pritam.khaire@alignedautomation.com",
    "anjali@huquo.com",
    "Career@huquo.com",
    "Dipti.Chhugani@in.ey.com",
    "Saumya.Walia@in.ey.com",
    "shanmukh.siva@navasoftware.com",
    "kashish@huquo.com",
    "career@huquo.com",
    "priya@huquo.com"
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
            from: "mohammadshahil4u@gmail.com",
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
                    filename: "Shahil_Resume.pdf", // Name of your PDF file in the project directory
                    path: "Shahil_Resume.pdf", // Directly use the file name if it's in the same directory
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