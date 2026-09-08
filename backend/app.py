from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
from models.translator import (
    translate_text,
    translate_multi_target,
    SUPPORTED_LANGUAGES,
    get_language_code,
    extract_key_vocabulary,
    generate_explanation,
    generate_mini_quiz,
    answer_student_doubt
)
from models.cinema_studio import get_cinema_scenes, translate_scene, generate_srt_file
from models.report_generator import generate_report_data, generate_markdown_report
import database

app = Flask(__name__)
CORS(app)

database.init_db()

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Vernacular AI Platform",
        "languages_count": len(SUPPORTED_LANGUAGES),
        "database": database.get_db_info()
    })

@app.get("/api/languages")
def get_languages():
    return jsonify({
        "languages": SUPPORTED_LANGUAGES,
        "total": len(SUPPORTED_LANGUAGES)
    })

@app.post("/api/translate")
def translate():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()
    source = data.get("source", "English")
    target = data.get("target", "Tamil")

    if not text:
        return jsonify({"error": "Please enter educational text or a question."}), 400

    result = translate_text(text, source, target)

    record_id = None
    try:
        record_id = database.save_translation(
            source_lang=source,
            target_lang=target,
            source_text=text,
            translated_text=result
        )
    except Exception as e:
        app.logger.error(f"Database save error: {e}")

    vocab = []
    explanation = ""
    quiz = []
    try:
        vocab = extract_key_vocabulary(text, source=source, target=target)
        explanation = generate_explanation(text, target=target)
        quiz = generate_mini_quiz(text, result, target=target)
    except Exception as e:
        app.logger.warning(f"Pedagogy pack generation error: {e}")

    return jsonify({
        "id": record_id,
        "source": source,
        "target": target,
        "source_code": get_language_code(source),
        "target_code": get_language_code(target),
        "translation": result,
        "vocabulary": vocab,
        "explanation": explanation,
        "quiz": quiz,
        "model": "Multi-Vernacular Pedagogical Engine"
    })

@app.post("/api/translate/broadcast")
def translate_broadcast():
    """Simultaneously translates text into multiple target languages for live broadcast."""
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()
    source = data.get("source", "English")
    targets = data.get("targets", ["Tamil", "Hindi", "Telugu", "Malayalam"])

    if not text:
        return jsonify({"error": "Text is required for broadcast."}), 400

    translations = translate_multi_target(text, source=source, targets=targets)
    return jsonify({
        "source": source,
        "text": text,
        "broadcast": translations
    })

@app.post("/api/ask_doubt")
def ask_doubt():
    """Answers a student doubt in their chosen mother tongue."""
    data = request.get_json(silent=True) or {}
    lesson = str(data.get("lesson") or data.get("context") or "").strip()
    question = str(data.get("question", "")).strip()
    target = data.get("target") or data.get("target_lang") or "Tamil"

    if not question:
        return jsonify({"error": "Doubt question is required."}), 400

    answer = answer_student_doubt(lesson, question, target=target)
    return jsonify({
        "question": question,
        "target": target,
        "answer": answer
    })

@app.get("/api/history")
def get_history():
    try:
        limit = request.args.get("limit", default=50, type=int)
        items = database.get_history(limit=limit)
        return jsonify({"history": items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.delete("/api/history/<int:item_id>")
def delete_history_item(item_id):
    try:
        success = database.delete_history_item(item_id)
        return jsonify({"success": success})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.delete("/api/history")
def clear_all_history():
    try:
        database.clear_all_history()
        return jsonify({"success": True, "message": "History cleared successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/api/favorite/<int:item_id>")
def toggle_favorite(item_id):
    try:
        new_status = database.toggle_favorite(item_id)
        return jsonify({"id": item_id, "is_favorite": new_status})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/database/info")
def get_database_info():
    try:
        return jsonify(database.get_db_info())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/database/export")
def export_database():
    fmt = request.args.get("format", "json").lower()
    try:
        if fmt == "csv":
            csv_data = database.export_as_csv()
            return Response(
                csv_data,
                mimetype="text/csv",
                headers={"Content-Disposition": "attachment;filename=vernacular_ai_database.csv"}
            )
        else:
            rows = database.get_all_rows()
            return jsonify({"database_export": rows, "total": len(rows)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/cinema/scenes")
def cinema_scenes():
    try:
        return jsonify({"scenes": get_cinema_scenes()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/api/cinema/translate")
def cinema_translate():
    try:
        data = request.get_json(silent=True) or {}
        scene_id = data.get("scene_id", "pursuit_of_happyness")
        target = data.get("target", "Tamil")
        result = translate_scene(scene_id, target=target)
        if not result:
            return jsonify({"error": "Scene not found"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/api/cinema/export_srt")
def cinema_export_srt():
    try:
        data = request.get_json(silent=True) or {}
        srt_content = generate_srt_file(data)
        filename = f"{data.get('scene_id', 'subtitle')}_{data.get('target_language', 'vernacular')}.srt"
        return Response(
            srt_content,
            mimetype="text/plain; charset=utf-8",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/project/report")
def project_report():
    try:
        return jsonify(generate_report_data())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/project/report/download")
def project_report_download():
    try:
        md = generate_markdown_report()
        return Response(
            md,
            mimetype="text/markdown; charset=utf-8",
            headers={"Content-Disposition": "attachment; filename=Vernacular_AI_Project_Report.md"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
