from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

MODEL_PATH = "../llm_models/gemma/2b_it_v2.gguf"
LLAMA_BIN = "../llama.cpp/build/bin/llama-cli"

@app.route("/", methods=["GET", "POST"])
def index():
    recipe = ""
    error = ""

    if request.method == "POST":
        ingredients = request.form["ingredients"]
        prompt = f"<start_of_turn>user\nPropose une recette simple avec : {ingredients}.\n<end_of_turn>\n<start_of_turn>model\n"

        try:
            process = subprocess.Popen(
                [LLAMA_BIN, "-m", MODEL_PATH, "-p", prompt, "-n", "128"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate(timeout=90)

            if process.returncode != 0:
                error = f"Model error: {stderr}"
            else:
                recipe = stdout.strip()

        except subprocess.TimeoutExpired:
            process.kill()
            recipe = ""
            error = "Model timed out. Please try with fewer ingredients or wait longer."

    return render_template("index.html", recipe=recipe, error=error)

if __name__ == "__main__":
    app.run(debug=True)
