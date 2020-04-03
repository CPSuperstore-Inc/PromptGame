from flask import Flask, render_template, request, session, redirect, flash

from PromptGame.api import app as api
from PromptGame.filters import app as filters
from PromptGame.security import SECRET_KEY

import PromptGame.game as game
import PromptGame.player as player
import PromptGame.round as round_mngr
import PromptGame.question as question
import PromptGame.response as response

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
    return render_template("index.twig")


@app.route("/newGame", methods=["POST"])
def new_game():
    code = game.new_game()
    session["id"] = player.join_game(request.form["name"], code)
    return redirect("/lobby")


@app.route("/joinGame", methods=["POST"])
def join_game():
    code = request.form["code"]
    g = game.get_game(request.form["code"])
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