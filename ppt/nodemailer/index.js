const http = require("http");
const nodemailer = require("nodemailer");
const recipients = require("./mails"); // import recipients

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

    // Function to send emails to each recipient
    const sendEmailToRecipient = (recipientIndex) => {
        if (recipientIndex >= recipients.length) {
            console.log("All emails sent!");
            response.end("All emails sent!");
            return;
        }

        const recipient = recipients[recipientIndex];

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
                    filename: "Shahil_Resume.pdf",
                    path: "Shahil_Resume.pdf",
                    contentType: "application/pdf"
                }
            ]
        };

        auth.sendMail(receiver, (error) => {
            if (error) {
                console.error(`Error sending email to ${recipient}: ${error}`);
                return;
            }
            console.log(`Email sent to ${recipient}`);
            sendEmailToRecipient(recipientIndex + 1);
        });
    };

    sendEmailToRecipient(0);
});

server.listen(8080, () => {
    console.log("Server running on port 8080");
});
