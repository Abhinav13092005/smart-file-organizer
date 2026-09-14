from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)


FILE_CATEGORIES = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"
    ],
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt",
        ".xls", ".xlsx", ".ppt", ".pptx"
    ],
    "Audio": [
        ".mp3", ".wav", ".aac", ".ogg", ".flac"
    ],
    "Videos": [
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".webm"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz"
    ]
}


def get_file_category(filename):
    extension = os.path.splitext(filename)[1].lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/organize", methods=["POST"])
def organize_files():

    files = request.files.getlist("files")

    if not files:
        return jsonify({
            "success": False,
            "message": "No files selected.",
            "categories": {
                "Images": 0,
                "Documents": 0,
                "Audio": 0,
                "Videos": 0,
                "Archives": 0,
                "Others": 0
            }
        })

    category_counts = {
        "Images": 0,
        "Documents": 0,
        "Audio": 0,
        "Videos": 0,
        "Archives": 0,
        "Others": 0
    }

    upload_folder = "organized_files"

    os.makedirs(upload_folder, exist_ok=True)

    for file in files:

        if file.filename == "":
            continue

        category = get_file_category(file.filename)

        category_counts[category] += 1

        category_folder = os.path.join(
            upload_folder,
            category
        )

        os.makedirs(category_folder, exist_ok=True)

        file_path = os.path.join(
            category_folder,
            file.filename
        )

        file.save(file_path)

    total_files = sum(category_counts.values())

    return jsonify({
        "success": True,
        "message": f"{total_files} file(s) organized successfully!",
        "categories": category_counts
    })


if __name__ == "__main__":
    app.run(debug=True)