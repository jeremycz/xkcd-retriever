import requests
import json
from random import randint
from PIL import Image


class Retriever:
    URL_ROOT = "https://xkcd.com/"
    URL_RESOURCE = "info.0.json"
    IMAGE_CACHE = "temp.png"

    def __init__(self, display_comic: bool = False):
        self._initialised = False
        self._latest_data = None
        self._max_ind = None
        self._min_ind = 1
        self._display_comic = display_comic

    def initialise(self) -> bool:
        """Get latest comic to determine maximum index"""
        req = requests.get(f"{Retriever.URL_ROOT}{Retriever.URL_RESOURCE}")
        if req.status_code != requests.codes.ok:
            print(
                f"Initialisation failed: Unable to access latest comic (status {req.status_code})"
            )
            return False

        # Get number of latest comic
        self._latest_data = req.json()
        if "num" not in self._latest_data:
            print(
                f"Unable to retrieve latest comic index - {json.dumps(self._latest_data)}"
            )
            return False

        self._max_ind = self._latest_data["num"]
        self._initialised = True
        print(f"Successfully initialised. Latest index: {self._max_ind}")
        return True

    def get_latest(self) -> None:
        if not self._initialised:
            print("Please initialise retriever before attempting to retrieve comics")
            return

        if self._display_comic:
            self._display(self._latest_data)

    def get_random(self) -> None:
        if not self._initialised:
            print("Please initialise retriever before attempting to retrieve comics")
            return

        self.get_comic(randint(self._min_ind, self._max_ind))

    def get_comic(self, ind: int) -> dict:
        if not self._initialised:
            print("Please initialise retriever before attempting to retrieve comics")
            return

        if ind > self._max_ind:
            print(f"Max comic index is: {self._max_ind}")
            return
        elif ind < self._min_ind:
            print(f"Min comic index is: {self._min_ind}")
            return

        req = requests.get(f"{Retriever.URL_ROOT}{ind}/{Retriever.URL_RESOURCE}")
        if req.status_code != requests.codes.ok:
            print(f"Unable to access comic {ind} (status {req.status_code})")
            return

        data = req.json()
        if self._display_comic:
            self._display(data)

        return data

    def _get_image(self, url: str) -> bool:
        req = requests.get(url, stream=True)
        if req.status_code != requests.codes.ok:
            print(f"{req.status_code}: Unable to retrieve image from '{url}'")
            return False

        with open(Retriever.IMAGE_CACHE, "wb") as f:
            for chunk in req.iter_content(1024):
                f.write(chunk)

        return True

    def _display(self, data: dict) -> None:
        print(f"{data.get('day', 0)}-{data.get('month', 0)}-{data.get('year', 0)}")
        print(f"Title: {data.get('title', '')}")
        print(f"Alt: {data.get('alt', '')}")

        if "img" in data and self._get_image(data["img"]):
            img = Image.open(Retriever.IMAGE_CACHE)
            img.show(title=data.get("title", ""))
