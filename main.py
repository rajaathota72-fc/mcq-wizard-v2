import streamlit as st
from config import *
import os
from openai import OpenAI
import google.generativeai as generativeai
import anthropic

from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
gemini_api_key = os.getenv('GOOGLE_API_KEY')
claude_api_key = os.getenv('CLAUDE_API_KEY')

user_input = {}
function_map = {
    "text_input": st.text_input,
    "button": st.button,
    "radio": st.radio,
    "selectbox": st.selectbox,
    "text_area": st.text_area,
    "checkbox": st.checkbox
}

# Create variables based on the keys in the fields dictionary
for key, value in fields.items():
    globals()[key] = None

def build_fields(i, my_dict):
    field_name = list(my_dict.keys())[i]
    field_dict = list(my_dict.values())[i]
    field_type = field_dict.get("type","")
    field_label = field_dict.get("label","")
    field_body = field_dict.get("body","")
    field_value = field_dict.get("value","")
    field_max_chars = field_dict.get("max_chars",None)
    field_help = field_dict.get("help","")
    field_on_click = field_dict.get("on_click",None)
    field_options = field_dict.get("options","")
    field_horizontal = field_dict.get("horizontal",False)
    kwargs = {}
    if field_label:
        kwargs['label'] = field_label
    if field_body:
        kwargs['body'] = field_body
    if field_value:
        kwargs['value'] = field_value
    if field_options:
        kwargs['options'] = field_options
    if field_max_chars:
        kwargs['max_chars'] = field_max_chars
    if field_help:
        kwargs['help'] = field_help
    if field_on_click:
        kwargs['on_click'] = field_on_click
    if field_horizontal:
        kwargs['horizontal'] = field_horizontal
    if field_type == "button":
        if field_on_click:
            # If there's an on_click action defined, attach it to the button
            if st.button(field_label):
                action_map[field_on_click]()
    else:
        # Example of dynamically accessing the function
        my_input_function = function_map[field_type]
        user_input[field_name] = my_input_function(**kwargs)
        globals()[field_name] = user_input[field_name]

def ai_handler():
    ai_prompt = build_prompt()
    selected_llm = st.session_state['selected_llm']
    if selected_llm in ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o"]:
        llm_configuration = LLM_CONFIGURATIONS[selected_llm]
        try:
            openai_client = OpenAI(api_key=openai_api_key)
            response = openai_client.chat.completions.create(
                    model=llm_configuration["model"],
                    frequency_penalty=llm_configuration.get("frequency_penalty", 0),
                    max_tokens=llm_configuration.get("max_tokens", 1000),
                    presence_penalty=llm_configuration.get("presence_penalty", 0),
                    temperature=llm_configuration.get("temperature", 1),
                    top_p=llm_configuration.get("top_p", 1),
                    messages=[
                        {"role": "user", "content": ai_prompt}
                    ]
                )
            input_price = int(response.usage.prompt_tokens) * llm_configuration["price_input_token_1M"] / 1000000
            output_price = int(response.usage.completion_tokens) * llm_configuration["price_output_token_1M"] / 1000000
            total_price = input_price + output_price
            st.write(f"**OpenAI Response:** {selected_llm}")
            st.success(response.choices[0].message.content.format())
            st.write("Price : ${:.6f}".format(total_price))
        except Exception as e:
            st.write(f"**OpenAI Response:** {selected_llm}")
            st.error(f"Error: {e}")
    if selected_llm == "gemini-pro":
        llm_configuration = LLM_CONFIGURATIONS[selected_llm]
        try:
            generativeai.configure(api_key=gemini_api_key)
            model = generativeai.GenerativeModel(llm_configuration["model"])
            gemini_response = model.generate_content(ai_prompt)
            st.markdown("**Gemini Response:**")
            st.success(gemini_response)
        except Exception as e:
            st.write("**Gemini Response:**")
            st.error(f"Error: {e}")
    if selected_llm in ["claude-opus", "claude-sonnet", "claude-haiku"]:
        llm_configuration = LLM_CONFIGURATIONS[selected_llm]
        try:
            client = anthropic.Anthropic(api_key=claude_api_key)
            anthropic_response = client.messages.create(
                model=llm_configuration["model"],
                max_tokens=llm_configuration["max_tokens"],
                temperature=llm_configuration["temperature"],
                messages=[
                    {"role": "user", "content": ai_prompt}
                ]
            )
            input_price = int(anthropic_response.usage.input_tokens) * llm_configuration[
                "price_input_token_1M"] / 1000000
            output_price = int(anthropic_response.usage.output_tokens) * llm_configuration[
                "price_output_token_1M"] / 1000000
            total_price = input_price + output_price
            response_cleaned = '\n'.join([block.text for block in anthropic_response.content if block.type == 'text'])
            st.write(f"**Anthropic Response: {selected_llm}**")
            st.success(response_cleaned)
            st.write("Price : ${:.6f}".format(total_price))
        except Exception as e:
            st.write(f"**Anthropic Response: {selected_llm}**")
            st.error(f"Error: {e}")



