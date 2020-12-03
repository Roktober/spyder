from dataclasses import dataclass


@dataclass
class Data:
    html: str
    uri: str
    title: str
    urls: set
