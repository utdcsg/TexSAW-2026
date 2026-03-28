import os
import subprocess
import tempfile
from google import genai
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyCX1cLubTcLwfaUkAgagJenZYqxhM5aacY"

def run_rocq(coq_source: str) -> tuple[bool, str]:
    """Write coq_source to a temp file, run coqc, return (success, output)."""
    with tempfile.NamedTemporaryFile(suffix=".v", mode="w", delete=False) as f:
        f.write(coq_source)
        tmp_path = f.name
    try:
        result = subprocess.run(
            ["coqc", tmp_path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = (result.stdout + result.stderr).strip()
        success = result.returncode == 0
        return success, output
    except FileNotFoundError:
        return False, "coqc not found. Make sure Coq is installed and on PATH."
    except subprocess.TimeoutExpired:
        return False, "coqc timed out after 30 seconds."
    finally:
        os.unlink(tmp_path)


def ask_gemini_for_proof(definitions: str, theorem: str) -> str:
    """Ask Gemini to produce a Rocq proof for the given theorem."""
    prompt = f"""You are an expert in the Rocq (formerly Coq) proof assistant.

Given the following definitions and a theorem, produce ONLY valid Rocq source code that proves the theorem. Do not include any explanation, markdown fences, or commentary — output raw .v file contents only.

Definitions:
{definitions}

Theorem to prove:
{theorem}

Your output should begin with `Proof.` and end with `Qed.` provide no surrounding quotes or structure whatsoever, as your output will be directly passed to Coq. Do not restate definitions or the theorem.

Do not use any special or custom tactics. Stick to builtins only.
"""
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model="gemini-2.5-flash-lite", contents=prompt)
    return response.text.strip()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    definitions = data.get("definitions", "").strip()
    theorem = data.get("theorem", "").strip()
    proof = data.get("proof", "").strip()

    if any([x in (definitions + theorem + proof).lower() for x in ["axiom", "admit", "abort"]]):
        return jsonify({
            "stage": "scholar_survived",
            "message": "Fake",
            "gemini_source": ""
        })

    # Step 1: Compile the user's submission
    user_source = "\n\n".join(filter(None, [definitions, theorem, proof]))
    user_ok, user_output = run_rocq(user_source)

    if not user_ok:
        return jsonify({
            "stage": "user_proof_failed",
            "message": "Your proof did not compile.",
            "output": user_output,
        })

    # Step 2: User's proof compiled — now ask Gemini to prove it
    gemini_source = ask_gemini_for_proof(definitions, theorem)
    gemini_ok, gemini_output = run_rocq("\n\n".join([definitions, theorem, gemini_source]))

    if gemini_ok:
        # Gemini also proved it — scholar survives
        return jsonify({
            "stage": "scholar_survived",
            "message": "Sorry, you failed to kill the scholar.",
            "gemini_source": gemini_source,
        })
    else:
        # Gemini failed — reveal the flag
        try:
            with open("flag.txt") as fh:
                flag = fh.read().strip()
        except FileNotFoundError:
            flag = "flag{placeholder_flag_not_found}"

        return jsonify({
            "stage": "flag",
            "message": flag,
            "gemini_source": gemini_source,
            "gemini_output": gemini_output,
        })


if __name__ == "__main__":
    app.run(debug=True)
