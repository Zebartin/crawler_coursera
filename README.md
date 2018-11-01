# crawler_coursera
Crawler for videos on Cousera.org without registering

### Note
- Type `python crawler_coursera.py -h` to get usage
```
Usage: python coursera.py -n [CourseNameInUrl]
        Use option -s to get srt subtitles for videos
        Note: If you can visit a course index with url like "https://www.coursera.org/learn/xxx", the [CourseNameInUrl] will be xxx.
        The fact that Coursera allows crawlers like this is that you can not crawl those homework.
```
- As is said in the usage, in order to point out which course you are aiming at:
  - Firstly, get into the welcome page of the course from wherever you notice it;
  - Secondly, copy the latter part of the url. For example, the url of [Wonders of Ancient Egypt](https://www.coursera.org/learn/wonders-ancient-egypt) is `https://www.coursera.org/learn/wonders-ancient-egypt`, and all we need is the part after `learn/`, that is, `wonders-ancient-egypt`;
  - Finally, run `crawler_coursera.py` for the course. For example, `python crawler_coursera.py -n wonders-ancient-egypt`.
  - Videos will be stored in directory `..\Coursera\[CourseName]\[ModuleName]`. Videos are divided according to course modules instead of weeks.
- In case you want the subtitles for videos, you can use option `-s`, like `python crawler_coursera.py -n CourseName -s`
  - First choice of language for subtitiles is Chinese;
  - English subtitles will be the next;
  - Of course you are free to modify py and set your favorite language.
- If you are in China or somewhere videos on Coursera are blocked, you'd better turn your VPN on, because no proxy is used here.
  
