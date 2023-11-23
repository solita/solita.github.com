---
layout: post
title: Unveiling the Power of Streamlit in Snowflake - A Guide to Hosting Interactive Apps in Snowflake
author: erikkronberg
excerpt: Creating and hosting Streamlit applications in Snowflake, a comprehensive guide
tags:
 - Snowflake
 - Streamlit
 - OpenAI
 - Prompting
---
Streamlit, an open-source Python library for creating custom 
web apps, particularly shines in machine learning and data 
science. With Streamlit’s integration into Snowflake this empowers 
developers to securely build, deploy, and share applications using 
Snowflake's robust data capabilities without the need to pull 
data outside the warm safety of Snowflakes secure walls.
It also opens up the avenue for users which are not that tech-savy to
view, filter and and even query data with natural language (with the help of LLMs) 
through the power of Streamlit.

## Streamlit and Snowflake Integration: The Final Piece in a Complete Data Platform Puzzle?

Streamlit's recent integration into Snowflake has opened up 
exciting opportunities for data visualization and interactivity 
directly within Snowflake accounts. Snowflake of course has always
covered the data aspect very well and with the addition of Snowpark
now also covered the AI & machine learning demand. But one important
aspect when working with data is also to visualize and make it easy 
to interact with. To tackle this Snowflake has put their money on Streamlit 
which they believe will take their data platform to the next 
level. 


This blog post explores the potential and current limitations of 
hosting Streamlit apps in Snowflake during its public preview, and
an introduction on how you yourself can create your first Streamlit 
application which utilize an LLM-model from OpenAI.



