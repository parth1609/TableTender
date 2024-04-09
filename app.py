import streamlit as st
import google.generativeai as genai

st.title("TableTender")

genai.configure(api_key=st.secrets["SECRET_KEY"])

# Select the model
model = genai.GenerativeModel('gemini-pro')

# Initialize chat history
if "context" not in st.session_state:
  st.session_state.context = [{
      "role":
      "user",
      "content":
      """You are restaurant OrderBOt , Your Name IS 'TableTender'. An automated service to collect orders for a pizza restaurant. \ 
    You first greet the customer, then collects the order, \
    and then asks if it's a pickup or delivery. \
    You wait to collect the entire order, then summarize it and check for a final \
    time if the customer wants to add anything else. \
    If it's a delivery, you ask for an address. \
    Finally you collect the payment.\
    Make sure to clarify all options, extras and sizes to uniquely \
    identify the item from the menu.\
    You respond in a short, very conversational friendly style. \
    \
    The menu includes \
    pepperoni pizza 12.95, 10.00, 7.00 \
    cheese pizza  10.95, 9.25, 6.50 \
    eggplant pizza  11.95, 9.75, 6.75 \
    fries 4.50, 3.50 \
    greek salad 7.25 \
    Toppings: \
    extra cheese 2.00, \
    mushrooms 1.50 \
    sausage 3.00 \
    canadian bacon 3.50 \
    AI sauce 1.50 \
    peppers 1.00 \
    Drinks: \
    coke 3.00, 2.00, 1.00 \
    sprite 3.00, 2.00, 1.00 \
    bottled water 5.00\
    
    """
  }]

# Display chat context from history on app rerun
for message in st.session_state.context:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])


# Process and store Query and Response
def llm_function(usr_msg):
  # Append user message to the context
  st.session_state.context.append({"role": "user", "content": usr_msg})

  # Prepare the input string with context for the model
  input_with_context = " ".join(
      [message["content"] for message in st.session_state.context])

  # Generate the system response using the model
  response = model.generate_content(input_with_context)

  # Displaying the system Message
  with st.chat_message("system"):
    st.markdown(response.text)

  # Storing the system response
  st.session_state.context.append({"role": "system", "content": response.text})


# Accept user input
usr_msg = st.chat_input("What's up?")

# Calling the Function when Input is Provided
if usr_msg:
  # Displaying the User Message
  with st.chat_message("user"):
    st.markdown(usr_msg)

  llm_function(usr_msg)
