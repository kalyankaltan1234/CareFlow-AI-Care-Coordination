import difflib
import re
from typing import Optional, Dict, Any, List

DISEASES_DB: Dict[str, Dict[str, Any]] = {
    "fever": {
        "name": "Fever (Pyrexia / Viral Infection)",
        "aliases": ["fever", "fevor", "fevr", "feveer", "temperature", "chills", "high temp", "feverish", "pyrexia"],
        "category": "Infectious & General Illness",
        "specialist": "Dr. Verma (General Medicine)",
        "symptoms": [
            "Body temperature rising above 98.6°F (37°C), often 100°F–102°F in mild to moderate cases",
            "Shivering, cold chills, and body tremors",
            "Generalized muscular body aches, joint fatigue, and physical weakness",
            "Excessive sweating and episodic hot flushes",
            "Mild headache, heavy eyes, and loss of appetite",
            "Dehydration and dry mouth"
        ],
        "precautions": [
            "Measure and log body temperature every 4 hours using a calibrated digital thermometer.",
            "Maintain high fluid intake: drink 2.5 to 3 liters of fluids daily (warm water, electrolytes, coconut water, clear broths).",
            "Ensure full bed rest in a well-ventilated, quiet room.",
            "Wear light, loose, breathable cotton garments — avoid heavy winter clothing if feeling hot.",
            "Apply lukewarm water sponge baths across the forehead, neck, and armpits if temperature exceeds 101°F."
        ],
        "medications": [
            " **Primary Antipyretic / Pain Relief**: **Paracetamol (Acetaminophen) 500mg or 650mg** (e.g. Dolo 650, Calpol, Tylenol). Take 1 tablet every 6 to 8 hours after food as needed. (Maximum adult limit: 3,000 mg in 24 hours).",
            " **Electrolyte & Hydration**: **Oral Rehydration Salts (ORS / Electral)** — Dissolve 1 sachet in 1 liter of clean drinking water and sip throughout the day to replenish sodium, potassium, and glucose.",
            " **Herbal / Supportive**: Warm ginger-tulsi tea or vitamin C supplements (500mg daily) to boost immune defense.",
            " **Medication Caution**: Do NOT combine multiple cold/cough syrups that already contain paracetamol to prevent accidental liver overdose. Avoid aspirin or ibuprofen until viral infections like Dengue are excluded."
        ],
        "what_to_avoid": [
            "Do NOT take ice-cold water or cold baths, as shivering forces internal body temperature higher.",
            "Do NOT self-prescribe unapproved antibiotics without a doctor's blood test.",
            "Avoid strenuous workouts, gym, sports, or heavy lifting until completely recovered.",
            "Avoid dehydrating beverages: high-sugar sodas, alcohol, and excessive coffee.",
            "Avoid skipping meals; consume easily digestible soups, khichdi, or porridge."
        ],
        "red_flags": [
            "Temperature spikes above 103°F (39.4°C) or does not reduce with standard paracetamol.",
            "Fever persists continuously for more than 72 consecutive hours (3 days).",
            "Accompanied by stiff neck, confusion, breathing difficulty, or purple petechial skin rashes.",
            "Persistent vomiting preventing fluid retention for over 12 hours."
        ],
        "doctor_schedule": "Dr. Verma (General Medicine) • Available Today at 11:30 AM & 03:00 PM"
    },
    "back_pain": {
            "name": "Back Pain (Lumbar Strain / Sciatica / Musculoskeletal)",
            "aliases": ["backpain", "back pain", "lower back pain", "lumbago", "sciatica", "spine pain", "slip disc", "lumbar", "back ache", "backache", "spine", "back stiffness", "lower back"],
            "category": "Musculoskeletal & Spine Disorders",
            "specialist": "Dr. Sanjay Kapoor (Orthopedics & Spine Care)",
            "symptoms": [
                "Dull, aching, or sharp piercing pain localized in the lower back (lumbar region)",
                "Stiffness, reduced range of motion, and difficulty standing upright or bending",
                "Pain radiating downward into buttocks, thighs, or calf/foot (Sciatic nerve impingement)",
                "Muscle spasms and involuntary tightening in spinal muscles upon walking or lifting",
                "Increased discomfort after prolonged sitting or sleeping in unsupportive postures"
            ],
            "precautions": [
                "Apply cold ice packs wrapped in a towel for 15-20 minutes 3 times daily during the first 48 hours to minimize acute inflammation.",
                "Switch to warm compresses or moist heat pads after 48 hours to relieve muscle stiffness and spasms.",
                "Sleep on a medium-firm supportive mattress; place a pillow under your knees when sleeping on your back or between knees if sleeping on your side.",
                "Avoid complete bed rest beyond 24-48 hours; gentle walking and light mobility prevent muscle deconditioning.",
                "Maintain ergonomic sitting posture: keep feet flat on the floor, hips and knees at 90 degrees, with lumbar back support."
            ],
            "medications": [
                "💊 **First-Line Analgesic / Anti-inflammatory**: **Paracetamol (Acetaminophen) 650mg** (e.g. Dolo 650 / Tylenol) or **Ibuprofen 400mg** (taken strictly after meals) every 8 hours as needed to control pain and inflammation.",
                "💊 **Supportive Muscle Relaxant (for spasms)**: **Thiocolchicoside 4mg/8mg** or **Chlorzoxazone / Paracetamol combination** (under doctor prescription) if experiencing severe muscle spasms and locking.",
                "🧴 **Topical Analgesic Gel & Sprays**: Apply **Diclofenac Diethylamine Gel 1.16%** (e.g., Volini, Omnigel, Voltaren) gently over the lumbar area 3 to 4 times daily without vigorous rubbing.",
                "⚡ **Neuropathic / Nerve Care**: **Methylcobalamin (Vitamin B12 1500 mcg)** and **Pregabalin 75mg** (strictly under physician advice) if radiating numbness, burning, or tingling is present.",
                "⚠️ **Medication Caution**: Do not combine multiple NSAIDs (e.g., avoid taking Ibuprofen and Diclofenac simultaneously). Patients with stomach ulcers, acid reflux, or kidney disease should avoid oral NSAIDs and use topical gels or paracetamol instead."
            ],
            "what_to_avoid": [
                "STRICTLY AVOID heavy weight lifting, bending forward at the waist without bending your knees, or twisting while lifting.",
                "Avoid prolonged sitting for more than 45 minutes continuously — stand, stretch, and walk for 2 minutes every hour.",
                "Do NOT stay in bed for days; prolonged immobilization weakens core spinal muscles and prolongs recovery.",
                "Avoid sleeping on soft, sagging mattresses or sleeping on your stomach, which strains the lumbar curve.",
                "Avoid high-impact jumping, sudden jerking movements, or running until acute pain subsides."
            ],
            "red_flags": [
                "CAUDA EQUINA EMERGENCY: Sudden loss of bowel or bladder control, or numbness around the groin/genital area ('saddle anesthesia').",
                "Progressive muscle weakness, foot drop (inability to lift front of foot), or difficulty walking.",
                "Back pain accompanied by unexplained high fever, chills, or sudden unexplained weight loss.",
                "Constant severe pain that worsens significantly at night or when lying completely flat."
            ],
            "doctor_schedule": "Dr. Sanjay Kapoor (Orthopedics & Spine Care) • Available Today at 11:30 AM & 04:00 PM"
        },
        "covid": {
            "name": "COVID-19 (Coronavirus Viral Infection)",
            "aliases": ["covid", "covid19", "covid-19", "coronavirus", "sars-cov-2", "corona", "omicron"],
            "category": "Viral Respiratory Infection",
            "specialist": "Dr. Sneha Reddy (General Medicine / Pulmonology)",
            "symptoms": [
                "Fever, dry hacking cough, sore throat, and severe fatigue",
                "Sudden loss of taste (ageusia) or smell (anosmia)",
                "Generalized muscular body aches, headaches, and nasal congestion",
                "Shortness of breath or chest heaviness upon mild physical movement"
            ],
            "precautions": [
                "Self-isolate immediately in a well-ventilated single room to protect household members.",
                "Monitor blood oxygen saturation (SpO2) and pulse using a finger pulse oximeter every 4-6 hours.",
                "Drink at least 2.5 to 3 liters of warm water, oral rehydration solutions, and herbal broths daily.",
                "Perform steam inhalation for 10 minutes once or twice daily to relieve airway congestion.",
                "Wear a well-fitted N95 or surgical mask if you must interact with caregivers."
            ],
            "medications": [
                "💊 **Fever & Body Ache Control**: **Paracetamol 650mg** (e.g. Dolo 650 / Calpol) every 6 to 8 hours after meals. (Do not exceed 3000mg/day).",
                "🍊 **Immune Defense Supplements**: **Vitamin C (500mg)** once daily and **Zinc (50mg)** once daily after lunch for 7-10 days.",
                "🍬 **Throat & Cough Relief**: Warm saline water gargles 3 times daily; OTC throat lozenges or honey-based cough syrups.",
                "⚠️ **Medication Caution**: Do NOT self-prescribe oral steroids (Dexamethasone/Prednisolone) or broad-spectrum antibiotics (Azithromycin) during the early viral phase without a doctor's explicit prescription."
            ],
            "what_to_avoid": [
                "Do NOT engage in heavy workouts, gym training, or cardiovascular exercise while recovering.",
                "Avoid unverified cocktail treatments, unprescribed blood thinners, or high-dose steroids.",
                "Avoid cold, icy beverages, smoking, vaping, or exposure to secondhand smoke."
            ],
            "red_flags": [
                "Oxygen saturation (SpO2) drops consistently below 94% on room air.",
                "Persistent chest pressure, painful breathing, or bluish discoloration of lips/fingertips.",
                "New onset confusion, extreme drowsiness, or inability to stay awake."
            ],
            "doctor_schedule": "Dr. Sneha Reddy (General Medicine) • Available Today at 11:30 AM & 03:00 PM"
        },
        "flu": {
            "name": "Influenza (Seasonal Viral Flu)",
            "aliases": ["flu", "influenza", "viral flu", "swine flu", "h1n1", "seasonal flu"],
            "category": "Viral Respiratory Infection",
            "specialist": "Dr. Sneha Reddy (General Medicine)",
            "symptoms": [
                "Sudden abrupt onset of high fever (100°F–103°F) with shivering and shaking chills",
                "Severe generalized muscular body aches and joint stiffness",
                "Persistent dry cough, sore throat, and hoarseness",
                "Headache, retro-orbital eye burning, and extreme prostrating exhaustion"
            ],
            "precautions": [
                "Rest completely in bed for the first 3 to 5 days; avoid returning to work or school prematurely.",
                "Consume warm soups, herbal teas with honey, and electrolyte solutions continuously.",
                "Practice respiratory etiquette: cough into elbows and wash hands frequently."
            ],
            "medications": [
                "💊 **Antipyretic & Body Ache Relief**: **Paracetamol 650mg** every 6 to 8 hours after food as needed.",
                "💧 **Hydration & Electrolytes**: **ORS / Electral** sachet in 1L water to replenish fluids lost through sweating.",
                "🍬 **Throat Care**: Saltwater gargles and menthol lozenges.",
                "⚠️ **Medication Caution**: Avoid aspirin in teenagers and children due to the risk of Reye's syndrome."
            ],
            "what_to_avoid": [
                "Do not consume alcohol, caffeine, or ice-cold drinks.",
                "Avoid strenuous physical exertion until fever has subsided for at least 48 hours.",
                "Do not take antibiotics; influenza is caused by a virus."
            ],
            "red_flags": [
                "Difficulty breathing, rapid shallow breathing, or chest pain.",
                "Fever that temporarily resolves and then returns with a worsening cough and green phlegm.",
                "Inability to retain liquids due to persistent nausea."
            ],
            "doctor_schedule": "Dr. Sneha Reddy (General Medicine) • Available Today at 11:30 AM & 03:00 PM"
        },
        "pneumonia": {
            "name": "Pneumonia (Lower Respiratory Infection)",
            "aliases": ["pneumonia", "chest infection", "lung infection", "bronchopneumonia"],
            "category": "Pulmonary & Respiratory Infection",
            "specialist": "Dr. Farhan Akhtar (Pulmonology & Chest Medicine)",
            "symptoms": [
                "High fever, shaking chills, and profuse sweating",
                "Cough producing thick green, yellow, or rust-colored phlegm",
                "Sharp stabbing chest pain that worsens when breathing deeply or coughing (pleuritic pain)",
                "Shortness of breath, rapid shallow breathing, and fatigue"
            ],
            "precautions": [
                "Obtain a chest X-ray and complete blood count (CBC) promptly under clinical supervision.",
                "Monitor oxygen saturation (SpO2) every 3 to 4 hours.",
                "Perform gentle deep breathing exercises and spirometry as tolerated to clear secretions.",
                "Maintain high fluid intake to help thin pulmonary mucus."
            ],
            "medications": [
                "💊 **Prescription Antibiotic / Antiviral Therapy**: Must be prescribed by a physician based on sputum/blood evaluation (e.g. Amoxicillin-Clavulanate, Azithromycin, or Ceftriaxone). Take full prescribed course.",
                "💊 **Fever & Pain Relief**: **Paracetamol 650mg** for fever and pleuritic chest discomfort.",
                "💊 **Mucolytic / Expectorant**: **Guaifenesin or Acetylcysteine** syrups to loosen heavy chest mucus.",
                "⚠️ **Medication Caution**: Never stop antibiotic treatment early even if symptoms improve."
            ],
            "what_to_avoid": [
                "STRICTLY AVOID smoking, vaping, or exposure to wood smoke and kitchen fumes.",
                "Avoid cough suppressants that completely stop productive coughing, as phlegm clearance is necessary.",
                "Avoid heavy physical exertion until lungs are cleared on medical follow-up."
            ],
            "red_flags": [
                "SpO2 dropping below 93% or persistent shortness of breath at rest.",
                "Confusion or altered mental state, especially in elderly patients.",
                "Coughing up fresh blood or persistent drop in blood pressure."
            ],
            "doctor_schedule": "Dr. Farhan Akhtar (Pulmonology) • Available Today at 11:30 AM & 04:00 PM"
        },
        "bronchitis": {
            "name": "Bronchitis (Acute Bronchial Airway Inflammation)",
            "aliases": ["bronchitis", "chest cold", "acute bronchitis", "bronchial infection"],
            "category": "Respiratory Care",
            "specialist": "Dr. Farhan Akhtar (Pulmonology & Chest Medicine)",
            "symptoms": [
                "Persistent hacking cough that may produce clear, yellow, or green mucus",
                "Soreness or burning sensation behind the breastbone when coughing",
                "Mild shortness of breath, wheezing, and chest tightness",
                "Low-grade fever, runny nose, and generalized fatigue"
            ],
            "precautions": [
                "Use a cool-mist humidifier or take steamy showers to soothe irritated bronchial passages.",
                "Drink plenty of warm liquids (water, ginger tea, clear broths) to thin airway secretions.",
                "Get plenty of rest and avoid sudden shifts from warm to cold environments."
            ],
            "medications": [
                "💊 **Expectorant Syrup**: **Guaifenesin 200mg–400mg** every 4 hours with a full glass of water.",
                "💊 **Fever & Chest Discomfort Relief**: **Paracetamol 650mg** after meals as needed.",
                "🍬 **Bronchial Soothers**: Honey-based syrups or throat lozenges.",
                "⚠️ **Medication Caution**: Over 90% of acute bronchitis cases are viral; routine antibiotics are not indicated unless a secondary bacterial infection develops."
            ],
            "what_to_avoid": [
                "Avoid tobacco smoke, secondhand smoke, and chemical aerosols (cleaners, spray paint).",
                "Avoid cold, drafty rooms and strenuous outdoor exercise in cold dry air."
            ],
            "red_flags": [
                "Cough lasting longer than 3 weeks or repeatedly bringing up blood.",
                "High fever exceeding 102°F or significant difficulty breathing.",
                "Wheezing that prevents normal sleep or speaking."
            ],
            "doctor_schedule": "Dr. Farhan Akhtar (Pulmonology) • Available Today at 11:30 AM & 04:00 PM"
        },
        "diarrhea": {
            "name": "Acute Diarrhea & Gastroenteritis (Stomach Infection)",
            "aliases": ["diarrhea", "diarrhoea", "loose motions", "stomach infection", "gastroenteritis", "dysentery", "loose stools", "watery stools", "upset stomach"],
            "category": "Gastrointestinal & Digestive Health",
            "specialist": "Dr. Sandeep Singhania (Gastroenterology)",
            "symptoms": [
                "Frequent, loose, or watery bowel movements (more than 3 times in 24 hours)",
                "Abdominal cramping, intestinal gurgling, and bloating",
                "Nausea, episodic vomiting, and loss of appetite",
                "Dehydration: dry mouth, sunken eyes, dark urine, and lightheadedness"
            ],
            "precautions": [
                "Immediate oral hydration is the cornerstone of treatment: drink WHO-Formula ORS continuously.",
                "Follow the BRAT diet: Bananas, Rice, Applesauce, Toast, and light khichdi.",
                "Wash hands thoroughly with soap before meals and after using the restroom.",
                "Avoid preparing food for others while actively experiencing loose stools."
            ],
            "medications": [
                "💧 **Primary Rehydration (Essential)**: **WHO-Formula Oral Rehydration Salts (ORS)** — dissolve 1 sachet in 1 liter clean drinking water; drink 200-300ml after each loose stool.",
                "💊 **Probiotic Restoration**: **Bacillus clausii spores** (e.g. Enterogermina mini-bottles) or **Lactobacillus capsules** twice daily for 5 days to restore healthy gut microbiome.",
                "💊 **Zinc Supplementation**: **Zinc sulfate 20mg** daily for 10-14 days to reduce stool frequency and speed mucosal healing.",
                "💊 **Stomach Cramp Relief**: **Dicyclomine 10mg / 20mg** (under physician consultation) if severe abdominal spasms occur.",
                "⚠️ **Medication Caution**: Do NOT take anti-motility drugs (like Loperamide / Imodium) if you have high fever or blood in stool, as they prevent bacterial toxin clearance."
            ],
            "what_to_avoid": [
                "STRICTLY AVOID dairy products (milk, cheese), greasy fried foods, and raw salads during acute recovery.",
                "Avoid caffeinated coffee, carbonated sugary sodas, and alcohol, which worsen dehydration.",
                "Avoid unboiled tap water, street food, and ice cubes made from unverified water sources."
            ],
            "red_flags": [
                "Signs of severe dehydration: inability to urinate for over 8 hours, extreme dizziness, or fainting.",
                "Visible blood or black tarry material in the stool.",
                "High fever exceeding 102°F or continuous vomiting preventing oral fluid intake for >12 hours."
            ],
            "doctor_schedule": "Dr. Sandeep Singhania (Gastroenterology) • Available Today at 10:30 AM & 03:00 PM"
        },
        "tonsillitis": {
            "name": "Tonsillitis & Sore Throat (Pharyngeal Infection)",
            "aliases": ["tonsillitis", "sore throat", "throat infection", "pharyngitis", "throat pain", "swollen tonsils", "strep throat"],
            "category": "ENT & Upper Respiratory Infection",
            "specialist": "Dr. Sneha Reddy (General Medicine / ENT)",
            "symptoms": [
                "Painful, raw, scratching throat sensation that worsens significantly when swallowing",
                "Red, swollen tonsils, occasionally with white patches or streaks of pus",
                "Swollen, tender lymph nodes in the neck and jawline",
                "Fever, headache, muffled voice, and foul breath"
            ],
            "precautions": [
                "Gargle with warm salt water (1/2 teaspoon salt in 1 cup warm water) every 3 to 4 hours.",
                "Sip warm clear liquids such as lemon-honey tea, warm water, and soothing broths.",
                "Use a cool-air humidifier to prevent throat drying during sleep."
            ],
            "medications": [
                "💊 **Pain & Inflammation Relief**: **Paracetamol 650mg** or **Ibuprofen 400mg** after food every 8 hours as needed.",
                "🍬 **Throat Antiseptic Lozenges**: Amylmetacresol / Dichlorobenzyl alcohol lozenges (e.g. Strepsils) or Benzydamine throat spray for local numbing.",
                "⚠️ **Medication Caution**: If throat swab confirms Group A Streptococcus (Strep throat), a full 10-day course of prescribed oral Penicillin or Amoxicillin is required. Do not take leftover antibiotics without a doctor's test."
            ],
            "what_to_avoid": [
                "Avoid very crunchy, hard, sharp foods (chips, crackers, raw vegetables) that irritate the throat.",
                "Avoid smoking, spicy curries, and very acidic citrus drinks that trigger burning pain."
            ],
            "red_flags": [
                "Severe difficulty breathing or inability to swallow own saliva (drooling).",
                "Inability to fully open the mouth (trismus / peritonsillar abscess warning).",
                "Severe asymmetrical swelling of one tonsil pushing the uvula to the side."
            ],
            "doctor_schedule": "Dr. Sneha Reddy (General Medicine) • Available Today at 11:30 AM & 03:00 PM"
        },
        "sinusitis": {
            "name": "Sinusitis (Sinus Infection & Inflammation)",
            "aliases": ["sinus", "sinusitis", "sinus headache", "nasal congestion", "sinus infection", "facial pressure"],
            "category": "ENT & Sinus Disorders",
            "specialist": "Dr. Sneha Reddy (General Medicine / ENT)",
            "symptoms": [
                "Thick, discolored yellow or green nasal discharge or post-nasal drip",
                "Facial pain, pressure, and fullness around eyes, forehead, cheeks, and bridge of nose",
                "Headache and pain in the upper jaw and teeth that worsens when bending forward",
                "Stuffy blocked nose, reduced sense of smell, and ear fullness"
            ],
            "precautions": [
                "Perform saline nasal irrigation (using a neti pot or sinus rinse bottle with sterile distilled water) twice daily.",
                "Inhale steam from a bowl of hot water with a towel over your head for 10-15 minutes.",
                "Apply warm moist towels to your cheeks, eyes, and forehead to relieve facial pressure.",
                "Elevate your head while sleeping to encourage sinus drainage."
            ],
            "medications": [
                "🧴 **Nasal Saline Spray**: Isotonic or hypertonic sterile saline nasal spray used 3 to 4 times daily.",
                "💊 **Pain & Facial Pressure Relief**: **Paracetamol 650mg** or **Ibuprofen 400mg** after meals.",
                "🧴 **Short-Term Decongestant Spray**: **Oxymetazoline 0.05% nasal spray** (1-2 sprays per nostril) — STRICTLY LIMIT TO MAXIMUM 3 CONSECUTIVE DAYS to avoid rebound congestion (rhinitis medicamentosa).",
                "💊 **Allergy/Mucus Reducer**: **Levocetirizine 5mg + Montelukast 10mg** once daily at night if allergic rhinitis is the trigger."
            ],
            "what_to_avoid": [
                "Do NOT use OTC medicated decongestant nasal sprays for more than 3 consecutive days.",
                "Avoid chlorinated swimming pools, cigarette smoke, and dry unhumidified rooms.",
                "Avoid blowing your nose violently through both nostrils simultaneously; blow gently one nostril at a time."
            ],
            "red_flags": [
                "Swelling, redness, or pain around one or both eyes.",
                "Severe stiff neck, high fever, or confusion.",
                "Visual disturbances such as double vision or blurred vision."
            ],
            "doctor_schedule": "Dr. Sneha Reddy (General Medicine) • Available Today at 11:30 AM & 03:00 PM"
        },
        "chikungunya": {
            "name": "Chikungunya (Mosquito-Borne Viral Arthralgia)",
            "aliases": ["chikungunya", "chikunguniya", "viral joint pain"],
            "category": "Vector-Borne Viral Infection",
            "specialist": "Dr. Arvind Swamy (Infectious Diseases)",
            "symptoms": [
                "Sudden high fever accompanied by severe, debilitating joint pain (arthralgia)",
                "Joint swelling, stiffness, and tenderness primarily affecting hands, wrists, ankles, and feet",
                "Maculopapular rash appearing 2 to 5 days after fever onset",
                "Muscle pain, severe headache, and extreme fatigue"
            ],
            "precautions": [
                "Get an RT-PCR or Chikungunya IgM antibody test to confirm diagnosis.",
                "Ensure extensive bed rest; avoid putting high mechanical stress on painful joints.",
                "Apply cool compresses or cold packs wrapped in a cloth to inflamed joints for 15 minutes.",
                "Drink plenty of fluids (minimum 3 liters daily) to maintain renal hydration."
            ],
            "medications": [
                "💊 **First-Line Pain & Fever Relief**: **Paracetamol 650mg** every 6 to 8 hours after food. (Avoid NSAIDs until Dengue is ruled out).",
                "💧 **Electrolyte & Hydration**: Oral Rehydration Salts (ORS) and coconut water daily.",
                "⚠️ **Medication Caution**: Avoid Aspirin and Ibuprofen during initial days until Dengue co-infection has been ruled out by lab tests."
            ],
            "what_to_avoid": [
                "Avoid vigorous exercise, running, or heavy lifting while joint inflammation is acute.",
                "Do not consume excessive salt or sugar; eat light, anti-inflammatory meals."
            ],
            "red_flags": [
                "Severe intractable joint pain preventing any mobility.",
                "Extreme neurological symptoms such as confusion or severe lethargy.",
                "Co-infection signs like bleeding gums or sudden drop in platelet count."
            ],
            "doctor_schedule": "Dr. Arvind Swamy (Infectious Diseases) • Available Today at 11:00 AM & 03:30 PM"
        },
        "uti": {
            "name": "Urinary Tract Infection (UTI / Cystitis)",
            "aliases": ["uti", "urinary tract infection", "burning urination", "urine infection", "cystitis", "painful urination"],
            "category": "Urological Infection",
            "specialist": "Dr. Pradeep Chawla (Urology & Renal Care)",
            "symptoms": [
                "Strong, persistent burning or stinging sensation during urination (dysuria)",
                "Frequent or urgent need to urinate, often passing only small amounts of urine",
                "Urine that appears cloudy, dark, bloody, or has a strong pungent odor",
                "Pelvic pressure and lower abdominal cramping"
            ],
            "precautions": [
                "Drink plenty of water (at least 3 liters daily) to flush bacteria out of the urinary tract.",
                "Urinate frequently and empty your bladder completely; do not hold urine.",
                "Wipe from front to back after using the bathroom to avoid spreading bacteria.",
                "Wear loose, breathable cotton underwear and avoid tight synthetic pants."
            ],
            "medications": [
                "💊 **Prescription Antibiotic**: Requires a urine routine & culture test. Standard first-line antibiotics (e.g. Nitrofurantoin 100mg twice daily or Fosfomycin 3g single dose) prescribed by a physician. Complete the full course.",
                "💊 **Urinary Analgesic (for burning)**: **Phenazopyridine 100mg–200mg** (short-term for 2 days) or **Disodium hydrogen citrate syrup** (alkalizer) in a glass of water to reduce urine acidity and stinging.",
                "💊 **Pain Relief**: **Paracetamol 650mg** for pelvic and abdominal discomfort.",
                "⚠️ **Medication Caution**: Note that Phenazopyridine turns urine a bright orange/red color, which is a normal harmless side effect."
            ],
            "what_to_avoid": [
                "Avoid holding urine for extended periods.",
                "Avoid caffeinated drinks, alcohol, carbonated sodas, and spicy foods, which irritate the bladder.",
                "Avoid using scented feminine hygiene products, bubble baths, or harsh douches."
            ],
            "red_flags": [
                "PYELONEPHRITIS EMERGENCY: High fever, shaking chills, and pain in the upper back and flank (kidney infection).",
                "Nausea and vomiting accompanied by severe loin pain.",
                "Gross visible blood or blood clots in the urine."
            ],
            "doctor_schedule": "Dr. Pradeep Chawla (Urology) • Available Today at 10:00 AM & 02:00 PM"
        },
        "conjunctivitis": {
            "name": "Conjunctivitis (Pink Eye / Ocular Inflammation)",
            "aliases": ["conjunctivitis", "pink eye", "eye infection", "red eye", "eye discharge", "sticky eyes"],
            "category": "Ophthalmology & Eye Care",
            "specialist": "Dr. Sneha Reddy (General Medicine / Ophthalmology)",
            "symptoms": [
                "Redness or pink coloration in the white of one or both eyes",
                "Gritty, burning, or scratchy sensation in the eyes as if sand is present",
                "Watery or thick yellowish-green discharge that forms a crust on eyelashes overnight",
                "Swelling of eyelids and mild sensitivity to bright light (photophobia)"
            ],
            "precautions": [
                "Wash hands thoroughly with soap before and after touching your face or eyes.",
                "Do NOT share towels, pillowcases, eye makeup, or eyeglasses with anyone.",
                "Apply cool or warm compresses with a clean lint-free cloth soaked in sterile water.",
                "Clean eye discharge gently from the inner corner outwards using sterile cotton pads."
            ],
            "medications": [
                "👁️ **Lubricating Eye Drops (Artificial Tears)**: Preservative-free carboxymethylcellulose 0.5% or polyethylene glycol eye drops (1 drop 4-5 times daily) to soothe irritation.",
                "👁️ **Antibacterial Eye Drops (if bacterial with thick pus)**: **Moxifloxacin 0.5% or Tobramycin 0.3% drops** (strictly under doctor's guidance, 1 drop 3 times daily for 5-7 days).",
                "👁️ **Antihistamine Drops (if allergic with intense itching)**: **Olopatadine 0.1% drops** twice daily.",
                "⚠️ **Medication Caution**: Never use leftover steroid eye drops without an ophthalmologist examining the cornea; steroids can cause severe corneal ulcers if herpes virus is present."
            ],
            "what_to_avoid": [
                "STRICTLY AVOID rubbing your eyes, which exacerbates inflammation and spreads infection.",
                "Do NOT wear contact lenses until the infection is completely cleared and approved by a doctor.",
                "Avoid wearing eye makeup (mascara, eyeliner) until full recovery; discard contaminated old makeup."
            ],
            "red_flags": [
                "Severe, deep ocular pain or marked decrease in vision.",
                "Extreme sensitivity to light (severe photophobia).",
                "Swelling and intense redness spreading across the eyelid and surrounding face (periorbital cellulitis)."
            ],
            "doctor_schedule": "Dr. Sneha Reddy (General Medicine) • Available Today at 11:30 AM & 03:00 PM"
        },
        "cervical_spondylosis": {
            "name": "Cervical Spondylosis (Neck Pain & Cervical Spine Strain)",
            "aliases": ["neck pain", "cervical", "cervical spondylosis", "cervical pain", "stiff neck", "neck stiffness", "neck ache"],
            "category": "Musculoskeletal & Spine Disorders",
            "specialist": "Dr. Sanjay Kapoor (Orthopedics & Spine Care)",
            "symptoms": [
                "Neck pain and stiffness that worsens with prolonged screen time or holding the head in one position",
                "Muscle spasms in the neck, trapezius, and upper shoulders",
                "Tension headaches originating at the base of the skull and radiating forward",
                "Tingling, numbness, or weakness in the shoulders, arms, or fingers"
            ],
            "precautions": [
                "Position computer screens at eye level so your head does not tilt forward ('tech neck').",
                "Use an ergonomic contour cervical pillow that supports the natural curve of your neck.",
                "Take 2-minute posture breaks every 30 minutes to do gentle neck retractions and shoulder rolls.",
                "Apply moist heat therapy to the neck and upper back for 15-20 minutes twice daily."
            ],
            "medications": [
                "💊 **First-Line Pain & Inflammation Relief**: **Paracetamol 650mg** or **Ibuprofen 400mg** after food.",
                "🧴 **Topical Analgesic Gel**: **Diclofenac Diethylamine Gel** gently applied to the back of the neck and shoulders 3 times daily.",
                "💊 **Muscle Relaxant**: **Thiocolchicoside 4mg** under prescription for acute locking spasms.",
                "⚡ **Nerve Health**: **Methylcobalamin (B12 1500 mcg)** for radiating arm numbness.",
                "⚠️ **Medication Caution**: Avoid sudden high-velocity neck cracking or unguided cervical manipulation."
            ],
            "what_to_avoid": [
                "Avoid sleeping with multiple stacked pillows or on your stomach.",
                "Avoid looking down at mobile phones for long periods; hold devices up at eye level.",
                "Avoid carrying heavy shoulder bags or backpacks on a single shoulder."
            ],
            "red_flags": [
                "Sudden loss of coordination or clumsiness in hands (dropping objects, difficulty buttoning shirts).",
                "Difficulty walking, balance loss, or feeling unsteady on your feet (cervical myelopathy warning).",
                "Radiating numbness accompanied by sharp chest pain."
            ],
            "doctor_schedule": "Dr. Sanjay Kapoor (Orthopedics) • Available Today at 11:30 AM & 04:00 PM"
        },
        "knee_pain": {
            "name": "Knee Pain & Osteoarthritis (Joint Degeneration & Sprain)",
            "aliases": ["knee pain", "joint pain", "knee stiffness", "meniscus", "ligament sprain", "knee ache", "knee swelling"],
            "category": "Musculoskeletal & Orthopedics",
            "specialist": "Dr. Sanjay Kapoor (Orthopedics & Joint Replacement)",
            "symptoms": [
                "Pain and soreness in the knee joint during or after walking, climbing stairs, or standing up",
                "Stiffness in the knee joint, especially in the morning or after resting",
                "Crepitus: a popping, crackling, or grinding sensation when bending the knee",
                "Mild swelling, warmth, and tenderness around the joint capsule"
            ],
            "precautions": [
                "Follow the R.I.C.E. protocol for acute flare-ups: Rest, Ice (15 mins), Compression (knee sleeve), Elevation.",
                "Engage in low-impact joint exercises such as swimming, stationary cycling, and quadriceps strengthening.",
                "Maintain a healthy body weight: every 1 kg of weight loss reduces 4 kg of pressure off knees.",
                "Wear cushioned, supportive footwear with good arch support; avoid hard flat soles or high heels."
            ],
            "medications": [
                "💊 **Oral Analgesic**: **Paracetamol 650mg** up to 3 times daily after food for mild-to-moderate joint ache.",
                "🧴 **Topical NSAID Gel**: **Diclofenac gel 1.16%** applied over the knee joint 3 times daily (significantly safer than oral NSAIDs for long-term joint care).",
                "💊 **Joint Supplementation**: **Glucosamine sulfate + Chondroitin** and **Collagen peptides** under orthopedic advice for cartilage support.",
                "⚠️ **Medication Caution**: Prolonged oral painkiller usage can damage kidneys and stomach lining; use topical treatments and physiotherapy as first-line maintenance."
            ],
            "what_to_avoid": [
                "Avoid deep squatting, sitting cross-legged on the floor, or high-impact jumping exercises.",
                "Avoid prolonged standing on hard concrete surfaces without cushioned footwear.",
                "Avoid ignoring persistent swelling or a knee that 'locks' and cannot straighten."
            ],
            "red_flags": [
                "Inability to bear any weight on the leg or feeling that the knee completely 'gives way'.",
                "Severe rapid swelling appearing within 2 hours of a twisting injury (hemarthrosis/ligament tear).",
                "Knee is intensely hot, red, and accompanied by high fever (septic arthritis emergency)."
            ],
            "doctor_schedule": "Dr. Sanjay Kapoor (Orthopedics) • Available Today at 11:30 AM & 04:00 PM"
        },
        "skin_rash": {
            "name": "Dermatitis, Eczema & Skin Rashes",
            "aliases": ["skin rash", "eczema", "dermatitis", "fungal infection", "ringworm", "itching", "itchy skin", "hives", "urticaria", "rash"],
            "category": "Dermatology & Skin Disorders",
            "specialist": "Dr. Tanvi Kapoor (Dermatology)",
            "symptoms": [
                "Red, inflamed patches of skin with persistent itching or stinging",
                "Dry, scaly, thickened, or peeling areas of the epidermis",
                "Small red bumps that may weep clear fluid when scratched",
                "Sensitive, swollen skin reactive to soaps, fabrics, or temperature changes"
            ],
            "precautions": [
                "Moisturize skin within 3 minutes after bathing using a thick ceramide or petroleum-based cream.",
                "Take short (5-10 minute) lukewarm baths using gentle, fragrance-free, soap-free cleansers.",
                "Wear soft, breathable loose-fitting 100% cotton garments; avoid wool and synthetic polyesters.",
                "Keep fingernails short and clean to prevent skin tearing and secondary bacterial infections."
            ],
            "medications": [
                "💊 **Antihistamine (for Itching)**: **Cetirizine 10mg** or **Fexofenadine 120mg** once daily with water to break the itch-scratch cycle.",
                "🧴 **Topical Anti-Itch**: **Calamine Lotion** applied generously over unbroken itchy skin 2-3 times daily.",
                "🧴 **Mild Anti-inflammatory Cream**: **Hydrocortisone 1% cream** on small stubborn patches twice daily for up to 5-7 days under clinical guidance.",
                "⚠️ **Medication Caution**: Do not use potent prescription steroid creams on the face or groin without a dermatologist's direct prescription."
            ],
            "what_to_avoid": [
                "STRICTLY AVOID scratching, rubbing, or scrubbing irritated skin.",
                "Avoid hot water showers, scented laundry detergents, fabric softeners, and chemical perfumes.",
                "Avoid self-treating with mixed combination creams containing steroids, antifungals, and antibacterials without diagnosis."
            ],
            "red_flags": [
                "Rash spreads rapidly over the entire body with high fever, skin peeling, or blisters.",
                "Signs of secondary infection: yellow pus, crusted honey-colored scabs, or red streaks spreading outward.",
                "Facial swelling or difficulty breathing accompanying the rash (anaphylaxis alert)."
            ],
            "doctor_schedule": "Dr. Tanvi Kapoor (Dermatology) • Available Today at 10:30 AM & 03:00 PM"
        },
        "chickenpox": {
            "name": "Chickenpox & Shingles (Varicella-Zoster Viral Exanthem)",
            "aliases": ["chickenpox", "chicken pox", "shingles", "herpes zoster", "varicella"],
            "category": "Viral Exanthem & Skin Infection",
            "specialist": "Dr. Arvind Swamy (Infectious Diseases / General Medicine)",
            "symptoms": [
                "Intensely itchy rash of fluid-filled blisters that eventually turn into scabs",
                "Fever, physical exhaustion, loss of appetite, and headache starting 1-2 days before the rash",
                "New crops of blisters appearing over 3 to 5 days, starting on chest/back and spreading outward",
                "In shingles: localized, intense burning or nerve pain along a single band on one side of the body"
            ],
            "precautions": [
                "Strict home isolation until all blisters have fully dried and scabbed over (usually 7-10 days).",
                "Keep patient separated from pregnant women, newborns, and immunocompromised individuals.",
                "Take cool or lukewarm oatmeal baths to soothe widespread skin itchiness.",
                "Wear light, soft cotton clothing; keep room comfortably cool to reduce sweating."
            ],
            "medications": [
                "💊 **Fever & Body Pain Control**: **Paracetamol 500mg or 650mg** every 6-8 hours after food. (CRITICAL: NEVER GIVE ASPIRIN or IBUPROFEN during chickenpox).",
                "🧴 **Topical Soothing**: **Calamine Lotion** dabbed onto individual itchy spots with cotton balls.",
                "💊 **Antihistamines**: **Cetirizine 10mg** once daily at bedtime to ease nocturnal itching.",
                "💊 **Prescription Antiviral**: **Acyclovir 800mg** 5 times daily (if initiated within 72 hours under physician prescription for adults/shingles).",
                "⛔ **CRITICAL MEDICATION WARNING**: STRICTLY AVOID Aspirin (causes fatal Reye's syndrome in viral exanthems) and Ibuprofen (increases risk of severe secondary necrotizing skin infections)."
            ],
            "what_to_avoid": [
                "STRICTLY AVOID scratching blisters to prevent permanent scarring and bacterial infection.",
                "Do NOT give Aspirin or Ibuprofen to anyone with chickenpox.",
                "Avoid close contact with public environments until every blister has formed a dry crust."
            ],
            "red_flags": [
                "Blisters become hot, red, extremely swollen, or begin leaking yellow pus.",
                "Fever lasts more than 4 days or spikes above 102°F.",
                "Persistent coughing, breathing difficulty, or unsteadiness/confusion (varicella pneumonia/encephalitis alert)."
            ],
            "doctor_schedule": "Dr. Arvind Swamy (Infectious Diseases) • Available Today at 11:00 AM & 03:30 PM"
        },
        "anxiety": {
            "name": "Anxiety, Stress & Panic Episode (Neuro-Wellness)",
            "aliases": ["anxiety", "panic attack", "nervousness", "palpitations", "insomnia", "stress", "restlessness", "racing heart"],
            "category": "Mental Health & Neuro-Psychiatry",
            "specialist": "Dr. Ananya Sharma (Neurology & Neuro-Wellness)",
            "symptoms": [
                "Rapid heartbeat (palpitations), pounding pulse, or tightness in the chest",
                "Persistent excessive worry, racing thoughts, restlessness, and feeling on edge",
                "Shortness of breath, sensation of a lump in the throat, or trembling hands",
                "Sleep disturbances: difficulty falling asleep, staying asleep, or waking up exhausted"
            ],
            "precautions": [
                "Practice the 4-7-8 rhythmic breathing technique: inhale for 4 seconds, hold for 7 seconds, exhale slowly for 8 seconds.",
                "Engage in sensory grounding (5-4-3-2-1 technique): identify 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, and 1 you can taste.",
                "Limit screen exposure and blue light for at least 1 hour before bedtime.",
                "Engage in daily 20-30 minute brisk walking or yoga to reduce circulating stress hormones."
            ],
            "medications": [
                "💊 **Supportive Herbal / Nutritional**: **Chamomile or Ashwagandha herbal tea** for relaxation.",
                "💊 **Magnesium Glycinate (200mg–400mg)** before bedtime to support muscle relaxation and nervous system calm.",
                "💊 **Clinical Neuro-Consultation**: For severe panic or generalized anxiety, a doctor may evaluate for SSRIs (e.g. Escitalopram) or short-term anxiolytics. Take only under direct psychiatric supervision.",
                "⚠️ **Medication Caution**: Avoid self-medicating with alcohol, sedatives, or over-the-counter sleep aids, which cause dependency and worsen baseline anxiety."
            ],
            "what_to_avoid": [
                "STRICTLY AVOID high caffeine intake: cut out energy drinks, pre-workout supplements, and excessive coffee.",
                "Avoid doomscrolling on news and social media, especially late at night.",
                "Avoid skipping meals: fluctuating blood sugar triggers adrenaline surges and panic feelings."
            ],
            "red_flags": [
                "Chest pain radiating to the jaw or left arm with profuse sweating (must rule out cardiac emergency immediately).",
                "Severe feelings of despair, self-harm thoughts, or inability to care for daily basic needs.",
                "Panic episodes lasting hours without relief or leading to hyperventilation-induced fainting."
            ],
            "doctor_schedule": "Dr. Ananya Sharma (Neurology) • Available Today at 10:00 AM & 02:30 PM"
        }
}

