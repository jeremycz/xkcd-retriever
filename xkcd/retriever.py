from typing import Tuple, Union
import json
from random import randint

import requests
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

    def initialise(self) -> Tuple[bool, Union[int, None]]:
        """Get latest comic to determine maximum index"""
        req = requests.get(f"{Retriever.URL_ROOT}{Retriever.URL_RESOURCE}")
        if req.status_code != requests.codes.ok:
            print(
                f"Initialisation failed: Unable to access latest comic (status {req.status_code})"
            )
            return False, None

        # Get number of latest comic
        self._latest_data = req.json()
        if "num" not in self._latest_data:
            print(
                f"Unable to retrieve latest comic index - {json.dumps(self._latest_data)}"
            )
            return False, None

        self._max_ind = self._latest_data["num"]
        self._initialised = True
        print(f"Successfully initialised. Latest index: {self._max_ind}")
        return True, self._max_ind

    def get_latest(self) -> Union[dict, None]:
        if not self._initialised:
            print("Please initialise retriever before attempting to retrieve comics")
            return None

        if self._display_comic:
            self._display(self._latest_data)

        return self._latest_data

    def get_random(self) -> Union[dict, None]:
        if not self._initialised:
            print("Please initialise retriever before attempting to retrieve comics")
            return None

        return self.get_comic(randint(self._min_ind, self._max_ind))

    def get_comic(self, ind: int) -> Union[dict, None]:
        if not self._initialised:
            print("Please initialise retriever before attempting to retrieve comics")
            return None

        if ind > self._max_ind:
            print(f"Max comic index is: {self._max_ind}")
            return None
        elif ind < self._min_ind:
            print(f"Min comic index is: {self._min_ind}")
            return None

        req = requests.get(f"{Retriever.URL_ROOT}{ind}/{Retriever.URL_RESOURCE}")
        if req.status_code != requests.codes.ok:
            print(f"Unable to access comic {ind} (status {req.status_code})")
            return None

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