### Key points before diving in
- As Streamlit in Snowflake still only is in public preview 
there are some limitations. This unfortunatly means that not 
all features are supported, see the full list here [Unsupported Streamlit Features](https://docs.snowflake.com/en/developer-guide/streamlit/limitations#unsupported-streamlit-features)
- Snowflake, as of now, only supports Streamlit v1.22.0 which means that no features
from the later versions are available, but this will surely be updated
in the future.
- You can also use your favorite python packages for Streamlit in Snowflake
with the little exception that they need to be in the Snowflake Anaconda Channel,
you can see which packages are available and what version here [Snowflake Conda Channel](https://repo.anaconda.com/pkgs/snowflake/)
- As of now only Azure Snowflake accounts have access to 
Streamlit in Snowflake, AWS and GCP will be rolled out in 
the coming months.
- You need to accept Anaconda's terms of service for your 
Snowflake account and also configure your firewall to 
allow traffic from *.snowflake.app. See more information 
on this at [Prerequisites for Streamlit in Snowflake](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit#prerequisites-for-using-sis)
- Creating a Streamlit app in Snowflake requires USAGE, 
CREATE STREAMLIT, and CREATE STAGE privileges. For 
viewing a Streamlit app, specific privileges within a 
Snowflake account are essential.

## Building your first MULTI-PAGE Streamlit Application in Snowflake

When creating a Streamlit application in Snowflake you can 
either create it using Snowsight or by uploading your files to a
Snowflake internal stage and the creating a Streamlit object
using SQL. As we also want to use a function that sends data to OpenAIs 
servers we first need to create a Snowflake User Defined Function, UDF, 
that has an External Access Integration for traffic to OpenAI. 
We can do this easily in four steps in Snowflake. 


One important thing is that 
you will need admin access for your Snowflake database and an OpenAI API 
key to do this.

**Step 1 - Create a Secret object for OpenAI API key**
```
CREATE OR REPLACE SECRET dash_open_ai_api
    TYPE = GENERIC_STRING
    SECRET_STRING = 'YOUR_OPENAI_API_KEY';
```
**Step 2 - Create a Network Rule object**
```
CREATE OR REPLACE NETWORK RULE dash_apis_network_rule
 MODE = EGRESS
 TYPE = HOST_PORT
 VALUE_LIST = ('api.openai.com');
```
**Step 3 - Create an External Access Integration object**
```
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dash_external_access_int
 ALLOWED_NETWORK_RULES = (dash_apis_network_rule)
 ALLOWED_AUTHENTICATION_SECRETS = (dash_open_ai_api)
 ENABLED = true;
```
**Step 4 - Create a UDF with your External Access Integration and your Python code**
```
CREATE OR REPLACE FUNCTION YOUR_DB.YOUR_SCHEMA.YOUR_FUNCTION("dict_1" VARCHAR(16777216), "dict_2" VARCHAR(16777216))
RETURNS VARCHAR(16777216)
LANGUAGE PYTHON
RUNTIME_VERSION = '3.9'
PACKAGES = ('openai')
HANDLER = 'complete_me'
EXTERNAL_ACCESS_INTEGRATIONS = (dash_external_access_int)
SECRETS = ('openai_key'=dash_open_ai_api)
AS '
import _snowflake
import openai
import json
def complete_me(dict_1,dict_2):
    openai.api_key = _snowflake.get_generic_secret_string(''openai_key'')
    messages = [json.loads(dict_1),json.loads(dict_2)]
    model="gpt-3.5-turbo"
    response = openai.ChatCompletion.create(model=model,messages=messages,temperature=0,)    
    return response.choices[0].message["content"]
';
```
Now that we have an UDF with an External Access Integration our next 
step is to implement this into a Streamlit application locally before
we can upload anything to our Snowflake Internal Stage. In the next steps 
we will go over the actual Streamlit application that we will then host on 
Snowflake. 

When creating Streamlit applications you need to follow a specific 
directory structure. You'll need a main folder, in this case we'll
name it "Streamlit" and in this folder you will place your main file,
and if you need it, a environment.yml file to add external packages. 
In our case we only need the OpenAI package but this is already imported
in the UDF so we have no need for an environment file. In the Streamlit
folder we also create another folder named "pages", here we will place 
our other pages which are not the main page. Which in our case will only
be one file. So in the end your directory structure should look like this.

```
└── streamlit/
    └── Home_Page.py
    └── pages/
         └── LLM_Control_Panel.py
```
The Home_Page.py will be the main page were you can generate 
your prompt via an user interface that calls on our Snowflake UDF which 
has access to OpenAI and returns and displays the result. 



**Main File - Home_Page.py** 

```
# Import the needed packages and funcitons
import streamlit as st
from snowflake.snowpark.context import get_active_session
from pages.LLM_Control_Panel import load_data

def main():

    # Need to have an active session to be able to make snowpark queries
    session = get_active_session()

    # Load the data for the user interface and prompt generation from the LLM Control Panel
    llm_title, llm_result, system_message, user_message, input_placeholder = load_data()

    # Title for the user interface
    st.title(llm_title)

    # Text input area for the user role in the prompt generation with a button below it
    user_input = st.text_input(label="Text input for prompt generation", placeholder=input_placeholder, label_visibility="collapsed")
    clicked = st.button(label="Get joke")
    
    # Define the user message
    user_message = f'{user_message} {user_input}'
    
    # If we have entered a message and clicked the button we then create the prompt and send it via our UDF
    # and then we take the result from the UDF and display it
    if user_input and clicked:
        # Construct objects with our system and user message for the prompt
        query = f"""SELECT
                    OBJECT_CONSTRUCT('role','system','content','{system_message}')::VARCHAR as dict1,
                    OBJECT_CONSTRUCT('role','user','content','{user_message}')::VARCHAR as dict2,
                    TEST_CHATGPT(dict1,dict2)
                """

        answer = session.sql(query).to_pandas()
        st.write("Got result!")
        st.subheader(llm_result)
        st.write("Providing answer")
        st.write(answer["TEST_CHATGPT(DICT1,DICT2)"][0])

if __name__ == '__main__':
    main()

```

The second file will have functionalties so that you modify the chat 
user interface and also the prompt that you send to OpenAI. 
The default settings is a LLM that is supposed to be a retired
comedian that tells slightly depressed and dark jokes about
a certain subject which is retrieved from the text input in 
the first tab.

 **Second file - LLM_Control_Panel.py**
```
# Import the needed packages
import streamlit as st

# If we haven't created session states we do so and set the variables to their standard values, 
# which is application that creates joke from the text input with some additional instructions.
if 'llm_title' not in st.session_state:
    st.session_state.llm_title = "Enter a something you want a slightly dark and tired joke about!"

if 'result_title' not in st.session_state:
    st.session_state.result_title = "Here's your joke. I hope it cheers you up, though it didn't for me."

if 'system_message' not in st.session_state:
    st.session_state.system_message = "You are a retired comedian, slightly depressed and with a very dark humour. Always end with a emoji related to the joke."

if 'user_message' not in st.session_state:
    st.session_state.user_message = "Tell me a short joke about"

if 'input_placeholder' not in st.session_state:
    st.session_state.input_placeholder = "Enter the thing you want a joke about here"

# A function to load the data from the session state which is used in the home page
def load_data():
    llm_title = st.session_state.llm_title
    result_title = st.session_state.result_title
    system_title = st.session_state.system_message
    user_title = st.session_state.user_message
    input_placeholder = st.session_state.input_placeholder
    return llm_title, result_title, system_title, user_title, input_placeholder

# Main function where the user can change the settings and layout by entering new text 
def main():
    st.header("Modify parameters for the LLM assistant")
    placeholder1, placeholder_col1 = st.columns(2)
    title_col1, title_col2 = st.columns([3,10])
    result_col1, result_col2 = st.columns([3,10])
    system_col1, system_col2 = st.columns([3,10])
    user_col1, user_col2  = st.columns([3,10])
    placeholder_col1, placeholder_col2  = st.columns([3,10])
    
    # Text input for the diffrent layout and prompt settings
    title_col1.subheader("LLM Title")
    with title_col2:
        llm_title = st.text_input("What you want to call your assisant, like 'ComedianGPT'")

    result_col1.subheader("Result Title")
    with result_col2:
        result_title = st.text_input("The header for the when the result is returned from the LLM")

    system_col1.subheader("System message")
    with system_col2:
        system_message = st.text_input("System message which is basically the instructions for the LLM.")

    user_col1.subheader("User message")
    with user_col2:
        user_message = st.text_input("User message for the LLM, like 'Tell me a short joke about {input}'")

    placeholder_col1.subheader("Input placeholder")
    with placeholder_col2:
        input_placeholder = st.text_input("The text for the placeholder in the text input area")

    # Button to change the variables
    clicked = st.button("Change variables")

    # If we click the button we only change the variables that has some text entered
    if clicked:
        if llm_title:
            st.session_state.llm_title = llm_title
        if result_title:
            st.session_state.result_title = result_title
        if system_message:
            st.session_state.system_message = system_message
        if user_message:
            st.session_state.user_message = user_message
        if input_placeholder:
            st.session_state.input_placeholder = input_placeholder

if __name__ == '__main__':
    main()
```

## Loading Streamlit Application into Snowflake Internal Stage

Now that we have our Streamlit application app ready, we now 
need to upload the files to a Snowflake internal stage in our
dedicated Streamlit Snowflake database. If you haven't created
an internal stage in your dedicated Streamlit database you can
do it now. We can upload our files by either by using Snowsight, 
if you are new to this you can read the documentation 
[here](https://docs.snowflake.com/en/user-guide/data-load-local-file-system-stage-ui#uploading-files-onto-a-stage),
or by using SQL in a SQL worksheet in Snowsight, see an example 
of how you can do this below.

```
PUT file:///<path_to_your_root_folder>/<internal_stage_name>/Home_Page.py @streamlit_db.steamlit_schema.streamlit_stage overwrite=true auto_compress=false;
PUT file:///<path_to_your_root_folder>/<internal_stage_name>/pages/LLM_Control_Panel.py @streamlit_db.steamlit_schema.streamlit_stage/pages/ overwrite=true auto_compress=false;
```

When we have succesfully uploaded our files into our Snowflake 
internal stage we can then create our Streamlit object using SQL. 
Here we only need to add the name of the application, the root 
location which is our Snowflake internal stage, the main file 
which in this case is the home_page.py file and also which 
warehouse we want to use. Se an example of this SQL query below.

```
CREATE STREAMLIT name_of_application
ROOT_LOCATION = '@streamlit_db.steamlit_schema.streamlit_stage'
MAIN_FILE = '/home_page.py'
QUERY_WAREHOUSE = my_warehouse;
```



## Congratulations, you have now created your first multi-page Streamlit application in Snowflake!

You can now visit it via the Streamlit tab in Snowsight and try it out.

![](/img/streamlit-in-snowflake/application_in_snowflake.png)


## Concluding Thoughts on Streamlit in Snowflake

Streamlit's integration into Snowflake marks a significant 
advancement in data visualization and interaction capabilities 
within Snowflake. The potential for dynamic, interactive 
applications is vast. Future developments, including broader 
AWS and GCP account integrations, promise to add even more functionality.
However at this early stage, there are a lot of functionalties missing..
To list a few here are some examples of things I hope will change in the future.

- With multi-page applications you can only edit the main page, so if 
you want to edit any other pages you need to edit it locally and then 
reupload to the internal stage and recreate the Streamlit object.
- I've had some problems with enviroment.yml files where I get package 
conflicts even though all the packages are from the Snowflake Anaconda 
Channel, which makes it hard to create more complex applications.
- As of now there is no possibility to upload any data or files as the 
st.file_uploader is not available in Streamlit in Snowflake, this also 
limits the possibilites of what kind of applications you can create in Snowflake.

But as already mentioned, Streamlit in Snowflake is in public preview and 
hopefully a lot of these bugs and limitations will be fixed when it's released 
in full. But until then we will have to work with what is available, which is
still quite a lot to be fair!

---


