import csv
import random
from datetime import datetime, timedelta
import pandas as pd

# Medical scenarios by outcome
categories = {
    "Improved": [
        # 1. Cardiology
        {
            "scenario": "Post-stent angina resolution with medication adjustment",
            "text": "Patient reports no anginal episodes since stent placement and a reduction in frequency of mild palpitations. Metoprolol dose decreased to 25mg BID. Continue aspirin and atorvastatin.",
            "labs": {"LDL": "65 mg/dL", "HDL": "50 mg/dL", "EKG": "No ischemic changes"}
        },
        {
            "scenario": "Heart failure NYHA class improvement",
            "text": "Patient's functional capacity improved from NYHA Class III to Class II with increased exercise tolerance and reduced dyspnea on exertion. Continue current regimen of ACE inhibitor, beta-blocker, and diuretic.",
            "labs": {"BNP": "150 pg/mL", "EF": "45%"}
        },
        {
            "scenario": "Hypertension controlled with lifestyle and medication",
            "text": "Blood pressure consistently below 130/80 mmHg on amlodipine 5mg daily and DASH diet adherence. Reports regular exercise. Continue current management.",
            "labs": {"BP": "120/75 mmHg", "Electrolytes": "Normal"}
        },
        {
            "scenario": "Resolution of pericardial effusion",
            "text": "Follow-up echocardiogram shows complete resolution of previously noted small pericardial effusion. No recurrence of chest pain or shortness of breath. Discontinue colchicine.",
            "labs": {"ECHO": "No effusion", "CRP": "1.0 mg/dL"}
        },
        {
            "scenario": "Improvement in claudication symptoms post-revascularization",
            "text": "Patient reports increased walking distance without claudication pain following peripheral artery angioplasty. Ankle-brachial index improved to 0.9. Continue aspirin and cilostazol.",
            "labs": {"ABI": "0.9", "Lipid panel": "Within target"}
        },
        # 2. Endocrinology
        {
            "scenario": "Improved glycemic control with diet and exercise",
            "text": "HbA1c decreased from 8.5% to 7.2% with consistent adherence to diabetic diet and regular physical activity. Metformin dosage remains stable. Reinforce lifestyle modifications.",
            "labs": {"HbA1c": "7.2%", "Fasting Glucose": "115 mg/dL"}
        },
        {
            "scenario": "Resolution of hyperthyroidism symptoms",
            "text": "Thyroid function tests normalized after completing a course of methimazole. No further symptoms of palpitations, tremors, or heat intolerance. Discontinue medication, monitor TSH every 3 months.",
            "labs": {"TSH": "1.8 mIU/L", "Free T3": "3.5 pg/mL"}
        },
        {
            "scenario": "Improvement in diabetic neuropathy symptoms",
            "text": "Patient reports decreased burning and tingling sensations in feet with gabapentin. Regular foot exams continue to show no new ulcerations. Maintain current medication.",
            "labs": {"Vibration perception": "Improved", "Monofilament test": "No loss of sensation"}
        },
        {
            "scenario": "Normalization of calcium levels in hyperparathyroidism",
            "text": "Serum calcium levels within normal range following parathyroidectomy. No symptoms of fatigue or bone pain. Monitor calcium and PTH levels annually.",
            "labs": {"Calcium": "9.5 mg/dL", "PTH": "30 pg/mL"}
        },
        {
            "scenario": "Weight loss and improved insulin sensitivity in PCOS",
            "text": "Patient achieved a 5% weight reduction through dietary changes and exercise. Fasting insulin decreased, and reports more regular menstrual cycles. Continue metformin and lifestyle advice.",
            "labs": {"Weight": "Reduced", "HOMA-IR": "Improved"}
        },
        # 3. Oncology
        {
            "scenario": "Stable disease after targeted therapy in lung cancer",
            "text": "Follow-up CT scan shows no evidence of tumor growth or new metastases after 12 months of EGFR inhibitor therapy. Patient remains asymptomatic. Continue current treatment.",
            "labs": {"CEA": "Stable", "Imaging": "No progression"}
        },
        {
            "scenario": "Sustained remission in Hodgkin's lymphoma",
            "text": "Five years post-ABVD chemotherapy, surveillance PET-CT remains negative for disease recurrence. Patient reports good energy levels and no B symptoms. Continue annual follow-up.",
            "labs": {"CBC": "Normal", "LDH": "Stable"}
        },
        {
            "scenario": "Improved pain control in metastatic bone cancer",
            "text": "Pain scores significantly reduced with adjustment of opioid analgesic and initiation of bisphosphonate therapy. Patient reports improved mobility. Continue current pain management.",
            "labs": {"Pain Score": "Improved", "Calcium": "Normal"}
        },
        {
            "scenario": "No evidence of recurrence post-surgical resection of melanoma",
            "text": "Three years following wide local excision and sentinel lymph node biopsy, regular skin exams show no signs of local recurrence or distant metastases. Continue annual dermatological surveillance.",
            "labs": {"LDH": "Normal", "Imaging": "No recurrence"}
        },
        {
            "scenario": "Decreased PSA levels in prostate cancer with androgen deprivation therapy",
            "text": "PSA level significantly decreased following initiation of LHRH agonist therapy. Patient reports decreased bone pain. Continue ADT and monitor PSA every 3 months.",
            "labs": {"PSA": "Significantly decreased", "Testosterone": "Castrate level"}
        },
        # 4. Pulmonology
        {
            "scenario": "Improved asthma control with inhaled corticosteroids",
            "text": "Reduced frequency of asthma exacerbations and rescue inhaler use since starting daily inhaled corticosteroid. FEV1 improved on spirometry. Continue current medication.",
            "labs": {"FEV1": "Improved", "SABA use": "Decreased"}
        },
        {
            "scenario": "Stabilization of pulmonary fibrosis progression",
            "text": "Serial high-resolution CT scans show no significant progression of fibrotic changes. Patient's oxygen saturation remains stable at rest and with exertion on current antifibrotic medication.",
            "labs": {"SpO2": "Stable", "DLCO": "Stable"}
        },
        {
            "scenario": "Resolution of pneumonia",
            "text": "Chest X-ray shows complete resolution of consolidation. Patient reports no cough, fever, or shortness of breath. Completed course of antibiotics. Advise symptomatic treatment for residual cough if needed.",
            "labs": {"CXR": "Clear", "WBC": "Normal"}
        },
        {
            "scenario": "Improved exercise tolerance in pulmonary hypertension",
            "text": "Six-minute walk distance increased following initiation of pulmonary vasodilator therapy. Patient reports less fatigue and dyspnea with activity. Continue current regimen.",
            "labs": {"6MWD": "Increased", "NT-proBNP": "Decreased"}
        },
        {
            "scenario": "Successful weaning from mechanical ventilation",
            "text": "Patient successfully extubated after a week of mechanical ventilation for acute respiratory failure. Maintaining adequate oxygenation on nasal cannula. Continue respiratory therapy.",
            "labs": {"ABG": "Within normal limits", "SpO2": "Stable on minimal support"}
        },
        # 5. Rheumatology
        {
            "scenario": "Reduced joint inflammation in psoriatic arthritis with biologic",
            "text": "Significant reduction in swollen and tender joint count since starting TNF-alpha inhibitor. Skin lesions also improved. Continue current biologic therapy.",
            "labs": {"Swollen joint count": "Decreased", "Tender joint count": "Decreased"}
        },
        {
            "scenario": "Improved mobility in ankylosing spondylitis with therapy",
            "text": "Patient reports increased spinal mobility and reduced morning stiffness with consistent physical therapy and NSAID use. Bath Ankylosing Spondylitis Disease Activity Index (BASDAI) improved.",
            "labs": {"BASDAI": "Improved", "ESR": "Decreased"}
        },
        {
            "scenario": "Resolution of gout flare with medication",
            "text": "No joint pain or swelling following a course of colchicine and NSAIDs for acute gout flare. Urate-lowering therapy initiated with allopurinol. Monitor serum uric acid.",
            "labs": {"Uric Acid": "To target", "CRP": "Normal"}
        },
        {
            "scenario": "Improved muscle strength in polymyalgia rheumatica with steroids",
            "text": "Patient reports significant improvement in proximal muscle strength and reduced pain with low-dose prednisone. Inflammatory markers normalized. Plan for gradual steroid taper.",
            "labs": {"CK": "Normal", "ESR": "Decreased"}
        },
        {
            "scenario": "Decreased frequency of Raynaud's phenomenon episodes",
            "text": "Reduced frequency and severity of Raynaud's attacks with nifedipine and avoidance of cold exposure. No new digital ulcers. Continue current management.",
            "labs": {"Digital exam": "No ulcers", "Capillaroscopy": "Stable"}
        },
        # 6. Nephrology
        {
            "scenario": "Stabilization of GFR in early CKD with ACE inhibitor",
            "text": "Estimated GFR remains stable on ACE inhibitor therapy. Blood pressure well-controlled. Continue current medication and monitor kidney function biannually.",
            "labs": {"eGFR": "Stable", "BP": "Controlled"}
        },
        {
            "scenario": "Reduced proteinuria with medication adjustment",
            "text": "Urine albumin-to-creatinine ratio decreased following increase in ACE inhibitor dosage. Continue current regimen and monitor proteinuria regularly.",
            "labs": {"ACR": "Decreased", "Serum albumin": "Stable"}
        },
        {
            "scenario": "No recurrence of kidney stones with dietary changes",
            "text": "No new episodes of renal colic or evidence of new stone formation on imaging after implementing dietary modifications and increased fluid intake. Continue current recommendations.",
            "labs": {"Urinalysis": "No crystals", "Imaging": "No new stones"}
        },
        {
            "scenario": "Improved fluid balance in chronic kidney disease",
            "text": "Reduced peripheral edema and stable weight with consistent diuretic therapy and fluid restriction. Monitor fluid status at each visit.",
            "labs": {"Weight": "Stable", "Electrolytes": "Normal"}
        },
        {
            "scenario": "Stabilization of anemia of chronic kidney disease with ESA",
            "text": "Hemoglobin levels maintained within target range with stable dose of erythropoiesis-stimulating agent. No new symptoms of fatigue or shortness of breath. Continue current ESA therapy.",
            "labs": {"Hgb": "Stable", "Ferritin": "Adequate"}
        },
        # 7. Infectious Disease
        {
            "scenario": "Sustained undetectable viral load in HIV",
            "text": "HIV viral load remains undetectable on current antiretroviral therapy for over a year. CD4 count stable. Continue current ART regimen and regular monitoring.",
            "labs": {"Viral Load": "<20 copies/mL", "CD4": "Stable"}
        },
        {
            "scenario": "Resolution of Lyme disease symptoms post-antibiotics",
            "text": "Patient reports complete resolution of joint pain, fatigue, and rash following a course of doxycycline. No new symptoms. Advise to watch for any recurrence.",
            "labs": {"Lyme serology": "Previously positive, not routinely repeated", "CRP": "Normal"}
        },
        {
            "scenario": "Negative blood cultures after treatment for bacteremia",
            "text": "Repeat blood cultures are negative after completing antibiotic therapy for previous bloodstream infection. Patient afebrile and clinically improved. Continue oral antibiotics as prescribed.",
            "labs": {"Blood cultures": "Negative", "WBC": "Normal"}
        },
        {
            "scenario": "Control of chronic hepatitis B with antiviral therapy",
            "text": "Hepatitis B viral load significantly reduced and liver enzymes normalized on tenofovir therapy. Continue current antiviral and monitor liver function regularly.",
            "labs": {"HBV DNA": "Low/Undetectable", "ALT": "Normal"}
        },
        {
            "scenario": "Resolution of cellulitis with antibiotic treatment",
            "text": "Area of skin redness, swelling, and pain has resolved after completing a course of oral antibiotics. No signs of systemic infection. Advise to monitor for any recurrence.",
            "labs": {"WBC": "Normal", "CRP": "Normal"}
        },
        # 8. Gastroenterology
        {
            "scenario": "Maintenance of remission in Crohn's disease with biologic",
            "text": "No active symptoms of abdominal pain, diarrhea, or bleeding while on maintenance infliximab therapy. Endoscopic evaluation showed mucosal healing previously. Continue current biologic.",
            "labs": {"CRP": "Low", "Fecal calprotectin": "Low"}
        },
        {
            "scenario": "Symptom control in irritable bowel syndrome with dietary changes",
            "text": "Patient reports significant improvement in abdominal bloating and altered bowel habits with adherence to a low-FODMAP diet. Continue dietary management.",
            "labs": {"Stool studies": "Negative", "CBC": "Normal"}
        },
        {
            "scenario": "Stable liver function in compensated cirrhosis",
            "text": "Liver enzymes remain stable, and no new signs of decompensation (ascites, encephalopathy) in patient with compensated cirrhosis. Continue current medical management and surveillance.",
            "labs": {"ALT": "Stable", "Bilirubin": "Stable", "Albumin": "Stable"}
        },
        {
            "scenario": "Resolution of Helicobacter pylori infection after treatment",
            "text": "Repeat testing for H. pylori is negative following completion of triple therapy. Patient reports resolution of epigastric pain. Advise to monitor for any recurrent symptoms.",
            "labs": {"H. pylori test": "Negative", "Endoscopy": "Previous gastritis resolved"}
        },
        {
            "scenario": "Improved nutritional status post-small bowel resection",
            "text": "Patient maintaining stable weight and tolerating oral diet well following small bowel resection. Vitamin levels within normal range with supplementation. Continue current nutritional support.",
            "labs": {"Prealbumin": "Stable", "Vitamin levels": "Normal"}
        },
        # 9. Neurology
        {
            "scenario": "Reduced migraine frequency with prophylactic medication",
            "text": "Frequency of migraine headaches decreased from weekly to monthly since starting topiramate. Intensity also reduced. Continue current prophylactic treatment.",
            "labs": {"Headache diary": "Improved frequency", "BP": "Stable"}
        },
        {
            "scenario": "Stable symptoms in multiple sclerosis with DMT",
            "text": "No new relapses or progression of neurological deficits while on current disease-modifying therapy. MRI brain shows no new lesions. Continue current DMT.",
            "labs": {"MRI Brain": "No new lesions", "EDSS": "Stable"}
        },
        {
            "scenario": "Improved motor function post-stroke rehabilitation",
            "text": "Significant improvement in strength and coordination of affected limb following intensive physical and occupational therapy. Continue home exercise program.",
            "labs": {"Motor strength": "Improved", "Functional assessment": "Improved"}
        },
        {
            "scenario": "Seizure freedom maintained with current antiepileptic medication",
            "text": "No seizures reported for over a year on current regimen of levetiracetam. EEG remains without epileptiform activity. Continue current AED dosage.",
            "labs": {"AED Level": "Therapeutic", "EEG": "No epileptiform activity"}
        },
        {
            "scenario": "Stabilization of Parkinson's disease symptoms with medication",
            "text": "Motor symptoms (tremor, rigidity, bradykinesia) remain well-controlled on current dopaminergic therapy. No significant fluctuations in motor function. Continue current regimen.",
            "labs": {"UPDRS score": "Stable", "Cognitive assessment": "Stable"}
        },
        # 10. Orthopedics
        {
            "scenario": "Improved range of motion post-shoulder surgery",
            "text": "Significant improvement in shoulder abduction and external rotation following rotator cuff repair and physical therapy. Pain well-managed with occasional NSAIDs. Continue home exercises.",
            "labs": {"ROM": "Improved", "Pain Score": "Low"}
        },
        {
            "scenario": "Pain control in chronic back pain with conservative management",
            "text": "Patient reports reduced back pain intensity with regular exercise, physical therapy, and occasional use of NSAIDs. No new neurological deficits. Continue current management.",
            "labs": {"Pain Score": "Improved", "Neurological exam": "Normal"}
        },
        {
            "scenario": "Healing of fracture with immobilization",
            "text": "Follow-up X-ray shows evidence of bony callus formation at the site of the distal radius fracture. Continue cast immobilization for another 4 weeks.",
            "labs": {"X-ray": "Healing fracture", "Pain Score": "Decreased"}
        },
        {
            "scenario": "Improved function after hip replacement",
            "text": "Patient reports improved mobility and reduced pain in the operated hip following total hip arthroplasty and rehabilitation. Able to perform activities of daily living independently. Continue home exercises.",
            "labs": {"ROM": "Improved", "Gait assessment": "Improved"}
        },
        {
            "scenario": "Stabilization of scoliosis curve with bracing",
            "text": "Serial X-rays show no significant progression of the scoliotic curve while wearing a back brace as prescribed. Continue brace wear and monitor every 6 months.",
            "labs": {"Cobb angle": "Stable", "Pulmonary function tests": "Stable"}
        },
    # 11. Dermatology
        {
            "scenario": "Reduced frequency of herpes simplex outbreaks with antiviral prophylaxis",
            "text": "Significantly fewer episodes of oral herpes reported since starting daily acyclovir. Outbreaks are also less severe and resolve more quickly. Continue prophylactic treatment.",
            "labs": {"Viral culture": "Negative during check-up", "Frequency of outbreaks": "Decreased"}
        },
        {
            "scenario": "Improvement in acne vulgaris with topical retinoids",
            "text": "Noticeable reduction in the number of inflammatory lesions and comedones with consistent use of topical tretinoin. No new significant breakouts. Continue current regimen.",
            "labs": {"Inflammatory lesion count": "Decreased", "Comedone count": "Decreased"}
        },
        {
            "scenario": "Resolution of contact dermatitis with avoidance of allergen",
            "text": "Skin rash has completely cleared after identifying and avoiding the causative agent. No new areas of redness, itching, or blistering. Advise on continued allergen avoidance.",
            "labs": {"Patch test": "Previously positive, not repeated", "Skin exam": "Clear"}
        },
        {
            "scenario": "Improvement in rosacea symptoms with topical metronidazole",
            "text": "Reduced facial redness, telangiectasias, and papules with regular application of topical metronidazole. Fewer flushing episodes reported. Continue current treatment.",
            "labs": {"Facial redness score": "Decreased", "Inflammatory lesion count": "Decreased"}
        },
        {
            "scenario": "Decreased scaling and itching in seborrheic dermatitis with medicated shampoo",
            "text": "Significant reduction in scalp scaling and itching with consistent use of ketoconazole shampoo. No new areas of involvement on the face or chest. Continue medicated shampoo use.",
            "labs": {"Scalp exam": "Improved", "Seborrheic dermatitis area score": "Decreased"}
        },
        # 12. Psychiatry
        {
            "scenario": "PHQ-9 remission in anxiety disorder with SSRI",
            "text": "Patient's PHQ-9 score decreased significantly, indicating remission of depressive symptoms associated with anxiety. Reports improved mood and increased engagement in activities on sertraline.",
            "labs": {"PHQ-9": "Remission range", "GAD-7": "Improved"}
        },
        {
            "scenario": "Reduced panic attack frequency with CBT and medication",
            "text": "Frequency of panic attacks significantly decreased with a combination of cognitive behavioral therapy and a low dose of lorazepam PRN. Patient reports improved coping skills.",
            "labs": {"Panic attack frequency": "Decreased", "Anxiety scale score": "Improved"}
        },
        {
            "scenario": "Improved sleep quality in insomnia with behavioral therapy",
            "text": "Patient reports improved sleep latency, duration, and overall sleep quality following implementation of sleep hygiene techniques and stimulus control therapy. Reduced reliance on sleep aids.",
            "labs": {"Sleep diary": "Improved metrics", "Insomnia Severity Index": "Decreased"}
        },
        {
            "scenario": "Stabilization of mood swings in bipolar disorder with medication",
            "text": "No manic or depressive episodes reported for the past 6 months on a stable dose of lamotrigine. Mood charts show consistent euthymia. Continue current medication.",
            "labs": {"Mood chart review": "Stable", "YMRS/HAM-D scores": "Within normal limits"}
        },
        {
            "scenario": "Decreased obsessive-compulsive symptoms with ERP therapy and SSRI",
            "text": "Significant reduction in the frequency and intensity of obsessions and compulsions with exposure and response prevention therapy and fluoxetine. Patient reports improved daily functioning.",
            "labs": {"Y-BOCS score": "Decreased", "Functional impairment scale": "Improved"}
        },
        # 13. Hematology
        {
            "scenario": "Normalization of platelet count in ITP with treatment",
            "text": "Platelet count increased to within the normal range following a course of corticosteroids and intravenous immunoglobulin. No new bleeding episodes. Tapering steroids as tolerated.",
            "labs": {"Platelets": "Within normal limits", "Bleeding score": "0"}
        },
        {
            "scenario": "Improved hemoglobin levels in chronic anemia with EPO",
            "text": "Hemoglobin levels increased and stabilized with erythropoietin stimulating agent therapy. Patient reports reduced fatigue and improved energy levels. Continue current EPO dosage.",
            "labs": {"Hgb": "Stable and improved", "Reticulocyte count": "Appropriate response"}
        },
        {
            "scenario": "Resolution of neutropenia post-chemotherapy",
            "text": "Absolute neutrophil count recovered to within the normal range following completion of chemotherapy cycle. No signs of infection. Continue with next chemotherapy cycle as scheduled.",
            "labs": {"ANC": "Within normal limits", "Temperature": "Afebrile"}
        },
        {
            "scenario": "Stable INR on warfarin with consistent monitoring",
            "text": "International Normalized Ratio consistently within the therapeutic range (2.0-3.0) with regular warfarin dose adjustments based on monthly INR checks. No bleeding or thrombotic events.",
            "labs": {"INR": "Consistently therapeutic", "CBC": "Stable"}
        },
        {
            "scenario": "Reduced frequency of sickle cell pain crises with hydroxyurea",
            "text": "Significantly fewer vaso-occlusive pain crises reported since starting hydroxyurea therapy. Reduced need for opioid analgesics. Continue current medication.",
            "labs": {"Frequency of pain crises": "Decreased", "Hgb F": "Increased"}
        },
        # 14. OB/GYN
        {
            "scenario": "Resolution of pelvic pain in endometriosis with hormonal therapy",
            "text": "Significant reduction in chronic pelvic pain and dysmenorrhea with continuous oral contraceptive pills. Improved quality of life reported. Continue current hormonal management.",
            "labs": {"Pain score": "Decreased", "Endometriosis symptom diary": "Improved"}
        },
        {
            "scenario": "Regular ovulation restored in PCOS with medication",
            "text": "Patient reports regular menstrual cycles following treatment with clomiphene citrate. Ovulation confirmed with basal body temperature charting. Continue current medication.",
            "labs": {"Ovulation tracking": "Positive", "Progesterone level": "Consistent with ovulation"}
        },
        {
            "scenario": "Improved bone density with osteoporosis treatment",
            "text": "Follow-up DEXA scan shows improved bone mineral density in the spine and hip after one year of bisphosphonate therapy. Continue current treatment and calcium/vitamin D supplementation.",
            "labs": {"DEXA scan": "Improved T-scores", "Calcium/Vitamin D levels": "Adequate"}
        },
        {
            "scenario": "Resolution of menopausal symptoms with low-dose HRT",
            "text": "Significant reduction in hot flashes, night sweats, and vaginal dryness with low-dose estrogen therapy. Patient reports improved sleep and overall well-being. Continue current HRT.",
            "labs": {"Menopausal symptom score": "Decreased", "Estradiol level": "Within therapeutic range"}
        },
        {
            "scenario": "Successful management of gestational diabetes with diet and exercise",
            "text": "Blood glucose levels consistently within target range with adherence to gestational diabetes diet and regular moderate exercise. No need for insulin therapy at this time. Continue current management.",
            "labs": {"Fasting glucose": "Within target", "Post-prandial glucose": "Within target"}
        },
        # 15. Pediatrics
        {
            "scenario": "Improved growth velocity in growth hormone deficiency with treatment",
            "text": "Child's growth velocity has increased significantly since starting recombinant human growth hormone therapy. Height percentile improving. Continue current treatment and monitor growth regularly.",
            "labs": {"Growth velocity": "Increased", "IGF-1 level": "Within target range"}
        },
        {
            "scenario": "Reduced frequency of seizures in epilepsy with medication",
            "text": "Frequency of seizures significantly decreased with the current dose of antiepileptic medication. No breakthrough seizures reported recently. Continue current AED regimen.",
            "labs": {"Seizure frequency log": "Decreased", "AED level": "Therapeutic"}
        },
        {
            "scenario": "Improved lung function in cystic fibrosis with therapy",
            "text": "FEV1 improved on pulmonary function testing with consistent use of mucolytics, bronchodilators, and chest physiotherapy. Reduced frequency of respiratory infections. Continue current regimen.",
            "labs": {"FEV1": "Improved", "Sweat chloride test": "Consistent with diagnosis"}
        },
        {
            "scenario": "Control of allergic rhinitis symptoms with antihistamines",
            "text": "Significant reduction in nasal congestion, rhinorrhea, and sneezing with daily antihistamine use and avoidance of known allergens. Improved quality of life. Continue current management.",
            "labs": {"Allergy testing": "Previously positive, not repeated", "Symptom diary": "Improved"}
        },
        {
            "scenario": "Improved developmental milestones in preterm infant with support",
            "text": "Infant is now meeting age-appropriate developmental milestones following early intervention and supportive care. Continue developmental follow-up.",
            "labs": {"Developmental assessment": "Age-appropriate", "Growth parameters": "Within normal limits"}
        },
        # 16. Ophthalmology
    {
        "scenario": "Improved visual acuity after cataract surgery",
        "text": "Patient reports significantly clearer vision following uncomplicated cataract extraction with intraocular lens implantation. Visual acuity improved from 20/200 to 20/30. Continue postoperative eye drops as prescribed.",
        "labs": {"Visual Acuity": "20/30", "IOP": "Normal"}
    },
    {
        "scenario": "Stabilization of glaucoma progression with medication",
        "text": "Intraocular pressure remains within target range on topical prostaglandin analog. Visual field testing shows no further deterioration. Continue current eye drops and regular monitoring.",
        "labs": {"IOP": "Controlled", "Visual Fields": "Stable"}
    },
    {
        "scenario": "Resolution of diabetic macular edema with anti-VEGF injections",
        "text": "Optical coherence tomography shows resolution of macular edema following a course of intravitreal anti-VEGF therapy. Visual acuity stabilized. Continue regular retinal evaluations.",
        "labs": {"OCT": "No edema", "Visual Acuity": "Stable"}
    },
    {
        "scenario": "Improved dry eye symptoms with punctal plugs",
        "text": "Patient reports significant reduction in eye irritation, redness, and foreign body sensation following punctal plug insertion. Ocular surface staining improved. Continue artificial tears as needed.",
        "labs": {"Tear Break-up Time": "Improved", "Ocular Surface Staining": "Reduced"}
    },
    {
        "scenario": "Resolution of bacterial conjunctivitis with antibiotic drops",
        "text": "No evidence of conjunctival injection or discharge after completing course of topical antibiotics. Visual acuity returned to baseline. Discontinue treatment.",
        "labs": {"Slit Lamp Exam": "Clear", "Visual Acuity": "Baseline"}
    },

    # 17. Urology
    {
        "scenario": "Reduced nocturia in BPH with alpha-blocker",
        "text": "Patient reports decreased nighttime urination from 4-5x/night to 1-2x/night since starting tamsulosin. Improved sleep quality. Continue current medication.",
        "labs": {"IPSS Score": "Improved", "Post-void Residual": "Normal"}
    },
    {
        "scenario": "Resolution of kidney stone with medical expulsive therapy",
        "text": "Patient passed 4mm renal stone confirmed on strainer after course of tamsulosin and hydration. No residual stones on follow-up imaging. Discontinue MET.",
        "labs": {"CT Scan": "No stones", "Urinalysis": "Normal"}
    },
    {
        "scenario": "Improved erectile function with PDE5 inhibitor",
        "text": "Patient reports satisfactory sexual function with use of sildenafil as needed. IIEF-5 score improved from 10 to 22. Continue current treatment.",
        "labs": {"IIEF-5": "22", "Testosterone": "Normal"}
    },
    {
        "scenario": "Reduced urinary incontinence with pelvic floor therapy",
        "text": "Significant decrease in stress incontinence episodes following completion of 12-week pelvic floor muscle training program. Pad use reduced from 3/day to occasional. Continue exercises.",
        "labs": {"Pad Test": "Improved", "Bladder Diary": "Fewer leaks"}
    },
    {
        "scenario": "Resolution of recurrent UTIs with prophylactic antibiotics",
        "text": "No urinary tract infections reported in past 6 months while on low-dose nitrofurantoin prophylaxis. Urinalyses remain clear. Continue current prevention strategy.",
        "labs": {"Urinalysis": "Negative", "Culture": "No growth"}
    },

    # 18. ENT
    {
        "scenario": "Improved hearing with hearing aid fitting",
        "text": "Patient reports significantly better communication ability and quality of life following proper hearing aid adjustment and acclimatization. Speech discrimination improved.",
        "labs": {"Audiogram": "Improved with aids", "Speech Discrimination": "Better"}
    },
    {
        "scenario": "Resolution of chronic sinusitis with FESS",
        "text": "No sinus symptoms reported following functional endoscopic sinus surgery. Nasal endoscopy shows patent sinus ostia with healthy mucosa. Continue saline rinses.",
        "labs": {"Nasal Endoscopy": "Normal", "CT Scan": "Clear"}
    },
    {
        "scenario": "Reduced vertigo episodes in Ménière's disease with diet",
        "text": "Frequency of vertigo attacks decreased from weekly to monthly with strict low-sodium diet and diuretic therapy. Hearing remains stable. Continue current management.",
        "labs": {"Vertigo Frequency": "Decreased", "Audiogram": "Stable"}
    },
    {
        "scenario": "Improved swallowing post-esophageal dilation",
        "text": "Patient reports normal swallowing function following endoscopic dilation for benign esophageal stricture. Weight stabilized. Follow up as needed.",
        "labs": {"Barium Swallow": "Normal transit", "Weight": "Stable"}
    },
    {
        "scenario": "Resolution of vocal nodules with voice therapy",
        "text": "Laryngoscopy shows complete resolution of vocal fold nodules following 3 months of voice therapy and vocal hygiene. Normal voice quality restored. Continue good vocal habits.",
        "labs": {"Laryngoscopy": "Normal cords", "Voice Assessment": "Improved"}
    },

    # 19. Physical Medicine & Rehabilitation
    {
        "scenario": "Improved mobility post-total knee replacement with rehab",
        "text": "Significant improvement in knee range of motion and walking endurance following intensive physical therapy after TKR. Pain well-controlled. Continue home exercise program.",
        "labs": {"ROM": "0-120°", "6MWT": "Improved"}
    },
    {
        "scenario": "Increased independence in ADLs after stroke rehab",
        "text": "Patient now performs basic activities of daily living independently following 8 weeks of inpatient rehabilitation. FIM score improved from 60 to 105. Continue outpatient therapy.",
        "labs": {"FIM Score": "105", "Barthel Index": "Improved"}
    },
    {
        "scenario": "Pain reduction in CRPS with multimodal therapy",
        "text": "Complex regional pain syndrome symptoms improved with combination of physical therapy, nerve blocks, and gabapentin. Pain scores decreased from 8/10 to 3/10. Continue current regimen.",
        "labs": {"Pain Score": "3/10", "Temperature Differential": "Reduced"}
    },
    {
        "scenario": "Improved balance in vestibular hypofunction with VRT",
        "text": "Dizziness Handicap Inventory score decreased from 60 to 20 following 6 weeks of vestibular rehabilitation therapy. Romberg test normal. Continue exercises.",
        "labs": {"DHI": "20", "Romberg": "Normal"}
    },
    {
        "scenario": "Increased prosthetic use and function with training",
        "text": "Transfemoral amputee now ambulating independently with prosthesis following intensive gait training. Wearing time increased to 10 hours daily. Continue prosthetic use.",
        "labs": {"Prosthetic Use": "10 hrs/day", "Timed Up-and-Go": "Improved"}
    },

    # 20. Allergy & Immunology
    {
        "scenario": "Reduced allergic rhinitis symptoms with immunotherapy",
        "text": "Significant decrease in seasonal allergy symptoms during second year of subcutaneous allergen immunotherapy. Reduced need for antihistamines. Continue maintenance injections.",
        "labs": {"Symptom Score": "Improved", "Medication Use": "Decreased"}
    },
    {
        "scenario": "Control of chronic urticaria with omalizumab",
        "text": "No new hives or angioedema reported since starting monthly omalizumab injections. UAS7 score decreased from 28 to 2. Continue current treatment.",
        "labs": {"UAS7": "2", "Quality of Life Score": "Improved"}
    },
    {
        "scenario": "Improved asthma control with allergen avoidance",
        "text": "Reduced asthma exacerbations and rescue inhaler use after implementing comprehensive dust mite avoidance measures. FEV1 improved. Continue environmental controls.",
        "labs": {"FEV1": "Improved", "ACQ": "Better"}
    },
    {
        "scenario": "Successful desensitization to antibiotic allergy",
        "text": "Patient tolerated full course of previously allergenic antibiotic following graded challenge. No adverse reactions. Allergy label can be removed from chart.",
        "labs": {"Drug Challenge": "Negative", "Symptoms": "None"}
    },
    {
        "scenario": "Reduced frequency of hereditary angioedema attacks with prophylaxis",
        "text": "No HAE attacks reported in past 6 months while on regular C1 esterase inhibitor prophylaxis. Quality of life improved. Continue current treatment.",
        "labs": {"Attack Frequency": "0", "C4 Level": "Normalized"}
    }
    ],
    "Stable": [
        # 1. Cardiology
        {
            "scenario": "Chronic atrial fibrillation with stable anticoagulation",
            "text": "Atrial fibrillation rate controlled with beta-blocker. Patient remains on stable dose of apixaban with no thromboembolic events or bleeding complications. Continue current management.",
            "labs": {"INR (if on warfarin previously)": "Stable", "Renal function": "Stable"}
        },
        {
            "scenario": "Stable heart failure with preserved ejection fraction",
            "text": "Patient with heart failure with preserved ejection fraction reports stable exercise tolerance and no increase in symptoms of fluid overload on current diuretic regimen. Continue current medications.",
            "labs": {"BNP": "Stable", "ECHO": "Stable EF"}
        },
        {
            "scenario": "Essential hypertension well-controlled on single agent",
            "text": "Blood pressure consistently within target range on a stable dose of lisinopril. Patient reports no adverse effects. Continue current antihypertensive medication.",
            "labs": {"BP": "Stable", "Electrolytes": "Normal"}
        },
        {
            "scenario": "Stable mitral valve prolapse, asymptomatic",
            "text": "Patient with known mitral valve prolapse remains asymptomatic with no new murmurs or echocardiographic changes. Continue routine follow-up.",
            "labs": {"ECHO": "Stable MVP", "EKG": "No significant changes"}
        },
        {
            "scenario": "Stable peripheral artery disease, no progression of claudication",
            "text": "Patient with peripheral artery disease reports stable claudication distance. Ankle-brachial index remains unchanged. Continue aspirin and statin therapy.",
            "labs": {"ABI": "Stable", "Peripheral pulses": "Stable"}
        },
        # 2. Endocrinology
        {
            "scenario": "Stable hypothyroidism on consistent levothyroxine dose",
            "text": "TSH level remains within the target range on the current dose of levothyroxine. Patient reports no new symptoms of hypo- or hyperthyroidism. Continue current medication.",
            "labs": {"TSH": "Stable", "Free T4": "Stable"}
        },
        {
            "scenario": "Type 2 diabetes managed with metformin, stable glycemic control",
            "text": "HbA1c remains stable on metformin monotherapy. Patient adheres to dietary recommendations and regular exercise. Continue current medication.",
            "labs": {"HbA1c": "Stable", "Fasting Glucose": "Stable"}
        },
        {
            "scenario": "Stable benign thyroid nodules on surveillance",
            "text": "Serial thyroid ultrasounds show no significant change in the size or characteristics of benign thyroid nodules. Continue annual ultrasound surveillance.",
            "labs": {"Thyroid ultrasound": "Stable nodules", "TSH": "Normal"}
        },
        {
            "scenario": "Stable hyperlipidemia managed with statin therapy",
            "text": "LDL cholesterol remains within target range on the current dose of atorvastatin. Patient reports no muscle aches or other side effects. Continue current medication.",
            "labs": {"Lipid panel": "Stable", "LFTs": "Normal"}
        },
        {
            "scenario": "Stable adrenal insufficiency on hydrocortisone replacement",
            "text": "Patient with adrenal insufficiency reports stable energy levels and no symptoms of adrenal crisis on current hydrocortisone replacement therapy. Continue current regimen.",
            "labs": {"Electrolytes": "Stable", "Cortisol levels (random)": "Consistent"}
        },
        # 3. Oncology
        {
            "scenario": "Stable metastatic colon cancer on maintenance chemotherapy",
            "text": "Follow-up imaging shows stable metastatic lesions with no evidence of new disease progression while on maintenance chemotherapy. Patient tolerating treatment well. Continue current regimen.",
            "labs": {"CEA": "Stable", "Imaging": "No progression"}
        },
        {
            "scenario": "Chronic myeloid leukemia stable on tyrosine kinase inhibitor",
            "text": "BCR-ABL transcript levels remain stable at a low level on current tyrosine kinase inhibitor therapy. Hematologic parameters are within normal limits. Continue current medication.",
            "labs": {"BCR-ABL": "Stable low level", "CBC": "Normal"}
        },
        {
            "scenario": "Stable multiple myeloma on maintenance therapy",
            "text": "Serum M-protein and free light chains remain stable on maintenance therapy post-stem cell transplant. No new lytic lesions on skeletal survey. Continue current regimen.",
            "labs": {"M-protein": "Stable", "Free light chains": "Stable"}
        },
        {
            "scenario": "Stable low-grade non-Hodgkin lymphoma, watchful waiting",
            "text": "No significant changes in lymph node size or symptoms in patient with low-grade non-Hodgkin lymphoma managed with watchful waiting. Continue regular monitoring.",
            "labs": {"CBC": "Stable", "Lymph node exam": "Stable"}
        },
        {
            "scenario": "Stable thyroid cancer post-thyroidectomy on levothyroxine",
            "text": "Thyroglobulin levels remain undetectable post-total thyroidectomy for papillary thyroid cancer. Patient on stable dose of levothyroxine. Continue regular follow-up and thyroglobulin monitoring.",
            "labs": {"Thyroglobulin": "Undetectable", "TSH": "Within target"}
        },
        # 4. Pulmonology
        {
            "scenario": "Stable COPD on long-acting bronchodilators",
            "text": "Patient with COPD reports stable symptoms of dyspnea and cough on current long-acting bronchodilator therapy. No recent exacerbations. Continue current regimen.",
            "labs": {"FEV1": "Stable", "Symptom score": "Stable"}
        },
        {
            "scenario": "Stable interstitial lung disease on antifibrotic medication",
            "text": "Serial pulmonary function tests and imaging show no significant progression of interstitial lung disease while on current antifibrotic medication. Continue current therapy.",
            "labs": {"FVC": "Stable", "DLCO": "Stable", "HRCT": "No significant change"}
        },
        {
            "scenario": "Well-controlled obstructive sleep apnea with CPAP",
            "text": "Patient reports consistent CPAP use with good adherence. AHI remains low, and daytime sleepiness is resolved. Continue current CPAP settings.",
            "labs": {"AHI": "Low", "CPAP compliance": "High"}
        },
        {
            "scenario": "Stable bronchiectasis managed with airway clearance techniques",
            "text": "Patient with bronchiectasis reports stable sputum production and no recent pulmonary exacerbations with consistent use of airway clearance techniques. Continue current management.",
            "labs": {"Sputum culture": "Stable flora", "Chest CT": "No acute changes"}
        },
        {
            "scenario": "Stable pulmonary hypertension on vasodilator therapy",
            "text": "Patient with pulmonary hypertension reports stable exercise tolerance and no worsening of symptoms on current vasodilator therapy. Continue current regimen.",
            "labs": {"6MWD": "Stable", "NT-proBNP": "Stable"}
        },
        # 5. Rheumatology
        {
            "scenario": "Rheumatoid arthritis stable on DMARD therapy",
            "text": "Patient with rheumatoid arthritis reports stable joint pain and stiffness on current disease-modifying antirheumatic drug (DMARD) therapy. No new swollen joints. Continue current regimen.",
            "labs": {"CRP": "Stable", "ESR": "Stable", "Swollen joint count": "Stable"}
        },
        {
            "scenario": "Stable systemic lupus erythematosus on immunosuppressants",
            "text": "Patient with SLE reports stable disease activity with current immunosuppressant therapy. No new organ involvement. Continue current medication.",
            "labs": {"Anti-dsDNA": "Stable", "Complement levels": "Stable", "Renal function": "Stable"}
        },
        {
            "scenario": "Gout managed with urate-lowering therapy, no flares",
            "text": "Patient on urate-lowering therapy reports no recent gout flares. Serum uric acid level is within target range. Continue current medication.",
            "labs": {"Uric acid": "Stable within target", "CRP": "Normal"}
        },
        {
            "scenario": "Stable scleroderma with supportive management",
            "text": "Patient with scleroderma reports stable skin thickening and no new organ involvement with current supportive management. Continue current therapies and monitoring.",
            "labs": {"Skin score": "Stable", "Pulmonary function tests": "Stable"}
        },
        {
            "scenario": "Sjogren's syndrome symptoms stable with symptomatic treatment",
            "text": "Patient with Sjogren's syndrome reports stable symptoms of dry eyes and dry mouth with current symptomatic treatments. Continue current management.",
            "labs": {"Schirmer's test": "Stable", "Salivary flow rate": "Stable"}
        },
        # 6. Nephrology
        {
            "scenario": "Stable CKD Stage 2 with conservative management",
            "text": "Estimated GFR remains stable in patient with CKD Stage 2 managed with blood pressure control and dietary modifications. Continue current recommendations and monitoring.",
            "labs": {"eGFR": "Stable", "Urine albumin-to-creatinine ratio": "Stable"}
        },
        {
            "scenario": "Stable proteinuria in glomerular disease with ACE inhibitor",
            "text": "Urine protein excretion remains stable on ACE inhibitor therapy in patient with glomerular disease. Continue current medication and monitor proteinuria regularly.",
            "labs": {"24-hour urine protein": "Stable", "Serum albumin": "Stable"}
        },
        {
            "scenario": "Stable autosomal dominant polycystic kidney disease",
            "text": "Serial renal ultrasounds show no significant increase in the size or number of kidney cysts in patient with ADPKD. Renal function remains stable. Continue current management.",
            "labs": {"Renal ultrasound": "Stable cysts", "eGFR": "Stable"}
        },
        {
            "scenario": "Stable nephrotic syndrome with immunosuppressant therapy",
            "text": "Proteinuria remains stable at a moderate level on current immunosuppressant therapy for nephrotic syndrome. Serum albumin stable. Continue current regimen.",
            "labs": {"24-hour urine protein": "Stable", "Serum albumin": "Stable"}
        },
        {
            "scenario": "Stable kidney transplant function",
            "text": "Kidney transplant recipient with stable graft function on current immunosuppression regimen. Serum creatinine remains stable. Continue current medications and regular monitoring.",
            "labs": {"Serum creatinine": "Stable", "Electrolytes": "Stable"}
        },
        # 7. Infectious Disease
        {
            "scenario": "Stable chronic hepatitis C, not on treatment",
            "text": "Patient with chronic hepatitis C not currently on antiviral therapy shows stable liver enzymes and no signs of disease progression. Continue regular monitoring of liver function.",
            "labs": {"ALT": "Stable", "HCV RNA": "Positive, stable viral load"}
        },
        {
            "scenario": "Stable HIV infection on antiretroviral therapy, virologically suppressed",
            "text": "HIV viral load remains undetectable on current antiretroviral regimen. CD4 count remains stable. Continue current ART and regular monitoring.",
            "labs": {"Viral Load": "<20 copies/mL", "CD4": "Stable"}
        },
        {
            "scenario": "Stable latent tuberculosis infection, completed prophylaxis",
            "text": "Patient with previously positive TB skin test completed a full course of isoniazid prophylaxis. Chest X-ray remains negative. No further treatment indicated.",
            "labs": {"TST/IGRA": "Previously positive, not routinely repeated", "CXR": "Negative"}
        },
        {
            "scenario": "Stable herpes simplex virus infection, infrequent outbreaks",
            "text": "Patient with history of herpes simplex virus infection reports infrequent and mild outbreaks, managed with episodic antiviral therapy as needed. Continue current approach.",
            "labs": {"Viral culture (if symptomatic)": "Positive during outbreak", "Frequency of outbreaks": "Low"}
        },
        {
            "scenario": "Stable cytomegalovirus infection in immunocompetent patient",
            "text": "Patient with serologic evidence of past CMV infection remains asymptomatic with no signs of active disease. No treatment indicated in immunocompetent individuals.",
            "labs": {"CMV IgG": "Positive, stable", "CMV PCR": "Negative"}
        },
        # 8. Gastroenterology
        {
            "scenario": "Stable ulcerative colitis in remission on maintenance therapy",
            "text": "Patient with ulcerative colitis remains in clinical remission on maintenance mesalamine therapy. No rectal bleeding or increased stool frequency. Continue current medication.",
            "labs": {"CRP": "Low", "Fecal calprotectin": "Low", "Sigmoidoscopy (previous)": "Mucosal healing"}
        },
        {
            "scenario": "Stable Barrett's esophagus without dysplasia on surveillance",
            "text": "Surveillance endoscopy of Barrett's esophagus shows no evidence of dysplasia. Patient remains on proton pump inhibitor therapy for GERD symptoms. Continue annual surveillance.",
            "labs": {"Endoscopic biopsy": "No dysplasia", "pH monitoring": "Controlled reflux"}
        },
        {
            "scenario": "Stable primary biliary cholangitis on ursodeoxycholic acid",
            "text": "Liver enzymes remain stable in patient with primary biliary cholangitis on ursodeoxycholic acid therapy. No new symptoms of liver failure. Continue current medication.",
            "labs": {"ALP": "Stable", "Bilirubin": "Stable", "AMA": "Positive, stable titer"}
        },
        {
            "scenario": "Stable diverticulosis, asymptomatic",
            "text": "Patient with known diverticulosis remains asymptomatic with no history of diverticulitis. Continue high-fiber diet recommendations.",
            "labs": {"Colonoscopy (previous)": "Diverticulosis noted", "CBC": "Normal"}
        },
        {
            "scenario": "Stable non-alcoholic fatty liver disease, no progression on imaging",
            "text": "Liver ultrasound shows stable hepatic steatosis without evidence of fibrosis. Patient advised on lifestyle modifications (diet and exercise). Continue annual monitoring.",
            "labs": {"ALT": "Mildly elevated, stable", "Liver ultrasound": "Stable steatosis"}
        },
        # 9. Neurology
        {
            "scenario": "Stable essential tremor managed with beta-blocker",
            "text": "Tremor frequency and amplitude remain stable on low-dose beta-blocker therapy. No significant impact on daily activities. Continue current medication.",
            "labs": {"Tremor assessment scale": "Stable", "Neurological exam": "Stable tremor"}
        },
        {
            "scenario": "Stable restless legs syndrome managed with dopamine agonist",
            "text": "Symptoms of restless legs syndrome remain well-controlled with current dopamine agonist therapy. No augmentation reported. Continue current medication.",
            "labs": {"IRLSSG rating scale": "Low", "Sleep study": "Stable"}
        },
        {
            "scenario": "Stable trigeminal neuralgia managed with carbamazepine",
            "text": "Frequency and intensity of trigeminal neuralgia pain episodes remain well-controlled on current dose of carbamazepine. No significant side effects reported. Continue current medication.",
            "labs": {"Pain diary": "Low frequency", "Neurological exam": "No new deficits"}
        },
        {
            "scenario": "Stable myasthenia gravis on cholinesterase inhibitor",
            "text": "Symptoms of muscle weakness remain stable on current dose of cholinesterase inhibitor. No new bulbar symptoms or respiratory compromise. Continue current medication.",
            "labs": {"MGFA classification": "Stable", "Antibody levels": "Stable"}
        },
        {
            "scenario": "Stable peripheral neuropathy managed with gabapentin",
            "text": "Symptoms of peripheral neuropathy (numbness, tingling) remain stable on current dose of gabapentin. No progression of sensory loss or motor weakness. Continue current medication.",
            "labs": {"Neurological exam": "Stable neuropathy", "EMG/NCS (previous)": "Stable findings"}
        },
        # 10. Orthopedics
        {
            "scenario": "Stable rotator cuff tendinopathy managed conservatively",
            "text": "Shoulder pain associated with rotator cuff tendinopathy remains stable with consistent physical therapy and avoidance of aggravating activities. Continue current management.",
            "labs": {"Pain score": "Stable", "Range of motion": "Stable"}
        },
        {
            "scenario": "Stable knee osteoarthritis managed with intra-articular injections",
            "text": "Knee pain associated with osteoarthritis remains controlled with periodic intra-articular hyaluronic acid injections. Continue current management and home exercises.",
            "labs": {"Pain score": "Stable", "Knee exam": "Stable"}
        },
        {
            "scenario": "Stable carpal tunnel syndrome managed with wrist splint",
            "text": "Symptoms of carpal tunnel syndrome (numbness, tingling in hand) remain stable with consistent use of a wrist splint, especially at night. Continue current management.",
            "labs": {"Nerve conduction studies (previous)": "Stable findings", "Symptom diary": "Stable"}
        },
        {
            "scenario": "Stable spinal stenosis managed with conservative therapy",
            "text": "Back and leg pain associated with spinal stenosis remain stable with regular exercise, physical therapy, and occasional NSAID use. Continue current management.",
            "labs": {"Pain score": "Stable", "Neurological exam": "No new deficits"}
        },
        {
            "scenario": "Stable hallux valgus, managed conservatively",
            "text": "Pain and deformity associated with hallux valgus remain stable with comfortable footwear and orthotics. No progression of symptoms. Continue current management.",
            "labs": {"Foot exam": "Stable deformity", "Pain score": "Stable"}
        },
   # 11. Dermatology
        {
            "scenario": "Stable vitiligo with no new areas of depigmentation",
            "text": "No new areas of depigmentation observed on skin examination. Existing vitiligo patches remain stable in size and distribution. Continue current topical steroid therapy.",
            "labs": {"Wood's lamp examination": "Stable", "Photography": "No progression"}
        },
        {
            "scenario": "Chronic urticaria controlled with antihistamine",
            "text": "Frequency and severity of hives remain well-controlled with daily non-sedating antihistamine. No angioedema reported. Continue current medication.",
            "labs": {"Urticaria activity score": "Low", "Angioedema history": "None"}
        },
        {
            "scenario": "Stable alopecia areata with no further hair loss",
            "text": "No new patches of hair loss observed. Existing areas of alopecia remain stable. Continue current topical minoxidil treatment.",
            "labs": {"Hair examination": "Stable", "SALT score": "Stable"}
        },
        {
            "scenario": "Chronic pruritus maintained with emollient use",
            "text": "Itching sensation remains manageable with regular use of emollients and avoidance of skin irritants. No new skin lesions. Continue current skin care regimen.",
            "labs": {"Pruritus scale score": "Stable", "Skin exam": "No new findings"}
        },
        {
            "scenario": "Stable hidradenitis suppurativa with topical treatment",
            "text": "No new active nodules or abscesses noted. Existing lesions remain stable with topical clindamycin. Continue current treatment and hygiene measures.",
            "labs": {"HS severity score": "Stable", "Inflammatory marker": "Stable"}
        },
        # 12. Psychiatry
        {
            "scenario": "Well-managed ADHD with stimulant medication",
            "text": "Patient continues to report improved focus and reduced impulsivity on current dose of stimulant medication. Academic and social functioning remain stable. Continue current regimen.",
            "labs": {"Vanderbilt assessment scale": "Stable", "Side effect monitoring": "None significant"}
        },
        {
            "scenario": "Stable PTSD symptoms with ongoing therapy",
            "text": "Frequency and intensity of intrusive thoughts and flashbacks remain stable with regular participation in trauma-focused psychotherapy. Continue current treatment plan.",
            "labs": {"PCL-5 score": "Stable", "Therapy attendance": "Consistent"}
        },
        {
            "scenario": "Chronic generalized anxiety disorder managed with SSRI",
            "text": "Anxiety symptoms remain controlled with current dose of SSRI. Patient reports stable mood and ability to engage in daily activities. Continue current medication.",
            "labs": {"GAD-7 score": "Stable", "Functional assessment": "Stable"}
        },
        {
            "scenario": "Stable bulimia nervosa with ongoing therapy and nutritional counseling",
            "text": "Frequency of binge-purge episodes remains stable at a low level with continued participation in cognitive behavioral therapy and nutritional counseling. Maintain current treatment team approach.",
            "labs": {"Eating disorder examination questionnaire": "Stable", "Electrolytes": "Stable"}
        },
        {
            "scenario": "Borderline personality disorder symptoms managed with DBT",
            "text": "Patient demonstrates consistent use of dialectical behavior therapy skills, resulting in stable interpersonal relationships and emotional regulation. Continue ongoing DBT.",
            "labs": {"DBT skills usage log": "Consistent", "Mood diary": "Stable"}
        },
        # 13. Hematology
        {
            "scenario": "Stable polycythemia vera with phlebotomy",
            "text": "Hematocrit levels remain stable within the target range with regular phlebotomy. No new thrombotic events. Continue current management.",
            "labs": {"Hematocrit": "Stable", "JAK2 mutation status": "Positive, stable"}
        },
        {
            "scenario": "Chronic lymphocytic leukemia stable on watchful waiting",
            "text": "No significant changes in white blood cell count or lymph node size on serial examinations. Patient remains asymptomatic. Continue watchful waiting with regular monitoring.",
            "labs": {"WBC count": "Stable", "Lymph node size": "Stable"}
        },
        {
            "scenario": "Essential thrombocythemia stable on low-dose aspirin",
            "text": "Platelet count remains stable on low-dose aspirin therapy. No new thrombotic or bleeding events. Continue current management.",
            "labs": {"Platelet count": "Stable", "Bone marrow biopsy": "Consistent with ET"}
        },
        {
            "scenario": "Myelodysplastic syndrome stable with supportive care",
            "text": "No significant progression of cytopenias or increase in blast percentage. Patient continues to receive supportive care with transfusions as needed. Monitor regularly for disease progression.",
            "labs": {"CBC with differential": "Stable", "Bone marrow aspirate": "Stable"}
        },
        {
            "scenario": "Factor V Leiden carrier state, no thrombotic events",
            "text": "Patient with known Factor V Leiden heterozygous mutation remains asymptomatic with no history of thrombotic events. Continue prophylactic measures and counsel on risk factors.",
            "labs": {"Factor V Leiden genotype": "Heterozygous, stable", "Coagulation studies": "Normal"}
        },
        # 14. OB/GYN
        {
            "scenario": "Stable uterine fibroids with no growth on surveillance",
            "text": "Serial pelvic ultrasounds show no significant increase in the size or number of uterine fibroids. Patient reports stable menstrual bleeding and no new pelvic pain. Continue annual surveillance.",
            "labs": {"Pelvic ultrasound": "Stable fibroids", "CBC": "Stable"}
        },
        {
            "scenario": "Well-controlled endometriosis with continuous oral contraceptives",
            "text": "Patient reports stable control of dysmenorrhea and pelvic pain with continuous oral contraceptive use. No new symptoms suggestive of disease progression. Continue current hormonal therapy.",
            "labs": {"Pain score": "Stable", "Endometriosis symptom diary": "Stable"}
        },
        {
            "scenario": "Stable cervical dysplasia (CIN 1) on surveillance",
            "text": "Repeat cervical cytology shows persistent low-grade squamous intraepithelial lesion (LSIL/CIN 1) without progression. Continue annual surveillance with Pap smear.",
            "labs": {"Pap smear": "Consistent LSIL/CIN 1", "HPV testing": "Persistent positive"}
        },
        {
            "scenario": "Stable polycystic ovarian syndrome with lifestyle management",
            "text": "Patient reports stable menstrual cycle regularity with consistent adherence to dietary modifications and exercise. No new metabolic complications. Continue lifestyle recommendations.",
            "labs": {"Menstrual cycle history": "Stable", "Metabolic panel": "Stable"}
        },
        {
            "scenario": "Asymptomatic uterine polyp on surveillance",
            "text": "Repeat pelvic ultrasound shows a stable, small uterine polyp without any associated bleeding or symptoms. Continue annual surveillance ultrasound.",
            "labs": {"Pelvic ultrasound": "Stable polyp", "Endometrial biopsy (previous)": "Benign"}
        },
        # 15. Pediatrics
        {
            "scenario": "Stable asthma severity on current controller medication",
            "text": "Child's asthma symptoms remain well-controlled with daily inhaled corticosteroid and as-needed short-acting beta-agonist. No recent exacerbations requiring oral steroids. Continue current regimen.",
            "labs": {"FEV1": "Stable", "SABA use": "Minimal"}
        },
        {
            "scenario": "Well-managed type 1 diabetes with insulin therapy",
            "text": "Blood glucose levels remain largely within target range with current insulin regimen and consistent carbohydrate counting. HbA1c stable. Continue current management.",
            "labs": {"HbA1c": "Stable", "Glucose logs": "Mostly within target"}
        },
        {
            "scenario": "Stable atopic dermatitis with topical corticosteroids and emollients",
            "text": "Skin condition remains stable with regular use of emollients and intermittent topical corticosteroids for mild flares. No new widespread involvement. Continue current skin care regimen.",
            "labs": {"Eczema Area and Severity Index (EASI)": "Stable", "Pruritus score": "Stable"}
        },
        {
            "scenario": "Stable food allergies with strict avoidance",
            "text": "No allergic reactions reported with strict avoidance of known food allergens. Continue carrying epinephrine auto-injector and adhering to dietary restrictions.",
            "labs": {"Allergy testing": "Previously positive, avoidance is primary management", "Reaction history": "None recent"}
        }
],
    "Worsened": [
        # 1. Cardiology
        {
            "scenario": "Unstable angina progressing to MI",
            "text": "Increasing frequency and severity of chest pain at rest. EKG now shows ST depression. Troponin trending upwards. Admit for urgent cardiac catheterization.",
            "labs": {"Troponin": "Rising trend", "EKG": "ST depression"}
        },
        {
            "scenario": "Acute decompensated heart failure",
            "text": "Increased shortness of breath at rest, orthopnea, and peripheral edema. BNP significantly elevated. Increased diuretic dosage and consider IV vasodilators.",
            "labs": {"BNP": "Significantly elevated", "Chest X-ray": "Pulmonary edema"}
        },
        {
            "scenario": "Hypertensive emergency with end-organ damage",
            "text": "Blood pressure 220/120 mmHg with new onset headache and blurred vision. Fundoscopic exam shows papilledema. Admit to ICU for controlled blood pressure lowering.",
            "labs": {"BP": "220/120 mmHg", "Fundoscopy": "Papilledema"}
        },
        {
            "scenario": "Severe bradycardia requiring intervention",
            "text": "Heart rate dropped to 35 bpm with symptomatic dizziness and near-syncope. EKG shows third-degree AV block. Temporary pacemaker insertion planned.",
            "labs": {"Heart rate": "35 bpm", "EKG": "Third-degree AV block"}
        },
        {
            "scenario": "Acute aortic dissection",
            "text": "Sudden onset of severe tearing chest pain radiating to the back. Blood pressure differential between arms. CT angiogram confirms aortic dissection. Emergent surgical consultation.",
            "labs": {"BP differential": "Significant", "CT Angiogram": "Aortic dissection"}
        },
        # 2. Endocrinology
        {
            "scenario": "Hyperosmolar hyperglycemic state",
            "text": "Markedly elevated blood glucose (>600 mg/dL) with altered mental status and dehydration. Serum osmolality elevated. Initiate aggressive fluid resuscitation and insulin infusion.",
            "labs": {"Glucose": ">600 mg/dL", "Serum osmolality": "Elevated"}
        },
        {
            "scenario": "Thyroid storm",
            "text": "Marked tachycardia, fever, agitation, and altered mental status in patient with hyperthyroidism. Elevated free T3 and T4. Initiate beta-blockers, thionamides, and supportive care.",
            "labs": {"Free T3": "Elevated", "Free T4": "Elevated", "Heart rate": "Tachycardic"}
        },
        {
            "scenario": "Severe hypoglycemia with seizure",
            "text": "Patient found unresponsive with blood glucose of 35 mg/dL and witnessed seizure. Administered intravenous dextrose. Evaluate for cause of severe hypoglycemia.",
            "labs": {"Glucose": "35 mg/dL", "Ketones": "Negative"}
        },
        {
            "scenario": "Adrenal crisis",
            "text": "Hypotension, nausea, vomiting, and abdominal pain in patient with known adrenal insufficiency. Electrolyte abnormalities noted. Administer intravenous hydrocortisone and fluids.",
            "labs": {"Sodium": "Low", "Potassium": "High", "Cortisol (random)": "Low"}
        },
        {
            "scenario": "Worsening diabetic ketoacidosis despite treatment",
            "text": "Persistent acidosis and elevated ketones despite ongoing insulin infusion and fluid resuscitation for DKA. Consider alternative diagnoses or treatment adjustments.",
            "labs": {"pH": "Persistently low", "Bicarbonate": "Persistently low", "Ketones": "Persistently high"}
        },
        # 3. Oncology
        {
            "scenario": "Malignant pleural effusion causing respiratory distress",
            "text": "Increasing shortness of breath and chest X-ray shows large pleural effusion in patient with metastatic lung cancer. Thoracentesis planned for symptom relief and fluid analysis.",
            "labs": {"Pleural fluid analysis": "Malignant cells", "SpO2": "Decreased"}
        },
        {
            "scenario": "Spinal cord compression from metastatic disease",
            "text": "New onset back pain with progressive lower extremity weakness and bowel/bladder dysfunction in patient with metastatic prostate cancer. MRI spine confirms spinal cord compression. Emergent radiation therapy consult.",
            "labs": {"MRI Spine": "Spinal cord compression", "Neurological exam": "Weakness, sensory deficits"}
        },
        {
            "scenario": "Superior vena cava syndrome",
            "text": "Facial swelling, neck vein distension, and shortness of breath in patient with mediastinal mass from lymphoma. Chest CT confirms SVC obstruction. Initiate radiation therapy and supportive care.",
            "labs": {"Chest CT": "SVC obstruction", "Respiratory status": "Compromised"}
        },
        {
            "scenario": "Febrile neutropenia post-chemotherapy",
            "text": "Fever (temperature > 100.4°F) and absolute neutrophil count < 500/μL in patient receiving chemotherapy. Initiate broad-spectrum antibiotics immediately.",
            "labs": {"Temperature": ">100.4°F", "ANC": "<500/μL", "Blood cultures": "Pending"}
        },
        {
            "scenario": "Brain metastases causing increased intracranial pressure",
            "text": "Worsening headache, nausea, vomiting, and new neurological deficits in patient with metastatic melanoma. MRI brain shows multiple brain metastases with edema. Initiate steroids and neurosurgery consult.",
            "labs": {"MRI Brain": "Brain metastases with edema", "Neurological exam": "Focal deficits"}
        },
        # 4. Pulmonology
        {
            "scenario": "Severe asthma exacerbation requiring intubation",
            "text": "Progressive respiratory distress despite aggressive bronchodilator therapy. Peak flow severely reduced. Arterial blood gas shows worsening hypercapnia and hypoxia. Intubation and mechanical ventilation required.",
            "labs": {"Peak flow": "Severely reduced", "ABG": "Worsening hypercapnia and hypoxia"}
        },
        {
            "scenario": "Pulmonary embolism with hemodynamic instability",
            "text": "Sudden onset of severe shortness of breath, chest pain, and hypotension. CT angiogram confirms large pulmonary embolism. Initiate systemic anticoagulation and consider thrombolysis.",
            "labs": {"CT Angiogram": "Pulmonary embolism", "BP": "Hypotensive"}
        },
        {
            "scenario": "Worsening pneumonia with respiratory failure",
            "text": "Increasing oxygen requirement and worsening infiltrates on chest X-ray despite antibiotic therapy for pneumonia. Arterial blood gas shows hypoxemia. Consider transfer to ICU for higher level of care.",
            "labs": {"CXR": "Worsening infiltrates", "ABG": "Hypoxemia"}
        },
        {
            "scenario": "Pneumothorax causing significant lung collapse",
            "text": "Sudden onset of unilateral chest pain and shortness of breath. Chest X-ray shows large pneumothorax with significant lung collapse. Chest tube insertion required.",
            "labs": {"Chest X-ray": "Large pneumothorax", "SpO2": "Decreased"}
        },
        {
            "scenario": "Acute exacerbation of interstitial lung disease",
            "text": "Rapidly progressive shortness of breath and hypoxemia in patient with known interstitial lung disease. High-resolution CT shows new ground-glass opacities. Initiate high-dose steroids and consider other immunosuppressants.",
            "labs": {"SpO2": "Decreased", "HRCT": "New ground-glass opacities"}
        },
        # 5. Rheumatology
        {
            "scenario": "Severe systemic lupus erythematosus flare with multi-organ involvement",
            "text": "Worsening fatigue, joint pain, rash, and new onset renal involvement (increased creatinine and proteinuria) in patient with SLE. Elevated inflammatory markers and dsDNA. Admit for high-dose steroids and immunosuppressants.",
            "labs": {"Creatinine": "Increased", "Proteinuria": "Increased", "dsDNA": "Elevated"}
        },
        {
            "scenario": "Acute gout flare with polyarticular involvement",
            "text": "Severe pain, redness, and swelling in multiple joints (knees, ankles, wrists). Serum uric acid elevated. Initiate high-dose NSAIDs and colchicine.",
            "labs": {"Uric acid": "Elevated", "CRP": "Elevated", "Joint aspiration": "Monosodium urate crystals"}
        },
        {
            "scenario": "Worsening rheumatoid arthritis with erosive disease",
            "text": "Increasing joint pain, swelling, and stiffness despite current DMARD therapy. New erosions seen on hand and foot X-rays. Consider switching to a biologic agent.",
            "labs": {"CRP": "Elevated", "ESR": "Elevated", "X-rays": "New erosions"}
        },
        {
            "scenario": "Giant cell arteritis with vision loss",
            "text": "New onset headache, scalp tenderness, and sudden vision loss in one eye. Elevated ESR and CRP. Initiate high-dose corticosteroids immediately.",
            "labs": {"ESR": "Markedly elevated", "CRP": "Elevated", "Temporal artery biopsy": "Pending"}
        },
        {
            "scenario": "Severe polymyositis with respiratory muscle weakness",
            "text": "Progressive proximal muscle weakness and new onset shortness of breath. Elevated creatine kinase. Pulmonary function tests show decreased vital capacity. Initiate high-dose corticosteroids and consider other immunosuppressants.",
            "labs": {"CK": "Markedly elevated", "Pulmonary function tests": "Reduced vital capacity", "EMG": "Myopathic changes"}
        },
        # 6. Nephrology
        {
            "scenario": "Acute kidney injury due to ATN",
            "text": "Rapid increase in serum creatinine and decreased urine output. Urine sediment shows muddy brown casts. Discontinue nephrotoxic medications and provide supportive care.",
            "labs": {"Creatinine": "Increased", "BUN": "Increased", "Urine sediment": "Muddy brown casts"}
        },
        {
            "scenario": "Worsening glomerulonephritis with nephrotic syndrome",
            "text": "Increasing peripheral edema, heavy proteinuria, and hypoalbuminemia. Serum creatinine also rising. Consider kidney biopsy for diagnosis and initiate immunosuppressive therapy.",
            "labs": {"Proteinuria": "Nephrotic range", "Serum albumin": "Low", "Creatinine": "Rising"}
        },
        {
            "scenario": "Acute renal vein thrombosis",
            "text": "Sudden onset of flank pain and hematuria. Serum creatinine rising. CT angiogram of the abdomen and pelvis confirms renal vein thrombosis. Initiate anticoagulation.",
            "labs": {"Creatinine": "Rising", "Hematuria": "Present", "CT Angiogram": "Renal vein thrombosis"}
        },
        {
            "scenario": "Hyperkalemia refractory to medical management",
            "text": "Severely elevated serum potassium (7.5 mEq/L) with EKG changes (peaked T waves). Refractory to calcium gluconate and insulin/glucose. Emergent hemodialysis indicated.",
            "labs": {"Potassium": "7.5 mEq/L", "EKG": "Peaked T waves"}
        },
        {
            "scenario": "Acute on chronic kidney disease exacerbation",
            "text": "Rapid worsening of kidney function in patient with known CKD, with increasing creatinine, metabolic acidosis, and fluid overload. Initiate more aggressive dialysis and medical management.",
            "labs": {"Creatinine": "Significantly increased", "pH": "Low", "Bicarbonate": "Low"}
        },
        # 7. Infectious Disease
        {
            "scenario": "Septic shock",
            "text": "Hypotension requiring vasopressors, elevated lactate, and signs of end-organ damage (oliguria, altered mental status) in the setting of confirmed infection. Continue broad-spectrum antibiotics and supportive care in ICU.",
            "labs": {"Lactate": "Elevated", "BP": "Hypotensive despite fluids", "Urine output": "Decreased"}
        },
        {
            "scenario": "Meningitis with altered mental status",
            "text": "Fever, severe headache, neck stiffness, and new onset altered mental status. Lumbar puncture shows elevated white blood cell count and protein in CSF. Initiate broad-spectrum antibiotics and antiviral therapy.",
            "labs": {"CSF WBC": "Elevated", "CSF Protein": "Elevated", "Mental status": "Altered"}
        },
        {
            "scenario": "Severe Clostridium difficile colitis with toxic megacolon",
            "text": "Worsening severe watery diarrhea, abdominal pain, and distension. Abdominal X-ray shows colonic dilation. Discontinue current antibiotics and initiate oral vancomycin and consider surgical consultation.",
            "labs": {"Stool C. difficile PCR": "Positive", "Abdominal X-ray": "Toxic megacolon"}
        },
        {
            "scenario": "Necrotizing fasciitis",
            "text": "Rapidly spreading skin and soft tissue infection with severe pain out of proportion to exam findings, crepitus, and systemic signs of infection. Emergent surgical debridement and broad-spectrum antibiotics required.",
            "labs": {"CRP": "Markedly elevated", "WBC": "Elevated", "Surgical findings": "Necrotizing fasciitis"}
        },
        {
            "scenario": "Multi-drug resistant organism infection",
            "text": "Persistent fever and elevated inflammatory markers despite broad-spectrum antibiotics. Cultures positive for a multi-drug resistant bacteria. Adjust antibiotics based on sensitivity results.",
            "labs": {"Blood/Sputum/Urine cultures": "Positive for MDRO", "Antibiotic sensitivities": "Limited options"}
        },
        # 8. Gastroenterology
        {
            "scenario": "Acute liver failure",
            "text": "Rapidly worsening jaundice, coagulopathy (elevated INR), and encephalopathy in patient with no prior liver disease. Evaluate for causes and consider liver transplant referral.",
            "labs": {"Bilirubin": "Markedly elevated", "INR": "Elevated", "Mental status": "Altered"}
        },
        {
            "scenario": "Severe pancreatitis with complications",
            "text": "Worsening severe abdominal pain, elevated lipase, and CT scan shows pancreatic necrosis and fluid collections. Patient developing organ dysfunction. Transfer to ICU for intensive management.",
            "labs": {"Lipase": "Markedly elevated", "CT Abdomen": "Necrosis and fluid collections", "Organ dysfunction markers": "Abnormal"}
        },
        {
            "scenario": "Perforated peptic ulcer",
            "text": "Sudden onset of severe abdominal pain with signs of peritonitis (rigid abdomen, rebound tenderness). Abdominal X-ray shows free air. Emergent surgical repair required.",
            "labs": {"Abdominal X-ray": "Free air", "WBC": "Elevated"}
        },
        {
            "scenario": "Severe inflammatory bowel disease flare requiring hospitalization",
            "text": "Increased frequency of bloody diarrhea, severe abdominal pain, and systemic symptoms (fever, tachycardia) in patient with IBD. Elevated inflammatory markers. Admit for intravenous steroids and consideration of biologic therapy.",
            "labs": {"CRP": "Markedly elevated", "Fecal calprotectin": "Markedly elevated", "Colonoscopy": "Severe inflammation"}
        },
        {
            "scenario": "Hepatic encephalopathy progression",
            "text": "Worsening confusion, asterixis, and elevated ammonia levels in patient with cirrhosis. Increase lactulose and consider rifaximin. Evaluate for precipitating factors.",
            "labs": {"Ammonia": "Elevated", "Mental status": "Worsening", "Asterixis": "Present"}
        },
        # 9. Neurology
        {
            "scenario": "Status epilepticus",
            "text": "Continuous seizure activity lasting longer than 5 minutes or recurrent seizures without regaining consciousness between episodes. Administer benzodiazepines and other anti-epileptic medications urgently.",
            "labs": {"EEG": "Continuous seizure activity", "Electrolytes": "May be abnormal"}
        },
        {
            "scenario": "Increasing intracranial pressure due to brain tumor",
            "text": "Worsening headache, vomiting, papilledema, and new focal neurological deficits in patient with known brain tumor. MRI brain shows increased tumor size and edema. Neurosurgery consult for possible intervention.",
            "labs": {"MRI Brain": "Increased tumor size and edema", "Neurological exam": "Worsening deficits"}
        },
        {
            "scenario": "Guillain-Barré syndrome with respiratory failure",
            "text": "Progressive ascending weakness leading to respiratory muscle involvement. Decreased vital capacity. Intubation and mechanical ventilation required. Initiate IVIG or plasmapheresis.",
            "labs": {"Pulmonary function tests": "Reduced vital capacity", "EMG/NCS": "Demyelinating polyneuropathy"}
        },
        {
            "scenario": "Myasthenic crisis",
            "text": "Worsening muscle weakness, particularly affecting bulbar muscles (swallowing, speech) and respiratory muscles, in patient with myasthenia gravis. Requires intubation and increased immunosuppression.",
            "labs": {"MGFA classification": "Worsening", "Pulmonary function tests": "Reduced"}
        },
        {
            "scenario": "Cerebral edema post-stroke",
            "text": "Worsening level of consciousness and signs of increased intracranial pressure following a large ischemic stroke. Repeat CT head shows cerebral edema with midline shift. Initiate hyperosmolar therapy and consider hemicraniectomy.",
            "labs": {"CT Head": "Cerebral edema with midline shift", "Neurological exam": "Worsening"}
        },
    # 10. Orthopedics
        {
            "scenario": "Compartment syndrome post-fracture",
            "text": "Severe pain out of proportion to injury, pallor, pulselessness, paresthesia, and paralysis in the affected limb. Increased pressure within the muscle compartment. Emergent fasciotomy required.",
            "labs": {"Compartment pressure": "Elevated", "Clinical exam": "5 Ps"}
        },
        {
            "scenario": "Open fracture with significant contamination",
            "text": "Open fracture with visible bone and significant soft tissue damage and contamination. High risk of infection. Emergent surgical debridement and intravenous antibiotics required.",
            "labs": {"Wound culture": "Pending", "X-ray": "Open fracture"}
        },
        {
            "scenario": "Dislocation requiring urgent reduction",
            "text": "Severe pain and deformity of a joint (e.g., hip, shoulder). Unable to move the joint. Requires urgent closed or open reduction to restore joint alignment.",
            "labs": {"X-ray": "Dislocation", "Clinical exam": "Deformity, inability to move joint"}
        },
        {
            "scenario": "Cauda equina syndrome",
            "text": "Severe back pain with bilateral leg weakness, saddle anesthesia, and bowel/bladder dysfunction. MRI spine confirms cauda equina compression. Emergent surgical decompression required.",
            "labs": {"MRI Spine": "Cauda equina compression", "Neurological exam": "Weakness, sensory deficits, bowel/bladder dysfunction"}
        },
        {
            "scenario": "Septic arthritis",
            "text": "Severe joint pain, swelling, and redness with fever. Joint aspiration shows purulent fluid. Initiate intravenous antibiotics and consider surgical drainage.",
            "labs": {"Joint aspiration": "Purulent fluid, positive gram stain and culture", "WBC": "Elevated"}
        },
        # 11. Dermatology
        {
            "scenario": "Stevens-Johnson syndrome",
            "text": "Rapidly progressing rash with mucosal involvement (mouth, eyes), fever, and skin detachment <10% BSA. Admit for supportive care and consider IVIG.",
            "labs": {"BSA detachment": "<10%", "Mucosal involvement": "Present"}
        },
        {
            "scenario": "Widespread bullous pemphigoid",
            "text": "Extensive blistering eruption with significant pruritus. Positive direct immunofluorescence. Initiate systemic corticosteroids and other immunosuppressants.",
            "labs": {"Direct immunofluorescence": "Positive", "Number of blisters": "Extensive"}
        },
        {
            "scenario": "Severe drug reaction with eosinophilia and systemic symptoms (DRESS)",
            "text": "Extensive rash, fever, lymphadenopathy, and internal organ involvement (liver, kidneys) in the setting of a new medication. Discontinue offending drug and initiate systemic corticosteroids.",
            "labs": {"Eosinophils": "Elevated", "LFTs/Renal function": "Abnormal"}
        },
        {
            "scenario": "Necrotizing soft tissue infection",
            "text": "Rapidly spreading skin infection with pain out of proportion to exam, fever, and systemic toxicity. Surgical debridement and broad-spectrum antibiotics required.",
            "labs": {"CRP": "Elevated", "Blood cultures": "Pending"}
        },
        {
            "scenario": "Erythroderma",
            "text": "Generalized redness and scaling affecting >90% of the body surface area. May be associated with fever and lymphadenopathy. Admit for supportive care and topical/systemic therapy.",
            "labs": {"BSA involvement": ">90%", "Skin biopsy": "May be needed"}
        },
        # 12. Psychiatry
        {
            "scenario": "Acute psychosis with catatonia",
            "text": "Patient is mute, immobile, and exhibits posturing or waxy flexibility. Requires inpatient management with lorazepam and possibly ECT.",
            "labs": {"Mental status exam": "Catatonic features"}
        },
        {
            "scenario": "Severe mania with aggression",
            "text": "Patient is highly agitated, aggressive, and poses a threat to self or others. Requires inpatient management with antipsychotics and mood stabilizers.",
            "labs": {"Mental status exam": "Agitation, aggression"}
        },
        {
            "scenario": "Suicidal ideation with plan and intent",
            "text": "Patient expresses a clear plan and intent to end their life. Requires immediate hospitalization for safety.",
            "labs": {"Suicidal ideation": "Present with plan and intent"}
        },
        {
            "scenario": "Severe panic attack with respiratory distress",
            "text": "Patient experiences overwhelming anxiety, chest pain, shortness of breath, and fear of impending doom. May require benzodiazepines and supportive care.",
            "labs": {"Anxiety level": "Severe", "Respiratory status": "Distressed"}
        },
         {
            "scenario": "Neuroleptic malignant syndrome",
            "text": "Fever, rigidity, altered mental status, and autonomic instability in a patient taking antipsychotic medication. Discontinue antipsychotic and provide supportive care.",
            "labs": {"CK": "Elevated", "WBC": "Elevated", "Mental status": "Altered"}
        },
        # 13. Hematology
        {
            "scenario": "Disseminated intravascular coagulation (DIC)",
            "text": "Widespread bleeding and clotting, often in the setting of sepsis or trauma. Elevated PT/PTT, low platelets, and elevated D-dimer. Requires treatment of the underlying cause and supportive care.",
            "labs": {"PT/PTT": "Elevated", "Platelets": "Low", "D-dimer": "Elevated"}
        },
        {
            "scenario": "Thrombotic thrombocytopenic purpura (TTP)",
            "text": "Microangiopathic hemolytic anemia, thrombocytopenia, and neurological symptoms. Low ADAMTS13 activity. Requires plasma exchange.",
            "labs": {"Platelets": "Low", "Hemoglobin": "Low", "ADAMTS13 activity": "Low"}
        },
        {
            "scenario": "Acute promyelocytic leukemia (APL) with coagulopathy",
            "text": "Bleeding and clotting abnormalities in a patient with APL. Requires emergent treatment with all-trans retinoic acid (ATRA).",
            "labs": {"Promyelocytes": "Elevated", "PT/PTT": "Elevated"}
        },
        {
            "scenario": "Heparin-induced thrombocytopenia (HIT)",
            "text": "Thrombocytopenia and thrombosis in a patient receiving heparin. Requires discontinuation of heparin and initiation of alternative anticoagulation.",
            "labs": {"Platelets": "Low", "HIT antibody": "Positive"}
        },
        {
             "scenario": "Acute hemolytic transfusion reaction",
             "text": "Fever, chills, back pain, and dark urine following a blood transfusion. Requires immediate cessation of the transfusion and supportive care.",
             "labs": {"Hemoglobin": "Decreasing", "Direct antiglobulin test (DAT)": "Positive"}
         },
        # 14. OB/GYN
        {
            "scenario": "Postpartum hemorrhage",
            "text": "Excessive bleeding after childbirth. Requires uterine massage, uterotonic medications, and possibly blood transfusion.",
            "labs": {"Hemoglobin": "Decreasing", "Estimated blood loss": "Significant"}
        },
        {
            "scenario": "Ruptured ectopic pregnancy",
            "text": "Severe abdominal pain, vaginal bleeding, and signs of shock in a pregnant woman. Requires emergent surgical intervention.",
            "labs": {"Hemoglobin": "Decreasing", "Pregnancy test": "Positive"}
        },
        {
            "scenario": "Placental abruption",
            "text": "Vaginal bleeding and abdominal pain in a pregnant woman. May lead to fetal distress. Requires close monitoring and possible emergent delivery.",
            "labs": {"Fetal heart rate": "May be abnormal"}
        },
        {
            "scenario": "Preterm labor with cervical change",
            "text": "Regular uterine contractions and cervical dilation before 37 weeks gestation. Requires tocolytic medications and steroids for fetal lung maturity.",
            "labs": {"Gestational age": "<37 weeks", "Cervical dilation": "Present"}
        },
        {
            "scenario": "Uterine rupture",
            "text": "Sudden abdominal pain and vaginal bleeding in a woman with a prior Cesarean section. Requires emergent surgical intervention.",
            "labs": {"Fetal heart rate": "May be abnormal", "Clinical exam": "Acute abdomen"}
        },
        # 15. Pediatrics
        {
            "scenario": "Severe bronchiolitis with respiratory failure",
            "text": "Respiratory distress, wheezing, and hypoxia in an infant. May require intubation and mechanical ventilation.",
            "labs": {"SpO2": "Decreased", "Respiratory rate": "Elevated"}
        },
        {
            "scenario": "Meningitis in a young child",
            "text": "Fever, irritability, and lethargy in a young child. May also have neck stiffness and bulging fontanelle. Requires lumbar puncture and antibiotics.",
            "labs": {"CSF WBC": "Elevated", "CSF Protein": "Elevated"}
        },
        {
            "scenario": "Diabetic ketoacidosis in a child",
            "text": "Elevated blood glucose, acidosis, and ketonemia in a child with diabetes. Requires insulin infusion and fluid resuscitation.",
            "labs": {"Glucose": "Elevated", "pH": "Low", "Ketones": "Elevated"}
        },
        {
            "scenario": "Intussusception",
            "text": "Severe abdominal pain, vomiting, and bloody stools in an infant. Requires air or hydrostatic enema for reduction.",
            "labs": {"Abdominal ultrasound": "Target sign"}
        },
        {
            "scenario": "Sepsis in a neonate",
            "text": "Fever, lethargy, and poor feeding in a newborn. Requires blood cultures and broad-spectrum antibiotics.",
            "labs": {"Blood cultures": "Pending", "WBC": "May be elevated or low"}
        }
]
}



