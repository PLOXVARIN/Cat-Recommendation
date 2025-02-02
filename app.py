from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
import io
import base64


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ข้อมูลแมวตัวอย่าง
cats_data = {
    'อายุ': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
    'พันธุ์': ['สก็อตติชโฟลด์', 'เมนคูน', 'เบงกอล', 'อะบิสซิเนียน', 'เปอร์เซีย', 
        'ไทย', 'โซมาเลีย', 'อเมริกันช็อตแฮร์', 'บริติชช็อตแฮร์', 'แร็กดอลล์'],
    'สีขน': ['ขาว', 'น้ำตาล', 'ลายเสือ', 'ดำ', 'เทาเงิน', 
        'ส้มขาว', 'ลายจุด', 'น้ำตาลแดง', 'ดำขาว', 'เทา'],
    'ลักษณะนิสัย': ['รักความสะอาด', 'ขี้เล่นและซุกซน', 'ขี้อ้อน', 'รักอิสระ', 'ฉลาด', 
                'ชอบล่าเหยื่อ', 'นอนหลับเยอะ', 'แสดงความรัก', 'สื่อสารด้วยเสียงร้อง', 'กินอาหารเป็นเวลา'],
    'กิจกรรม': ['ชอบดูทีวี', 'ชอบนอนตากแดด', 'ชอบไล่จับแมลง', 'ชอบเล่นของเล่น', 'ชอบสำรวจ',
        'ชอบปีนต้นไม้', 'ชอบขุดทราย', 'ชอบวิ่งไล่แสง', 'ชอบซ่อนตัว', 'ชอบเล่นน้ำ']
}
cats_df = pd.DataFrame(cats_data)

# Fitness Function
def fitness_function(cat, user_preferences):
    weights = {
        'อายุ': 0.2,
        'พันธุ์': 0.3,
        'สีขน': 0.1,
        'ลักษณะนิสัย': 0.2,
        'กิจกรรม': 0.2
    }
    fitness = 0
    for feature, weight in weights.items():
        if feature == 'พันธุ์' or feature == 'สีขน' or feature == 'กิจกรรม' or feature == 'ลักษณะนิสัย':
            if cat[feature] == user_preferences[feature]:
                fitness += weight
        else:
            fitness += weight * (1 - abs(cat[feature] - user_preferences[feature]) / max(cat[feature], user_preferences[feature]))
    return fitness

# Genetic Algorithm
def genetic_algorithm(cats_df, user_preferences, population_size=5, generations=10):
    population = cats_df.to_dict('records')
    performance_data = {
        'generation': [],
        'max_fitness': [],
        'avg_fitness': [],
        'processing_time': []
    }
    
    for generation in range(generations):
        start_time = time.time()  # เริ่มจับเวลา
        
        # คำนวณ Fitness
        fitness_scores = [fitness_function(cat, user_preferences) for cat in population]
        max_fitness = max(fitness_scores)
        avg_fitness = sum(fitness_scores) / len(fitness_scores)
        
        # เลือกพ่อแม่พันธุ์ (Selection)
        parents = []
        for _ in range(2):
            max_index = fitness_scores.index(max(fitness_scores))
            parents.append(population[max_index])
            fitness_scores[max_index] = -1
        
        # สร้างลูกผสม (Crossover)
        child = {}
        for feature in population[0].keys():
            if random.random() < 0.5:
                child[feature] = parents[0][feature]
            else:
                child[feature] = parents[1][feature]
        
        # Mutation
        if random.random() < 0.1:
            feature_to_mutate = random.choice(list(child.keys()))
            if feature_to_mutate == 'อายุ':
                child[feature_to_mutate] = random.randint(1, 5)
            elif feature_to_mutate == 'ลักษณะนิสัย':
                child[feature_to_mutate] = random.choice(['รักความสะอาด', 'ขี้เล่นและซุกซน', 'ขี้อ้อน', 'รักอิสระ', 'ฉลาด', 'ชอบล่าเหยื่อ', 'นอนหลับเยอะ', 'แสดงความรัก', 'สื่อสารด้วยเสียงร้อง', 'กินอาหารเป็นเวลา'])
            elif feature_to_mutate == 'พันธุ์':
                child[feature_to_mutate] = random.choice(['สก็อตติชโฟลด์', 'เมนคูน', 'เบงกอล', 'อะบิสซิเนียน', 'เปอร์เซีย','ไทย', 'โซมาเลีย', 'อเมริกันช็อตแฮร์', 'บริติชช็อตแฮร์', 'แร็กดอลล์'])
            elif feature_to_mutate == 'สีขน':
                child[feature_to_mutate] = random.choice(['ขาว', 'น้ำตาล', 'ลายเสือ', 'ดำ', 'เทาเงิน', 'ส้มขาว', 'ลายจุด', 'น้ำตาลแดง', 'ดำขาว', 'เทา'])
            elif feature_to_mutate == 'กิจกรรม':
                child[feature_to_mutate] = random.choice(['ชอบดูทีวี', 'ชอบนอนตากแดด', 'ชอบไล่จับแมลง', 'ชอบเล่นของเล่น', 'ชอบสำรวจ', 'ชอบปีนต้นไม้', 'ชอบขุดทราย', 'ชอบวิ่งไล่แสง', 'ชอบซ่อนตัว', 'ชอบเล่นน้ำ'])
        
        # แทนที่ประชากรเดิม (Replacement)
        population.append(child)
        
        # จับเวลาและเก็บข้อมูลประสิทธิภาพ
        processing_time = time.time() - start_time
        performance_data['generation'].append(generation + 1)
        performance_data['max_fitness'].append(max_fitness)
        performance_data['avg_fitness'].append(avg_fitness)
        performance_data['processing_time'].append(processing_time)
    
    best_cat = max(population, key=lambda cat: fitness_function(cat, user_preferences))
    return best_cat, performance_data

def plot_performance(performance_data):
    plt.figure(figsize=(10, 6))
    
    # กราฟค่าความเหมาะสมสูงสุดและค่าเฉลี่ย
    plt.plot(performance_data['generation'], performance_data['max_fitness'], label='Max Fitness', marker='o')
    plt.plot(performance_data['generation'], performance_data['avg_fitness'], label='Average Fitness', marker='x')
    
    plt.title('Genetic Algorithm Performance')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    
    # แปลงกราฟเป็นรูปภาพ Base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    
    return image_base64

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
            'ลักษณะนิสัย': request.form['personality'],
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
    best_cat, performance_data = genetic_algorithm(cats_df, user_preferences)
    session['best_cat'] = best_cat
    
    # สร้างกราฟ
    graph_image = plot_performance(performance_data)
    
    return render_template('progress.html', best_cat=best_cat, performance_data=performance_data, graph_image=graph_image)


# หน้าแสดงผลลัพธ์
@app.route('/find_new_cat', methods=['GET'])
def find_new_cat():
    # ใช้ข้อมูลเดิมใน session เพื่อค้นหาแมวใหม่
    if 'user_preferences' in session:
        user_preferences = session['user_preferences']
        best_cat = genetic_algorithm(cats_df, user_preferences)
        session['best_cat'] = best_cat  # เก็บผลลัพธ์ใหม่ใน session
    return redirect(url_for('result'))

@app.route('/result')
def result():
    if 'best_cat' not in session:
        return redirect(url_for('create_model'))
    best_cat = session['best_cat']
    return render_template('result.html', best_cat=best_cat)

if __name__ == '__main__':
    app.run(debug=True)
