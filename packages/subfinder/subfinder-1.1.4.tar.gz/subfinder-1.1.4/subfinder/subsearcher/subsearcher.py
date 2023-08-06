# -*- coding: utf8 -*-
from __future__ import unicode_literals
from abc import abstractmethod, ABCMeta
import os
import re
import cgi
try:
    import urlparse
except ImportError as e:
    from urllib import parse as urlparse
import requests
from subfinder.tools.compressed_file import CompressedFile
from . import exceptions


registered_subsearchers = {}


def register_subsearcher(name, subsearcher_cls):
    """ register a subsearcher, the `name` is a key used for searching subsearchers.
    if the subsearcher named `name` already exists, then it's will overrite the old subsearcher.
    """
    if not issubclass(subsearcher_cls, BaseSubSearcher):
        raise ValueError(
            '{} is not a subclass of BaseSubSearcher'.format(subsearcher_cls))
    registered_subsearchers[name] = subsearcher_cls


def register(subsearcher_cls=None, name=None):
    def decorator(subsearcher_cls):
        if name is None:
            _name = subsearcher_cls.__name__
        else:
            _name = name
        register_subsearcher(_name, subsearcher_cls)
        return subsearcher_cls
    return decorator(subsearcher_cls) if subsearcher_cls is not None else decorator


def get_subsearcher(name, default=None):
    return registered_subsearchers.get(name, default)


def get_all_subsearchers():
    return registered_subsearchers