def clean_extracted_condition(cond: str) -> str:
    """Cleans punctuation, stop words, and modifiers from extracted condition string."""
    cond = re.sub(r'^(a|an|the|my|severe|mild|chronic|acute|constant|some|unbearable|moderate)\s+', '', cond.strip(), flags=re.I)
    cond = re.sub(r'\s+(since|from|for|today|yesterday|past|last).*$', '', cond.strip(), flags=re.I)
    cond = re.sub(r'\s+(symptoms|precautions|what|options|and|specialist|treatment|cure|help|guidance|medicine|details|advice|doctor).*$', '', cond.strip(), flags=re.I)
    return cond.strip().title()

def generate_dynamic_disease_profile(condition_name: str) -> Dict[str, Any]:
    """Dynamically synthesizes a high-fidelity clinical profile for any disease, virus, or symptom."""
    c_lower = condition_name.lower()
    
    if any(k in c_lower for k in ["pain", "spine", "back", "neck", "knee", "bone", "joint", "disc", "muscle", "ortho", "sprain", "fracture", "ligament", "sciatica", "lumbago"]):
        domain = "Musculoskeletal & Orthopedic Disorders"
        specialist = "Dr. Sanjay Kapoor (Orthopedics & Spine Care)"
        doctor_schedule = "Dr. Sanjay Kapoor (Orthopedics) • Available Today at 11:30 AM & 04:00 PM"
        symptoms = [
            f"Localized pain, throbbing discomfort, or sharp stiffness in the affected {condition_name} region",
            "Restricted movement, muscle spasms, and guarding when bending, standing, or shifting posture",
            "Tenderness upon physical pressure and discomfort aggravated by prolonged immobility or physical strain",
            "Radiating discomfort or dull persistent ache extending to adjacent muscle groups"
        ]
        precautions = [
            "Apply cold ice packs wrapped in a cloth for 15-20 minutes during acute flare-ups to reduce swelling.",
            "Switch to warm compresses or moist heat pads after 48 hours to ease muscle stiffness and spasms.",
            "Maintain spinal ergonomics, avoid awkward postures, and rest on a firm, supportive surface.",
            "Engage in gentle, pain-free mobility; avoid complete bed rest beyond 24-48 hours to prevent muscle deconditioning."
        ]
        medications = [
            "💊 **First-Line Analgesic / Anti-inflammatory**: **Paracetamol (Acetaminophen) 650mg** (e.g. Dolo 650 / Tylenol) or **Ibuprofen 400mg** (taken strictly after food) every 8 hours as needed for pain and inflammation.",
            "🧴 **Topical Pain Relief**: Apply **Diclofenac Diethylamine Gel 1.16%** (e.g. Volini / Omnigel / Voltaren) gently over the painful area 3 to 4 times daily.",
            "💊 **Muscle Relaxant (if in spasm)**: **Thiocolchicoside 4mg/8mg** or **Chlorzoxazone** (under physician consultation) if severe involuntary muscle locking occurs.",
            "⚠️ **Medication Caution**: Do not combine multiple NSAIDs together. Patients with gastritis, stomach ulcers, or kidney disease should consult a doctor before taking oral painkillers."
        ]
        what_to_avoid = [
            "Avoid heavy weight lifting, sudden jerking movements, or excessive twisting of the spine/joints.",
            "Do NOT remain completely immobilized in bed for days, as inactivity weakens supportive muscles.",
            "Avoid poor ergonomics: avoid slouching on soft sofas, working without lumbar support, or poor footwear."
        ]
        red_flags = [
            "Sudden loss of bowel or bladder control, or numbness in the groin/saddle area (cauda equina emergency).",
            "Progressive muscle weakness, severe numbness, or loss of sensation in limbs.",
            "Severe pain accompanied by high fever, sudden chills, or unexplained rapid weight loss."
        ]

    elif any(k in c_lower for k in ["virus", "viral", "infect", "fever", "zika", "ebola", "flu", "dengue", "chikungunya", "covid", "bacteri", "pathogen", "norovirus", "rotavirus"]):
        domain = "Infectious & Communicable Disease"
        specialist = "Dr. Arvind Swamy (Infectious Diseases / General Medicine)"
        doctor_schedule = "Dr. Arvind Swamy (Infectious Diseases) • Available Today at 11:00 AM & 03:30 PM"
        symptoms = [
            f"Fever spikes, shivering chills, and persistent fatigue characteristic of {condition_name}",
            "Generalized muscular body aches, joint soreness, and weakness",
            "Headache, mild eye strain, and loss of appetite",
            "Potential skin rash, mild gastrointestinal upset, or dehydration"
        ]
        precautions = [
            "Maintain strict hydration: drink 2.5 to 3 liters of fluids daily (warm water, ORS, coconut water, clear broths).",
            "Ensure complete bed rest in an isolated, well-ventilated room to prevent household transmission.",
            "Monitor body temperature every 4 to 6 hours using a digital thermometer.",
            "Practice frequent hand hygiene and wear a mask if in close contact with vulnerable family members."
        ]
        medications = [
            "💊 **Fever & Body Ache Relief**: **Paracetamol (Acetaminophen) 500mg or 650mg** (e.g. Dolo 650) every 6-8 hours after food as needed. (Maximum: 3,000 mg/24h).",
            "💧 **Electrolyte & Hydration Support**: **Oral Rehydration Salts (ORS / Electral)** — 1 packet mixed in 1 liter clean water sipped regularly throughout the day.",
            "🍊 **Immune Defense**: **Vitamin C (500mg)** and **Zinc (50mg)** daily to support natural immune response.",
            "⚠️ **Medication Caution**: Avoid aspirin or ibuprofen unless specific viral causes (like Dengue) are ruled out by a medical professional. Do NOT take unprescribed antibiotics for viral infections."
        ]
        what_to_avoid = [
            "Do NOT take unprescribed antibiotics; antibiotics are ineffective against viruses and disrupt gut flora.",
            "Avoid strenuous physical exercise, gym workouts, or lifting while febrile.",
            "Avoid dehydrating beverages such as alcohol, high-caffeine energy drinks, and sugary sodas."
        ]
        red_flags = [
            "Persistent high fever exceeding 103°F (39.4°C) unresponsive to standard paracetamol.",
            "Difficulty breathing, chest tightness, or blood oxygen saturation (SpO2) falling below 94%.",
            "Confusion, extreme lethargy, persistent vomiting preventing hydration, or visible bleeding."
        ]

    elif any(k in c_lower for k in ["cough", "lung", "chest", "breath", "respirat", "asthma", "bronch", "pneumo"]):
        domain = "Pulmonary & Respiratory Medicine"
        specialist = "Dr. Farhan Akhtar (Pulmonology & Chest Medicine)"
        doctor_schedule = "Dr. Farhan Akhtar (Pulmonology) • Available Today at 11:30 AM & 04:00 PM"
        symptoms = [
            f"Persistent cough (dry or productive with phlegm) associated with {condition_name}",
            "Chest tightness, mild breathlessness upon exertion, or wheezing sounds",
            "Throat irritation, post-nasal drip, and physical exhaustion from coughing fits",
            "Mild low-grade fever, hoarseness, and nasal congestion"
        ]
        precautions = [
            "Practice warm water steam inhalation for 10 minutes 1-2 times daily to loosen airway secretions.",
            "Stay well-hydrated with warm water, herbal teas with honey, and warm clear soups.",
            "Keep indoor air clean: use an air purifier, avoid dust, mold, and sudden exposure to cold air.",
            "Sleep with your head slightly elevated using an extra pillow to reduce nocturnal coughing."
        ]
        medications = [
            "💊 **Supportive Cough Relief**: **Dextromethorphan syrup** (for dry, hacking cough) or **Guaifenesin/Ambroxol syrup** (for productive wet cough) as directed on packaging.",
            "💊 **Airway & Allergy Support**: **Montelukast 10mg + Levocetirizine 5mg** once daily at bedtime for allergic/reactive bronchospasm.",
            "🍬 **Throat Lozenges**: Menthol or honey-lemon lozenges to soothe dry mucosal irritation.",
            "⚠️ **Medication Caution**: Patients with asthma or COPD should not stop regular inhalers. Consult a pulmonologist if wheezing worsens."
        ]
        what_to_avoid = [
            "STRICTLY AVOID active and passive smoking, vaping, or exposure to industrial smoke/chemical fumes.",
            "Avoid very cold drinks, ice creams, and unpasteurized refrigerated dairy if mucus production increases.",
            "Avoid suppressing a productive cough with heavy sedatives; clearing mucus is protective."
        ]
        red_flags = [
            "Shortness of breath at rest, gasping for air, or inability to speak in full sentences.",
            "Coughing up fresh blood or rust-colored sputum.",
            "Bluish discoloration of lips/fingertips (cyanosis) or high fever with rapid shallow breathing."
        ]

    elif any(k in c_lower for k in ["stomach", "gut", "digest", "bowel", "nausea", "vomit", "diarrhea", "loose", "gast", "acid", "liver", "abdomen", "cramp"]):
        domain = "Gastroenterology & Digestive Health"
        specialist = "Dr. Sandeep Singhania (Gastroenterology)"
        doctor_schedule = "Dr. Sandeep Singhania (Gastroenterology) • Available Today at 10:30 AM & 03:00 PM"
        symptoms = [
            f"Abdominal cramping, bloating, or localized discomfort from {condition_name}",
            "Nausea, episodic vomiting, or frequent loose watery bowel movements",
            "Acid reflux, burning sensation in upper stomach/chest, or loss of appetite",
            "Dehydration, dry mouth, and generalized abdominal fatigue"
        ]
        precautions = [
            "Follow the BRAT diet (Bananas, Rice, Applesauce, Toast) and consume bland, easily digestible food.",
            "Sip Oral Rehydration Salts (ORS) or electrolyte water slowly in small, frequent amounts.",
            "Avoid dairy, spicy curries, deep-fried foods, and raw salads until the digestive tract calms.",
            "Rest in an upright or inclined position after meals to prevent acid backflow."
        ]
        medications = [
            "💧 **Electrolyte Replacement**: **WHO-Formula ORS (Oral Rehydration Salts)** — 1 sachet in 1 liter clean drinking water; sip after every loose bowel movement.",
            "💊 **Probiotic Gut Flora Support**: **Lactobacillus / Bacillus clausii spores** (e.g. Enterogermina / Darolac) twice daily to restore microbiome balance.",
            "💊 **Acid Suppression (if acid/burning)**: **Pantoprazole 40mg** or **Omeprazole 20mg** once daily 30 minutes before breakfast.",
            "⚠️ **Medication Caution**: Do NOT take anti-motility drugs (like Loperamide) if you have high fever or bloody stool, as they trap toxins in the gut."
        ]
        what_to_avoid = [
            "Avoid spicy, oily, greasy fast foods, citrus juices, caffeine, and alcoholic beverages.",
            "Avoid taking NSAID painkillers (like Aspirin, Ibuprofen) on an empty stomach.",
            "Avoid large, heavy meals; eat small, frequent portions throughout the day."
        ]
        red_flags = [
            "Blood in vomit ('coffee-ground' emesis) or dark tarry black/bloody stools.",
            "Inability to keep liquids down for more than 12 hours due to unceasing vomiting.",
            "Severe, rigid, rebound abdominal pain that suddenly worsens."
        ]

    elif any(k in c_lower for k in ["skin", "rash", "itch", "derma", "eczema", "hive", "allergy", "urticaria", "fungal", "boil"]):
        domain = "Dermatology & Skin Allergy"
        specialist = "Dr. Tanvi Kapoor (Dermatology & Skin Care)"
        doctor_schedule = "Dr. Tanvi Kapoor (Dermatology) • Available Today at 10:30 AM & 03:00 PM"
        symptoms = [
            f"Visible skin eruption, red erythematous patches, or hives related to {condition_name}",
            "Intense itching, burning sensation, or localized stinging across the affected area",
            "Dryness, flaking, peeling skin, or small fluid-filled bumps",
            "Swelling or warmth surrounding the affected dermatological lesions"
        ]
        precautions = [
            "Apply cool, damp cotton compresses to the itchy areas to immediately soothe skin inflammation.",
            "Bathe with lukewarm or cool water using mild, fragrance-free, soap-free cleansers.",
            "Keep nails trimmed short to prevent skin breakage and secondary bacterial infections.",
            "Wear loose, soft, breathable 100% cotton clothing; avoid wool, nylon, and tight garments."
        ]
        medications = [
            "💊 **Non-Drowsy Antihistamine**: **Cetirizine 10mg** or **Levocetirizine 5mg** or **Fexofenadine 120mg (Allegra)** once daily with water for allergic itching and hives.",
            "🧴 **Soothing Topical Lotion**: Apply **Calamine Lotion** gently over the affected skin 2-3 times daily.",
            "🧴 **Moisturizing Barrier**: Apply a bland ceramide-based moisturizer or pure white petroleum jelly on damp skin.",
            "⚠️ **Medication Caution**: Avoid prolonged application of high-potency steroid creams without a dermatologist's direct prescription."
        ]
        what_to_avoid = [
            "STRICTLY AVOID scratching, picking, or rubbing the rash, which causes skin breakdown and scarring.",
            "Avoid hot showers, harsh scented soaps, deodorants, perfumes, and synthetic detergents.",
            "Avoid self-treating with mixed combination creams containing steroids, antifungals, and antibacterials without diagnosis."
        ]
        red_flags = [
            "ANAPHYLAXIS SIGNS: Swelling of lips, tongue, face, or difficulty breathing (dial 911 / 112 immediately).",
            "Rapidly spreading rash accompanied by high fever, blisters, or skin peeling (Stevens-Johnson alert).",
            "Signs of secondary infection: spreading warmth, red streaks, or yellow pus discharge."
        ]

    else:
        domain = "Internal & General Medicine"
        specialist = "Dr. Sneha Reddy (General Medicine)"
        doctor_schedule = "Dr. Sneha Reddy (General Medicine) • Available Today at 11:30 AM & 03:00 PM"
        symptoms = [
            f"Discomfort, localized or systemic clinical symptoms associated with {condition_name}",
            "General fatigue, lowered energy levels, and disrupted daily routine",
            "Mild inflammation, aches, or physical malaise",
            "Fluctuating symptom intensity influenced by physical exertion, rest, or hydration"
        ]
        precautions = [
            "Ensure adequate hydration: consume 2.5 to 3 liters of clean drinking water daily.",
            "Prioritize adequate rest (7-8 hours of sleep) to enable natural immune and physiological repair.",
            "Maintain a detailed daily symptom log noting triggers, timing, and response to food or activity.",
            "Follow a balanced, nutrient-dense diet rich in vegetables, fruits, and lean proteins."
        ]
        medications = [
            "💊 **General Symptom & Pain Relief**: **Paracetamol (Acetaminophen) 500mg or 650mg** (e.g. Dolo 650) every 6-8 hours after food for general pain or fever.",
            "💧 **Electrolyte & Hydration**: **Oral Rehydration Salts (ORS)** or coconut water if feeling fatigued or dehydrated.",
            "🍊 **Multivitamin Support**: Standard daily multivitamin or Vitamin C 500mg to support cellular recovery.",
            "⚠️ **Medication Caution**: Always check for drug allergies and consult a physician before starting any prescription medication."
        ]
        what_to_avoid = [
            "Avoid unverified home remedies, unprescribed antibiotic usage, or sudden drastic dietary changes.",
            "Avoid heavy physical exertion, sleep deprivation, and extreme stress while unwell.",
            "Avoid excessive alcohol, smoking, and high-sugar processed foods."
        ]
        red_flags = [
            "High fever persisting beyond 3 days (>102°F / 38.9°C).",
            "Sudden severe pain, chest discomfort, shortness of breath, or dizziness.",
            "Rapid deterioration of symptoms or failure to improve with basic at-home care."
        ]

    return {
        "name": condition_name,
        "aliases": [condition_name.lower()],
        "category": domain,
        "specialist": specialist,
        "symptoms": symptoms,
        "precautions": precautions,
        "medications": medications,
        "what_to_avoid": what_to_avoid,
        "red_flags": red_flags,
        "doctor_schedule": doctor_schedule
    }

