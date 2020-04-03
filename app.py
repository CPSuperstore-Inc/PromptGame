from flask import Flask, render_template, request, session, redirect, flash

from PromptGame.api import app as api
from PromptGame.filters import app as filters
from PromptGame.security import SECRET_KEY

import PromptGame.game as game
import PromptGame.player as player
import PromptGame.round as round_mngr
import PromptGame.question as question
import PromptGame.response as response
import PromptGame.category as category

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(filters)

@app.context_processor
def inject_dict_for_all_templates():
    return {
        "development": True
    }


@app.route("/")
def index():
    return render_template("index.twig", categories=category.get_categories())


@app.route("/newGame", methods=["POST"])
def new_game():
    code = game.new_game()
    session["id"] = player.join_game(request.form["name"], code)
    return redirect("/lobby")


@app.route("/joinGame", methods=["POST"])
def join_game():
    code = request.form["code"]
    g = game.get_game(request.form["code"].lower().replace(" ", ""))
    if g is None:
        flash("Game Code: {} Does Not Exist!".format(code))
        return redirect("/")

    session["id"] = player.join_game(request.form["name"], g["id"])
    return redirect("/lobby")


@app.route("/lobby")
def lobby():
    return render_template("lobby.twig", game=player.get_game_info(session["id"]))


@app.route("/round/<rid>", methods=["GET", "POST"])
def round_play(rid):
    if request.method == "GET":
        g = player.get_game_info(session["id"])
        game.remove_code(g["id"])
        player.select_alien(g["id"])
        round_data = round_mngr.get_round(rid, g["id"])
        alien = player.is_alien(session["id"])

        if alien:
            q = question.get_question(round_data["falseQuestion"])
        else:
            q = question.get_question(round_data["regularQuestion"])

        return render_template("prompt.twig", round=round_data, alien=alien, question=q, rid=rid)

    if request.method == "POST":
        g = player.get_game_info(session["id"])
        response.set_response(
            round_mngr.get_round(rid, g["id"])["id"], session["id"], request.form["response"]
        )
        return redirect("/response/{}".format(rid))


@app.route("/response/<rid>")
def responses(rid):
    g = player.get_game_info(session["id"])
    player.select_alien(g["id"])
    round_data = round_mngr.get_round(rid, g["id"])
    alien = player.is_alien(session["id"])
    q = question.get_question(round_data["regularQuestion"])

    return render_template("responses.twig", round=round_data, alien=alien, question=q, rid=rid)


@app.route("/endGame/<gid>")
def end_game(gid):
    del session["id"]
    return redirect("/")


@app.route("/addQuestion", methods=["POST"])
def add_question():
    question.add_question(request.form["category"], request.form["question"])

    flash("Added question to question bank. Thank you for your response!")
    return redirect("/questionManager")


@app.route("/addCategory", methods=["POST"])
def add_category():
    category.add_category(request.form["category"])

    flash("Added category to category list. Thank you for your response!")
    return redirect("/questionManager")


@app.route('/questionManager')
def question_management():
    return render_template("questionManager.twig", questions=question.get_all_questions(), categories=category.get_categories())


@app.route("/editQuestion/<qid>", methods=["POST"])
def edit_question(qid):
    question.edit_question(qid, request.form["category"], request.form["question"])
    flash("Successfully Updated Question")
    return redirect("/questionManager")


@app.route("/deleteQuestion/<qid>")
def delete_question(qid):
    question.delete_question(qid)
    flash("Successfully Deleted Question")
    return redirect("/questionManager")
