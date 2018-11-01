#coding=utf-8
import sys, getopt
import os
import json
import re
import requests

def crawl_coursera(course_slug, dname, subtitle):
    url = 'https://www.coursera.org/learn/{}'.format(course_slug)
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        while True:
            r = requests.get(url)
            if r.text.find('<title>Page Not Found</title>') != -1:
                print('404: Unable to find course named {}'.format(course_slug))
                return
            data_dict = json.loads(re.findall(re.compile(r'window\.App=(.*?});'), r.text)[0])['context']['dispatcher']['stores']['NaptimeStore']['data']
            if 'onDemandCourseMaterialLessons.v1' in data_dict:
                break
        course = re.findall(re.compile(r'<h1 class="title.*?>(.*?)</h1>'), r.text)[0]
        print('Course {}:'.format(course))
        dname = dname + '\\' + course
        module_num = 1
        lecture_flag = False
        module_dict = data_dict['onDemandCourseMaterialLessons.v1']
        video_dict = data_dict['onDemandCourseMaterialItems.v2']
        for module in module_dict.values():
            print('\tModule: {}'.format(module['name']))
            video_num = 1
            mname = '{}\\{}_{}'.format(dname, module_num, module['name'])
            for item in module['itemIds']:
                video = video_dict[item]
                if video['contentSummary']['typeName'] == 'lecture':
                    lecture_flag = True
                    mname = mname.replace('?', '').replace(':', '').replace('/', '_').strip()
                    if not os.path.exists(mname):
                        os.makedirs(mname)
                    print('\t\t{}.{}'.format(video_num, video['name']))
                    crawl_one_video('{}/{}-{}'.format(course_slug, video['slug'], video['id']), '{}\\{}_{}.mp4'.format(mname, video_num, video['name']), subtitle)
                    video_num += 1
            if lecture_flag:
                module_num += 1
                lecture_flag = False
    else:
        print('{}: Unable to find course named {}'.format(r.status_code, course_slug))

def crawl_one_video(lesson, fname, subtitle):
    url = 'https://www.coursera.org/lecture/{}'.format(lesson)
    r = requests.get(url)
    fname = fname.replace('?', '').replace(':', '').replace('/', '_')
    if subtitle:
        sname = fname.replace('.mp4', '.srt')
        if not (os.path.exists(sname) and os.path.getsize(sname) != 0):
            sub_dict = json.loads(re.findall(re.compile(r'"subtitles":({.*?})'), r.text)[0])
            surl = ''
            if 'zh-CN' in sub_dict:
                surl = sub_dict['zh-CN']
            elif 'zh-TW' in sub_dict:
                surl = sub_dict['zh-TW']
            else:
                surl = sub_dict['en']
            with open(sname, 'wb') as f:
                f.write(requests.get('https://www.coursera.org{}'.format(surl)).content)
    if os.path.exists(fname):
        if os.path.getsize(fname) != 0:
            return
    if r.status_code == requests.codes.ok:
        videoURL = re.findall(re.compile(r'"contentURL":"(.*?)"'), r.text)[0]
        with open(fname, 'wb') as f:
            f.write(requests.get(videoURL).content)
    else:
        print('{}: {}'.format(r.status_code, url))

if __name__ == '__main__':
    cname = ''
    subtitle_flag = False
    opts, args = getopt.getopt(sys.argv[1:], "hsn:")
    for op, value in opts:
        if op == '-h':
            print('Usage: python coursera.py -n [CourseNameInUrl]')
            print('\tUse option -s to get srt subtitles for videos')
            print('\tNote: If you can visit a course index with url like "https://www.coursera.org/learn/xxx", the [CourseNameInUrl] will be xxx.')
            print('\tThe fact that Coursera allows crawlers like this is that you can not crawl those homework.')
            sys.exit()
        elif op == '-s':
            subtitle_flag = True
        elif op == '-n':
            cname = value
    crawl_coursera(cname, '..\\Coursera', subtitle_flag)