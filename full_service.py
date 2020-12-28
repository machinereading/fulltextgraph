from flask import Flask, request, jsonify
import jpype
import full_text_graph_generator as fg
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

print("Start JVM")
jpype.startJVM(jpype.getDefaultJVMPath())
@app.route("/full-parser", methods=["POST"])
def get_full_text():
    jpype.attachThreadToJVM()
    data = request.get_json()
    text = data["text"]
    option = data["option"]
    if option == "surface":
        result_graph = fg.get_full_text_graph(text, False, False)
    elif option == "surface-frame":
        result_graph = fg.get_full_text_graph(text, True, False)
    elif option == "surface-frame-l2k":
        result_graph = fg.get_full_text_graph(text, True, True)

    return jsonify(result_graph)

app.run(host="kbox.kaist.ac.kr", port="47362")