import streamlit as st
import requests

# Title
st.title("🤝 Your Personal Assistant")

# Subheader
st.subheader("What can your personal assistant do?")

st.markdown("""
1. Answer questions on various topics  
2. Arrange calendar events and meetings  
3. Read your emails and summarize them  
4. Manage your tasks and to-do lists  
5. Take quick notes  
6. Track expenses and budgeting
""")

# Chat section
st.subheader("💬 Chat with your assistant")

# Create session history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_message = st.chat_input("Ask something...")

# If user sends message
if user_message:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        # Send message to n8n webhook
        response = requests.post(
            "http://n8n:5678/webhook/ca968cc8-de39-4aca-bdc4-ded7e58d1f36",
            json={"message": user_message},
            timeout=30
        )

        # Convert response
        data = response.json()

        # Extract AI response
        if isinstance(data, list) and len(data) > 0:
            ai_response = data[0].get("output", "No response returned")
        else:
            ai_response = "Unexpected response format"

    except requests.exceptions.RequestException as e:
        ai_response = f"Connection error: {e}"

    except ValueError:
        ai_response = f"Invalid JSON response: {response.text}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(ai_response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })







# import streamlit as st
# import requests

# # create the title for the page
# st.title("🤝 Your Personal Assistant")

# # add subheader
# st.subheader("What can your personal assistant do?")

# # create a list of what your assistant can do
# st.markdown("""
#             1. Answer questions on various topics.   
#             2. Arrange Calendar events and meetings.  
#             3. Read your emails and send replies, can even summarize them for you.
#             4. Manage your tasks and to-do lists.
#             5. Take quick notes for you.
#             6. Track your expenses and budgeting.
#             """)

# # add chats subheader
# st.subheader("💬 Chat with your assistant")

# # create a session state for message history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # show the messages in chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # create a chat input box
# user_message = st.chat_input()

      
# # if user sends a message
# if user_message:
#     with st.chat_message("user"):
#         st.markdown(user_message)
#         # append the user message to message history
#         st.session_state.messages.append({"role": "user", "content": user_message})
    
#     # send the user message to the n8n webhook
#     response = requests.post(
#         "http://n8n:5678/webhook/ca968cc8-de39-4aca-bdc4-ded7e58d1f36",  # replace with your n8n webhook URL
#         json={"message": user_message}
#     )
    
#     # get the AI response from webhook
#     ai_response = response.json()[0]["output"]
    
#     # display the AI response in chat
#     with st.chat_message("assistant"):
#         st.markdown(ai_response)
#         # append the AI response to message history
#         st.session_state.messages.append({"role": "assistant", "content": ai_response})