def build_prompt():
    final_prompt = generate_mcq_prompt(user_input)
    return final_prompt

def generate_mcq_prompt(config):
    topic_content = config.get("topic_content", "")
    original_content_only = config.get("original_content_only", False)
    learning_objective = config.get("learning_objective", "")
    questions_num = config.get("questions_num", 1)
    correct_ans_num = config.get("correct_ans_num", 1)
    question_level = config.get("question_level", "University")
    custom_level = config.get("custom_level", "")
    distractors_num = config.get("distractors_num", 3)
    distractors_difficulty = config.get("distractors_difficulty", "Normal")
    learner_feedback = config.get("learner_feedback", False)
    hints = config.get("hints", False)
    output_format = config.get("output_format", "Plain Text")

    if question_level == 'Other' and custom_level:
        question_level = custom_level

    mcq_prompt = (
        f"Please write {questions_num} {question_level} level multiple-choice question(s), each with "
        f"{correct_ans_num} correct answer(s) and {distractors_num} distractors, "
        "based on text that I will provide.\n"
    )

    if original_content_only:
        mcq_prompt += "Please create questions based solely on the provided text.\n"
    else:
        mcq_prompt += "Please create questions that incorporate both the provided text as well as your knowledge of the topic.\n"

    if distractors_difficulty == "Obvious":
        mcq_prompt += "Distractors should be obviously incorrect options.\n"
    elif distractors_difficulty == "Challenging":
        mcq_prompt += "Distractors should sound like they could be plausible, but are ultimately incorrect.\n"

    if learning_objective:
        mcq_prompt += f"Focus on meeting the following learning objective(s): {learning_objective}.\n"

    if learner_feedback:
        mcq_prompt += "Please provide a feedback section for each question that says why the correct answer is the best answer and the other options are incorrect.\n"

    if hints:
        mcq_prompt += "Also, include a hint for each question.\n"

    if output_format == "OLX":
        mcq_prompt += "Please write your MCQs in Open edX OLX format.\n"

    mcq_prompt += """
Format each question like the following:
Question: [Question Text] \n
A) [Answer A] \n
B) [Answer B] \n
....
N) [Answer N] \n

Solution: [Answer A, B...N]\n\n
"""

    if learner_feedback:
        mcq_prompt += "Feedback: [Feedback]\n\n"

    if hints:
        mcq_prompt += "Hint: [Hint]\n\n"

    mcq_prompt += (
        "Here is the text:\n"
        "===============\n"
        f"{topic_content}"
    )

    return mcq_prompt

action_map = {"ai_handler": ai_handler}

def main():
    st.title(APP_TITLE)
    st.markdown(APP_INTRO)

    if APP_HOW_IT_WORKS:
        with st.expander("Learn how this works", expanded=False):
            st.markdown(APP_HOW_IT_WORKS)

    for i in range(len(fields)):
        # Access each dictionary by its index
        build_fields(i, fields)

    with st.expander("Show prompt"):
        final_prompt = build_prompt()
        st.write(final_prompt)

    # Display LLM selection dropdown
    selected_llm = st.selectbox("Select Language Model", options=LLM_CONFIGURATIONS.keys(), key="selected_llm")

    for i in range(len(actions)):
        # Access each dictionary by its index
        build_fields(i, actions)

if __name__ == "__main__":
    main()

