from __future__ import unicode_literals

import io
import os
import subprocess
import sys
import time


from .common import AudioConversionError, PostProcessor

from ..compat import (
    compat_subprocess_get_DEVNULL,
)
from ..utils import (
    encodeArgument,
    encodeFilename,
    get_exe_version,
    is_outdated_version,
    PostProcessingError,
    prepend_extension,
    shell_quote,
    subtitles_filename,
)


class FFmpegPostProcessorError(PostProcessingError):
    pass


class FFmpegPostProcessor(PostProcessor):
    def __init__(self, downloader=None, deletetempfiles=False):
        PostProcessor.__init__(self, downloader)
        self._deletetempfiles = deletetempfiles
        self._determine_executables()

    def check_version(self):
        if not self.available:
            raise FFmpegPostProcessorError('ffmpeg or avconv not found. Please install one.')

        required_version = '10-0' if self.basename == 'avconv' else '1.0'
        if is_outdated_version(
                self._versions[self.basename], required_version):
            warning = 'Your copy of %s is outdated, update %s to version %s or newer if you encounter any errors.' % (
                self.basename, self.basename, required_version)
            if self._downloader:
                self._downloader.report_warning(warning)

    @staticmethod
    def get_versions(downloader=None):
        return FFmpegPostProcessor(downloader)._versions

    def _determine_executables(self):
        programs = ['avprobe', 'avconv', 'ffmpeg', 'ffprobe']
        prefer_ffmpeg = self._downloader.params.get('prefer_ffmpeg', False)

        self.basename = None
        self.probe_basename = None

        self._paths = None
        self._versions = None
        if self._downloader:
            location = self._downloader.params.get('ffmpeg_location')
            if location is not None:
                if not os.path.exists(location):
                    self._downloader.report_warning(
                        'ffmpeg-location %s does not exist! '
                        'Continuing without avconv/ffmpeg.' % (location))
                    self._versions = {}
                    return
                elif not os.path.isdir(location):
                    basename = os.path.splitext(os.path.basename(location))[0]
                    if basename not in programs:
                        self._downloader.report_warning(
                            'Cannot identify executable %s, its basename should be one of %s. '
                            'Continuing without avconv/ffmpeg.' %
                            (location, ', '.join(programs)))
                        self._versions = {}
                        return None
                    location = os.path.dirname(os.path.abspath(location))
                    if basename in ('ffmpeg', 'ffprobe'):
                        prefer_ffmpeg = True

                self._paths = dict(
                    (p, os.path.join(location, p)) for p in programs)
                self._versions = dict(
                    (p, get_exe_version(self._paths[p], args=['-version']))
                    for p in programs)
        if self._versions is None:
            self._versions = dict(
                (p, get_exe_version(p, args=['-version'])) for p in programs)
            self._paths = dict((p, p) for p in programs)

        if prefer_ffmpeg:
            prefs = ('ffmpeg', 'avconv')
        else:
            prefs = ('avconv', 'ffmpeg')
        for p in prefs:
            if self._versions[p]:
                self.basename = p
                break

        if prefer_ffmpeg:
            prefs = ('ffprobe', 'avprobe')
        else:
            prefs = ('avprobe', 'ffprobe')
        for p in prefs:
            if self._versions[p]:
                self.probe_basename = p
                break

    @property
    def available(self):
        return self.basename is not None

    @property
    def executable(self):
        return self._paths[self.basename]

    @property
    def probe_executable(self):
        return self._paths[self.probe_basename]

    def run_ffmpeg_multiple_files(self, input_paths, out_path, opts):
        self.check_version()

        oldest_mtime = min(
            os.stat(encodeFilename(path)).st_mtime for path in input_paths)

        files_cmd = []
        for path in input_paths:
            files_cmd.extend([encodeArgument('-i'), encodeFilename(path, True)])
        cmd = ([encodeFilename(self.executable, True), encodeArgument('-y')] +
               files_cmd +
               [encodeArgument(o) for o in opts] +
               [encodeFilename(self._ffmpeg_filename_argument(out_path), True)])

        if self._downloader.params.get('verbose', False):
            self._downloader.to_screen('[debug] ffmpeg command line: %s' % shell_quote(cmd))
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            stderr = stderr.decode('utf-8', 'replace')
            msg = stderr.strip().split('\n')[-1]
            raise FFmpegPostProcessorError(msg)
        os.utime(encodeFilename(out_path), (oldest_mtime, oldest_mtime))
        if self._deletetempfiles:
            for ipath in input_paths:
                os.remove(ipath)

    def run_ffmpeg(self, path, out_path, opts):
        self.run_ffmpeg_multiple_files([path], out_path, opts)

    def _ffmpeg_filename_argument(self, fn):
        # ffmpeg broke --, see https://ffmpeg.org/trac/ffmpeg/ticket/2127 for details
        if fn.startswith('-'):
            return './' + fn
        return fn


