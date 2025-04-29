from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Простий словник відповідей
knowledge_base = {
    "пів'яблука": "Правильно: пів'яблука — через апостроф, бо наступне слово починається з я, ю, є, ї.",
    "пів яблука": "Правильно: пів'яблука — через апостроф, бо наступне слово починається з я, ю, є, ї.",
    "півострів": "Правильно: півострів — разом, без апострофа, бо після 'пів' стоїть приголосний.",
    "одинадцять": "Правильний наголос: одинадцЯть.",
    "кроїти": "Правильний наголос: кроїтИ.",
    "кома перед що": "Кома перед 'що' ставиться, якщо це підрядне речення.",
    "кома перед бо": "Кома перед 'бо' потрібна, бо це складнопідрядне речення.",
    "дієприслівник": "Дієприслівник — це незмінювана форма дієслова, що означає додаткову дію: працюючи, читаючи."
}

def search_answer(query):
    lower_query = query.lower()
    for key in knowledge_base:
        if key in lower_query:
            return knowledge_base[key]
    return None

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    user_query = req.get('queryResult', {}).get('queryText', '')
    
    response_text = search_answer(user_query)
    if not response_text:
        response_text = "На жаль, я ще не знаю точної відповіді, але вже вчуся!"
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"[{datetime.datetime.now()}] {user_query}\n")
    
    return jsonify({
        "fulfillmentText": response_text
    })

if __name__ == '__main__':
    app.run(debug=True)
