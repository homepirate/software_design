from models import TransportationOrder


class FraudDetectionService:
    suspicious_keywords = ["fraud", "scam", "suspicious"]

    def check_order(self, order: TransportationOrder) -> bool:
        for message in order.messages:
            if any(keyword in message.text.lower() for keyword in self.suspicious_keywords):
                return True
        return False