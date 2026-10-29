from typing import Literal, TypedDict

class Video(TypedDict):
    title: str
    views: int
    tags: list[str]

def get_video(id: int) -> Video | None:
    if id == 1:
        return {"title": "Jesus Story", "views": 1000, "tags": ["short", "story"]}
    return None

def set_quality(q: Literal["low", "high"]) -> None:
    print(f"Quality: {q}")

video = get_video(1)
if video is not None:        # None check zaroori hai
    print(video["title"])