STOP_WORDS = {
    'what', 'are', 'the', 'for', 'and', 'from', 'with', 'have', 'has', 'had', 'can', 'you',
    'give', 'tell', 'about', 'some', 'any', 'this', 'that', 'how', 'why', 'who', 'when', 'where',
    'into', 'also', 'been', 'suffering', 'facing', 'having', 'options', 'specialist', 'precautions',
    'symptoms', 'details', 'help', 'care', 'treatment', 'medicine', 'medicines', 'doctor', 'schedule'
}

def clean_extracted_condition(cond: str) -> str:
    """Cleans punctuation, stop words, and modifiers from extracted condition string."""
    cond = re.sub(r'^(a|an|the|my|severe|mild|chronic|acute|constant|some|unbearable|moderate)\s+', '', cond.strip(), flags=re.I)
    cond = re.sub(r'\s+(since|from|for|today|yesterday|past|last)\b.*$', '', cond.strip(), flags=re.I)
    cond = re.sub(r'\s+(symptoms|precautions|what|options|and|specialist|treatment|cure|help|guidance|medicine|details|advice|doctor)\b.*$', '', cond.strip(), flags=re.I)
    return cond.strip().title()

def extract_condition_or_virus(text: str, reported_disease: Optional[str] = None) -> Optional[str]:
    """Extracts any disease, virus, symptom, or infection from user message or intake state."""
    # 1. Check reported_disease from registration form
    if reported_disease and reported_disease.strip() and reported_disease.lower() not in ['none', 'null', 'general', 'general inquiry', 'inquiry']:
        return clean_extracted_condition(reported_disease)
    
    # 2. Match natural conversational patterns
    patterns = [
        r'(?:suffering\s+(?:with|from)|dealing\s+with|diagnosed\s+with|facing|struggling\s+with|complaint\s+of)\s+([a-zA-Z\s\-]{3,35}?)[\.,\?!]',
        r'(?:suffering\s+(?:with|from)|dealing\s+with|diagnosed\s+with|facing|struggling\s+with|complaint\s+of)\s+([a-zA-Z\s\-]{3,35})$',
        r'(?:symptoms|precautions|treatment|medication|details|guide|care|cure|medicine)\s+(?:of|for|about|in)\s+([a-zA-Z\s\-]{3,35}?)[\.,\?!]',
        r'(?:symptoms|precautions|treatment|medication|details|guide|care|cure|medicine)\s+(?:of|for|about|in)\s+([a-zA-Z\s\-]{3,35})$',
        r'(?:tell\s+me\s+about|info\s+on|details\s+on|guide\s+for|about)\s+([a-zA-Z\s\-]{3,30}?)[\.,\?!]',
        r'(?:tell\s+me\s+about|info\s+on|details\s+on|guide\s+for|about)\s+([a-zA-Z\s\-]{3,30})$',
        r'\b([a-zA-Z\-]{3,20}\s+(?:virus|infection|disease|syndrome|fever|flu|disorder|pain|ache|strain|sprain))\b',
        r'\b([a-zA-Z\-]{3,20}(?:virus|bacteria))\b',
        r'\b(?:i\s+have|i\s+got|having)\s+([a-zA-Z\s\-]{3,30}?)[\.,\?!]',
        r'\b(?:i\s+have|i\s+got|having)\s+([a-zA-Z\s\-]{3,30})$'
    ]
    for pat in patterns:
        m = re.search(pat, text, re.I)
        if m:
            res = clean_extracted_condition(m.group(1))
            if len(res) >= 3 and res.lower() not in ['an appointment', 'a doctor', 'a question', 'a slot', 'help', 'some help']:
                return res
    return None

