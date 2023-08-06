from .process import Process


class Client:

    @staticmethod
    def create_profile(**data):
        data["service"] = "create_profile"
        p = Process()
        result = p.call_zevents(**data)
        return result

    @staticmethod
    def get_profile_cursor(**data):
        data["service"] = "get_profile_cursor"
        p = Process()
        result = p.call_zevents(**data)
        return result

    @staticmethod
    def get_profile(**data):
        data["service"] = "get_profile"
        p = Process()
        result = p.call_zevents(**data)
        return result

    @staticmethod
    def download_profile(**data):
        data["service"] = "download_profile"
        p = Process()
        result = p.call_zevents(**data)
        return result

    @staticmethod
    def delete_profile(**data):
        data["service"] = "delete_profile"
        p = Process()
        result = p.call_zevents(**data)
        return result

    @staticmethod
    def create_event(**data):
        data["service"] = "create_event"
        p = Process()
        result = p.call_zevents(**data)
        return result

    @staticmethod
    def get_event_cursor(**data):
        data["service"] = "get_event_cursor"
        p = Process()
        result = p.call_zevents(**data)
        return result

    @staticmethod
    def get_event(**data):
        data["service"] = "get_event"
        p = Process()
        result = p.call_zevents(**data)
        return result




