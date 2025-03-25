from models import TransportationOrder


class FraudDetectionService:
    def check_order(self, order: TransportationOrder) -> bool:
        """
        Проверяет заявку на наличие подозрительной активности.
        Пример проверки: если в тексте любого сообщения встречаются подозрительные ключевые слова.
        """
        suspicious_keywords = ["fraud", "scam", "suspicious"]
        for message in order.messages:
            if any(keyword in message.text.lower() for keyword in suspicious_keywords):
                return True
        return False