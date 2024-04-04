import os
from PIL import Image
import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.pipelines.linear_sync_pipeline  import  LinearSyncPipeline
from lyzr_automata import Logger
from dotenv import load_dotenv; load_dotenv()

# Setup your config
st.set_page_config(
    page_title="Analyze Competitor Content",
    layout="centered",   
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Analyze Competitor Content by Lyzr")
st.markdown("### Welcome to the Analyze Competitor Content!")
st.markdown("Analyze Competitor Content app offers invaluable insights by dissecting competitors' titles and content.!!!")

# Custom function to style the app
def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Analyze Competitor Content

# replace this with your openai api key or create an environment variable for storing the key.
API_KEY = os.getenv('OPENAI_API_KEY')

 

open_ai_model_text = OpenAIModel(
    api_key= API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.5,
        "max_tokens": 1500,
    },
)

def analyze_competitor_content(content_title, target_audience):
    
    content_strategy_analyst = Agent(
        prompt_persona="""You are a Content Strategy Analyst expert who analyze a list of competitor content titles and devise a comprehensive strategy to differentiate our brand. Your task is to meticulously examine the competitor landscape, identify gaps, and propose 10 unique content topics that showcase our brand's expertise and distinct value proposition. Leveraging your expertise in content analysis, market research, and strategic planning, you'll develop innovative ideas that resonate with our target audience and set us apart from the competition.""",
        role="Content Strategy Analyst", 
    )

    contnet_generator =  Task(
        name="Campaign Generator",
        agent=content_strategy_analyst,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions=f"Use the description provided, given a list of competitor content titles, analyze and suggest 10 unique content topics that would differentiate our brand, and the Target Audience: {target_audience}. [IMPORTANT!] Setup the events in a detailed manner",
        log_output=True,
        enhance_prompt=False,
        default_input=content_title
    )


    logger = Logger()
    

    main_output = LinearSyncPipeline(
        logger=logger,
        name="Analyze Competitor Content",
        completion_message="App Generated all things!",
        tasks=[
            contnet_generator,
        ],
    ).run()

    return main_output


if __name__ == "__main__":
    style_app() 
    titles = st.text_area("Write down list of competitor content titles")
    audience = st.text_area('Targeted Audience')

    button=st.button('Submit')
    if (button==True):
        generated_output = analyze_competitor_content(content_title=titles, target_audience=audience)
        title_output = generated_output[0]['task_output']
        st.write(title_output)
        st.markdown('---')
   
    with st.expander("ℹ️ - About this App"):
        st.markdown("""
        This app uses Lyzr Automata Agent suggest the 10 unique content topics that would differentiate your brand. For any inquiries or issues, please contact Lyzr.
        
        """)
        st.link_button("Lyzr", url='https://www.lyzr.ai/', use_container_width = True)
        st.link_button("Book a Demo", url='https://www.lyzr.ai/book-demo/', use_container_width = True)
        st.link_button("Discord", url='https://discord.gg/nm7zSyEFA2', use_container_width = True)
        st.link_button("Slack", url='https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw', use_container_width = True)