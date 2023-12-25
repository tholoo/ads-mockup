from advertiser import Advertiser
from base_model import BaseAdvertising


class Ad(BaseAdvertising):
    def __init__(
        self,
        id: int,
        title: str,
        imgUrl: str,
        link: str,
        advertiser: Advertiser,
        clicks: int = 0,
        views: int = 0,
    ) -> None:
        self._imgUrl = imgUrl
        self._link = link
        self._advertiser = advertiser
        super().__init__(id, title, clicks, views)

    def set_title(self, title: str) -> None:
        self._name = title

    def get_img_url(self) -> str:
        return self._imgUrl

    def set_img_url(self, url: str) -> None:
        self._imgUrl = url

    def get_link(self) -> str:
        return self._link

    def set_link(self, link: str) -> None:
        self._link = link

    def set_advertiser(self, advertiser: Advertiser) -> None:
        self._advertiser = advertiser

    def describe_me(self) -> str:
        return "This class is responsible for managing Ads"

    def inc_clicks(self) -> None:
        super().inc_clicks()
        self._advertiser.inc_clicks()

    def inc_views(self) -> None:
        super().inc_views()
        self._advertiser.inc_views()
