from datetime import datetime
import io
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import cv2
import numpy as _np
import pandas as pd
from PIL import Image, ImageTk
import speech_recognition as sr
import webbrowser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# ==========================================
# 1. EXPANDED MULTILINGUAL MEDICAL DATASET
# ==========================================
training_data = {
    'symptoms': [
        (
            'fever cough cold sore throat fatigue body ache fiebre tos resfriado'
            ' garganta fatigue douleur fievre toux  बुखार खांसी जुकाम'
            ' كحة سخونة زكام'
        ),
        (
            'high fever chills persistent cough chest congestion fiebre alta'
            ' escalofrios tos congestion pulmonaire तेज बुखार ठंड लगना'
            ' ارتفاع درجة الحرارة كحة حادة'
        ),
        (
            'runny nose sneezing watery eyes mild headache congestion nasal'
            ' estornudos yjos llorosos rhinite سيلان الرأس عطي سيلان الأنف'
        ),
        (
            'shortness of breath wheezing dry cough tightness falta de aire'
            ' sibilancias tos seca শ্বাসকষ্ট ضيق التنفس كحة جافة'
        ),
        (
            'sharp chest pain radiating to left arm dizziness sweating dolor'
            ' de pecho brazo izquierdo mareo sudoración छाתי درد بازو فالس چپ'
            ' ألم حاد في الصدر تعرق ودوخة'
        ),
        (
            'palpitations irregular heartbeat shortness of breath palpitaciones'
            ' arritmia دقات قلب غير منتظمة تسارع القلب خفقان'
        ),
        (
            'high blood pressure severe headache blurred vision presion alta'
            ' dolor de cabeza vision borrosa ضغط دم مرتفع صداع حاد'
        ),
        (
            'throbbing headache sensitivity to light nausea vomiting migraña'
            ' dolor de cabeza nausea vomito صداع نصفي غثيان وقيء'
        ),
        (
            'dizziness spinning sensation loss of balance tinnitus mareo vertigo'
            ' perte d equilibre دوخة فقدان التوازن طنين الأذن'
        ),
        (
            'severe abdominal cramps watery diarrhea nausea dehydration'
            ' dolores abdominales diarrea deshidratacion إسهال شديد مغص بطن'
        ),
        (
            'burning stomach pain acid reflux bloating after eating acidez'
            ' estomacal reflux gastrique حرقان المعدة حموضة واجترار'
        ),
        (
            'sharp pain lower right abdomen fever loss of appetite apendicitis'
            ' douleur abdo appendicite ألم أسفل البطن الأيمن اشتباه الزائدة'
        ),
        (
            'itchy red rash hives swelling after eating peanuts alergia'
            ' ronchas erupcion cutanea طفح جلدي حكة حساسية'
        ),
        (
            'joint pain stiffness swelling morning fatigue dolor articular'
            ' rigidez artrose ألم المفاصل تيبس صباحي'
        ),
        (
            'persistent sadness lack of energy sleep disturbances anxiety'
            ' depresion tristeza insomnio اكتئاب قلق اضطراب النوم'
        ),
        (
            'severe toothache swollen gums bleeding jaw pain hot cold'
            ' sensitivity dolor de muela encías hinchadas sangrado sensibilidad'
            ' al frio calor دنتل ألم الأسنان التهاب اللثة نزيف أسنان'
        ),
        (
            'white patches in mouth painful ulcers bleeding gums difficulty'
            ' chewing llagas en la boca aftas candidiasis بثور الفم تقرحات اللثة'
        ),
    ],
    'disease': [
        'Influenza / Viral Upper Respiratory Infection',
        'Pneumonia or Severe Bronchial Infection',
        'Allergic Rhinitis / Common Cold',
        'Asthma Exacerbation or Bronchitis',
        'Possible Acute Coronary Syndrome (Cardiac Issue)',
        'Arrhythmia or Cardiac Palpitations',
        'Hypertensive Urgency / High Blood Pressure',
        'Migraine Headache',
        'Vertigo or Inner Ear Disturbance',
        'Gastroenteritis (Stomach Bug / Food Poisoning)',
        'Gastritis / Acid Reflux (GERD)',
        'Suspected Appendicitis',
        'Allergic Reaction / Anaphylaxis Risk',
        'Rheumatoid Arthritis / Joint Inflammation',
        'Depressive Disorder / Chronic Fatigue',
        'Acute Pulpitis / Dental Abscess / Gingivitis',
        'Oral Candidiasis (Thrush) or Stomatitis',
    ],
}