def match_disease(query: str, reported_disease: Optional[str] = None, fallback_to_dynamic: bool = True) -> Optional[Dict[str, Any]]:
    """Finds the best matching disease profile from user text or reported condition using exact, fuzzy, and dynamic clinical matching."""
    cleaned = query.lower()
    
    # 1. Exact alias/keyword check in database
    for disease_key, data in DISEASES_DB.items():
        for alias in data["aliases"]:
            if re.search(r'\b' + re.escape(alias) + r'\b', cleaned):
                return data

    # 1b. Check reported_disease if provided
    if reported_disease and reported_disease.strip() and reported_disease.lower() not in ['none', 'null', 'general', 'general inquiry', 'inquiry']:
        rep_clean = reported_disease.lower().strip()
        for disease_key, data in DISEASES_DB.items():
            for alias in data["aliases"]:
                if alias in rep_clean or rep_clean in alias:
                    return data

    # Dynamic profile fallback
    if fallback_to_dynamic:
        extracted = extract_condition_or_virus(query, reported_disease)
        if extracted:
            ext_lower = extracted.lower()
            for disease_key, data in DISEASES_DB.items():
                for alias in data["aliases"]:
                    if re.search(r'\b' + re.escape(alias) + r'\b', ext_lower):
                        return data
            return generate_dynamic_disease_profile(extracted)

    # Fuzzy matching for typos
    tokens = [w for w in re.findall(r'\b\w{4,}\b', cleaned) if w not in STOP_WORDS]
    alias_to_key = {}
    for key, data in DISEASES_DB.items():
        for alias in data["aliases"]:
            alias_to_key[alias] = key

    all_aliases = list(alias_to_key.keys())
    for token in tokens:
        matches = difflib.get_close_matches(token, all_aliases, n=1, cutoff=0.8)
        if matches:
            best_alias = matches[0]
            matched_key = alias_to_key[best_alias]
            return DISEASES_DB[matched_key]

    # Substring matching
    for disease_key, data in DISEASES_DB.items():
        for alias in data["aliases"]:
            if alias in cleaned:
                return data

    return None


