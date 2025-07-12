class Response:
    @staticmethod
    def error(message):
        return {"status": "error", "error": message}
    @staticmethod
    def success(data):
        return {"status": "success", "data": data}