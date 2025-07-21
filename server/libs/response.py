class Response:
    @staticmethod
    def error(message):
        return {"status": "error", "error": str(message)}

    @staticmethod
    def success(data):
        if hasattr(data, "to_dict"):
            data = data.to_dict()
        elif isinstance(data, list):
            data = [item.to_dict() if hasattr(item, "to_dict") else item for item in data]
        elif not isinstance(data, dict):
            data = {"value": str(data)}

        return {"status": "success", "data": data}
