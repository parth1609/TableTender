
import streamlit as st
import google.generativeai as genai
from st_login_form import login_form
from supabase import create_client, Client

st.title("TableTender")

genai.configure(api_key=st.secrets["SECRET_KEY"])

# Select the model
model = genai.GenerativeModel('gemini-pro')

# **Security:** Read Supabase credentials from environment variables
url = st.secrets['SUPABASE_URL']
key = st.secrets['SUPABASE_KEY']

# Create a Supabase client
supabase: Client = create_client(url, key)

with st.sidebar:
  client = login_form()


# Initialize chat history
if "context" not in st.session_state:
  st.session_state.context = [{
    "role":
      "user",
      "content":
      """ Welcome to TableTender, your friendly pizza ordering assistant! 
1.I'll greet you and ask about your pizza preferences.

2.  You can choose from various sizes, toppings, and crust options. Feel free to ask questions about the menu!
3.  Let me know if you'd like your pizza delivered or if you'll be picking it up.
4.  I'll summarize your order before finalizing it. You can make any changes at this point.
5.  If you choose delivery, I'll ask for your address to ensure speedy service.
6. Let me know your preferred payment method, and we'll get your delicious pizza on the way!

Don't hesitate to ask if you have any questions about your order !  
    
    The menu includes 
    pepperoni pizza 12.95, 10.00, 7.00 
    cheese pizza  10.95, 9.25, 6.50 
    eggplant pizza  11.95, 9.75, 6.75
    \n
    Toppings: 
    extra cheese 2.00, 
    mushrooms 1.50 
    sausage 3.00 
    \n
    Drinks: 
    coke 3.00, 2.00, 1.00 
    sprite 3.00, 2.00, 1.00 
    bottled water 5.00
    
    """
  }]

# Display chat context from history on app rerun after login
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


if st.session_state["authenticated"]:
  if st.session_state["username"]:
    st.success(f"Welcome {st.session_state['username']}")
  else:
    st.success("Welcome guest")

  if st.button("Logout"):
    st.session_state["authenticated"] = False
    st.session_state["username"] = None  # Clear username as well (optional)
    st.experimental_rerun()  # Rerun the app to clear UI elements

  # Calling the Function when Input is Provided
  if usr_msg:
    # Displaying the User Message
    with st.chat_message("user"):
      st.markdown(usr_msg)

    llm_function(usr_msg)
else:
  st.error("Not authenticated. Please login to chat with TableTender.")

