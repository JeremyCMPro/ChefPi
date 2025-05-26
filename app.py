import gradio as gr
import subprocess

MODEL_PATH = "../llm_models/gemma/2b_it_v2.gguf"
LLAMA_BIN = "../llama.cpp/build/bin/llama-cli"

def generate_recipe(ingredients):
    prompt = f"<start_of_turn>user\nPropose une recette simple avec : {ingredients}.\n<end_of_turn>\n<start_of_turn>model\n"

    try:
        result = subprocess.run(
            [LLAMA_BIN, "-m", MODEL_PATH, "-p", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300
        )
        output = result.stdout.decode()
        return output.strip().split("<end_of_turn>")[0]
    except Exception as e:
        return f"Erreur : {e}"

gr.Interface(
    fn=generate_recipe,
    inputs=gr.Textbox(label="Ingrédients (ex: riz, œufs, tomates)", placeholder="Entrer les ingrédients..."),
    outputs=gr.Textbox(label="Recette générée"),
    title="ChefPI : Votre Assistant de Cuisine Local",
    description="Proposez des recettes instantanées à partir d’ingrédients, grâce à un modèle LLM tournant localement sur un Raspberry Pi !"
).launch()
