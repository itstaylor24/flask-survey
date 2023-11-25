from flask import Flask, render_template, request, redirect, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey


app = Flask(__name__)
# app.config["SECRET_KEY"] = "I_love_to_code"
# debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
RESPONSES_KEY = "responses"


@app.route('/')
def begin_survey():
    """shows survey title and instructions"""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("begin-survey.html", title=title, instructions=instructions)


@app.route("/begin", methods=["POST"])
def start_survey():

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")


@app.route('/answer', methods=["POST"])
def save_answer():

    your_choice = request.form['choice']
    responses = session[RESPONSES_KEY]

    responses.append(your_choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/done_survey")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/done")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/done")
def complete():
    """Survey complete. Show completion page."""

    return render_template("done_survey.html")