class FFmpegExtractAudioPP(FFmpegPostProcessor):
    def __init__(self, downloader=None, preferredcodec=None, preferredquality=None, nopostoverwrites=False):
        FFmpegPostProcessor.__init__(self, downloader)
        if preferredcodec is None:
            preferredcodec = 'best'
        self._preferredcodec = preferredcodec
        self._preferredquality = preferredquality
        self._nopostoverwrites = nopostoverwrites

    def get_audio_codec(self, path):

        if not self.probe_executable:
            raise PostProcessingError('ffprobe or avprobe not found. Please install one.')
        try:
            cmd = [
                encodeFilename(self.probe_executable, True),
                encodeArgument('-show_streams'),
                encodeFilename(self._ffmpeg_filename_argument(path), True)]
            if self._downloader.params.get('verbose', False):
                self._downloader.to_screen('[debug] %s command line: %s' % (self.basename, shell_quote(cmd)))
            handle = subprocess.Popen(cmd, stderr=compat_subprocess_get_DEVNULL(), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            output = handle.communicate()[0]
            if handle.wait() != 0:
                return None
        except (IOError, OSError):
            return None
        audio_codec = None
        for line in output.decode('ascii', 'ignore').split('\n'):
            if line.startswith('codec_name='):
                audio_codec = line.split('=')[1].strip()
            elif line.strip() == 'codec_type=audio' and audio_codec is not None:
                return audio_codec
        return None

    def run_ffmpeg(self, path, out_path, codec, more_opts):
        if codec is None:
            acodec_opts = []
        else:
            acodec_opts = ['-acodec', codec]
        opts = ['-vn'] + acodec_opts + more_opts
        try:
            FFmpegPostProcessor.run_ffmpeg(self, path, out_path, opts)
        except FFmpegPostProcessorError as err:
            raise AudioConversionError(err.msg)

    def run(self, information):
        path = information['filepath']

        filecodec = self.get_audio_codec(path)
        if filecodec is None:
            raise PostProcessingError('WARNING: unable to obtain file audio codec with ffprobe')

        more_opts = []
        if self._preferredcodec == 'best' or self._preferredcodec == filecodec or (self._preferredcodec == 'm4a' and filecodec == 'aac'):
            if filecodec == 'aac' and self._preferredcodec in ['m4a', 'best']:
                # Lossless, but in another container
                acodec = 'copy'
                extension = 'm4a'
                more_opts = ['-bsf:a', 'aac_adtstoasc']
            elif filecodec in ['aac', 'mp3', 'vorbis', 'opus']:
                # Lossless if possible
                acodec = 'copy'
                extension = filecodec
                if filecodec == 'aac':
                    more_opts = ['-f', 'adts']
                if filecodec == 'vorbis':
                    extension = 'ogg'
            else:
                # MP3 otherwise.
                acodec = 'libmp3lame'
                extension = 'mp3'
                more_opts = []
                if self._preferredquality is not None:
                    if int(self._preferredquality) < 10:
                        more_opts += ['-q:a', self._preferredquality]
                    else:
                        more_opts += ['-b:a', self._preferredquality + 'k']
        else:
            # We convert the audio (lossy)
            acodec = {'mp3': 'libmp3lame', 'aac': 'aac', 'm4a': 'aac', 'opus': 'opus', 'vorbis': 'libvorbis', 'wav': None}[self._preferredcodec]
            extension = self._preferredcodec
            more_opts = []
            if self._preferredquality is not None:
                # The opus codec doesn't support the -aq option
                if int(self._preferredquality) < 10 and extension != 'opus':
                    more_opts += ['-q:a', self._preferredquality]
                else:
                    more_opts += ['-b:a', self._preferredquality + 'k']
            if self._preferredcodec == 'aac':
                more_opts += ['-f', 'adts']
            if self._preferredcodec == 'm4a':
                more_opts += ['-bsf:a', 'aac_adtstoasc']
            if self._preferredcodec == 'vorbis':
                extension = 'ogg'
            if self._preferredcodec == 'wav':
                extension = 'wav'
                more_opts += ['-f', 'wav']

        prefix, sep, ext = path.rpartition('.')  # not os.path.splitext, since the latter does not work on unicode in all setups
        new_path = prefix + sep + extension

        # If we download foo.mp3 and convert it to... foo.mp3, then don't delete foo.mp3, silly.
        if new_path == path:
            self._nopostoverwrites = True

        try:
            if self._nopostoverwrites and os.path.exists(encodeFilename(new_path)):
                self._downloader.to_screen('[youtube] Post-process file %s exists, skipping' % new_path)
            else:
                self._downloader.to_screen('[' + self.basename + '] Destination: ' + new_path)
                self.run_ffmpeg(path, new_path, acodec, more_opts)
        except:
            etype, e, tb = sys.exc_info()
            if isinstance(e, AudioConversionError):
                msg = 'audio conversion failed: ' + e.msg
            else:
                msg = 'error running ' + self.basename
            raise PostProcessingError(msg)

        # Try to update the date time for extracted audio file.
        if information.get('filetime') is not None:
            try:
                os.utime(encodeFilename(new_path), (time.time(), information['filetime']))
            except:
                self._downloader.report_warning('Cannot update utime of audio file')

        information['filepath'] = new_path
        return self._nopostoverwrites, information


class FFmpegVideoConvertorPP(FFmpegPostProcessor):
    def __init__(self, downloader=None, preferedformat=None):
        super(FFmpegVideoConvertorPP, self).__init__(downloader)
        self._preferedformat = preferedformat

    def run(self, information):
        path = information['filepath']
        prefix, sep, ext = path.rpartition('.')
        outpath = prefix + sep + self._preferedformat
        if information['ext'] == self._preferedformat:
            self._downloader.to_screen('[ffmpeg] Not converting video file %s - already is in target format %s' % (path, self._preferedformat))
            return True, information
        self._downloader.to_screen('[' + 'ffmpeg' + '] Converting video from %s to %s, Destination: ' % (information['ext'], self._preferedformat) + outpath)
        self.run_ffmpeg(path, outpath, [])
        information['filepath'] = outpath
        information['format'] = self._preferedformat
        information['ext'] = self._preferedformat
        return False, information


class FFmpegEmbedSubtitlePP(FFmpegPostProcessor):
    # See http://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt
    _lang_map = {
        'aa': 'aar',
        'ab': 'abk',
        'ae': 'ave',
        'af': 'afr',
        'ak': 'aka',
        'am': 'amh',
        'an': 'arg',
        'ar': 'ara',
        'as': 'asm',
        'av': 'ava',
        'ay': 'aym',
        'az': 'aze',
        'ba': 'bak',
        'be': 'bel',
        'bg': 'bul',
        'bh': 'bih',
        'bi': 'bis',
        'bm': 'bam',
        'bn': 'ben',
        'bo': 'bod',
        'br': 'bre',
        'bs': 'bos',
        'ca': 'cat',
        'ce': 'che',
        'ch': 'cha',
        'co': 'cos',
        'cr': 'cre',
        'cs': 'ces',
        'cu': 'chu',
        'cv': 'chv',
        'cy': 'cym',
        'da': 'dan',
        'de': 'deu',
        'dv': 'div',
        'dz': 'dzo',
        'ee': 'ewe',
        'el': 'ell',
        'en': 'eng',
        'eo': 'epo',
        'es': 'spa',
        'et': 'est',
        'eu': 'eus',
        'fa': 'fas',
        'ff': 'ful',
        'fi': 'fin',
        'fj': 'fij',
        'fo': 'fao',
        'fr': 'fra',
        'fy': 'fry',
        'ga': 'gle',
        'gd': 'gla',
        'gl': 'glg',
        'gn': 'grn',
        'gu': 'guj',
        'gv': 'glv',
        'ha': 'hau',
        'he': 'heb',
        'hi': 'hin',
        'ho': 'hmo',
        'hr': 'hrv',
        'ht': 'hat',
        'hu': 'hun',
        'hy': 'hye',
        'hz': 'her',
        'ia': 'ina',
        'id': 'ind',
        'ie': 'ile',
        'ig': 'ibo',
        'ii': 'iii',
        'ik': 'ipk',
        'io': 'ido',
        'is': 'isl',
        'it': 'ita',
        'iu': 'iku',
        'ja': 'jpn',
        'jv': 'jav',
        'ka': 'kat',
        'kg': 'kon',
        'ki': 'kik',
        'kj': 'kua',
        'kk': 'kaz',
        'kl': 'kal',
        'km': 'khm',
        'kn': 'kan',
        'ko': 'kor',
        'kr': 'kau',
        'ks': 'kas',
        'ku': 'kur',
        'kv': 'kom',
        'kw': 'cor',
        'ky': 'kir',
        'la': 'lat',
        'lb': 'ltz',
        'lg': 'lug',
        'li': 'lim',
        'ln': 'lin',
        'lo': 'lao',
        'lt': 'lit',
        'lu': 'lub',
        'lv': 'lav',
        'mg': 'mlg',
        'mh': 'mah',
        'mi': 'mri',
        'mk': 'mkd',
        'ml': 'mal',
        'mn': 'mon',
        'mr': 'mar',
        'ms': 'msa',
        'mt': 'mlt',
        'my': 'mya',
        'na': 'nau',
        'nb': 'nob',
        'nd': 'nde',
        'ne': 'nep',
        'ng': 'ndo',
        'nl': 'nld',
        'nn': 'nno',
        'no': 'nor',
        'nr': 'nbl',
        'nv': 'nav',
        'ny': 'nya',
        'oc': 'oci',
        'oj': 'oji',
        'om': 'orm',
        'or': 'ori',
        'os': 'oss',
        'pa': 'pan',
        'pi': 'pli',
        'pl': 'pol',
        'ps': 'pus',
        'pt': 'por',
        'qu': 'que',
        'rm': 'roh',
        'rn': 'run',
        'ro': 'ron',
        'ru': 'rus',
        'rw': 'kin',
        'sa': 'san',
        'sc': 'srd',
        'sd': 'snd',
        'se': 'sme',
        'sg': 'sag',
        'si': 'sin',
        'sk': 'slk',
        'sl': 'slv',
        'sm': 'smo',
        'sn': 'sna',
        'so': 'som',
        'sq': 'sqi',
        'sr': 'srp',
        'ss': 'ssw',
        'st': 'sot',
        'su': 'sun',
        'sv': 'swe',
        'sw': 'swa',
        'ta': 'tam',
        'te': 'tel',
        'tg': 'tgk',
        'th': 'tha',
        'ti': 'tir',
        'tk': 'tuk',
        'tl': 'tgl',
        'tn': 'tsn',
        'to': 'ton',
        'tr': 'tur',
        'ts': 'tso',
        'tt': 'tat',
        'tw': 'twi',
        'ty': 'tah',
        'ug': 'uig',
        'uk': 'ukr',
        'ur': 'urd',
        'uz': 'uzb',
        've': 'ven',
        'vi': 'vie',
        'vo': 'vol',
        'wa': 'wln',
        'wo': 'wol',
        'xh': 'xho',
        'yi': 'yid',
        'yo': 'yor',
        'za': 'zha',
        'zh': 'zho',
        'zu': 'zul',
    }

    @classmethod
    def _conver_lang_code(cls, code):
        """Convert language code from ISO 639-1 to ISO 639-2/T"""
        return cls._lang_map.get(code[:2])

    def run(self, information):
        if information['ext'] != 'mp4':
            self._downloader.to_screen('[ffmpeg] Subtitles can only be embedded in mp4 files')
            return True, information
        subtitles = information.get('requested_subtitles')
        if not subtitles:
            self._downloader.to_screen('[ffmpeg] There aren\'t any subtitles to embed')
            return True, information

        sub_langs = list(subtitles.keys())
        filename = information['filepath']
        input_files = [filename] + [subtitles_filename(filename, lang, sub_info['ext']) for lang, sub_info in subtitles.items()]

        opts = [
            '-map', '0',
            '-c', 'copy',
            # Don't copy the existing subtitles, we may be running the
            # postprocessor a second time
            '-map', '-0:s',
            '-c:s', 'mov_text',
        ]
        for (i, lang) in enumerate(sub_langs):
            opts.extend(['-map', '%d:0' % (i + 1)])
            lang_code = self._conver_lang_code(lang)
            if lang_code is not None:
                opts.extend(['-metadata:s:s:%d' % i, 'language=%s' % lang_code])

        temp_filename = prepend_extension(filename, 'temp')
        self._downloader.to_screen('[ffmpeg] Embedding subtitles in \'%s\'' % filename)
        self.run_ffmpeg_multiple_files(input_files, temp_filename, opts)
        os.remove(encodeFilename(filename))
        os.rename(encodeFilename(temp_filename), encodeFilename(filename))

        return True, information


class FFmpegMetadataPP(FFmpegPostProcessor):
    def run(self, info):
        metadata = {}
        if info.get('title') is not None:
            metadata['title'] = info['title']
        if info.get('upload_date') is not None:
            metadata['date'] = info['upload_date']
        if info.get('uploader') is not None:
            metadata['artist'] = info['uploader']
        elif info.get('uploader_id') is not None:
            metadata['artist'] = info['uploader_id']
        if info.get('description') is not None:
            metadata['description'] = info['description']
            metadata['comment'] = info['description']
        if info.get('webpage_url') is not None:
            metadata['purl'] = info['webpage_url']

        if not metadata:
            self._downloader.to_screen('[ffmpeg] There isn\'t any metadata to add')
            return True, info

        filename = info['filepath']
        temp_filename = prepend_extension(filename, 'temp')

        if info['ext'] == 'm4a':
            options = ['-vn', '-acodec', 'copy']
        else:
            options = ['-c', 'copy']

        for (name, value) in metadata.items():
            options.extend(['-metadata', '%s=%s' % (name, value)])

        self._downloader.to_screen('[ffmpeg] Adding metadata to \'%s\'' % filename)
        self.run_ffmpeg(filename, temp_filename, options)
        os.remove(encodeFilename(filename))
        os.rename(encodeFilename(temp_filename), encodeFilename(filename))
        return True, info


class FFmpegMergerPP(FFmpegPostProcessor):
    def run(self, info):
        filename = info['filepath']
        args = ['-c', 'copy', '-map', '0:v:0', '-map', '1:a:0']
        self._downloader.to_screen('[ffmpeg] Merging formats into "%s"' % filename)
        self.run_ffmpeg_multiple_files(info['__files_to_merge'], filename, args)
        return True, info


class FFmpegAudioFixPP(FFmpegPostProcessor):
    def run(self, info):
        filename = info['filepath']
        temp_filename = prepend_extension(filename, 'temp')

        options = ['-vn', '-acodec', 'copy']
        self._downloader.to_screen('[ffmpeg] Fixing audio file "%s"' % filename)
        self.run_ffmpeg(filename, temp_filename, options)

        os.remove(encodeFilename(filename))
        os.rename(encodeFilename(temp_filename), encodeFilename(filename))

        return True, info


class FFmpegFixupStretchedPP(FFmpegPostProcessor):
    def run(self, info):
        stretched_ratio = info.get('stretched_ratio')
        if stretched_ratio is None or stretched_ratio == 1:
            return True, info

        filename = info['filepath']
        temp_filename = prepend_extension(filename, 'temp')

        options = ['-c', 'copy', '-aspect', '%f' % stretched_ratio]
        self._downloader.to_screen('[ffmpeg] Fixing aspect ratio in "%s"' % filename)
        self.run_ffmpeg(filename, temp_filename, options)

        os.remove(encodeFilename(filename))
        os.rename(encodeFilename(temp_filename), encodeFilename(filename))

        return True, info


class FFmpegFixupM4aPP(FFmpegPostProcessor):
    def run(self, info):
        if info.get('container') != 'm4a_dash':
            return True, info

        filename = info['filepath']
        temp_filename = prepend_extension(filename, 'temp')

        options = ['-c', 'copy', '-f', 'mp4']
        self._downloader.to_screen('[ffmpeg] Correcting container in "%s"' % filename)
        self.run_ffmpeg(filename, temp_filename, options)

        os.remove(encodeFilename(filename))
        os.rename(encodeFilename(temp_filename), encodeFilename(filename))

        return True, info


class FFmpegSubtitlesConvertorPP(FFmpegPostProcessor):
    def __init__(self, downloader=None, format=None):
        super(FFmpegSubtitlesConvertorPP, self).__init__(downloader)
        self.format = format

    def run(self, info):
        subs = info.get('requested_subtitles')
        filename = info['filepath']
        new_ext = self.format
        new_format = new_ext
        if new_format == 'vtt':
            new_format = 'webvtt'
        if subs is None:
            self._downloader.to_screen('[ffmpeg] There aren\'t any subtitles to convert')
            return True, info
        self._downloader.to_screen('[ffmpeg] Converting subtitles')
        for lang, sub in subs.items():
            ext = sub['ext']
            if ext == new_ext:
                self._downloader.to_screen(
                    '[ffmpeg] Subtitle file for %s is already in the requested'
                    'format' % new_ext)
                continue
            new_file = subtitles_filename(filename, lang, new_ext)
            self.run_ffmpeg(
                subtitles_filename(filename, lang, ext),
                new_file, ['-f', new_format])

            with io.open(new_file, 'rt', encoding='utf-8') as f:
                subs[lang] = {
                    'ext': ext,
                    'data': f.read(),
                }

        return True, info
