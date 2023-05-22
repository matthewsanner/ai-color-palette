from flask import Flask, render_template, request
import openai
import json
from dotenv import dotenv_values
config = dotenv_values(".env")

openai.api_key = config["API_KEY"]

app = Flask(__name__,
            template_folder="templates",
            static_folder="static",
            static_url_path=''
            )

# Completion format

# def get_colors(msg):
#     prompt = f"""
#     You are a color palette generating assistant that responds to text prompts for color palettes. If possible you should find colors directly associated with the prompt, or if there are no obvious choices then find colors that fit the mood or vibe of the prompt. The palettes should be between 3 and 6 colors. Don't repeat colors.

#     Desired Format: a JSON array of hexadecimal color codes

#     Q: Convert the following description of a color palette into a list of colors: {msg}
#     A:
#     """

#     response = openai.Completion.create(
#         prompt=prompt,
#         model="text-davinci-003",
#         max_tokens=200
#     )

#     colors= json.loads(response["choices"][0]["text"])

#     return colors


def get_colors(msg):
    messages = [
        {"role": "system", "content": "You are a color palette generating assistant that responds to text prompts. If possible you, should find colors that are directly associated with the prompt, or if there are no obvious choices then find colors that fit the mood or vibe of the prompt. The palettes should be between 3 and 5 colors. Don't repeat colors. Give responses in a JSON array of hexadecimal color codes."},
        {"role": "user", "content": "4 Google colors"},
        {"role": "assistant",
            "content": '["#42854F", "#34A853", "#FBBC05", "#EA4335"]'},
        {"role": "user", "content": f"Convert the following description of a color palette into a list of colors: {msg}"}
    ]

    response = openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo",
        max_tokens=200
    )

    colors = json.loads(response["choices"][0]["message"]["content"])

    return colors


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}


if __name__ == "__main__":
    app.run(debug=True)