localized_outputs = {
    0: {
        'English (Global)': {
            'disease': 'Influenza / Viral Upper Respiratory Infection',
            'specialist': 'General Physician',
            'severity': 'Moderate',
            'advice': (
                'Rest, hydrate, and track temperature. Consult a doctor if'
                ' symptoms persist.'
            ),
        },
        'Español (Spanish)': {
            'disease': (
                'Influenza / Infección Viral de las Vías Respiratorias'
                ' Superiores'
            ),
            'specialist': 'Médico General',
            'severity': 'Moderado',
            'advice': (
                'Descansa, hidrátate y monitorea tu temperatura. Consulta a un'
                ' médico si los síntomas persisten.'
            ),
        },
        'Français (French)': {
            'disease': (
                'Grippe / Infection Virale des Voies Respiratoires'
                ' Supérieures'
            ),
            'specialist': 'Médecin Généraliste',
            'severity': 'Modéré',
            'advice': (
                'Reposez-vous, hydratez-vous et surveillez votre température.'
                ' Consultez un médecin si les symptômes persistent.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': (
                'इन्फ्लूएंजा / वायरल ऊपरी श्वसन पथ का संक्रमण (सर्दी-जुकाम)'
            ),
            'specialist': 'सामान्य चिकित्सक (General Physician)',
            'severity': 'मध्यम (Moderate)',
            'advice': (
                'आराम करें, पानी पिएं और तापमान की निगरानी करें। लक्षण बने'
                ' रहने पर डॉक्टर से मिलें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'أنفلونزا / عدوى الجهاز التنفسي العلوي الفيروسية',
            'specialist': 'طبيب عام',
            'severity': 'متوسط',
            'advice': (
                'استرح، أكثر من السوائل، وراقب درجة حرارتك. استشر طبيباً إذا'
                ' استمرت الأعراض.'
            ),
        },
    },
    1: {
        'English (Global)': {
            'disease': 'Pneumonia or Severe Bronchial Infection',
            'specialist': 'Pulmonologist',
            'severity': 'High',
            'advice': (
                'Urgent medical evaluation needed. Chest X-ray and clinical'
                ' exam recommended.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Neumonía o Infección Bronquial Severa',
            'specialist': 'Neumólogo',
            'severity': 'Alto',
            'advice': (
                'Se necesita evaluación médica urgente. Se recomienda radiografía'
                ' de tórax y examen clínico.'
            ),
        },
        'Français (French)': {
            'disease': 'Pneumonie ou Infection Bronchique Sévère',
            'specialist': 'Pneumologue',
            'severity': 'Élevé',
            'advice': (
                'Évaluation médicale urgente nécessaire. Radiographie pulmonaire'
                ' et examen clinique recommandés.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'निमोनिया या गंभीर ब्रोंकियल संक्रमण',
            'specialist': 'पल्मोनोलॉजिस्ट (Chest Specialist)',
            'severity': 'उच्च (High)',
            'advice': (
                'तत्काल चिकित्सा मूल्यांकन की आवश्यकता है। छाती का एक्स-रे और'
                ' क्लिनिकल परीक्षण की सिफारिश की जाती है।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'التهاب رئوي أو عدوى شعبية حادة',
            'specialist': 'استشاري أمراض الصدر والرئة',
            'severity': 'مرتفع',
            'advice': (
                'مطلوب تقييم طبي عاجل. يوصى بإجراء أشعة على الصدر وفحص سريري.'
            ),
        },
    },
    2: {
        'English (Global)': {
            'disease': 'Allergic Rhinitis / Common Cold',
            'specialist': 'Allergist / General Physician',
            'severity': 'Low',
            'advice': (
                'Avoid triggers, stay hydrated, and use antihistamines if'
                ' necessary.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Rinitis Alérgica / Resfriado Común',
            'specialist': 'Alergólogo / Médico General',
            'severity': 'Bajo',
            'advice': (
                'Evita alérgenos, mantente hidratado y usa antihistamínicos si'
                ' es necesario.'
            ),
        },
        'Français (French)': {
            'disease': 'Rhinite Allergic / Rhume des Foins',
            'specialist': 'Allergologue / Médecin Généraliste',
            'severity': 'Faible',
            'advice': (
                'Évitez les déclencheurs, hydratez-vous et utilisez des'
                ' antihistaminiques si nécessaire.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'एलर्जीक राइनाइटिस / सामान्य सर्दी-जुकाम',
            'specialist': 'एलर्जी विशेषज्ञ / सामान्य चिकित्सक',
            'severity': 'कम (Low)',
            'advice': (
                'एलर्जी पैदा करने वाली चीजों से बचें, हाइड्रेटेड रहें और आवश्यकता'
                ' हो तो एंटीहिस्टामाइन लें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'التهاب الأنف التحسسي / البرد الشائع',
            'specialist': 'طبيب الحساسية والمناعة / طبيب عام',
            'severity': 'منخفض',
            'advice': (
                'تجنب مسببات الحساسية، حافظ على ترطيب جسمك، واستخدم مضادات'
                ' الهيستامين عند الضرورة.'
            ),
        },
    },
    3: {
        'English (Global)': {
            'disease': 'Asthma Exacerbation or Bronchitis',
            'specialist': 'Pulmonologist',
            'severity': 'High',
            'advice': (
                'Use rescue inhaler if prescribed. Seek emergency care if'
                ' breathing worsens.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Exacerbación de Asma o Bronquitis',
            'specialist': 'Neumólogo',
            'severity': 'Alto',
            'advice': (
                'Usa tu inhalador de rescate si está recetado. Busca atención'
                ' de emergencia si empeora la respiración.'
            ),
        },
        'Français (French)': {
            'disease': 'Crise d Asthme ou Bronchite',
            'specialist': 'Pneumologue',
            'severity': 'Élevé',
            'advice': (
                'Utilisez votre inhalateur de secours si prescrit. Consultez'
                ' d urgence si la respiration s aggrave.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'दमा का दौरा (अस्थमा अटैक) या ब्रोंकाइटिस',
            'specialist': 'पल्मोनोलॉजिस्ट (Pulmonologist)',
            'severity': 'उच्च (High)',
            'advice': (
                'निर्धारित होने पर बचाव inhaler का उपयोग करें। सांस लेने में'
                ' कठिनाई बढ़ने पर तुरंत आपातकालीन चिकित्सा लें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'نوبة ربو حادة أو التهاب الشعب الهوائية',
            'specialist': 'استشاري أمراض الصدر',
            'severity': 'مرتفع',
            'advice': (
                'استخدم بخاخ الإنقاذ إذا تم وصفه. اطلب الععاية الطارئة إذا ساءت'
                ' حالة التنفس.'
            ),
        },
    },
    4: {
        'English (Global)': {
            'disease': 'Possible Acute Coronary Syndrome (Cardiac Issue)',
            'specialist': 'Cardiologist',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ EMERGENCY: Call emergency services immediately. Do not wait.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Posible Síndrome Coronario Agudo (Problema Cardíaco)',
            'specialist': 'Cardiólogo',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ EMERGENCIA: Llama a los servicios de emergencia'
                ' inmediatamente. No esperes.'
            ),
        },
        'Français (French)': {
            'disease': 'Syndrome Coronaire Aigu Possible (Problème Cardiaque)',
            'specialist': 'Cardiologue',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ URGENCE : Appelez immédiatement les services d urgence. N'
                ' attendez pas.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'संभावित तीव्र कोरोनरी सिंड्रोम (हार्ट अटैक की आशंका)',
            'specialist': 'हृदय रोग विशेषज्ञ (Cardiologist)',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ आपातकाल: तुरंत एम्बुलेंस या आपातकालीन सेवाओं को कॉल करें।'
                ' प्रतीक्षा न करें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'متالشية الشريان التاجي الحادة المحتملة (مشكلة قلبية)',
            'specialist': 'استشاري أمراض القلب',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ حالة طارئة: اتصل بخدمات الطوارئ فوراً. لا تنتظر أو تتأخر.'
            ),
        },
    },
    5: {
        'English (Global)': {
            'disease': 'Arrhythmia or Cardiac Palpitations',
            'specialist': 'Cardiologist',
            'severity': 'High',
            'advice': (
                'Avoid caffeine, monitor heart rate, and consult a'
                ' cardiologist.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Arritmia o Palpitaciones Cardíacas',
            'specialist': 'Cardiólogo',
            'severity': 'Alto',
            'advice': (
                'Evita la cafeína, monitorea tu frecuencia cardíaca y consulta'
                ' a un cardiólogo.'
            ),
        },
        'Français (French)': {
            'disease': 'Arythmie ou Palpitations Cardiaques',
            'specialist': 'Cardiologue',
            'severity': 'Élevé',
            'advice': (
                'Évitez la caféine, surveillez votre fréquence cardiaque et'
                ' consultez un cardiologue.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'अरिथ्मिया या हृदय की धड़कन में असंतुलन (Palpitations)',
            'specialist': 'हृदय रोग विशेषज्ञ (Cardiologist)',
            'severity': 'उच्च (High)',
            'advice': (
                'कैफीन से बचें, दिल की धड़कन की निगरानी करें और कार्डियोलॉजिस्ट'
                ' से मिलें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'اضطراب نظم القلب أو خفقان القلب',
            'specialist': 'طبيب قلب',
            'severity': 'مرتفع',
            'advice': (
                'تجنب الكافيين، راقب معدل ضربات القلب، واستشر طبيب قلب.'
            ),
        },
    },
    6: {
        'English (Global)': {
            'disease': 'Hypertensive Urgency / High Blood Pressure',
            'specialist': 'Cardiologist',
            'severity': 'High',
            'advice': (
                'Sit down quietly, rest, and check blood pressure immediately.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Urgencia Hipertensiva / Presión arterial alta',
            'specialist': 'Cardiólogo',
            'severity': 'Alto',
            'advice': (
                'Siéntate tranquilamente, descansa y revisa tu presión arterial'
                ' de inmediato.'
            ),
        },
        'Français (French)': {
            'disease': 'Urgence Hypertensive / Pression Artérielle Élevée',
            'specialist': 'Cardiologue',
            'severity': 'Élevé',
            'advice': (
                'Asseyez-vous calmement, reposez-vous et vérifiez votre tension'
                ' artérielle immédiatement.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'हाइपरटेंसिव अर्जेंसी / उच्च रक्तचाप (High BP)',
            'specialist': 'हृदय रोग विशेषज्ञ / जनरल फिजिशियन',
            'severity': 'उच्च (High)',
            'advice': (
                'चुपचाप बैठ जाएं, आराम करें और तुरंत अपना ब्लड प्रेशर चेक करवाएं।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'حالة طوارئ ضغط الدم / ارتفاع ضغط الدم الشديد',
            'specialist': 'استشاري أمراض القلب والأوعية الدموية',
            'severity': 'مرتفع',
            'advice': 'اجلس بهدوء، استرح، وتأكد من قياس ضغط الدم فوراً.',
        },
    },
    7: {
        'English (Global)': {
            'disease': 'Migraine Headache',
            'specialist': 'Neurologist',
            'severity': 'Moderate',
            'advice': (
                'Rest in a dark, quiet room. Take prescribed migraine'
                ' medication.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Migraña / Dolor de Cabeza Severo',
            'specialist': 'Neurólogo',
            'severity': 'Moderado',
            'advice': (
                'Descansa en una habitación oscura y silenciosa. Toma los'
                ' medicamentos recetados para la migraña.'
            ),
        },
        'Français (French)': {
            'disease': 'Migraine / Céphalée Sévère',
            'specialist': 'Neurologue',
            'severity': 'Modéré',
            'advice': (
                'Reposez-vous dans une pièce sombre et calme. Prenez vos'
                ' médicaments prescrits contre la migraine.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'माइग्रेन सिरदर्द (Migraine Headache)',
            'specialist': 'न्यूरोलॉजिस्ट (Neurologist)',
            'severity': 'मध्यम (Moderate)',
            'advice': (
                'अंधेरे और शांत कमरे में आराम करें। डॉक्टर द्वारा दी गई माइग्रेन'
                ' की दवा लें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'صداع نصفي (شقيقة)',
            'specialist': 'طبيب أعصاب',
            'severity': 'متوسط',
            'advice': (
                'استرح في غرفة مظلمة وهادئة. تناول أدوية الصداع النصفي الموصوفة.'
            ),
        },
    },
    8: {
        'English (Global)': {
            'disease': 'Vertigo or Inner Ear Disturbance',
            'specialist': 'ENT Specialist',
            'severity': 'Moderate',
            'advice': (
                'Avoid sudden head movements. Sit down until dizziness subsides.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Vértigo o Trastorno del Oído Interno',
            'specialist': 'Especialista en Otorrinolaringología (ENT)',
            'severity': 'Moderado',
            'advice': (
                'Evita movimientos bruscos de cabeza. Siéntate hasta que pase el'
                ' mareo.'
            ),
        },
        'Français (French)': {
            'disease': 'Vertige ou Troubles de l Oreille Interne',
            'specialist': 'Oto-rhino-laryngologiste (ORL)',
            'severity': 'Modéré',
            'advice': (
                'Évitez les mouvements brusques de la tête. Asseyez-vous'
                ' jusqu à ce que les vertiges s'
                'atténuent.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'चक्कर आना (वर्टिगो) या कान के आंतरिक भाग की समस्या',
            'specialist': 'कान, नाक, गला विशेषज्ञ (ENT Specialist)',
            'severity': 'मध्यम (Moderate)',
            'advice': (
                'अचानक सिर न हिलाएं। चक्कर पूरी तरह ठीक होने तक शांति से बैठ'
                ' जाएं।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'دوار (فيرتيجو) أو اضطراب الأذن الداخلية',
            'specialist': 'طبيب أنف وأذن وحنجرة',
            'severity': 'متوسط',
            'advice': 'تجنب تحريك الرأس فجأة. اجلس حتى يزول الدوار.',
        },
    },
    9: {
        'English (Global)': {
            'disease': 'Gastroenteritis (Stomach Bug / Food Poisoning)',
            'specialist': 'Gastroenterologist',
            'severity': 'Moderate',
            'advice': (
                'Drink oral rehydration solutions (ORS) and stick to a bland'
                ' diet.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Gastroenteritis (Infección Estomacal / Intoxicación)',
            'specialist': 'Gastroenterólogo',
            'severity': 'Moderado',
            'advice': (
                'Bebe sueros de rehidratación oral (SUERO) y mantén una dieta'
                ' blanda.'
            ),
        },
        'Français (French)': {
            'disease': 'Gastro-entérite (Intoxication Alimentaire / Bug)',
            'specialist': 'Gastro-entérologue',
            'severity': 'Modéré',
            'advice': (
                'Buvez des solutions de réhydratation orale (SRO) et suivez un'
                ' régime alimentaire fade.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'गैस्ट्रोएन्टेराइटिस (पेट का संक्रमण / फूड पॉइजनिंग)',
            'specialist': 'गैस्ट्रोएंटेरोलॉजिस्ट (Gastroenterologist)',
            'severity': 'मध्यम (Moderate)',
            'advice': (
                'ओआरएस (ORS) या जीवन रक्षक घोल पिएं और हल्का एवं सादा भोजन लें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'التهاب المعدة والأمعاء (تسمم غذائي / نزلة معوية)',
            'specialist': 'استشاري الجهاز الهضمي',
            'severity': 'متوسط',
            'advice': 'اشرب محاليل معالجة الجفاف والتزم بنظام غذائي خفيف.',
        },
    },
    10: {
        'English (Global)': {
            'disease': 'Gastritis / Acid Reflux (GERD)',
            'specialist': 'Gastroenterologist',
            'severity': 'Low',
            'advice': 'Eat smaller meals and avoid spicy or acidic foods.',
        },
        'Español (Spanish)': {
            'disease': 'Gastritis / Reflujo Ácido (ERGE)',
            'specialist': 'Gastroenterólogo',
            'severity': 'Bajo',
            'advice': (
                'Consume porciones pequeñas y evita alimentos picantes o'
                ' ácidos.'
            ),
        },
        'Français (French)': {
            'disease': 'Gastrite / Reflux Acide (RGO)',
            'specialist': 'Gastro-entérologue',
            'severity': 'Faible',
            'advice': (
                'Faites de petits repas et évitez les aliments épicés ou'
                ' acides.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'गैस्ट्राइटिस / एसिड रिफ्लक्स (GERD / सीने में जलन)',
            'specialist': 'गैस्ट्रोएंटेरोलॉजिस्ट',
            'severity': 'कम (Low)',
            'advice': (
                'थोड़ा-थोड़ा करके भोजन करें और अत्यधिक मसालेदार या खट्टी'
                ' चीजों से बचें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'التهاب المعدة / ارتجاع المريء (GERD)',
            'specialist': 'استشاري الجهاز الهضمي',
            'severity': 'منخفض',
            'advice': (
                'تناول وجبات أصغر حجماً وتجنب الأطعمة الحارة أو الحامضية.'
            ),
        },
    },
    11: {
        'English (Global)': {
            'disease': 'Suspected Appendicitis',
            'specialist': 'General Surgeon',
            'severity': 'CRITICAL EMERGENCY',
            'advice': '⚠️ EMERGENCY: Go to the nearest emergency room immediately.',
        },
        'Español (Spanish)': {
            'disease': 'Sospecha de Apendicitis',
            'specialist': 'Cirujano General',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ EMERGENCIA: Acude a la sala de urgencias más cercana de'
                ' inmediato.'
            ),
        },
        'Français (French)': {
            'disease': 'Suspicion d Appendicite',
            'specialist': 'Chirurgien Généraliste',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ URGENCE : Rendez-vous immédiatement aux urgences les plus'
                ' proches.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'संभावित एपेंडिसाइटिस (Appendicitis)',
            'specialist': 'सामान्य सर्जन (General Surgeon)',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ आपातकाल: तुरंत नजदीकी अस्पताल के इमरजेंसी वार्ड में जाएं।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'اشتباه التهاب الزائدة الدودية',
            'specialist': 'جراح عام',
            'severity': 'CRITICAL EMERGENCY',
            'advice': '⚠️ حالة طارئة: اذهب إلى أقرب غرفة طوارئ فوراً.',
        },
    },
    12: {
        'English (Global)': {
            'disease': 'Allergic Reaction / Anaphylaxis Risk',
            'specialist': 'Emergency Physician',
            'severity': 'CRITICAL EMERGENCY',
            'advice': '⚠️ Seek immediate medical care if breathing is affected.',
        },
        'Español (Spanish)': {
            'disease': 'Reacción Alérgica / Riesgo de Anafilaxia',
            'specialist': 'Médico de Urgencias',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ Busca atención médica inmediata si la respiración se ve'
                ' afectada.'
            ),
        },
        'Français (French)': {
            'disease': 'Réaction Allergique / Risque d Anaphylaxie',
            'specialist': 'Médecin Urgentiste',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ Consultez d urgence si la respiration est affectée.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'गंभीर एलर्जी प्रतिक्रिया / एनाफिलेक्सिस का खतरा',
            'specialist': 'आपातकालीन चिकित्सक (Emergency Physician)',
            'severity': 'CRITICAL EMERGENCY',
            'advice': (
                '⚠️ सांस लेने में दिक्कत होने पर तुरंत चिकित्सीय सहायता लें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'تفاعل تحسسي خطير / خطر الحساسية المفرطة',
            'specialist': 'طبيب طوارئ',
            'severity': 'CRITICAL EMERGENCY',
            'advice': '⚠️ اطلب الرعاية الطبية الفورية إذا تأثر التنفس.',
        },
    },
    13: {
        'English (Global)': {
            'disease': 'Rheumatoid Arthritis / Joint Inflammation',
            'specialist': 'Rheumatologist',
            'severity': 'Moderate',
            'advice': (
                'Gentle movement and anti-inflammatory medications prescribed'
                ' by a specialist.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Artritis Reumatoide / Inflamación Articular',
            'specialist': 'Reumatólogo',
            'severity': 'Moderado',
            'advice': (
                'Movimiento suave y medicamentos antiinflamatorios recetados'
                ' por un especialista.'
            ),
        },
        'Français (French)': {
            'disease': 'Polyarthrite Rhumatoïde / Inflammation Articulaire',
            'specialist': 'Rhumatologue',
            'severity': 'Modéré',
            'advice': (
                'Mouvements doux et anti-inflammatoires prescrits par un'
                ' spécialiste.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'रुमेटॉइड गठिया / जोड़ों में सूजन',
            'specialist': 'रुमेटोलॉजिस्ट (Rheumatologist)',
            'severity': 'मध्यम (Moderate)',
            'advice': (
                'विशेषज्ञ द्वारा बताए गए हल्के व्यायाम और एंटी-इंफ्लेमेटरी दवाएं'
                ' लें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'التهاب المفاصل الروماتويدي / التهاب المفاصل',
            'specialist': 'استشاري روماتيزم ومفاصل',
            'severity': 'متوسط',
            'advice': (
                'حركة خفيفة وأدوية مضادة للالتهابات يصفها الطبيب المختص.'
            ),
        },
    },
    14: {
        'English (Global)': {
            'disease': 'Depressive Disorder / Chronic Fatigue',
            'specialist': 'Psychiatrist',
            'severity': 'Moderate',
            'advice': (
                'Prioritize sleep hygiene and consult a licensed mental health'
                ' professional.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Trastorno Depresivo / Fatiga Crónica',
            'specialist': 'Psiquiatra / Psicólogo',
            'severity': 'Moderado',
            'advice': (
                'Prioriza la higiene del sueño y consulta a un profesional de'
                ' salud mental.'
            ),
        },
        'Français (French)': {
            'disease': 'Trouble Dépressif / Fatigue Chronique',
            'specialist': 'Psychiatre',
            'severity': 'Modéré',
            'advice': (
                'Privilégiez l hygiène du sommeil et consultez un professionnel'
                ' de la santé mentale.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'अवसाद विकार (डिप्रेसन) / पुरानी थकान',
            'specialist': 'मनोचिकित्सक (Psychiatrist)',
            'severity': 'मध्यम (Moderate)',
            'advice': (
                'अपनी नींद की गुणवत्ता का ध्यान रखें और किसी मनोचिकित्सक से'
                ' परामर्श करें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'اضطراب الاكتئاب / الإرهاق المزمن',
            'specialist': 'طبيب نفسي',
            'severity': 'متوسط',
            'advice': (
                'أعطِ الأولوية لجودة النوم واستشر أخصائي صحة نفسية معتمد.'
            ),
        },
    },
    15: {
        'English (Global)': {
            'disease': 'Acute Pulpitis / Dental Abscess / Gingivitis',
            'specialist': 'Dentist / Oral Surgeon',
            'severity': 'High',
            'advice': (
                'Rinse with warm salt water. Avoid extreme temperatures. Visit'
                ' a dentist urgently.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Pulpitis Aguda / Absceso Dental / Gingivitis',
            'specialist': 'Dentista / Cirujano Maxilofacial',
            'severity': 'Alto',
            'advice': (
                'Enjuaga con agua tibia con sal. Evita temperaturas extremas.'
                ' Visita al dentista urgentemente.'
            ),
        },
        'Français (French)': {
            'disease': 'Pulpite Aiguë / Abcès Dentaire / Gingivite',
            'specialist': 'Dentiste / Chirurgien Dentiste',
            'severity': 'Élevé',
            'advice': (
                'Rincez à l eau tiède salée. Évitez les températures extrêmes.'
                ' Consultez un dentiste d urgence.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'तीव्र पल्पिटिस / डेंटलabscess / मसूड़े की सूजन (Gingivitis)',
            'specialist': 'दंत चिकित्सक (Dentist / Oral Surgeon)',
            'severity': 'उच्च (High)',
            'advice': (
                'गुनगुने नमक के पानी से कुल्ला करें। बहुत ठंडी या गर्म चीजें'
                ' खाने से बचें। तुरंत दंत चिकित्सक से मिलें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'التهاب العصب الحاد / خراج الأسنان / التهاب اللثة',
            'specialist': 'طبيب أسنان / جراح فم وأسنان',
            'severity': 'مرتفع',
            'advice': (
                'تمضمض بماء دافئ وملح. تجنب الأطعمة شديدة البرودة أو السخونة.'
                ' قم بزيارة طبيب الأسنان فوراً.'
            ),
        },
    },
    16: {
        'English (Global)': {
            'disease': 'Oral Candidiasis (Thrush) or Stomatitis',
            'specialist': 'Dentist / Periodontist',
            'severity': 'Moderate',
            'advice': (
                'Maintain oral hygiene, use antifungal rinses if prescribed,'
                ' and consult a dentist.'
            ),
        },
        'Español (Spanish)': {
            'disease': 'Candidiasis Bucal (Muguet) o Estomatitis',
            'specialist': 'Dentist / Periodoncista',
            'severity': 'Moderado',
            'advice': (
                'Mantén la higiene bucal, usa enjuagues antifúngicos si te'
                ' fueron recetados y consulta a un dentista.'
            ),
        },
        'Français (French)': {
            'disease': 'Candidose Buccale (Muguet) ou Stomatite',
            'specialist': 'Dentiste / Parodontologue',
            'severity': 'Modéré',
            'advice': (
                'Maintenez une bonne hygiène bucco-dentaire, utilisez des bains'
                ' de bouche antifongiques si prescrits.'
            ),
        },
        'हिन्दी (Hindi)': {
            'disease': 'ओरल कैंडिडासिस (मुंह के छाले/थ्रश) या स्टोमैटाइटिस',
            'specialist': 'दंत चिकित्सक / पेरियोडोंटिस्ट',
            'severity': 'मध्यम (Moderate)',
            'advice': (
                'मुंह की स्वच्छता बनाए रखें, डॉक्टर के कहे अनुसार एंटीफंगल'
                ' माउथवॉश का उपयोग करें।'
            ),
        },
        'العربية (Arabic)': {
            'disease': 'التهاب الفم الفطري (قلاع الفم) أو التهاب الفم',
            'specialist': 'طبيب أسنان / أخصائي لثة',
            'severity': 'متوسط',
            'advice': (
                'حافظ على نظافة الفم، استخدم غسول مضاد للفطريات إذا وصفه الطبيب،'
                ' واستشر طبيب أسنان.'
            ),
        },
    },
}

# UI Localization Dictionaries for Dynamic Translation
ui_texts = {
    'English (Global)': {
        'title': (
            '🌐 AuraHealth: Global Multimodal Triage, Live Camera & Speech'
            ' (Any Language)'
        ),
        'select_lang': 'Select Report Output & Analysis Language:',
        'step1': (
            '1. Describe Symptoms (Type in any language or Speak via'
            ' Microphone):'
        ),
        'mic_btn': '🎤 Speak Symptoms',
        'step2': (
            '2. Computer Vision (Optional: Open Live Camera for Oral Scan):'
        ),
        'cam_btn': '📷 Open Live Camera',
        'cam_status_default': 'No camera snapshot captured',
        'cam_status_captured': 'Captured via Live Webcam',
        'step3': '3. Enter Location Details (for Live Google Maps Search):',
        'city': 'City:',
        'district': 'District:',
        'state': 'State/Province:',
        'country': 'Country:',
        'analyze_btn': '⚡ Run Multilingual Neural Analysis',
        'map_btn': '🗺️ Open Google Maps',
        'export_btn': '📄 Export Report',
        'telemetry': 'Neural Diagnostic Telemetry & Computer Vision Log:',
        'ready_status': (
            '👉 STATUS: Ready. Use the buttons above to locate real'
            ' specialists on Google Maps or export this record.'
        ),
    },
    'Español (Spanish)': {
        'title': (
            '🌐 AuraHealth: Triaje Multilingüe, Cámara en Vivo y Voz (Cualquier'
            ' Idioma)'
        ),
        'select_lang': (
            'Selecciona el idioma del informe y de la interfaz:'
        ),
        'step1': (
            '1. Describe tus síntomas (Escribe o habla por el micrófono):'
        ),
        'mic_btn': '🎤 Decir Síntomas',
        'step2': (
            '2. Visión por Computadora (Opcional: Abrir cámara en vivo):'
        ),
        'cam_btn': '📷 Abrir Cámara en Vivo',
        'cam_status_default': 'Ninguna foto de cámara capturada',
        'cam_status_captured': 'Capturado mediante cámara web',
        'step3': '3. Ingresa detalles de ubicación (para Google Maps):',
        'city': 'Ciudad:',
        'district': 'Distrito / Barrio:',
        'state': 'Estado / Provincia:',
        'country': 'País:',
        'analyze_btn': '⚡ Ejecutar Análisis Neural Multilingüe',
        'map_btn': '🗺️ Abrir Google Maps',
        'export_btn': '📄 Exportar Informe',
        'telemetry': (
            'Telemetría de Diagnóstico Neural y Registro de Visión por'
            ' Computadora:'
        ),
        'ready_status': (
            '👉 ESTADO: Listo. Usa los botones de arriba para buscar'
            ' especialistas reales en Google Maps.'
        ),
    },
    'Français (French)': {
        'title': (
            '🌐 AuraHealth: Triage Multilingue, Caméra Directe & Vocal'
            ' (Toutes Langues)'
        ),
        'select_lang': 'Sélectionnez la langue du rapport et de l interface :',
        'step1': (
            '1. Décrivez vos symptômes (Tapez ou parlez via le micro) :'
        ),
        'mic_btn': '🎤 Dicter les Symptômes',
        'step2': (
            '2. Vision par Ordinateur (Optionnel : Ouvrir la caméra en direct) :'
        ),
        'cam_btn': '📷 Ouvrir Caméra en Direct',
        'cam_status_default': 'Aucune capture de caméra',
        'cam_status_captured': 'Capturé via webcam en direct',
        'step3': '3. Entrez les détails du lieu (pour Google Maps) :',
        'city': 'Ville :',
        'district': 'Quartier / District :',
        'state': 'État / Province :',
        'country': 'Pays :',
        'analyze_btn': '⚡ Lancer l Analyse Neuronale Multilingue',
        'map_btn': '🗺️ Ouvrir Google Maps',
        'export_btn': '📄 Exporter le Rapport',
        'telemetry': 'Journal de Télémétrie et Vision par Ordinateur :',
        'ready_status': (
            '👉 ÉTAT : Prêt. Utilisez les boutons ci-dessus pour localiser des'
            ' spécialistes.'
        ),
    },
    'हिन्दी (Hindi)': {
        'title': (
            '🌐 ऑराहेल्थ: वैश्विक बहु-भाषी त्रियाग, लाइव कैमरा और स्पीच (कोई'
            ' भी भाषा)'
        ),
        'select_lang': 'रिपोर्ट आउटपुट और इंटरफ़ेस की भाषा चुनें:',
        'step1': (
            '1. अपने लक्षण बताएं (किसी भी भाषा में टाइप करें या माइक से बोलें):'
        ),
        'mic_btn': '🎤 लक्षण बोलकर दर्ज करें',
        'step2': (
            '2. कंप्यूटर विज़न (वैकल्पिक: मौखिक जांच के लिए लाइव कैमरा खोलें):'
        ),
        'cam_btn': '📷 लाइव कैमरा खोलें',
        'cam_status_default': 'कोई कैमरा स्नैपशॉट नहीं लिया गया',
        'cam_status_captured': 'लाइव वेबकैम से कैप्चर किया गया',
        'step3': '3. स्थान का विवरण दर्ज करें (गूगल मैप्स खोज के लिए):',
        'city': 'शहर (City):',
        'district': 'जिला (District):',
        'state': 'राज्य (State):',
        'country': 'देश (Country):',
        'analyze_btn': '⚡ बहु-भाषी न्यूरल विश्लेषण चलाएं',
        'map_btn': '🗺️ गूगल मैप्स खोलें',
        'export_btn': '📄 रिपोर्ट एक्सपोर्ट करें',
        'telemetry': 'न्यूरल डायग्नोस्टिक टेलीमेट्री और कंप्यूटर विज़न लॉग:',
        'ready_status': (
            '👉 स्थिति: तैयार। गूगल मैप्स पर असली विशेषज्ञों को खोजने के लिए'
            ' ऊपर दिए गए बटनों का उपयोग करें।'
        ),
    },
    'العربية (Arabic)': {
        'title': (
            '🌐 أورا هيلث: الفرز الطبي متعدد اللغات، الكاميرا الحية والصوت'
            ' (أي لغة)'
        ),
        'select_lang': 'اختر لغة التقرير وواجهة المستخدم:',
        'step1': (
            '1. صف الأعراض (اكتب بأي لغة أو استخدم الميكروفون للتحدث):'
        ),
        'mic_btn': '🎤 انطق الأعراض',
        'step2': (
            '2. الرؤية الحاسوبية (اختياري: فتح الكاميرا الحية لفحص الفم):'
        ),
        'cam_btn': '📷 فتح الكاميرا الحية',
        'cam_status_default': 'لم يتم التقاط صورة بالكاميرا',
        'cam_status_captured': 'تم التقاط الصورة عبر الكاميرا الحية',
        'step3': '3. أدخل تفاصيل الموقع (للبحث في خرائط جوجل):',
        'city': 'المدينة:',
        'district': 'المنطقة / الحي:',
        'state': 'الولاية / المقاطعة:',
        'country': 'الدولة:',
        'analyze_btn': '⚡ تشغيل التحليل العصبي متعدد اللغات',
        'map_btn': '🗺️ فتح خرائط جوجل',
        'export_btn': '📄 تصدير التقرير',
        'telemetry': 'سجل التشخيص العصبي وسجل الرؤية الحاسوبية:',
        'ready_status': (
            '👉 الحالة: جاهز. استخدم الأزرار أعلاه للعثور على أطباء مختصين على'
            ' خرائط جوجل.'
        ),
    },
}

# Train the ML model
df = pd.DataFrame(training_data)
ml_model = make_pipeline(TfidfVectorizer(), MultinomialNB())
ml_model.fit(df['symptoms'], df.index)


# ==========================================
# 2. AURAHEALTH ULTIMATE APP GUI
# ==========================================
class AuraHealthUltimateApp:

  def __init__(self, root):
    self.root = root
    self.root.title(
        'AuraHealth: Multilingual Neural Triage, Camera & Speech AI Pro'
    )
    self.root.geometry('940x880')
    self.root.config(bg='#0f172a')

    # Header Frame
    header_frame = tk.Frame(root, bg='#1e293b', height=70)
    header_frame.pack(fill=tk.X)

    self.title_label = tk.Label(
        header_frame,
        text='',
        font=('Segoe UI', 13, 'bold'),
        bg='#1e293b',
        fg='#38bdf8',
    )
    self.title_label.pack(pady=15)

    # Main Frame Container
    main_frame = tk.Frame(root, bg='#0f172a')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Language Selection Row
    lang_frame = tk.Frame(main_frame, bg='#0f172a')
    lang_frame.grid(row=0, column=0, columnspan=4, sticky='w', pady=(0, 8))

    self.lang_label_widget = tk.Label(
        lang_frame,
        text='',
        font=('Segoe UI', 10, 'bold'),
        bg='#0f172a',
        fg='#f8fafc',
    )
    self.lang_label_widget.pack(side=tk.LEFT)

    self.lang_var = tk.StringVar(value='English (Global)')
    self.lang_dropdown = ttk.Combobox(
        lang_frame,
        textvariable=self.lang_var,
        values=[
            'English (Global)',
            'Español (Spanish)',
            'Français (French)',
            'हिन्दी (Hindi)',
            'العربية (Arabic)',
        ],
        state='readonly',
        width=22,
    )
    self.lang_dropdown.pack(side=tk.LEFT, padx=10)
    # Bind language change event to instantly update all UI labels
    self.lang_dropdown.bind('<<ComboboxSelected>>', self.update_ui_language)

    # Symptoms Input & Speech Recognition Section
    input_header = tk.Frame(main_frame, bg='#0f172a')
    input_header.grid(row=1, column=0, columnspan=4, sticky='w', pady=(5, 5))

    self.step1_label = tk.Label(
        input_header,
        text='',
        font=('Segoe UI', 10, 'bold'),
        bg='#0f172a',
        fg='#f8fafc',
    )
    self.step1_label.pack(side=tk.LEFT)

    self.mic_btn = tk.Button(
        input_header,
        text='',
        font=('Segoe UI', 9, 'bold'),
        bg='#ef4444',
        fg='white',
        padx=8,
        pady=2,
        relief=tk.FLAT,
        command=self.listen_to_speech,
    )
    self.mic_btn.pack(side=tk.LEFT, padx=15)

    self.symptom_input = tk.Text(
        main_frame,
        font=('Segoe UI', 10),
        width=100,
        height=3,
        bg='#1e293b',
        fg='#f8fafc',
        insertbackground='white',
        relief=tk.FLAT,
    )
    self.symptom_input.grid(row=2, column=0, columnspan=4, pady=(0, 10))

    # Computer Vision (Live Camera Feed) Section
    vision_header = tk.Frame(main_frame, bg='#0f172a')
    vision_header.grid(row=3, column=0, columnspan=4, sticky='w', pady=(5, 5))

    self.step2_label = tk.Label(
        vision_header,
        text='',
        font=('Segoe UI', 10, 'bold'),
        bg='#0f172a',
        fg='#f8fafc',
    )
    self.step2_label.pack(side=tk.LEFT)

    self.camera_btn = tk.Button(
        vision_header,
        text='',
        font=('Segoe UI', 9, 'bold'),
        bg='#d97706',
        fg='white',
        padx=8,
        pady=2,
        relief=tk.FLAT,
        command=self.open_live_camera,
    )
    self.camera_btn.pack(side=tk.LEFT, padx=15)

    self.img_status_label = tk.Label(
        vision_header,
        text='',
        font=('Segoe UI', 9, 'italic'),
        bg='#0f172a',
        fg='#94a3b8',
    )
    self.img_status_label.pack(side=tk.LEFT)

    # Location Inputs Section
    self.step3_label = tk.Label(
        main_frame,
        text='',
        font=('Segoe UI', 10, 'bold'),
        bg='#0f172a',
        fg='#f8fafc',
    )
    self.step3_label.grid(row=4, column=0, sticky='w', pady=(5, 5))

    self.city_lbl = tk.Label(
        main_frame, text='', font=('Segoe UI', 9), bg='#0f172a', fg='#94a3b8'
    )
    self.city_lbl.grid(row=5, column=0, sticky='w')
    self.city_entry = tk.Entry(
        main_frame,
        font=('Segoe UI', 9),
        width=18,
        bg='#1e293b',
        fg='#f8fafc',
        insertbackground='white',
    )
    self.city_entry.grid(row=5, column=1, sticky='w', padx=5, pady=3)

    self.district_lbl = tk.Label(
        main_frame, text='', font=('Segoe UI', 9), bg='#0f172a', fg='#94a3b8'
    )
    self.district_lbl.grid(row=5, column=2, sticky='w')
    self.district_entry = tk.Entry(
        main_frame,
        font=('Segoe UI', 9),
        width=18,
        bg='#1e293b',
        fg='#f8fafc',
        insertbackground='white',
    )
    self.district_entry.grid(row=5, column=3, sticky='w', padx=5, pady=3)

    self.state_lbl = tk.Label(
        main_frame, text='', font=('Segoe UI', 9), bg='#0f172a', fg='#94a3b8'
    )
    self.state_lbl.grid(row=6, column=0, sticky='w')
    self.state_entry = tk.Entry(
        main_frame,
        font=('Segoe UI', 9),
        width=18,
        bg='#1e293b',
        fg='#f8fafc',
        insertbackground='white',
    )
    self.state_entry.grid(row=6, column=1, sticky='w', padx=5, pady=3)

    self.country_lbl = tk.Label(
        main_frame, text='', font=('Segoe UI', 9), bg='#0f172a', fg='#94a3b8'
    )
    self.country_lbl.grid(row=6, column=2, sticky='w')
    self.country_entry = tk.Entry(
        main_frame,
        font=('Segoe UI', 9),
        width=18,
        bg='#1e293b',
        fg='#f8fafc',
        insertbackground='white',
    )
    self.country_entry.grid(row=6, column=3, sticky='w', padx=5, pady=3)

    # Action Buttons Frame
    btn_frame = tk.Frame(main_frame, bg='#0f172a')
    btn_frame.grid(row=7, column=0, columnspan=4, pady=10)

    self.analyze_btn = tk.Button(
        btn_frame,
        text='',
        font=('Segoe UI', 10, 'bold'),
        bg='#0ea5e9',
        fg='white',
        padx=10,
        pady=6,
        relief=tk.FLAT,
        command=self.process_medical_request,
    )
    self.analyze_btn.pack(side=tk.LEFT, padx=5)

    self.map_btn = tk.Button(
        btn_frame,
        text='',
        font=('Segoe UI', 10, 'bold'),
        bg='#10b981',
        fg='white',
        padx=10,
        pady=6,
        relief=tk.FLAT,
        command=self.launch_google_maps,
        state=tk.DISABLED,
    )
    self.map_btn.pack(side=tk.LEFT, padx=5)

    self.export_btn = tk.Button(
        btn_frame,
        text='',
        font=('Segoe UI', 10, 'bold'),
        bg='#8b5cf6',
        fg='white',
        padx=10,
        pady=6,
        relief=tk.FLAT,
        command=self.export_report,
        state=tk.DISABLED,
    )
    self.export_btn.pack(side=tk.LEFT, padx=5)

    # Results Console
    self.telemetry_label = tk.Label(
        main_frame,
        text='',
        font=('Segoe UI', 10, 'bold'),
        bg='#0f172a',
        fg='#f8fafc',
    )
    self.telemetry_label.grid(row=8, column=0, sticky='w', pady=(3, 0))

    self.result_area = scrolledtext.ScrolledText(
        main_frame,
        wrap=tk.WORD,
        font=('Consolas', 10),
        width=100,
        height=11,
        bg='#1e293b',
        fg='#38bdf8',
    )
    self.result_area.grid(row=9, column=0, columnspan=4, pady=(3, 0))

    self.current_specialist = ''
    self.last_report_text = ''
    self.cv_analysis_result = 'No camera image evaluated.'

    # Initialize GUI text according to default language
    self.update_ui_language()

  def update_ui_language(self, event=None):
    lang = self.lang_var.get()
    t = ui_texts.get(lang, ui_texts['English (Global)'])

    self.title_label.config(text=t['title'])
    self.lang_label_widget.config(text=t['select_lang'])
    self.step1_label.config(text=t['step1'])
    self.mic_btn.config(text=t['mic_btn'])
    self.step2_label.config(text=t['step2'])
    self.camera_btn.config(text=t['cam_btn'])

    # Only update default status label if no capture has occurred yet
    if 'No camera' in self.img_status_label.cget(
        'text'
    ) or 'Ninguna foto' in self.img_status_label.cget(
        'text'
    ) or 'Aucune' in self.img_status_label.cget(
        'text'
    ) or 'कोई' in self.img_status_label.cget(
        'text'
    ) or 'لم يتم' in self.img_status_label.cget('text'):
      self.img_status_label.config(text=t['cam_status_default'])

    self.step3_label.config(text=t['step3'])
    self.city_lbl.config(text=t['city'])
    self.district_lbl.config(text=t['district'])
    self.state_lbl.config(text=t['state'])
    self.country_lbl.config(text=t['country'])
    self.analyze_btn.config(text=t['analyze_btn'])
    self.map_btn.config(text=t['map_btn'])
    self.export_btn.config(text=t['export_btn'])
    self.telemetry_label.config(text=t['telemetry'])

  def listen_to_speech(self):
    recognizer = sr.Recognizer()
    try:
      with sr.Microphone() as source:
        messagebox.showinfo(
            'Microphone Active',
            'Listening now... Speak your symptoms clearly into your microphone.',
        )
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

      text = recognizer.recognize_google(audio)
      self.symptom_input.delete('1.0', tk.END)
      self.symptom_input.insert(tk.END, text)
      messagebox.showinfo(
          'Success', f'Speech captured successfully:\n"{text}"'
      )
    except sr.UnknownValueError:
      messagebox.showerror(
          'Error',
          'Could not understand audio. Please speak clearly or type manually.',
      )
    except sr.RequestError:
      messagebox.showerror(
          'Network Error',
          'Speech recognition service unavailable. Check internet connection.',
      )
    except Exception as e:
      messagebox.showerror(
          'Microphone Error',
          f'Could not access microphone: {e}\n(Ensure PyAudio is installed).',
      )

  def open_live_camera(self):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
      messagebox.showerror(
          'Camera Error',
          'Could not access webcam. Ensure your camera is connected and'
          ' available.',
      )
      return

    messagebox.showinfo(
        'Live Camera Feed',
        'Webcam active!\n• Position your mouth/teeth clearly in front of the'
        ' lens.\n• Press [SPACEBAR] to capture snapshot.\n• Press [ESC] to'
        ' cancel.',
    )

    img_captured = None
    while True:
      ret, frame = cap.read()
      if not ret:
        break

      display_frame = frame.copy()
      cv2.putText(
          display_frame,
          'Press SPACE to Capture Snapshot | Press ESC to Exit',
          (20, 40),
          cv2.FONT_HERSHEY_SIMPLEX,
          0.6,
          (0, 255, 0),
          2,
      )

      cv2.imshow(
          'AuraHealth Live Oral Scanner (Press SPACE to Capture)', display_frame
      )

      key = cv2.waitKey(1) & 0xFF
      if key == 27:
        break
      elif key == 32:
        img_captured = frame
        break

    cap.release()
    cv2.destroyAllWindows()

    if img_captured is not None:
      lang = self.lang_var.get()
      t = ui_texts.get(lang, ui_texts['English (Global)'])
      self.img_status_label.config(
          text=t['cam_status_captured'], fg='#34d399'
      )

      try:
        hsv = cv2.cvtColor(img_captured, cv2.COLOR_BGR2HSV)
        red_pixels = cv2.countNonZero(
            cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
        ) + cv2.countNonZero(
            cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
        )
        total_pixels = img_captured.shape[0] * img_captured.shape[1]
        red_ratio = (red_pixels / total_pixels) * 100

        if red_ratio > 12:
          self.cv_analysis_result = (
              f'🔴 CV Alert: High mucosal redness/inflammation detected'
              f' ({red_ratio:.1f}% anomaly density). Possible gingivitis,'
              ' abscess, or oral lesion.'
          )
        else:
          self.cv_analysis_result = (
              f'🟢 CV Scan: Normal tone distribution ({red_ratio:.1f}%'
              ' redness). Standard dental visual profile.'
          )
      except Exception as e:
        self.cv_analysis_result = f'CV Processing Error: {e}'

      messagebox.showinfo(
          'Vision Analysis Complete',
          'Live Camera Oral Inspection complete!\nCheck the telemetry console'
          ' for details.',
      )

  def process_medical_request(self):
    user_text = self.symptom_input.get('1.0', tk.END).strip().lower()
    selected_lang = self.lang_var.get()
    t = ui_texts.get(selected_lang, ui_texts['English (Global)'])
    self.result_area.delete('1.0', tk.END)

    if not user_text and 'No camera' in self.img_status_label.cget(
        'text'
    ) and 'Ninguna' not in self.img_status_label.cget(
        'text'
    ) and 'Aucune' not in self.img_status_label.cget(
        'text'
    ) and 'कोई' not in self.img_status_label.cget(
        'text'
    ) and 'لم يتم' not in self.img_status_label.cget('text'):
      messagebox.showwarning(
          'Input Error',
          'Please describe your symptoms via text/speech or take a live camera'
          ' snapshot.',
      )
      return

    if not user_text and (
        'Captured' in self.img_status_label.cget('text')
        or 'cámara' in self.img_status_label.cget('text')
        or 'webcam' in self.img_status_label.cget('text')
        or 'कैप्चर' in self.img_status_label.cget('text')
        or 'الكاميرا' in self.img_status_label.cget('text')
    ):
      user_text = 'dolor de muela encías hinchadas دنتل ألم الأسنان severe toothache'

    predicted_idx = ml_model.predict([user_text])[0]

    lang_dict = localized_outputs.get(
        predicted_idx, localized_outputs[0]
    ).get(selected_lang, localized_outputs[predicted_idx]['English (Global)'])

    condition = lang_dict['disease']
    self.current_specialist = lang_dict['specialist']
    severity = lang_dict['severity']
    advice = lang_dict['advice']

    if 'CRITICAL' in severity.upper():
      messagebox.showerror(
          '🚨 CRITICAL MEDICAL ALERT',
          'WARNING: The symptom profile matches a CRITICAL EMERGENCY.\nSeek'
          ' immediate medical care or call local emergency services!',
      )

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = '=================================================================\n'
    report += f' ⚡ AURAHEALTH MULTILINGUAL NEURAL TRIAGE REPORT [{selected_lang}]\n'
    report += '=================================================================\n'
    report += f'• Timestamp          : {timestamp}\n'
    report += f'• Language Mode      : {selected_lang}\n'
    report += f'• Input Vectors      : "{user_text}"\n'
    report += f'• Computer Vision    : {self.cv_analysis_result}\n'
    report += f'• Predicted Pathology: {condition}\n'
    report += f'• Triage Severity    : [{severity}]\n'
    report += f'• Recommended Expert : {self.current_specialist}\n'
    report += f'• Clinical Guidance  : {advice}\n\n'
    report += f'{t["ready_status"]}'

    self.last_report_text = report
    self.result_area.insert(tk.END, report)
    self.map_btn.config(state=tk.NORMAL)
    self.export_btn.config(state=tk.NORMAL)

  def launch_google_maps(self):
    if not self.current_specialist:
      messagebox.showwarning('Error', 'Please run neural analysis first.')
      return

    city = self.city_entry.get().strip()
    district = self.district_entry.get().strip()
    state = self.state_entry.get().strip()
    country = self.country_entry.get().strip()

    location_parts = [
        self.current_specialist.split('(')[0].strip(),
        'near',
        district,
        city,
        state,
        country,
    ]
    query_string = '+'.join([p for p in location_parts if p])
    google_maps_url = (
        f'https://www.google.com/maps/search/{query_string.replace(" ", "+")}'
    )
    webbrowser.open(google_maps_url)

  def export_report(self):
    if not self.last_report_text:
      messagebox.showwarning('Error', 'No report available to export.')
      return

    file_path = filedialog.asksaveasfilename(
        defaultextension='.txt',
        filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
        initialfile='AuraHealth_Multilingual_Report.txt',
    )

    if file_path:
      try:
        with open(file_path, 'w', encoding='utf-8') as f:
          f.write(self.last_report_text)
        messagebox.showinfo(
            'Success', f'Report successfully saved to:\n{file_path}'
        )
      except Exception as e:
        messagebox.showerror('Error', f'Could not save file: {e}')


# ==========================================
# 3. EXECUTION LOOP
# ==========================================
if __name__ == '__main__':
  root = tk.Tk()
  app = AuraHealthUltimateApp(root)
  root.mainloop()
