# youtubepy
youtubepy is a package to search for youtube videos through python code.

# Usage
```python
from youtubepy import Video
video = Video("me at the zoo")
result = video.search()
print(result)
> https://www.youtube.com/watch?v=A8AlbaDmaec
```

Attributes available for Video
```
search()
title()
channel_url()
channel_name()
thumbnail()
duration()
view_count()
like_count()
dislike_count()
average_rating()
```

```python
from youtubepy import ExtractInfo
video = ExtractInfo("https://youtu.be/A8AlbaDmaec")
title = video.title()
print(title)
> Me at the zoo - 4k Upscaled, 60 FPS
```

Attributes available for ExtractInfo
```
title()
channel_url()
channel_name()
thumbnail()
duration()
view_count()
like_count()
dislike_count()
average_rating()
```

This version works faster than all other versions!

Note - This package is currently under development