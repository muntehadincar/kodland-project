from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam.db'  
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    highest_score = db.Column(db.Integer, default=0)
    
class ExamResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer, nullable=False)

class Question(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.String(255), nullable=False)
    option_a=db.Column(db.String(100), nullable=False)
    option_b=db.Column(db.String(100), nullable=False)
    option_c=db.Column(db.String(100), nullable=False)
    option_d=db.Column(db.String(100), nullable=False)
    correct_option=db.Column(db.String(1), nullable=False)

with app.app_context():
    questions = [
        # Discord.py Sorusu
        Question(
            text="Discord.py kullanarak bir bot oluşturmak için hangi nesne kullanılır?",
            option_a="Bot()",
            option_b="Client()",
            option_c="DiscordBot()",
            option_d="Command()",
            correct_option="B"
        ),
        # Flask Sorusu
        Question(
            text="Flask’te bir route tanımlamak için hangi dekoratör kullanılır?",
            option_a="@route",
            option_b="@flask.route",
            option_c="@app.route",
            option_d="@url.route",
            correct_option="C"
        ),
        # Yapay Zeka Sorusu
        Question(
            text="Bir yapay zeka modelini eğitmek için en çok kullanılan Python kütüphanelerinden biri nedir?",
            option_a="NumPy",
            option_b="Scikit-learn",
            option_c="Requests",
            option_d="Matplotlib",
            correct_option="B"
        ),
        # TensorFlow ve ImageAI Sorusu
        Question(
            text="TensorFlow ve ImageAI hangi alanla ilgilidir?",
            option_a="Doğal Dil İşleme",
            option_b="Veri Tabanı Yönetimi",
            option_c="Bilgisayar Görüşü",
            option_d="Web Geliştirme",
            correct_option="C"
        ),
        # BeautifulSoup Sorusu
        Question(
            text="Python'da BeautifulSoup kütüphanesi ne için kullanılır?",
            option_a="Web Scraping",
            option_b="Makine Öğrenmesi",
            option_c="Oyun Geliştirme",
            option_d="Veritabanı Yönetimi",
            correct_option="A"
        ),
        # Discord.py Bot Özellik Sorusu
        Question(
            text="Discord.py botunda bir komut çalıştırmak için hangi decorator kullanılır?",
            option_a="@client.command",
            option_b="@bot.command",
            option_c="@command",
            option_d="@message.command",
            correct_option="B"
        ),
        # Flask ve Veritabanı Sorusu
        Question(
            text="Flask uygulamasında veritabanı bağlantısı nasıl yapılır?",
            option_a="db.create_all()",
            option_b="db.init_app(app)",
            option_c="app.run()",
            option_d="None of the above",
            correct_option="B"
        ),
        # Yapay Zeka ve Regresyon Sorusu
        Question(
            text="Python'da bir regresyon problemi çözmek için hangi kütüphane sıklıkla kullanılır?",
            option_a="TensorFlow",
            option_b="NumPy",
            option_c="Scikit-learn",
            option_d="Flask",
            correct_option="C"
        ),
        # Bilgisayar Görüşü ve Model Eğitimi Sorusu
        Question(
            text="Bilgisayar görüşü (Computer Vision) için en popüler derin öğrenme kütüphanesi hangisidir?",
            option_a="OpenCV",
            option_b="Pillow",
            option_c="Keras",
            option_d="TensorFlow",
            correct_option="D"
        ),
        # Doğal Dil İşleme Sorusu
        Question(
            text="NLTK kütüphanesinde hangi işlev, metni kelimelere ayırmak için kullanılır?",
            option_a="nltk.sent_tokenize()",
            option_b="nltk.word_tokenize()",
            option_c="nltk.pos_tag()",
            option_d="nltk.stem()",
            correct_option="B"
        ),
    ]

    db.session.bulk_save_objects(questions)
    db.session.commit()

    db.create_all()  

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/exam', methods=['GET', 'POST'])
def exam():
    questions = Question.query.limit(10).all()
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        score = 0
        
        for question in questions:
            selected_option = request.form.get(f"q{question.id}")  
            if selected_option == question.correct_option: 
                score+=1
        exam_result = ExamResult(user_id=user.id, score=score)
        db.session.add(exam_result)

        if score > user.highest_score:
            user.highest_score = score
        
        db.session.commit()
        
        return redirect(url_for('result', username=username, score=score))

    return render_template('exam.html', questions=questions)

@app.route('/result')
def result():
    username = request.args.get('username')
    score = request.args.get('score', type=int)
    user = User.query.filter_by(username=username).first()

    if user:
        highest_score = user.highest_score
    else:
        highest_score = 0

    all_time_high_score = db.session.query(db.func.max(User.highest_score)).scalar()

    return render_template('result.html', username=username, score=score, highest_score=highest_score, all_time_high_score=all_time_high_score)

@app.route('/save_username', methods=['POST'])
def save_username():
    data = request.get_json()
    username = data.get('username')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True) 
