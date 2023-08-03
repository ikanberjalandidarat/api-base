from flask import Flask, request, jsonify
from fuzzywuzzy import fuzz

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def classify_review(review_text):

    # Function to classify the review text
    threshold = 88
    categories = {
        "Connection Issue": ["ngelag", "gamenya ngelag", "gamenya pecah",	"disconnect", "diskonek", "disconnect",	"ngelag", "sinyal", "sinyal lag", "gak stabil", "tiba tiba lag", "suka lag", "jaringan", "koneksi"],
        "Lost Account": ["Reset",	"Riset",	"Hilang",	  "rollback",	"akun hilang",	"akun ilang", "akun gue ilang"],
        "Graphic Issues": ["graphic", "gambar", "Patah",	"Slowmo", "Slow",	"Burik",	"smooth", "grafik rendah"],
        "Too similar to competitors": ["FIFA",	"PES",	"Efootball",	"DLS",	"Plagiat",	"Copy", "niru"],
        "Offline Mode": ["Offline", 	"Ofline"],
        "Freeze": ["Freeze",	"ngefreeze",	"ga gerak",	"tidak gerak",	"tidak bergerak",	"diem", "diam",	"ngeframe"],
        "Matchmaking": ["ga nemu lawan",	"ga ada lawan",	"lawan ga balance", "lawan ga adil", "lawak tidak adil"],
        "License": ["Lisensi",	"License",	"Official",	"Resmi",	"ofisiel"],
        "Bug/Error": ["Bug",	"Error",	"Bermasalah",	"ngebug",	"Bugs",	"Masalah", "Server kendala", "kendala"],
        "Failed Install": ["Install",	"Download",	"gabisa main",	"gagal install",	"gagal download", "ga bisa download", "ga bisa install",	"gagal main",	"gagal"],
        "Game Size": ["size",	"ukuran",	"berat",	"gak cukup", "gak muat", "ga kuat", "penyimpanan", "storage"],
        "Local Content": ["Komentator",	"Commentary",	"Narration",	"Narator",	"Lokal",	"Suara komentator", "pemain indo", "pemain lokal", "pemain indonesia"],
        "Cannot enter to the game": ["nyangkut", "diam di lobby", "layar hitam", "loading", "crash", "stuck", "lama login", "lama loading", "ga bisa login"],
        "Improve the game": ["tingkatkan", "tingkatin", "grafik", "optimisasi", "optimal", "yang bener"],
        "Realistic": ["realistik", "realistik", "robot", "kaku", "animasi", "gak realistik"],
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            similarity = fuzz.partial_ratio(review_text.lower(), keyword.lower())
            if similarity >= threshold:
                return category

    return "Others"  # Return a default category if no match is found

@app.route('/classify_review', methods=['POST'])
def classify_review_endpoint():
    # Get the review text from the request
    review_text = request.json.get('review_text')
    if not review_text:
        return jsonify(error="Review text not provided"), 400

    # Call the classify_review function to get the category
    category = classify_review(review_text)

    return jsonify(category=category)

if __name__ == '__main__':
    app.run(debug=True)
