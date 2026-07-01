import streamlit as st
import yagmail
import pandas as pd
import io
import tempfile

st.set_page_config(page_title="Bulk Email Sender", page_icon="📧")

st.title("📧 Bulk Email Sender")

# Sender credentials
sender = st.text_input("Your Gmail")
password = st.text_input("App Password", type="password")

# Subject and message
subject = st.text_input("Email Subject")
message = st.text_area("Custom Message")

# Upload files
email_file = st.file_uploader("Upload Email List (.txt or .csv)")
resume_file = st.file_uploader("Upload Resume (PDF)")

if st.button("Send Emails"):

    if not sender or not password:
        st.error("Please enter Gmail and App Password")

    elif not email_file or not resume_file:
        st.error("Please upload both email list and resume")

    else:
        try:
            # Read email list
            content = email_file.read().decode("utf-8")

            if email_file.name.endswith(".csv"):
                # Handle all CSV formats
                df = pd.read_csv(io.StringIO(content), header=None)
                recipients = []

                for col in df.columns:
                    recipients.extend(df[col].dropna().tolist())

                recipients = [email.strip() for email in recipients if email.strip()]
            else:
                recipients = [
                    email.strip()
                    for email in content.splitlines()
                    if email.strip()
                ]

            if len(recipients) == 0:
                st.error("No recipients found in file.")
                st.stop()

            st.write(f"Total recipients: {len(recipients)}")
            st.write("Recipients:", recipients)

            # # Save resume temporarily
            # with tempfile.NamedTemporaryFile(delete=False) as tmp:
            #     tmp.write(resume_file.read())
            #     resume_path = tmp.name
            # Save resume with correct filename
            temp_dir = tempfile.gettempdir()
            resume_path = f"{temp_dir}/{resume_file.name}"

            with open(resume_path, "wb") as f:
                f.write(resume_file.read())


            # Setup mail
            yag = yagmail.SMTP(user=sender, password=password)

            progress = st.progress(0)

            for i, recipient in enumerate(recipients):
                yag.send(
                    to=recipient,
                    subject=subject,
                    contents=message,
                    attachments=resume_path
                )

                progress.progress((i + 1) / len(recipients))
                st.write(f"Sent to: {recipient}")

            st.success("All emails sent successfully!")

        except Exception as e:
            st.error(f"Error: {str(e)}")
