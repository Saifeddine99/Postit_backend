from flask import Blueprint, request, jsonify, g
from .db_models import Post, db
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv

from .decorators import rate_limit, token_required

# Load environment variables from .env file
load_dotenv()

# Access OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Initialize LangChain components
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, 
                 model="gpt-4o", 
                 temperature=0.7,
                 max_tokens=None,
                 )


gen_post_bp = Blueprint('generate_post', __name__)

@gen_post_bp.route('/', methods=['POST'])
@rate_limit # Apply rate limiting
@token_required
def gen_post():
    try:
        data = request.get_json()
        
        content = data.get('content')
        platform = data.get('platform')
        tone_style = data.get('tone_style')

        if not content or not platform or not tone_style:
            return jsonify({"error": "Missing required parameters"}), 400

        # Prompt Template
        post_generation_prompt_template = """
        You are a social media manager. Create a {platform} post based on the following content, considering the specified tone and style.

        Content: {content}

        Tone and Style: {tone_style}

        Output the post in a format suitable for the specified platform.
        """

        post_generation_prompt = PromptTemplate(
            input_variables=["platform", "content", "tone_style"],
            template=post_generation_prompt_template,
        )

        post_generation_chain = LLMChain(llm=llm, prompt=post_generation_prompt)

        # Run LangChain
        result = post_generation_chain.run(platform=platform, content=content, tone_style=tone_style)

        return jsonify({"post": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@gen_post_bp.route('/save', methods=['POST'])
@rate_limit # Apply rate limiting
@token_required
def save_post():
    try:
        user_id = g.user_id  # Access the user ID

        data = request.get_json()

        content = data.get('content')
        platform = data.get('platform')
        tone_style = data.get('tone_style')
        generated_post = data.get('generated_post')

        if not user_id or not content or not generated_post:
            return jsonify({"error": "Missing required parameters"}), 400
        
        # Generate a title for the generated_post using LangChain
        title_prompt_template = """
        Create a short, concise title (under 10 words) for the following social media post:

        {post}
        """
        title_prompt = PromptTemplate(
            input_variables=["post"],
            template=title_prompt_template,
        )
        title_chain = LLMChain(llm=llm, prompt=title_prompt)

        title = title_chain.run(post=generated_post).strip()
        # Potential errors during title generation:
        if not title:  # Check if the title is empty
            title = "No Title!"

        new_post = Post(user_id=user_id, title=title, content=content, generated_post=generated_post, platform=platform, tone_and_style=tone_style)
        db.session.add(new_post)
        db.session.commit()
        
        return(jsonify({"result": "saved successfully!"})), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500