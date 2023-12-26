from advertiser import Advertiser
from base_model import BaseAdvertising


class Ad(BaseAdvertising):
    def __init__(
        self,
        id: int,
        title: str,
        img_url: str,
        link: str,
        advertiser: Advertiser,
    ) -> None:
        super().__init__(id, title)
        self._img_url = img_url
        self._link = link
        self._advertiser = advertiser

    def set_title(self, title: str) -> None:
        self._name = title

    def get_img_url(self) -> str:
        return self._img_url

    def set_img_url(self, url: str) -> None:
        self._img_url = url

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
