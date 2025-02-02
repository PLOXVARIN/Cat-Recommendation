import pandas as pd
import random

# ข้อมูลแมวตัวอย่าง
cats_data = {
    'อายุ': [1, 2, 3, 4, 5,1, 2, 3, 4, 5],
    'พันธุ์': ['สก็อตติชโฟลด์', 'เมนคูน', 'เบงกอล', 'อะบิสซิเนียน', 'เปอร์เซีย', 
        'ไทย', 'โซมาเลีย', 'อเมริกันช็อตแฮร์', 'บริติชช็อตแฮร์', 'แร็กดอลล์',
        ],
    'สีขน': ['ขาว', 'น้ำตาล', 'ลายเสือ', 'ดำ', 'เทาเงิน', 
        'ส้มขาว', 'ลายจุด', 'น้ำตาลแดง', 'ดำขาว', 'เทา',
        ],
    'ลักษณะนิสัย': ['รักความสะอาด' ,'ขี้เล่นและซุกซน' ,'ขี้อ้อน' ,'รักอิสระ'  ,'ฉลาด' ,
                'ชอบล่าเหยื่อ' ,'นอนหลับเยอะ' ,'แสดงความรัก' ,'สื่อสารด้วยเสียงร้อง' ,'กินอาหารเป็นเวลา'],
    'กิจกรรม': [ 'ชอบดูทีวี', 'ชอบนอนตากแดด', 'ชอบไล่จับแมลง', 'ชอบเล่นของเล่น', 'ชอบสำรวจ',
        'ชอบปีนต้นไม้', 'ชอบขุดทราย', 'ชอบวิ่งไล่แสง', 'ชอบซ่อนตัว', 'ชอบเล่นน้ำ',
        ]
}
cats_df = pd.DataFrame(cats_data)

# Fitness Function
def fitness_function(cat, user_preferences):
    weights = {
        'อายุ': 0.2,
        'พันธุ์': 0.2,
        'สีขน': 0.1,
        'ลักษณะนิสัย': 0.2,
        'กิจกรรม': 0.2
    }
    fitness = 0
    for feature, weight in weights.items():
        if feature in ['พันธุ์', 'สีขน', 'กิจกรรม', 'ลักษณะนิสัย']:  
            if cat[feature] == user_preferences[feature]:  
                fitness += weight  
        else:
            fitness += weight * (1 - abs(cat[feature] - user_preferences[feature]) / max(cat[feature], user_preferences[feature]))
    return fitness

# Genetic Algorithm
def genetic_algorithm(cats_df, user_preferences, population_size=5, generations=100):
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
                child[feature_to_mutate] = random.randint(1, 5)
            elif feature_to_mutate == 'ลักษณะนิสัย':
                child[feature_to_mutate] = random.choice(['รักความสะอาด' ,'ขี้เล่นและซุกซน' ,'ขี้อ้อน' ,'รักอิสระ'  ,'ฉลาด' ,'ชอบล่าเหยื่อ' ,'นอนหลับเยอะ' ,'แสดงความรัก' ,'สื่อสารด้วยเสียงร้อง' ,'กินอาหารเป็นเวลา'])
            elif feature_to_mutate == 'พันธุ์':
                child[feature_to_mutate] = random.choice(['สก็อตติชโฟลด์', 'เมนคูน', 'เบงกอล', 'อะบิสซิเนียน', 'เปอร์เซีย','ไทย', 'โซมาเลีย', 'อเมริกันช็อตแฮร์', 'บริติชช็อตแฮร์', 'แร็กดอลล์',])
            elif feature_to_mutate == 'สีขน':
                child[feature_to_mutate] = random.choice(['ขาว', 'น้ำตาล', 'ลายเสือ', 'ดำ', 'เทาเงิน', 
        'ส้มขาว', 'ลายจุด', 'น้ำตาลแดง', 'ดำขาว', 'เทา',])
            elif feature_to_mutate == 'กิจกรรม':
                child[feature_to_mutate] = random.choice(['ชอบดูทีวี', 'ชอบนอนตากแดด', 'ชอบไล่จับแมลง', 'ชอบเล่นของเล่น', 'ชอบสำรวจ','ชอบปีนต้นไม้', 'ชอบขุดทราย', 'ชอบวิ่งไล่แสง', 'ชอบซ่อนตัว', 'ชอบเล่นน้ำ'])
            
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
    'อายุ': 2,
    'พันธุ์': 'ไทย',
    'สีขน': 'ดำ',
    'ลักษณะนิสัย': 'ขี้เล่นและซุกซน',  # เปลี่ยนเป็นลักษณะนิสัยแทนตัวเลข
    'กิจกรรม': 'ชอบนอนตากแดด'
}

# เรียกใช้ Genetic Algorithm
print("เริ่มทำงาน Genetic Algorithm")
best_cat = genetic_algorithm(cats_df, user_preferences)
print("การทำงานเสร็จสิ้น")
