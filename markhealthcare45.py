# ============================================================
# AURAHEALTH - STREAMLIT WEB VERSION
# ============================================================

import io
import urllib.parse
from datetime import datetime

import cv2
import numpy as np
import pandas as pd
import streamlit as st
import speech_recognition as sr

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AuraHealth",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #0f172a;
        color: #f8fafc;
    }

    [data-testid="stHeader"] {
        background: #0f172a;
    }

    [data-testid="stSidebar"] {
        background: #111827;
    }

    .aura-header {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
    }

    .aura-header h1 {
        color: #38bdf8;
        font-size: 30px;
        margin: 0;
    }

    .section-title {
        color: #38bdf8;
        font-size: 19px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .result-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
        min-height: 170px;
    }

    .result-card h3 {
        color: #38bdf8;
        margin-bottom: 8px;
    }

    .critical-card {
        background: #450a0a;
        border: 2px solid #ef4444;
        border-radius: 14px;
        padding: 20px;
        margin: 15px 0;
    }

    .critical-card h2 {
        color: #fca5a5;
    }

    .info-card {
        background: #172554;
        border: 1px solid #2563eb;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
    }

    .footer-card {
        background: #1e293b;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 15px;
        margin-top: 30px;
        color: #cbd5e1;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MULTILINGUAL MEDICAL TRAINING DATA
# ============================================================

training_data = {
    "symptoms": [
        (
            "fever cough cold sore throat fatigue body ache fiebre tos "
            "resfriado garganta fatigue douleur fievre toux बुखार खांसी "
            "जुकाम كحة سخونة زكام"
        ),
        (
            "high fever chills persistent cough chest congestion fiebre alta "
            "escalofrios tos congestion pulmonaire तेज बुखार ठंड लगना "
            "ارتفاع درجة الحرارة كحة حادة"
        ),
        (
            "runny nose sneezing watery eyes mild headache congestion nasal "
            "estornudos ojos llorosos rhinite سيلان الأنف عطس"
        ),
        (
            "shortness of breath wheezing dry cough tightness falta de aire "
            "sibilancias tos seca श्वासकष्ट ضيق التنفس كحة جافة"
        ),
        (
            "sharp chest pain radiating to left arm dizziness sweating dolor "
            "de pecho brazo izquierdo mareo sudoración छाती दर्द बाजू दर्द "
            "ألم حاد في الصدر تعرق ودوخة"
        ),
        (
            "palpitations irregular heartbeat shortness of breath "
            "palpitaciones arritmia دقات قلب غير منتظمة تسارع القلب خفقان"
        ),
        (
            "high blood pressure severe headache blurred vision presion alta "
            "dolor de cabeza vision borrosa ضغط دم مرتفع صداع حاد"
        ),
        (
            "throbbing headache sensitivity to light nausea vomiting migraña "
            "dolor de cabeza nausea vomito صداع نصفي غثيان وقيء"
        ),
        (
            "dizziness spinning sensation loss of balance tinnitus mareo "
            "vertigo perte d equilibre دوخة فقدان التوازن طنين الأذن"
        ),
        (
            "severe abdominal cramps watery diarrhea nausea dehydration "
            "dolores abdominales diarrea deshidratacion إسهال شديد مغص بطن"
        ),
        (
            "burning stomach pain acid reflux bloating after eating acidez "
            "estomacal reflux gastrique حرقان المعدة حموضة واجترار"
        ),
        (
            "sharp pain lower right abdomen fever loss of appetite "
            "apendicitis douleur abdo appendicite ألم أسفل البطن الأيمن"
        ),
        (
            "itchy red rash hives swelling after eating peanuts alergia "
            "ronchas erupcion cutanea طفح جلدي حكة حساسية"
        ),
        (
            "joint pain stiffness swelling morning fatigue dolor articular "
            "rigidez artrose ألم المفاصل تيبس صباحي"
        ),
        (
            "persistent sadness lack of energy sleep disturbances anxiety "
            "depresion tristeza insomnio اكتئاب قلق اضطراب النوم"
        ),
        (
            "severe toothache swollen gums bleeding jaw pain hot cold "
            "sensitivity dolor de muela encías hinchadas sangrado sensibilidad "
            "al frio calor ألم الأسنان التهاب اللثة نزيف أسنان"
        ),
        (
            "white patches in mouth painful ulcers bleeding gums difficulty "
            "chewing llagas en la boca aftas candidiasis بثور الفم تقرحات "
            "اللثة"
        ),
    ],

    "disease": [
        "Influenza / Viral Upper Respiratory Infection",
        "Pneumonia or Severe Bronchial Infection",
        "Allergic Rhinitis / Common Cold",
        "Asthma Exacerbation or Bronchitis",
        "Possible Acute Coronary Syndrome (Cardiac Issue)",
        "Arrhythmia or Cardiac Palpitations",
        "Hypertensive Urgency / High Blood Pressure",
        "Migraine Headache",
        "Vertigo or Inner Ear Disturbance",
        "Gastroenteritis (Stomach Bug / Food Poisoning)",
        "Gastritis / Acid Reflux (GERD)",
        "Suspected Appendicitis",
        "Allergic Reaction / Anaphylaxis Risk",
        "Rheumatoid Arthritis / Joint Inflammation",
        "Depressive Disorder / Chronic Fatigue",
        "Acute Pulpitis / Dental Abscess / Gingivitis",
        "Oral Candidiasis (Thrush) or Stomatitis",
    ],
}


# ============================================================
# LOCALIZED OUTPUTS
# ============================================================

localized_outputs = {

    0: {
        "English (Global)": {
            "disease": "Influenza / Viral Upper Respiratory Infection",
            "specialist": "General Physician",
            "severity": "Moderate",
            "advice": "Rest, hydrate, and track temperature. Consult a doctor if symptoms persist.",
        },
        "Español (Spanish)": {
            "disease": "Influenza / Infección Viral de las Vías Respiratorias Superiores",
            "specialist": "Médico General",
            "severity": "Moderado",
            "advice": "Descansa, hidrátate y monitorea tu temperatura. Consulta a un médico si los síntomas persisten.",
        },
        "Français (French)": {
            "disease": "Grippe / Infection Virale des Voies Respiratoires Supérieures",
            "specialist": "Médecin Généraliste",
            "severity": "Modéré",
            "advice": "Reposez-vous, hydratez-vous et surveillez votre température. Consultez un médecin si les symptômes persistent.",
        },
        "हिन्दी (Hindi)": {
            "disease": "इन्फ्लूएंजा / वायरल ऊपरी श्वसन पथ का संक्रमण (सर्दी-जुकाम)",
            "specialist": "सामान्य चिकित्सक (General Physician)",
            "severity": "मध्यम (Moderate)",
            "advice": "आराम करें, पानी पिएं और तापमान की निगरानी करें। लक्षण बने रहने पर डॉक्टर से मिलें।",
        },
        "العربية (Arabic)": {
            "disease": "أنفلونزا / عدوى الجهاز التنفسي العلوي الفيروسية",
            "specialist": "طبيب عام",
            "severity": "متوسط",
            "advice": "استرح، أكثر من السوائل، وراقب درجة حرارتك. استشر طبيباً إذا استمرت الأعراض.",
        },
    },

    1: {
        "English (Global)": {
            "disease": "Pneumonia or Severe Bronchial Infection",
            "specialist": "Pulmonologist",
            "severity": "High",
            "advice": "Urgent medical evaluation needed. Chest X-ray and clinical exam recommended.",
        },
        "Español (Spanish)": {
            "disease": "Neumonía o Infección Bronquial Severa",
            "specialist": "Neumólogo",
            "severity": "Alto",
            "advice": "Se necesita evaluación médica urgente. Se recomienda radiografía de tórax y examen clínico.",
        },
        "Français (French)": {
            "disease": "Pneumonie ou Infection Bronchique Sévère",
            "specialist": "Pneumologue",
            "severity": "Élevé",
            "advice": "Évaluation médicale urgente nécessaire. Radiographie pulmonaire et examen clinique recommandés.",
        },
        "हिन्दी (Hindi)": {
            "disease": "निमोनिया या गंभीर ब्रोंकियल संक्रमण",
            "specialist": "पल्मोनोलॉजिस्ट (Chest Specialist)",
            "severity": "उच्च (High)",
            "advice": "तत्काल चिकित्सा मूल्यांकन की आवश्यकता है। छाती का एक्स-रे और क्लिनिकल परीक्षण आवश्यक हो सकता है।",
        },
        "العربية (Arabic)": {
            "disease": "التهاب رئوي أو عدوى شعبية حادة",
            "specialist": "استشاري أمراض الصدر والرئة",
            "severity": "مرتفع",
            "advice": "مطلوب تقييم طبي عاجل. يوصى بإجراء أشعة على الصدر وفحص سريري.",
        },
    },

    2: {
        "English (Global)": {
            "disease": "Allergic Rhinitis / Common Cold",
            "specialist": "Allergist / General Physician",
            "severity": "Low",
            "advice": "Avoid triggers, stay hydrated, and use antihistamines if necessary.",
        },
        "Español (Spanish)": {
            "disease": "Rinitis Alérgica / Resfriado Común",
            "specialist": "Alergólogo / Médico General",
            "severity": "Bajo",
            "advice": "Evita alérgenos, mantente hidratado y usa antihistamínicos si es necesario.",
        },
        "Français (French)": {
            "disease": "Rhinite Allergique / Rhume des Foins",
            "specialist": "Allergologue / Médecin Généraliste",
            "severity": "Faible",
            "advice": "Évitez les déclencheurs, hydratez-vous et utilisez des antihistaminiques si nécessaire.",
        },
        "हिन्दी (Hindi)": {
            "disease": "एलर्जीक राइनाइटिस / सामान्य सर्दी-जुकाम",
            "specialist": "एलर्जी विशेषज्ञ / सामान्य चिकित्सक",
            "severity": "कम (Low)",
            "advice": "एलर्जी पैदा करने वाली चीजों से बचें, हाइड्रेटेड रहें और आवश्यकता हो तो एंटीहिस्टामाइन लें।",
        },
        "العربية (Arabic)": {
            "disease": "التهاب الأنف التحسسي / البرد الشائع",
            "specialist": "طبيب الحساسية والمناعة / طبيب عام",
            "severity": "منخفض",
            "advice": "تجنب مسببات الحساسية، حافظ على ترطيب جسمك، واستخدم مضادات الهيستامين عند الضرورة.",
        },
    },

    3: {
        "English (Global)": {
            "disease": "Asthma Exacerbation or Bronchitis",
            "specialist": "Pulmonologist",
            "severity": "High",
            "advice": "Use rescue inhaler if prescribed. Seek emergency care if breathing worsens.",
        },
        "Español (Spanish)": {
            "disease": "Exacerbación de Asma o Bronquitis",
            "specialist": "Neumólogo",
            "severity": "Alto",
            "advice": "Usa tu inhalador de rescate si está recetado. Busca atención de emergencia si empeora la respiración.",
        },
        "Français (French)": {
            "disease": "Crise d'Asthme ou Bronchite",
            "specialist": "Pneumologue",
            "severity": "Élevé",
            "advice": "Utilisez votre inhalateur de secours si prescrit. Consultez d'urgence si la respiration s'aggrave.",
        },
        "हिन्दी (Hindi)": {
            "disease": "दमा का दौरा (अस्थमा अटैक) या ब्रोंकाइटिस",
            "specialist": "पल्मोनोलॉजिस्ट (Pulmonologist)",
            "severity": "उच्च (High)",
            "advice": "निर्धारित होने पर बचाव inhaler का उपयोग करें। सांस लेने में कठिनाई बढ़ने पर तुरंत चिकित्सा सहायता लें।",
        },
        "العربية (Arabic)": {
            "disease": "نوبة ربو حادة أو التهاب الشعب الهوائية",
            "specialist": "استشاري أمراض الصدر",
            "severity": "مرتفع",
            "advice": "استخدم بخاخ الإنقاذ إذا تم وصفه. اطلب الرعاية الطارئة إذا ساءت حالة التنفس.",
        },
    },

    4: {
        "English (Global)": {
            "disease": "Possible Acute Coronary Syndrome (Cardiac Issue)",
            "specialist": "Cardiologist",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ EMERGENCY: Call emergency services immediately. Do not wait.",
        },
        "Español (Spanish)": {
            "disease": "Posible Síndrome Coronario Agudo (Problema Cardíaco)",
            "specialist": "Cardiólogo",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ EMERGENCIA: Llama a los servicios de emergencia inmediatamente. No esperes.",
        },
        "Français (French)": {
            "disease": "Syndrome Coronaire Aigu Possible (Problème Cardiaque)",
            "specialist": "Cardiologue",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ URGENCE : Appelez immédiatement les services d'urgence. N'attendez pas.",
        },
        "हिन्दी (Hindi)": {
            "disease": "संभावित तीव्र कोरोनरी सिंड्रोम (हार्ट अटैक की आशंका)",
            "specialist": "हृदय रोग विशेषज्ञ (Cardiologist)",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ आपातकाल: तुरंत एम्बुलेंस या आपातकालीन सेवाओं को कॉल करें। प्रतीक्षा न करें।",
        },
        "العربية (Arabic)": {
            "disease": "متلازمة الشريان التاجي الحادة المحتملة (مشكلة قلبية)",
            "specialist": "استشاري أمراض القلب",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ حالة طارئة: اتصل بخدمات الطوارئ فوراً. لا تنتظر أو تتأخر.",
        },
    },

    5: {
        "English (Global)": {
            "disease": "Arrhythmia or Cardiac Palpitations",
            "specialist": "Cardiologist",
            "severity": "High",
            "advice": "Avoid caffeine, monitor heart rate, and consult a cardiologist.",
        },
        "Español (Spanish)": {
            "disease": "Arritmia o Palpitaciones Cardíacas",
            "specialist": "Cardiólogo",
            "severity": "Alto",
            "advice": "Evita la cafeína, monitorea tu frecuencia cardíaca y consulta a un cardiólogo.",
        },
        "Français (French)": {
            "disease": "Arythmie ou Palpitations Cardiaques",
            "specialist": "Cardiologue",
            "severity": "Élevé",
            "advice": "Évitez la caféine, surveillez votre fréquence cardiaque et consultez un cardiologue.",
        },
        "हिन्दी (Hindi)": {
            "disease": "अरिथ्मिया या हृदय की धड़कन में असंतुलन (Palpitations)",
            "specialist": "हृदय रोग विशेषज्ञ (Cardiologist)",
            "severity": "उच्च (High)",
            "advice": "कैफीन से बचें, दिल की धड़कन की निगरानी करें और कार्डियोलॉजिस्ट से मिलें।",
        },
        "العربية (Arabic)": {
            "disease": "اضطراب نظم القلب أو خفقان القلب",
            "specialist": "طبيب قلب",
            "severity": "مرتفع",
            "advice": "تجنب الكافيين، راقب معدل ضربات القلب، واستشر طبيب قلب.",
        },
    },

    6: {
        "English (Global)": {
            "disease": "Hypertensive Urgency / High Blood Pressure",
            "specialist": "Cardiologist",
            "severity": "High",
            "advice": "Sit down quietly, rest, and check blood pressure immediately.",
        },
        "Español (Spanish)": {
            "disease": "Urgencia Hipertensiva / Presión arterial alta",
            "specialist": "Cardiólogo",
            "severity": "Alto",
            "advice": "Siéntate tranquilamente, descansa y revisa tu presión arterial de inmediato.",
        },
        "Français (French)": {
            "disease": "Urgence Hypertensive / Pression Artérielle Élevée",
            "specialist": "Cardiologue",
            "severity": "Élevé",
            "advice": "Asseyez-vous calmement, reposez-vous et vérifiez votre tension artérielle immédiatement.",
        },
        "हिन्दी (Hindi)": {
            "disease": "हाइपरटेंसिव अर्जेंसी / उच्च रक्तचाप (High BP)",
            "specialist": "हृदय रोग विशेषज्ञ / जनरल फिजिशियन",
            "severity": "उच्च (High)",
            "advice": "चुपचाप बैठ जाएं, आराम करें और तुरंत अपना ब्लड प्रेशर चेक करवाएं।",
        },
        "العربية (Arabic)": {
            "disease": "حالة طوارئ ضغط الدم / ارتفاع ضغط الدم الشديد",
            "specialist": "استشاري أمراض القلب والأوعية الدموية",
            "severity": "مرتفع",
            "advice": "اجلس بهدوء، استرح، وتأكد من قياس ضغط الدم فوراً.",
        },
    },

    7: {
        "English (Global)": {
            "disease": "Migraine Headache",
            "specialist": "Neurologist",
            "severity": "Moderate",
            "advice": "Rest in a dark, quiet room. Take prescribed migraine medication.",
        },
        "Español (Spanish)": {
            "disease": "Migraña / Dolor de Cabeza Severo",
            "specialist": "Neurólogo",
            "severity": "Moderado",
            "advice": "Descansa en una habitación oscura y silenciosa. Toma los medicamentos recetados para la migraña.",
        },
        "Français (French)": {
            "disease": "Migraine / Céphalée Sévère",
            "specialist": "Neurologue",
            "severity": "Modéré",
            "advice": "Reposez-vous dans une pièce sombre et calme. Prenez vos médicaments prescrits contre la migraine.",
        },
        "हिन्दी (Hindi)": {
            "disease": "माइग्रेन सिरदर्द (Migraine Headache)",
            "specialist": "न्यूरोलॉजिस्ट (Neurologist)",
            "severity": "मध्यम (Moderate)",
            "advice": "अंधेरे और शांत कमरे में आराम करें। डॉक्टर द्वारा दी गई माइग्रेन की दवा लें।",
        },
        "العربية (Arabic)": {
            "disease": "صداع نصفي (شقيقة)",
            "specialist": "طبيب أعصاب",
            "severity": "متوسط",
            "advice": "استرح في غرفة مظلمة وهادئة. تناول أدوية الصداع النصفي الموصوفة.",
        },
    },

    8: {
        "English (Global)": {
            "disease": "Vertigo or Inner Ear Disturbance",
            "specialist": "ENT Specialist",
            "severity": "Moderate",
            "advice": "Avoid sudden head movements. Sit down until dizziness subsides.",
        },
        "Español (Spanish)": {
            "disease": "Vértigo o Trastorno del Oído Interno",
            "specialist": "Especialista en Otorrinolaringología (ENT)",
            "severity": "Moderado",
            "advice": "Evita movimientos bruscos de cabeza. Siéntate hasta que pase el mareo.",
        },
        "Français (French)": {
            "disease": "Vertige ou Troubles de l'Oreille Interne",
            "specialist": "Oto-rhino-laryngologiste (ORL)",
            "severity": "Modéré",
            "advice": "Évitez les mouvements brusques de la tête. Asseyez-vous jusqu'à ce que les vertiges s'atténuent.",
        },
        "हिन्दी (Hindi)": {
            "disease": "चक्कर आना (वर्टिगो) या कान के आंतरिक भाग की समस्या",
            "specialist": "कान, नाक, गला विशेषज्ञ (ENT Specialist)",
            "severity": "मध्यम (Moderate)",
            "advice": "अचानक सिर न हिलाएं। चक्कर पूरी तरह ठीक होने तक शांति से बैठ जाएं।",
        },
        "العربية (Arabic)": {
            "disease": "دوار (فيرتيجو) أو اضطراب الأذن الداخلية",
            "specialist": "طبيب أنف وأذن وحنجرة",
            "severity": "متوسط",
            "advice": "تجنب تحريك الرأس فجأة. اجلس حتى يزول الدوار.",
        },
    },

    9: {
        "English (Global)": {
            "disease": "Gastroenteritis (Stomach Bug / Food Poisoning)",
            "specialist": "Gastroenterologist",
            "severity": "Moderate",
            "advice": "Drink oral rehydration solutions (ORS) and stick to a bland diet.",
        },
        "Español (Spanish)": {
            "disease": "Gastroenteritis (Infección Estomacal / Intoxicación)",
            "specialist": "Gastroenterólogo",
            "severity": "Moderado",
            "advice": "Bebe sueros de rehidratación oral y mantén una dieta blanda.",
        },
        "Français (French)": {
            "disease": "Gastro-entérite (Intoxication Alimentaire)",
            "specialist": "Gastro-entérologue",
            "severity": "Modéré",
            "advice": "Buvez des solutions de réhydratation orale et suivez un régime alimentaire léger.",
        },
        "हिन्दी (Hindi)": {
            "disease": "गैस्ट्रोएन्टेराइटिस (पेट का संक्रमण / फूड पॉइजनिंग)",
            "specialist": "गैस्ट्रोएंटेरोलॉजिस्ट (Gastroenterologist)",
            "severity": "मध्यम (Moderate)",
            "advice": "ओआरएस (ORS) या जीवन रक्षक घोल पिएं और हल्का एवं सादा भोजन लें।",
        },
        "العربية (Arabic)": {
            "disease": "التهاب المعدة والأمعاء (تسمم غذائي / نزلة معوية)",
            "specialist": "استشاري الجهاز الهضمي",
            "severity": "متوسط",
            "advice": "اشرب محاليل معالجة الجفاف والتزم بنظام غذائي خفيف.",
        },
    },

    10: {
        "English (Global)": {
            "disease": "Gastritis / Acid Reflux (GERD)",
            "specialist": "Gastroenterologist",
            "severity": "Low",
            "advice": "Eat smaller meals and avoid spicy or acidic foods.",
        },
        "Español (Spanish)": {
            "disease": "Gastritis / Reflujo Ácido (ERGE)",
            "specialist": "Gastroenterólogo",
            "severity": "Bajo",
            "advice": "Consume porciones pequeñas y evita alimentos picantes o ácidos.",
        },
        "Français (French)": {
            "disease": "Gastrite / Reflux Acide (RGO)",
            "specialist": "Gastro-entérologue",
            "severity": "Faible",
            "advice": "Faites de petits repas et évitez les aliments épicés ou acides.",
        },
        "हिन्दी (Hindi)": {
            "disease": "गैस्ट्राइटिस / एसिड रिफ्लक्स (GERD / सीने में जलन)",
            "specialist": "गैस्ट्रोएंटेरोलॉजिस्ट",
            "severity": "कम (Low)",
            "advice": "थोड़ा-थोड़ा करके भोजन करें और अत्यधिक मसालेदार या खट्टी चीजों से बचें।",
        },
        "العربية (Arabic)": {
            "disease": "التهاب المعدة / ارتجاع المريء (GERD)",
            "specialist": "استشاري الجهاز الهضمي",
            "severity": "منخفض",
            "advice": "تناول وجبات أصغر حجماً وتجنب الأطعمة الحارة أو الحامضية.",
        },
    },

    11: {
        "English (Global)": {
            "disease": "Suspected Appendicitis",
            "specialist": "General Surgeon",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ EMERGENCY: Go to the nearest emergency room immediately.",
        },
        "Español (Spanish)": {
            "disease": "Sospecha de Apendicitis",
            "specialist": "Cirujano General",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ EMERGENCIA: Acude a la sala de urgencias más cercana de inmediato.",
        },
        "Français (French)": {
            "disease": "Suspicion d'Appendicite",
            "specialist": "Chirurgien Généraliste",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ URGENCE : Rendez-vous immédiatement aux urgences les plus proches.",
        },
        "हिन्दी (Hindi)": {
            "disease": "संभावित एपेंडिसाइटिस (Appendicitis)",
            "specialist": "सामान्य सर्जन (General Surgeon)",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ आपातकाल: तुरंत नजदीकी अस्पताल के इमरजेंसी वार्ड में जाएं।",
        },
        "العربية (Arabic)": {
            "disease": "اشتباه التهاب الزائدة الدودية",
            "specialist": "جراح عام",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ حالة طارئة: اذهب إلى أقرب غرفة طوارئ فوراً.",
        },
    },

    12: {
        "English (Global)": {
            "disease": "Allergic Reaction / Anaphylaxis Risk",
            "specialist": "Emergency Physician",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ Seek immediate medical care if breathing is affected.",
        },
        "Español (Spanish)": {
            "disease": "Reacción Alérgica / Riesgo de Anafilaxia",
            "specialist": "Médico de Urgencias",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ Busca atención médica inmediata si la respiración se ve afectada.",
        },
        "Français (French)": {
            "disease": "Réaction Allergique / Risque d'Anaphylaxie",
            "specialist": "Médecin Urgentiste",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ Consultez d'urgence si la respiration est affectée.",
        },
        "हिन्दी (Hindi)": {
            "disease": "गंभीर एलर्जी प्रतिक्रिया / एनाफिलेक्सिस का खतरा",
            "specialist": "आपातकालीन चिकित्सक (Emergency Physician)",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ सांस लेने में दिक्कत होने पर तुरंत चिकित्सीय सहायता लें।",
        },
        "العربية (Arabic)": {
            "disease": "تفاعل تحسسي خطير / خطر الحساسية المفرطة",
            "specialist": "طبيب طوارئ",
            "severity": "CRITICAL EMERGENCY",
            "advice": "⚠️ اطلب الرعاية الطبية الفورية إذا تأثر التنفس.",
        },
    },

    13: {
        "English (Global)": {
            "disease": "Rheumatoid Arthritis / Joint Inflammation",
            "specialist": "Rheumatologist",
            "severity": "Moderate",
            "advice": "Gentle movement and anti-inflammatory medications prescribed by a specialist.",
        },
        "Español (Spanish)": {
            "disease": "Artritis Reumatoide / Inflamación Articular",
            "specialist": "Reumatólogo",
            "severity": "Moderado",
            "advice": "Movimiento suave y medicamentos antiinflamatorios recetados por un especialista.",
        },
        "Français (French)": {
            "disease": "Polyarthrite Rhumatoïde / Inflammation Articulaire",
            "specialist": "Rhumatologue",
            "severity": "Modéré",
            "advice": "Mouvements doux et anti-inflammatoires prescrits par un spécialiste.",
        },
        "हिन्दी (Hindi)": {
            "disease": "रुमेटॉइड गठिया / जोड़ों में सूजन",
            "specialist": "रुमेटोलॉजिस्ट (Rheumatologist)",
            "severity": "मध्यम (Moderate)",
            "advice": "विशेषज्ञ द्वारा बताए गए हल्के व्यायाम और एंटी-इंफ्लेमेटरी दवाएं लें।",
        },
        "العربية (Arabic)": {
            "disease": "التهاب المفاصل الروماتويدي / التهاب المفاصل",
            "specialist": "استشاري روماتيزم ومفاصل",
            "severity": "متوسط",
            "advice": "حركة خفيفة وأدوية مضادة للالتهابات يصفها الطبيب المختص.",
        },
    },

    14: {
        "English (Global)": {
            "disease": "Depressive Disorder / Chronic Fatigue",
            "specialist": "Psychiatrist",
            "severity": "Moderate",
            "advice": "Prioritize sleep hygiene and consult a licensed mental health professional.",
        },
        "Español (Spanish)": {
            "disease": "Trastorno Depresivo / Fatiga Crónica",
            "specialist": "Psiquiatra / Psicólogo",
            "severity": "Moderado",
            "advice": "Prioriza la higiene del sueño y consulta a un profesional de salud mental.",
        },
        "Français (French)": {
            "disease": "Trouble Dépressif / Fatigue Chronique",
            "specialist": "Psychiatre",
            "severity": "Modéré",
            "advice": "Privilégiez l'hygiène du sommeil et consultez un professionnel de la santé mentale.",
        },
        "हिन्दी (Hindi)": {
            "disease": "अवसाद विकार (डिप्रेसन) / पुरानी थकान",
            "specialist": "मनोचिकित्सक (Psychiatrist)",
            "severity": "मध्यम (Moderate)",
            "advice": "अपनी नींद की गुणवत्ता का ध्यान रखें और किसी मनोचिकित्सक से परामर्श करें।",
        },
        "العربية (Arabic)": {
            "disease": "اضطراب الاكتئاب / الإرهاق المزمن",
            "specialist": "طبيب نفسي",
            "severity": "متوسط",
            "advice": "أعطِ الأولوية لجودة النوم واستشر أخصائي صحة نفسية معتمد.",
        },
    },

    15: {
        "English (Global)": {
            "disease": "Acute Pulpitis / Dental Abscess / Gingivitis",
            "specialist": "Dentist / Oral Surgeon",
            "severity": "High",
            "advice": "Rinse with warm salt water. Avoid extreme temperatures. Visit a dentist urgently.",
        },
        "Español (Spanish)": {
            "disease": "Pulpitis Aguda / Absceso Dental / Gingivitis",
            "specialist": "Dentista / Cirujano Maxilofacial",
            "severity": "Alto",
            "advice": "Enjuaga con agua tibia con sal. Evita temperaturas extremas. Visita al dentista urgentemente.",
        },
        "Français (French)": {
            "disease": "Pulpite Aiguë / Abcès Dentaire / Gingivite",
            "specialist": "Dentiste / Chirurgien Dentiste",
            "severity": "Élevé",
            "advice": "Rincez à l'eau tiède salée. Évitez les températures extrêmes. Consultez un dentiste d'urgence.",
        },
        "हिन्दी (Hindi)": {
            "disease": "तीव्र पल्पिटिस / डेंटल एब्सेस / मसूड़े की सूजन (Gingivitis)",
            "specialist": "दंत चिकित्सक (Dentist / Oral Surgeon)",
            "severity": "उच्च (High)",
            "advice": "गुनगुने नमक के पानी से कुल्ला करें। बहुत ठंडी या गर्म चीजें खाने से बचें। तुरंत दंत चिकित्सक से मिलें।",
        },
        "العربية (Arabic)": {
            "disease": "التهاب العصب الحاد / خراج الأسنان / التهاب اللثة",
            "specialist": "طبيب أسنان / جراح فم وأسنان",
            "severity": "مرتفع",
            "advice": "تمضمض بماء دافئ وملح. تجنب الأطعمة شديدة البرودة أو السخونة. قم بزيارة طبيب الأسنان فوراً.",
        },
    },

    16: {
        "English (Global)": {
            "disease": "Oral Candidiasis (Thrush) or Stomatitis",
            "specialist": "Dentist / Periodontist",
            "severity": "Moderate",
            "advice": "Maintain oral hygiene, use antifungal rinses if prescribed, and consult a dentist.",
        },
        "Español (Spanish)": {
            "disease": "Candidiasis Bucal (Muguet) o Estomatitis",
            "specialist": "Dentist / Periodoncista",
            "severity": "Moderado",
            "advice": "Mantén la higiene bucal, usa enjuagues antifúngicos si te fueron recetados y consulta a un dentista.",
        },
        "Français (French)": {
            "disease": "Candidose Buccale (Muguet) ou Stomatite",
            "specialist": "Dentiste / Parodontologue",
            "severity": "Modéré",
            "advice": "Maintenez une bonne hygiène bucco-dentaire et consultez un dentiste.",
        },
        "हिन्दी (Hindi)": {
            "disease": "ओरल कैंडिडासिस (मुंह के छाले/थ्रश) या स्टोमैटाइटिस",
            "specialist": "दंत चिकित्सक / पेरियोडोंटिस्ट",
            "severity": "मध्यम (Moderate)",
            "advice": "मुंह की स्वच्छता बनाए रखें, डॉक्टर के कहे अनुसार एंटीफंगल माउथवॉश का उपयोग करें।",
        },
        "العربية (Arabic)": {
            "disease": "التهاب الفم الفطري (قلاع الفم) أو التهاب الفم",
            "specialist": "طبيب أسنان / أخصائي لثة",
            "severity": "متوسط",
            "advice": "حافظ على نظافة الفم، استخدم غسول مضاد للفطريات إذا وصفه الطبيب، واستشر طبيب أسنان.",
        },
    },
}


# ============================================================
# UI TRANSLATIONS
# ============================================================

ui_texts = {

    "English (Global)": {
        "title": "🌐 AuraHealth: Global Multimodal Triage, Live Camera & Speech AI",
        "symptoms": "1. Describe Symptoms",
        "camera": "2. Computer Vision — Optional Oral Scan",
        "location": "3. Enter Location Details",
        "city": "City",
        "district": "District",
        "state": "State / Province",
        "country": "Country",
        "analyze": "⚡ Run Multilingual Neural Analysis",
        "maps": "🗺️ Open Google Maps",
        "export": "📄 Export Report",
    },

    "Español (Spanish)": {
        "title": "🌐 AuraHealth: Triaje Multilingüe, Cámara y Voz",
        "symptoms": "1. Describe tus síntomas",
        "camera": "2. Visión por Computadora — Escaneo Oral",
        "location": "3. Ingresa los detalles de ubicación",
        "city": "Ciudad",
        "district": "Distrito",
        "state": "Estado / Provincia",
        "country": "País",
        "analyze": "⚡ Ejecutar Análisis Neural Multilingüe",
        "maps": "🗺️ Abrir Google Maps",
        "export": "📄 Exportar Informe",
    },

    "Français (French)": {
        "title": "🌐 AuraHealth: Triage Multilingue, Caméra et Voix",
        "symptoms": "1. Décrivez vos symptômes",
        "camera": "2. Vision par Ordinateur — Scan Oral",
        "location": "3. Entrez les détails du lieu",
        "city": "Ville",
        "district": "District",
        "state": "État / Province",
        "country": "Pays",
        "analyze": "⚡ Lancer l'Analyse Neuronale Multilingue",
        "maps": "🗺️ Ouvrir Google Maps",
        "export": "📄 Exporter le Rapport",
    },

    "हिन्दी (Hindi)": {
        "title": "🌐 ऑराहेल्थ: बहुभाषी ट्रायेज, लाइव कैमरा और स्पीच AI",
        "symptoms": "1. अपने लक्षण बताएं",
        "camera": "2. कंप्यूटर विज़न — वैकल्पिक ओरल स्कैन",
        "location": "3. स्थान का विवरण दर्ज करें",
        "city": "शहर",
        "district": "जिला",
        "state": "राज्य",
        "country": "देश",
        "analyze": "⚡ बहु-भाषी न्यूरल विश्लेषण चलाएं",
        "maps": "🗺️ गूगल मैप्स खोलें",
        "export": "📄 रिपोर्ट एक्सपोर्ट करें",
    },

    "العربية (Arabic)": {
        "title": "🌐 أورا هيلث: الفرز الطبي متعدد اللغات والكاميرا والصوت",
        "symptoms": "1. صف الأعراض",
        "camera": "2. الرؤية الحاسوبية — فحص الفم اختياري",
        "location": "3. أدخل تفاصيل الموقع",
        "city": "المدينة",
        "district": "المنطقة",
        "state": "الولاية / المقاطعة",
        "country": "الدولة",
        "analyze": "⚡ تشغيل التحليل العصبي متعدد اللغات",
        "maps": "🗺️ فتح خرائط جوجل",
        "export": "📄 تصدير التقرير",
    },
}


# ============================================================
# TRAIN MODEL
# ============================================================

df = pd.DataFrame(training_data)

ml_model = make_pipeline(
    TfidfVectorizer(),
    MultinomialNB()
)

ml_model.fit(
    df["symptoms"],
    df.index
)


# ============================================================
# SESSION STATE
# ============================================================

if "specialist" not in st.session_state:
    st.session_state.specialist = ""

if "report" not in st.session_state:
    st.session_state.report = ""

if "cv_result" not in st.session_state:
    st.session_state.cv_result = "No camera image evaluated."


# ============================================================
# LANGUAGE SELECTOR
# ============================================================

languages = list(ui_texts.keys())

selected_lang = st.sidebar.selectbox(
    "🌐 Select Report / Interface Language",
    languages,
)

t = ui_texts[selected_lang]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
    <div class="aura-header">
        <h1>{t["title"]}</h1>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DISCLAIMER
# ============================================================

st.warning(
    "⚠️ This is an experimental AI screening/triage demonstration. "
    "It is NOT a medical diagnosis and does not replace a qualified "
    "healthcare professional. For a medical emergency, contact your "
    "local emergency service immediately."
)


# ============================================================
# SYMPTOMS
# ============================================================

st.markdown(
    f'<div class="section-title">{t["symptoms"]}</div>',
    unsafe_allow_html=True,
)

symptom_text = st.text_area(
    "symptoms_input",
    height=150,
    placeholder=(
        "Example: fever, cough, sore throat, fatigue..."
    ),
    label_visibility="collapsed",
)


# ============================================================
# MICROPHONE
# ============================================================

st.markdown("### 🎤 Speech Input")

audio = st.audio_input(
    "🎤 Speak Symptoms"
)

speech_text = ""

if audio is not None:

    try:

        recognizer = sr.Recognizer()

        audio_bytes = audio.getvalue()

        audio_file = io.BytesIO(
            audio_bytes
        )

        with sr.AudioFile(audio_file) as source:

            audio_data = recognizer.record(
                source
            )

        speech_text = recognizer.recognize_google(
            audio_data
        )

        st.success(
            f"Speech captured: {speech_text}"
        )

        if not symptom_text:
            symptom_text = speech_text

    except sr.UnknownValueError:

        st.error(
            "Could not understand the audio. "
            "Please speak clearly or type your symptoms."
        )

    except sr.RequestError:

        st.error(
            "Speech recognition service is unavailable."
        )

    except Exception as e:

        st.error(
            f"Speech processing error: {e}"
        )


# ============================================================
# CAMERA
# ============================================================

st.markdown(
    f'<div class="section-title">{t["camera"]}</div>',
    unsafe_allow_html=True,
)

camera = st.camera_input(
    "📷 Open Camera"
)

camera_available = camera is not None


if camera_available:

    st.image(
        camera,
        caption="Captured Camera Image",
        width=400,
    )

    try:

        image_bytes = camera.getvalue()

        image_array = np.frombuffer(
            image_bytes,
            dtype=np.uint8,
        )

        frame = cv2.imdecode(
            image_array,
            cv2.IMREAD_COLOR,
        )

        if frame is None:

            st.session_state.cv_result = (
                "CV Processing Error: Image could not be decoded."
            )

        else:

            hsv = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2HSV,
            )

            red_mask_1 = cv2.inRange(
                hsv,
                (0, 50, 50),
                (10, 255, 255),
            )

            red_mask_2 = cv2.inRange(
                hsv,
                (170, 50, 50),
                (180, 255, 255),
            )

            red_pixels = (
                cv2.countNonZero(red_mask_1)
                +
                cv2.countNonZero(red_mask_2)
            )

            total_pixels = (
                frame.shape[0] *
                frame.shape[1]
            )

            red_ratio = (
                red_pixels /
                total_pixels
            ) * 100

            if red_ratio > 12:

                st.session_state.cv_result = (
                    "🔴 CV Alert: High mucosal redness/"
                    "inflammation detected "
                    f"({red_ratio:.1f}% anomaly density). "
                    "Possible gingivitis, abscess, or oral lesion."
                )

            else:

                st.session_state.cv_result = (
                    "🟢 CV Scan: Normal tone distribution "
                    f"({red_ratio:.1f}% redness). "
                    "Standard dental visual profile."
                )

    except Exception as e:

        st.session_state.cv_result = (
            f"CV Processing Error: {e}"
        )

    st.info(
        st.session_state.cv_result
    )