def format_disease_response(data: Dict[str, Any], patient_name: str, patient_age: Optional[str] = None, patient_place: Optional[str] = None) -> str:
    """Formats a comprehensive clinical response detailing symptoms, precautions, medications, what to avoid, and red flags."""
    lines = []
    
    meta_info = []
    if patient_age:
        meta_info.append(f"Age: {patient_age} yrs")
    if patient_place:
        meta_info.append(f"Place: {patient_place}")
        
    meta_str = f" ({', '.join(meta_info)})" if meta_info else ""
    lines.append(f"Hello **{patient_name}**{meta_str}, here is the customized clinical care guide for **{data['name']}**:\n")
    
    # 1. Symptoms
    lines.append("🔍 **Common Symptoms & Clinical Signs**:")
    for s in data["symptoms"]:
        lines.append(f"• {s}")
    lines.append("")

    # 2. Precautions
    lines.append("🛡️ **Key Precautions & Immediate At-Home Care**:")
    for p in data["precautions"]:
        lines.append(f"• {p}")
        
    # Age-specific guidance
    if patient_age:
        try:
            age_int = int(re.sub(r'\D', '', str(patient_age)))
            if age_int < 12:
                lines.append("• 👶 **Pediatric Precaution**: Do not administer aspirin to children under 16 without pediatrician instruction (risk of Reye's syndrome). Use pediatric weight-adjusted oral suspensions.")
            elif age_int >= 60:
                lines.append("• 👴 **Senior / Geriatric Precaution**: Ensure assistance with mobility to prevent falls while dizzy. Monitor resting blood pressure and renal hydration twice daily.")
        except Exception:
            pass
    lines.append("")

    # 3. Medications
    if "medications" in data and data["medications"]:
        lines.append("💊 **Medications You Can Use (Supportive & First-Line Guidance)**:")
        for m in data["medications"]:
            lines.append(f"• {m}")
        lines.append("")

    # 4. What to Avoid
    lines.append("🚫 **What to Avoid (Diet & Habits)**:")
    for a in data["what_to_avoid"]:
        lines.append(f"• {a}")
    lines.append("")

    # 5. Red Flags
    lines.append("🚨 **Red-Flag Warnings (Seek Emergency Hospital Care If)**:")
    for r in data["red_flags"]:
        lines.append(f"• {r}")
    lines.append("")

    # 6. Care Coordination
    lines.append("📅 **Recommended Specialist & Next Steps**:")
    lines.append(f"• **Recommended Department**: {data['specialist']}")
    if patient_place:
        lines.append(f"• **Regional Care Network**: Clinic partner coordination available in **{patient_place}**.")
    lines.append(f"• **Available Slots**: {data['doctor_schedule']}")
    lines.append("• *Reply with 'Book appointment' if you would like me to reserve a slot with our coordinator.*")

    return "\n".join(lines)