class BaseSubSearcher(object):
    """ The abstract class for search subtitles.

    You must implement following methods:
    - search_subs
    """
    __metaclass__ = ABCMeta

    SUPPORT_LANGUAGES = []
    SUPPORT_EXTS = []

    def __init__(self, subfinder,  **kwargs):
        """
        subfinder: SubFinder
        debug: 是否输出调试信息
        """
        self.session = requests.session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        self.subfinder = subfinder
        self.api_urls = kwargs.get('api_urls', {})
        self.API_URL = self.api_urls.get(
            self.shortname, self.__class__.API_URL)

    def _debug(self, msg):
        self.subfinder.logger.debug(msg)

    @classmethod
    def _check_languages(cls, languages):
        for lang in languages:
            if lang not in cls.SUPPORT_LANGUAGES:
                raise exceptions.LanguageError(
                    '{} doesn\'t support "{}" language'.format(cls.__name__, lang))

    @classmethod
    def _check_exts(cls, exts):
        for ext in exts:
            if ext not in cls.SUPPORT_EXTS:
                raise exceptions.ExtError(
                    '{} doesn\'t support "{}" ext'.format(cls.__name__, ext))

    @classmethod
    def _join_url(cls, url, path):
        """ join absolute `url` and `path`(href)
        """
        return urlparse.urljoin(url, path)

    @classmethod
    def _get_videoname(cls, videofile):
        """parse the `videofile` and return it's basename
        """
        name = os.path.basename(videofile)
        name = os.path.splitext(name)[0]
        return name

    RE_SEASON = re.compile(
        r'[Ss](?P<season>\d+)\.?')
    RE_SEASON_EPISODE = re.compile(
        r'[Ss](?P<season>\d+)\.?[Ee](?P<episode>\d+)')
    RE_RESOLUTION = re.compile(r'(?P<resolution>720[Pp]|1080[Pp]|2160[Pp]|HR)')
    RE_SOURCE = re.compile(
        r'\.(?P<source>BD|Blu[Rr]ay|BDrip|WEB-DL|HDrip|HDTVrip|HDTV|HD|DVDrip)\.')
    RE_AUDIO_ENC = re.compile(
        r'(?P<audio_encoding>mp3|DD5\.1|DDP5\.1|AC3\.5\.1)')
    RE_VIDEO_ENC = re.compile(r'(?P<video_encoding>x264|H\.264|AVC1|H\.265)')

    @classmethod
    def _parse_videoname(cls, videoname):
        """ parse videoname and return video info dict
        video info contains:
        - title, the name of video
        - sub_title, the sub_title of video
        - resolution,
        - source,
        -
        - season, defaults to 0
        - episode, defaults to 0
        """
        info = {
            'title': '',
            'season': 0,
            'episode': 0,
            'resolution': '',
            'source': '',
            'audio_encoding': '',
            'video_encoding': '',
        }
        mapping = {
            'resolution': cls.RE_RESOLUTION,
            'source': cls.RE_SOURCE,
            'audio_encoding': cls.RE_AUDIO_ENC,
            'video_encoding': cls.RE_VIDEO_ENC
        }
        index = len(videoname)
        m = cls.RE_SEASON_EPISODE.search(videoname)
        if m:
            info['season'] = int(m.group('season'))
            info['episode'] = int(m.group('episode'))
            index, _ = m.span()
            info['title'] = videoname[0:index].strip('.')
        else:
            m = cls.RE_SEASON.search(videoname)
            if m:
                info['season'] = int(m.group('season'))
                index, _ = m.span()
                info['title'] = videoname[0:index].strip('.')
        
        for k, r in mapping.items():
            m = r.search(videoname)
            if m:
                info[k] = m.group(k)
                i, e = m.span()
                if info['title'] == '' or i < index:
                    index = i
                    info['title'] = videoname[0:index].strip('.')

        if info['title'] == '':
            i = videoname.find('.')
            info['title'] = videoname[:i] if i > 0 else videoname

        return info
    
    @classmethod
    def _gen_keyword(cls, videoinfo):
        """ 获取关键词
        """
        keyword = videoinfo.get('title')
        if videoinfo['season'] != 0:
            keyword += '.S{:02d}'.format(videoinfo['season'])
        if videoinfo['episode'] != 0:
            keyword += '.E{:02d}'.format(videoinfo['episode'])
        # replace space with '+'
        keyword = re.sub(r'\s+', ' ', keyword)
        return keyword

    @classmethod
    def _gen_subname(cls, videofile, origin_file, language=None, ext=None):
        if not language:
            language_ = []
            try:
                for l in cls.COMMON_LANGUAGES:
                    if origin_file.find(l) >= 0:
                        language_.append(l)
            except Exception:
                pass
            language = '&'.join(language_)
        if language and not language.startswith('.'):
            language = '.' + language

        basename = os.path.basename(videofile)
        basename, _ = os.path.splitext(basename)
        if not ext:
            _, ext = os.path.splitext(origin_file)
        if not ext.startswith('.'):
            ext = '.' + ext

        return '{basename}{language}{ext}'.format(
            basename=basename,
            language=language,
            ext=ext)

    @classmethod
    def _extract(cls, compressed_file, videofile, exts):
        """ 解压字幕文件，如果无法解压，则直接返回 compressed_file。
        exts 参数用于过滤掉非字幕文件，只有文件的扩展名在 exts 中，才解压该文件。
        """
        if not CompressedFile.is_compressed_file(compressed_file):
            return [compressed_file]

        root = os.path.dirname(compressed_file)
        subs = []
        cf = CompressedFile(compressed_file)
        for name in cf.namelist():
            if cf.isdir(name):
                continue
            # make `name` to unicode string
            origin_file = CompressedFile.decode_file_name(name)
            _, ext = os.path.splitext(origin_file)
            ext = ext[1:]
            if ext not in exts:
                continue
            subname = cls._gen_subname(videofile, origin_file)
            subpath = os.path.join(root, subname)
            cf.extract(name, subpath)
            subs.append(subpath)
        cf.close()
        return subs

    @classmethod
    def _filter_subinfo_list(cls, subinfo_list, videoinfo, languages, exts):
        """ filter subinfo list base on:
        - season
        - episode
        - languages
        - exts
        -
        return a best matched subinfo
        """
        filter_field_list = [
            'season',
            'episode',
            'resolution',
            'source',
            'video_encoding',
            'audio_encoding'
        ]
        filtered_subinfo_list = dict((f, []) for f in filter_field_list)

        for subinfo in subinfo_list:
            title = subinfo.get('title')
            videoinfo_ = cls._parse_videoname(title)
            last_field = None
            for field in filter_field_list:
                i = videoinfo.get(field)
                if isinstance(i, str):
                    i = i.lower()
                j = videoinfo_.get(field)
                if isinstance(j, str):
                    j = j.lower()
                if i == j:
                    last_field = field
                else:
                    break
            if last_field is not None:
                filtered_subinfo_list[last_field].append(subinfo)
        for field in filter_field_list[::-1]:
            if len(filtered_subinfo_list[field]) > 0:
                # sort by download_count and rate
                sorted_subinfo_list = sorted(filtered_subinfo_list[field],
                                             key=lambda item: (
                    item['rate'], item['download_count']),
                    reverse=True)
                return sorted_subinfo_list[0]
        return None

    def _download_subs(self, download_link, videofile, referer='', sub_title=''):
        """ 下载字幕
        videofile: 视频文件路径
        sub_title: 字幕标题（文件名）
        download_link: 下载链接
        referer: referer
        """
        root = os.path.dirname(videofile)
        name, _ = os.path.splitext(os.path.basename(videofile))
        ext = ''

        headers = {
            'Referer': referer
        }
        res = self.session.get(download_link, headers=headers, stream=True)
        referer = res.url

        # 尝试从 Content-Disposition 中获取文件后缀名
        content_disposition = res.headers.get('Content-Disposition', '')
        if content_disposition:
            _, params = cgi.parse_header(content_disposition)
            filename = params.get('filename')
            if filename:
                _, ext = os.path.splitext(filename)
                ext = ext[1:]

        if ext == '':
            # 尝试从url 中获取文件后缀名
            p = urlparse.urlparse(res.url)
            path = p.path
            if path:
                _, ext = os.path.splitext(path)
                ext = ext[1:]

        if ext == '':
            # 尝试从字幕标题中获取文件后缀名
            _, ext = os.path.splitext(sub_title)
            ext = ext[1:]

        filename = '{}.{}'.format(name, ext)
        filepath = os.path.join(root, filename)
        with open(filepath, 'wb') as fp:
            for chunk in res.iter_content(8192):
                fp.write(chunk)

        return filepath, referer

    def _search_subs(self, videofile, languages, exts, keyword=None):
        """ search subtitles of videofile.

        `videofile` is the absolute(or relative) path of the video file.

        `languages` is the language of subtitle, e.g chn, eng, the support for language is difference, depende on
        implemention of subclass. `languages` accepts one language or a list of language

        `exts` is the format of subtitle, e.g ass, srt, sub, idx, the support for ext is difference,
        depende on implemention of subclass. `ext` accepts one ext or a list of ext

        `keyword` is used to searching on the subtitle website.

        return a list of subtitle info
        [
            {
                'link': '',     # download link
                'language': '', # language
                'ext': '',      # ext
                'subname': '',  # the filename of subtitles
                'downloaded': False, # it's tell `SubFinder` whether need to download.
            },
            {
                'link': '',
                'language': '',
                'ext': '',
                'subname': '',
            },
            ...
        ]
        - `link`, it's optional, but if `downloaded` is False, then `link` is required.
        - `language`, it's optional
        - `subname`, it's optional, but if `downloaded` is False, then `subname` is required.
        - `downloaded`, `downloaded` is required.
            if `downloaded` is True, then `SubFinder` will not download again,
            otherwise `SubFinder` will download link.

        sub-class should implement this private method.
        """
        return []

    def search_subs(self, videofile, languages=None, exts=None, keyword=None):
        if languages is None:
            languages = self.SUPPORT_LANGUAGES
        elif isinstance(languages, str):
            languages = [languages]
        self._check_languages(languages)

        if exts is None:
            exts = self.SUPPORT_EXTS
        elif isinstance(exts, str):
            exts = [exts]
        self._check_exts(exts)

        return self._search_subs(videofile, languages, exts, keyword)

    def __str__(self):
        if hasattr(self.__class__, 'shortname'):
            name = self.__class__.shortname
        else:
            name = self.__class__.__name__
        return '<{}>'.format(name)

    def __unicode__(self):
        return self.__str__()
