from base_model import BaseAdvertising


class Advertiser(BaseAdvertising):
    __total_clicks: int = 0

    def __init__(self, id: int, name: str, clicks: int = 0, views: int = 0) -> None:
        super().__init__(id, name, clicks, views)

    @staticmethod
    def get_total_clicks() -> int:
        return Advertiser.__total_clicks

    @staticmethod
    def help() -> str:
        field_descriptions = {
            "id": "Advertiser's id",
            "name": "Advertiser's name",
            "clicks": "Number of clicks",
            "views": "Number of views",
            "total_clicks": "Total number of clicks",
        }
        return "\n".join(
            f"{field_name}: {field_desc}"
            for field_name, field_desc in field_descriptions.items()
        )

    def inc_clicks(self) -> None:
        super().inc_clicks()
        Advertiser.__total_clicks += 1

    def describe_me(self) -> str:
        return "This class is responsible for managing Advertisers"
