from dataclasses import dataclass


@dataclass
class Media:
    media_id: str = None
    title: str = None
    description: str = None

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.media_id}: {self.title}'
