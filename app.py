from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ข้อมูลแมวตัวอย่าง
cats_data = {
    'ชื่อ': ['แมวน้อย', 'มิว', 'โบ', 'ซันนี่', 'ลูซี'],
    'อายุ': [1, 2, 3, 4, 5],
    'พันธุ์': ['เปอร์เซีย', 'ไทย', 'สก็อตติชโฟลด์', 'เบงกอล', 'แร็กดอลล์'],
    'สีขน': ['ขาว', 'ดำ', 'เทา', 'ลายเสือ', 'น้ำตาล'],
    'น้ำหนัก': [3.5, 4.0, 5.5, 6.0, 4.5],
    'กิจกรรม': ['ชอบเล่น', 'ชอบนอน', 'ชอบกิน', 'ชอบปีน', 'ชอบสำรวจ']
}
cats_df = pd.DataFrame(cats_data)

# Fitness Function
def fitness_function(cat, user_preferences):
    weights = {
        'อายุ': 0.2,
        'พันธุ์': 0.3,
        'สีขน': 0.1,
        'น้ำหนัก': 0.2,
        'กิจกรรม': 0.2
    }
    fitness = 0
    for feature, weight in weights.items():
        if feature == 'พันธุ์' or feature == 'สีขน' or feature == 'กิจกรรม':
            if cat[feature] == user_preferences[feature]:
                fitness += weight
        else:
            fitness += weight * (1 - abs(cat[feature] - user_preferences[feature]) / max(cat[feature], user_preferences[feature]))
    return fitness

# Genetic Algorithm
def genetic_algorithm(cats_df, user_preferences, population_size=5, generations=10):
    population = cats_df.to_dict('records')
    for generation in range(generations):
        fitness_scores = [fitness_function(cat, user_preferences) for cat in population]
        parents = []
        for _ in range(2):
            max_index = fitness_scores.index(max(fitness_scores))
            parents.append(population[max_index])
            fitness_scores[max_index] = -1
        child = {}
        for feature in population[0].keys():
            if random.random() < 0.5:
                child[feature] = parents[0][feature]
            else:
                child[feature] = parents[1][feature]
        if random.random() < 0.1:
            feature_to_mutate = random.choice(list(child.keys()))
            if feature_to_mutate == 'อายุ':
                child[feature_to_mutate] = random.randint(1, 10)
            elif feature_to_mutate == 'น้ำหนัก':
                child[feature_to_mutate] = round(random.uniform(2.0, 7.0), 1)
            elif feature_to_mutate == 'พันธุ์':
                child[feature_to_mutate] = random.choice(['เปอร์เซีย', 'ไทย', 'สก็อตติชโฟลด์', 'เบงกอล', 'แร็กดอลล์'])
            elif feature_to_mutate == 'สีขน':
                child[feature_to_mutate] = random.choice(['ขาว', 'ดำ', 'เทา', 'ลายเสือ', 'น้ำตาล'])
            elif feature_to_mutate == 'กิจกรรม':
                child[feature_to_mutate] = random.choice(['ชอบเล่น', 'ชอบนอน', 'ชอบกิน', 'ชอบปีน', 'ชอบสำรวจ'])
        population.append(child)
    best_cat = max(population, key=lambda cat: fitness_function(cat, user_preferences))
    return best_cat

# หน้าแรก
@app.route('/')
def index():
    return render_template('index.html')

# หน้าสร้างรุ่น
@app.route('/create_model', methods=['GET', 'POST'])
def create_model():
    if request.method == 'POST':
        user_preferences = {
            'อายุ': int(request.form['age']),
            'พันธุ์': request.form['breed'],
            'สีขน': request.form['color'],
            'น้ำหนัก': float(request.form['weight']),
            'กิจกรรม': request.form['activity']
        }
        session['user_preferences'] = user_preferences
        return redirect(url_for('progress'))
    return render_template('create_model.html')

# หน้าการติดตามความคืบหน้า
@app.route('/progress')
def progress():
    if 'user_preferences' not in session:
        return redirect(url_for('create_model'))
    user_preferences = session['user_preferences']
    best_cat = genetic_algorithm(cats_df, user_preferences)
    session['best_cat'] = best_cat
    return render_template('progress.html', best_cat=best_cat)

# หน้าแสดงผลลัพธ์
@app.route('/result')
def result():
    if 'best_cat' not in session:
        return redirect(url_for('create_model'))
    best_cat = session['best_cat']
    return render_template('result.html', best_cat=best_cat)

if __name__ == '__main__':
    app.run(debug=True)