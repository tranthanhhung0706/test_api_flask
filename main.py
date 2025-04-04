import os
from flask import Flask, request, jsonify
from docling.document_converter import DocumentConverter

app = Flask(__name__)
converter = DocumentConverter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Tạo thư mục nếu chưa có

@app.route("/convert", methods=["POST"])
def convert_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)

    # Lưu file vào thư mục tạm
    pdf_file.save(file_path)

    try:
        # Chuyển đổi PDF
        result = converter.convert(file_path)
        document = result.document

        # Xuất các định dạng
        markdown_output = document.export_to_markdown()
        json_output = document.export_to_dict()
        text_output = document.export_to_text()

        return jsonify({
            "markdown": markdown_output,
            "json": json_output,
            "text": text_output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Xóa file sau khi xử lý xong
        if os.path.exists(file_path):
            os.remove(file_path)

# if __name__ == "__main__":
#     app.run(debug=True)
