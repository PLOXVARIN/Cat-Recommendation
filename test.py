import pandas as pd
import random

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
    
    print("ประชากรเริ่มต้น:")
    for i, cat in enumerate(population):
        print(f"แมวที่ {i+1}: {cat}")
    
    for generation in range(generations):
        print(f"\n=== รุ่นที่ {generation+1} ===")
        
        # คำนวณ Fitness
        fitness_scores = [fitness_function(cat, user_preferences) for cat in population]
        
        print("\nค่าความเหมาะสมของแต่ละแมว:")
        for i, fitness in enumerate(fitness_scores):
            print(f"แมวที่ {i+1}: {fitness}")
        
        # เลือกพ่อแม่พันธุ์ (Selection)
        parents = []
        for _ in range(2):
            max_index = fitness_scores.index(max(fitness_scores))
            parents.append(population[max_index])
            fitness_scores[max_index] = -1
        
        print("\nเลือกพ่อแม่พันธุ์:")
        for i, parent in enumerate(parents):
            print(f"พ่อแม่พันธุ์ที่ {i+1}: {parent}")
        
        # สร้างลูกผสม (Crossover)
        child = {}
        for feature in population[0].keys():
            if random.random() < 0.5:
                child[feature] = parents[0][feature]
            else:
                child[feature] = parents[1][feature]
        
        print("\nสร้างลูกผสม:")
        print(f"ลูกผสม: {child}")
        
        # Mutation
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
            
            print(f"\nเกิดการกลายพันธุ์ที่คุณลักษณะ: {feature_to_mutate}")
            print(f"ลูกผสมหลังการกลายพันธุ์: {child}")
        
        # แทนที่ประชากรเดิม (Replacement)
        population.append(child)
        
        print("\nประชากรใหม่:")
        for i, cat in enumerate(population):
            print(f"แมวที่ {i+1}: {cat}")
    
    # คืนค่าแมวที่เหมาะสมที่สุด
    best_cat = max(population, key=lambda cat: fitness_function(cat, user_preferences))
    print(f"\nแมวที่เหมาะที่สุด: {best_cat}")
    return best_cat

# ข้อมูลความชอบของผู้ใช้
user_preferences = {
    'อายุ': 3,
    'พันธุ์': 'ไทย',
    'สีขน': 'ดำ',
    'น้ำหนัก': 4.0,
    'กิจกรรม': 'ชอบเล่น'
}

# เรียกใช้ Genetic Algorithm
print("เริ่มทำงาน Genetic Algorithm")
best_cat = genetic_algorithm(cats_df, user_preferences)
print("การทำงานเสร็จสิ้น")