def generate_notes(num_notes=500):
    notes = []
    outcomes = ["Improved", "Stable", "Worsened"]
    for _ in range(num_notes):
        outcome = random.choice(outcomes)
        scenario = random.choice(categories[outcome])
        note = (
            f"{scenario['text']} "
            f"Labs: {', '.join([f'{k}={v}' for k, v in scenario['labs'].items()])}. "
        )
        notes.append({"note_text": note, "trial_outcome": outcome})
    return notes

# Generate CSV
#notes = generate_notes(1000)
import pandas as pd

df = pd.read_csv(r'C:\Users\pinak\Downloads\Internship\clinical_notes_replaced.csv')

# Drop duplicates to keep only unique notes
unique_notes = df[['note_text', 'trial_outcome']]

# Create the list of dictionaries
notes = []
for _, row in unique_notes.iterrows():
    notes.append({
        "note_text": row['note_text'],
        "trial_outcome": row['trial_outcome']
    })

# Now notes is a list of dictionaries with unique note_text and trial_outcome



# Find duplicate note_texts and replace them
seen_notes = {}
new_notes_list = []
replaced_count = 0

for note in notes:
    note_text = note["note_text"]
    outcome = note["trial_outcome"]
    if note_text not in seen_notes:
        seen_notes[note_text] = 1
        new_notes_list.append(note)
    else:
        seen_notes[note_text] += 1

        # Try to find a replacement note from the same outcome category
        possible_replacements = []
        for scenario in categories[outcome]:
            replacement_text = (
                f"{scenario['text']} "
                f"Labs: {', '.join([f'{k}={v}' for k, v in scenario['labs'].items()])}. "
            )
            if replacement_text not in seen_notes:
                possible_replacements.append({
                    "note_text": replacement_text,
                    "trial_outcome": outcome
                })

        if possible_replacements:
            replacement_note = random.choice(possible_replacements)
            new_notes_list.append(replacement_note)
            seen_notes[replacement_note["note_text"]] = 1
            replaced_count += 1
        else:
            # If no replacement found, keep the original duplicate
            new_notes_list.append(note)

print(f"Number of duplicate note_texts found and attempted to replace: {sum(count - 1 for count in seen_notes.values() if count > 1)}")
print(f"Number of duplicate notes successfully replaced: {replaced_count}")

# Write the new list of notes to a new CSV file
with open("clinical_notes_replaced.csv", "w", newline="", encoding="utf-8-sig") as csvfile:
    fieldnames = ["note_text", "trial_outcome"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(new_notes_list)

print("New CSV file 'clinical_notes_replaced.csv' created with potential duplicate replacements.")