else:

    st.caption(
        "No camera snapshot captured."
    )


# ============================================================
# LOCATION
# ============================================================

st.markdown(
    f'<div class="section-title">{t["location"]}</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:

    city = st.text_input(
        t["city"]
    )

    state = st.text_input(
        t["state"]
    )

with col2:

    district = st.text_input(
        t["district"]
    )

    country = st.text_input(
        t["country"]
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("---")

analyze = st.button(
    t["analyze"],
    type="primary",
    use_container_width=True,
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    user_text = (
        symptom_text.strip().lower()
    )

    if not user_text and speech_text:

        user_text = (
            speech_text.strip().lower()
        )

    # Same fallback behavior as your
    # original Tkinter application.
    if not user_text and camera_available:

        user_text = (
            "dolor de muela encías hinchadas "
            "دنتل ألم الأسنان severe toothache"
        )

    if not user_text:

        st.error(
            "Please describe your symptoms using "
            "text or speech, or capture a camera image."
        )

        st.stop()

    # ----------------------------------------
    # PREDICTION
    # ----------------------------------------

    try:

        predicted_idx = ml_model.predict(
            [user_text]
        )[0]

    except Exception as e:

        st.error(
            f"AI prediction error: {e}"
        )

        st.stop()

    # ----------------------------------------
    # LOCALIZED RESULT
    # ----------------------------------------

    result_data = localized_outputs[
        predicted_idx
    ].get(
        selected_lang,
        localized_outputs[
            predicted_idx
        ]["English (Global)"],
    )

    condition = result_data["disease"]

    specialist = result_data["specialist"]

    severity = result_data["severity"]

    advice = result_data["advice"]

    st.session_state.specialist = specialist

    # ----------------------------------------
    # CRITICAL ALERT
    # ----------------------------------------

    if "CRITICAL" in severity.upper():

        st.markdown(
            f"""
            <div class="critical-card">

            <h2>🚨 CRITICAL MEDICAL ALERT</h2>

            <p>
            The symptom profile matches a critical emergency
            category in this demonstration model.
            </p>

            <strong>
            {advice}
            </strong>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # ----------------------------------------
    # TIMESTAMP
    # ----------------------------------------

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # ----------------------------------------
    # REPORT
    # ----------------------------------------

    report = ""

    report += (
        "=================================================================\n"
    )

    report += (
        " ⚡ AURAHEALTH MULTILINGUAL NEURAL "
        f"TRIAGE REPORT [{selected_lang}]\n"
    )

    report += (
        "=================================================================\n"
    )

    report += (
        f"• Timestamp          : {timestamp}\n"
    )

    report += (
        f"• Language Mode      : {selected_lang}\n"
    )

    report += (
        f'• Input Vectors      : "{user_text}"\n'
    )

    report += (
        f"• Computer Vision    : "
        f"{st.session_state.cv_result}\n"
    )

    report += (
        f"• Predicted Pathology: {condition}\n"
    )

    report += (
        f"• Triage Severity    : [{severity}]\n"
    )

    report += (
        f"• Recommended Expert : {specialist}\n"
    )

    report += (
        f"• Clinical Guidance  : {advice}\n"
    )

    report += (
        "\n"
        "IMPORTANT: This is an experimental AI "
        "screening result and not a medical diagnosis.\n"
    )

    st.session_state.report = report

    # ========================================================
    # RESULTS
    # ========================================================

    st.markdown("## 🩺 AuraHealth Analysis Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:

        st.markdown(
            f"""
            <div class="result-card">

            <h3>Predicted Condition</h3>

            <p>{condition}</p>

            <h3>Recommended Specialist</h3>

            <p>{specialist}</p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with result_col2:

        st.markdown(
            f"""
            <div class="result-card">

            <h3>Triage Severity</h3>

            <p><strong>{severity}</strong></p>

            <h3>Clinical Guidance</h3>

            <p>{advice}</p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # ========================================================
    # TELEMETRY
    # ========================================================

    st.markdown(
        "### 🔬 Neural Diagnostic Telemetry & CV Log"
    )

    st.code(
        report,
        language="text",
    )


# ============================================================
# GOOGLE MAPS
# ============================================================

if st.session_state.specialist:

    st.markdown("---")

    st.markdown(
        "### 🗺️ Find Recommended Specialist"
    )

    location_parts = [
        st.session_state.specialist
        .split("(")[0]
        .strip(),
        "near",
        district,
        city,
        state,
        country,
    ]

    location_parts = [
        x for x in location_parts
        if x.strip()
    ]

    query = " ".join(
        location_parts
    )

    maps_url = (
        "https://www.google.com/maps/search/"
        +
        urllib.parse.quote_plus(query)
    )

    st.link_button(
        t["maps"],
        maps_url,
        use_container_width=True,
    )


# ============================================================
# EXPORT REPORT
# ============================================================

if st.session_state.report:

    st.markdown("---")

    st.download_button(
        label=t["export"],
        data=st.session_state.report,
        file_name=(
            "AuraHealth_Multilingual_Report.txt"
        ),
        mime="text/plain",
        use_container_width=True,
    )


# ============================================================
# FOOTER 
# ============================================================

st.markdown(
    """
    <div class="footer-card">

    <strong>AuraHealth — Experimental AI Demonstration</strong>

    <br><br>

    This application uses a limited demonstration dataset and
    simple machine-learning and computer-vision techniques.
    Its output should not be interpreted as a confirmed diagnosis
    or medical advice.

    <br><br>

    Camera analysis is experimental and should not be used to
    determine whether a person has a medical condition.

    </div>
    """,
    unsafe_allow_html=True,
)
