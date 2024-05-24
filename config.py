APP_TITLE = "AI Assessment MCQ Wizard"
APP_INTRO = """This application generates multiple-choice questions (MCQs) for automated AI assessments.
You can configure various settings including the topic, language model, and prompts.
"""

APP_HOW_IT_WORKS = """1. Fill in the details of the assessment.
2. Choose the language model.
3. Configure the prompt and additional options.
4. Generate MCQs with hints and feedback if desired.
"""

SHARED_ASSET = ""

fields = {
    "topic_content": {
        "type": "text_area",
        "label": "Enter the content for question generation:",
        "max_chars": 50000,
        "key": "topic_content",
        "value": "AI processors like CPUs, GPUs, TPUs, and LPUs each serve unique roles in AI applications. CPUs, such as Intel Core and Apple M1/M2, are versatile for general-purpose computing and small datasets. GPUs, like Nvidia Tesla, excel in parallel processing for large-scale machine learning and deep learning tasks. TPUs, developed by Google, optimize TensorFlow operations, boosting performance for AI applications using this framework. LPUs, pioneered by Groq, specialize in natural language processing, enhancing chatbots and other language-based AI. Choosing the right processor depends on specific needs: CPUs for general tasks, GPUs for large data, TPUs for TensorFlow, and LPUs for language processing."
    },
    "original_content_only": {
        "type": "checkbox",
        "label": "Focus only on the provided text",
        "key": "original_content_only"
    },
    "learning_objective": {
        "type": "text_area",
        "label": "Specify a learning objective (optional):",
        "max_chars": 1000,
        "key": "learning_objective",
        "value": "Learn about AI hardware"
},
    "questions_num": {
        "type": "selectbox",
        "label": "Number of questions:",
        "options": [1, 2, 3, 4, 5],
        "key": "questions_num"
    },
    "correct_ans_num": {
        "type": "selectbox",
        "label": "Correct answers per question:",
        "options": [1, 2, 3, 4],
        "key": "correct_ans_num"
    },
    "question_level": {
        "type": "selectbox",
        "label": "Question difficulty level:",
        "options": ['Grade School', 'High School', 'University', 'Other'],
        "key": "question_level"
    },
    "custom_level": {
        "type": "text_input",
        "label": "Specify other level: (only if other is selected)",
        "key": "custom_level"
    },
    "distractors_num": {
        "type": "selectbox",
        "label": "Number of distractors:",
        "options": [1, 2, 3, 4, 5],
        "key": "distractors_num"
    },
    "distractors_difficulty": {
        "type": "selectbox",
        "label": "Distractors difficulty",
        "options": ['Normal', 'Obvious', 'Challenging'],
        "key": "distractors_difficulty"
    },
    "learner_feedback": {
        "type": "checkbox",
        "label": "Include Feedback",
        "key": "learner_feedback"
    },
    "hints": {
        "type": "checkbox",
        "label": "Include hints",
        "key": "hints"
    },
    "output_format": {
        "type": "selectbox",
        "label": "Output format:",
        "options": ['Plain Text', 'OLX'],
        "key": "output_format"
    }
}

actions = {
    "submit": {
          "type": "button",
          "on_click": "ai_handler",
          "label": "Submit"
        }
}

LLM_CONFIGURATIONS = {
    "gpt-3.5-turbo": {
        "model": "gpt-3.5-turbo-0125",
        "frequency_penalty": 0,
        "max_tokens": 1000,
        "presence_penalty": 0,
        "temperature": 1,
        "top_p": 1,
        "price_input_token_1M": 0.50,
        "price_output_token_1M": 1.50
    },
    "gpt-4-turbo": {
        "model": "gpt-4-turbo",
        "frequency_penalty": 0,
        "max_tokens": 1000,
        "presence_penalty": 0,
        "temperature": 1,
        "top_p": 1,
        "price_input_token_1M": 10,
        "price_output_token_1M": 30
    },
    "gpt-4o": {
        "model": "gpt-4o",
        "frequency_penalty": 0,
        "max_tokens": 1000,
        "presence_penalty": 0,
        "temperature": 1,
        "top_p": 1,
        "price_input_token_1M": 5,
        "price_output_token_1M": 15
    },
    "gemini-pro": {
        "model": "gemini-pro",
        "price_input_token_1M": 7,
        "price_output_token_1M": 21
    },
    "claude-opus": {
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000,
        "temperature": 1,
        "price_input_token_1M": 15,
        "price_output_token_1M": 75
    },
    "claude-sonnet": {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 1000,
        "temperature": 1,
        "price_input_token_1M": 3,
        "price_output_token_1M": 15
    },
    "claude-haiku": {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1000,
        "temperature": 1,
        "price_input_token_1M": 0.25,
        "price_output_token_1M": 1.25
    }
}

