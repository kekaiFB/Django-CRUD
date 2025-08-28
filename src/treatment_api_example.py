"""
Пример простого API сервера для тестирования получения рекомендаций по лечению
Запустите этот файл для тестирования: python treatment_api_example.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/treatment', methods=['POST'])
def get_treatment_recommendations():
    """
    API endpoint для получения рекомендаций по лечению
    Принимает данные диагноза и возвращает рекомендации
    """
    try:
        data = request.get_json()
        
        # Извлекаем данные из запроса
        diagnosis = data.get('diagnosis', 'Неизвестно')
        temperature = data.get('temperature')
        saturation = data.get('saturation')
        heart_rate = data.get('heart_rate')
        leukocytes = data.get('leukocytes')
        crp = data.get('crp')
        esr = data.get('esr')
        age = data.get('age')
        gender = data.get('gender')
        
        # Генерируем рекомендации на основе диагноза и параметров
        recommendations = generate_recommendations(
            diagnosis, temperature, saturation, heart_rate, 
            leukocytes, crp, esr, age, gender
        )
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'received_data': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def generate_recommendations(diagnosis, temperature, saturation, heart_rate, 
                           leukocytes, crp, esr, age, gender):
    """
    Генерирует рекомендации по лечению на основе диагноза и клинических данных
    """
    
    base_recommendations = []
    
    # Базовые рекомендации по диагнозу
    if diagnosis == "Пневмония":
        base_recommendations.extend([
            "Антибактериальная терапия: Амоксициллин-клавуланат 875/125 мг 2 раза в день",
            "При тяжелом течении: Левофлоксацин 500 мг 1 раз в день",
            "Симптоматическая терапия: жаропонижающие, муколитики",
            "Контроль сатурации кислорода",
            "Рентгенологический контроль через 7-10 дней"
        ])
        
    elif diagnosis == "ХОБЛ":
        base_recommendations.extend([
            "Бронхолитики: Сальбутамол по требованию",
            "Ингаляционные глюкокортикостероиды при частых обострениях",
            "Отказ от курения",
            "Легочная реабилитация",
            "Вакцинация против гриппа и пневмококка"
        ])
        
    elif diagnosis == "Бронхит":
        base_recommendations.extend([
            "Симптоматическая терапия: муколитики, отхаркивающие",
            "При бактериальной этиологии: Амоксициллин 500 мг 3 раза в день",
            "Обильное питье",
            "Увлажнение воздуха",
            "Отказ от курения"
        ])
        
    elif diagnosis == "БА":
        base_recommendations.extend([
            "Ингаляционные бета-2-агонисты короткого действия",
            "Ингаляционные глюкокортикостероиды",
            "Контроль пиковой скорости выдоха",
            "Избегание триггеров",
            "План действий при обострении"
        ])
        
    else:
        base_recommendations.append("Консультация специалиста для уточнения тактики лечения")
    
    # Дополнительные рекомендации на основе клинических данных
    additional_recommendations = []
    
    if temperature and temperature > 38.5:
        additional_recommendations.append("Жаропонижающие препараты при температуре выше 38.5°C")
    
    if saturation and saturation < 95:
        additional_recommendations.append("Кислородотерапия при сатурации ниже 95%")
        additional_recommendations.append("Контроль газов крови")
    
    if heart_rate and heart_rate > 100:
        additional_recommendations.append("Контроль сердечного ритма")
        additional_recommendations.append("При необходимости - консультация кардиолога")
    
    if leukocytes and leukocytes > 10:
        additional_recommendations.append("Признаки воспаления - усиление антибактериальной терапии")
    
    if crp and crp > 50:
        additional_recommendations.append("Высокий СРБ - показана госпитализация")
    
    if age and age > 65:
        additional_recommendations.append("Учет возрастных особенностей при назначении терапии")
        additional_recommendations.append("Контроль функции почек и печени")
    
    # Объединяем все рекомендации
    all_recommendations = base_recommendations + additional_recommendations
    
    # Форматируем в читаемый вид
    formatted_recommendations = "\n".join([f"• {rec}" for rec in all_recommendations])
    
    return formatted_recommendations

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности API"""
    return jsonify({
        'status': 'healthy',
        'service': 'Treatment Recommendations API',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("Запуск API сервера для рекомендаций по лечению...")
    print("API будет доступен по адресу: http://localhost:5000")
    print("Endpoint для рекомендаций: POST /treatment")
    print("Проверка здоровья: GET /health")
    print("\nДля тестирования Django приложения измените TREATMENT_API_URL на:")
    print("http://localhost:5000/treatment")
    print("\nНажмите Ctrl+C для остановки сервера")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
