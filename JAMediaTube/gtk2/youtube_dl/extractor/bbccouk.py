from __future__ import unicode_literals

import xml.etree.ElementTree

from .common import InfoExtractor
from ..utils import ExtractorError
from ..compat import compat_HTTPError


class BBCCoUkIE(InfoExtractor):
    IE_NAME = 'bbc.co.uk'
    IE_DESC = 'BBC iPlayer'
    _VALID_URL = r'https?://(?:www\.)?bbc\.co\.uk/(?:(?:(?:programmes|iplayer(?:/[^/]+)?/(?:episode|playlist))/)|music/clips[/#])(?P<id>[\da-z]{8})'

    _TESTS = [
        {
            'url': 'http://www.bbc.co.uk/programmes/b039g8p7',
            'info_dict': {
                'id': 'b039d07m',
                'ext': 'flv',
                'title': 'Kaleidoscope, Leonard Cohen',
                'description': 'The Canadian poet and songwriter reflects on his musical career.',
                'duration': 1740,
            },
            'params': {
                # rtmp download
                'skip_download': True,
            }
        },
        {
            'url': 'http://www.bbc.co.uk/iplayer/episode/b00yng5w/The_Man_in_Black_Series_3_The_Printed_Name/',
            'info_dict': {
                'id': 'b00yng1d',
                'ext': 'flv',
                'title': 'The Man in Black: Series 3: The Printed Name',
                'description': "Mark Gatiss introduces Nicholas Pierpan's chilling tale of a writer's devilish pact with a mysterious man. Stars Ewan Bailey.",
                'duration': 1800,
            },
            'params': {
                # rtmp download
                'skip_download': True,
            },
            'skip': 'Episode is no longer available on BBC iPlayer Radio',
        },
        {
            'url': 'http://www.bbc.co.uk/iplayer/episode/b03vhd1f/The_Voice_UK_Series_3_Blind_Auditions_5/',
            'info_dict': {
                'id': 'b00yng1d',
                'ext': 'flv',
                'title': 'The Voice UK: Series 3: Blind Auditions 5',
                'description': "Emma Willis and Marvin Humes present the fifth set of blind auditions in the singing competition, as the coaches continue to build their teams based on voice alone.",
                'duration': 5100,
            },
            'params': {
                # rtmp download
                'skip_download': True,
            },
            'skip': 'Currently BBC iPlayer TV programmes are available to play in the UK only',
        },
        {
            'url': 'http://www.bbc.co.uk/iplayer/episode/p026c7jt/tomorrows-worlds-the-unearthly-history-of-science-fiction-2-invasion',
            'info_dict': {
                'id': 'b03k3pb7',
                'ext': 'flv',
                'title': "Tomorrow's Worlds: The Unearthly History of Science Fiction",
                'description': '2. Invasion',
                'duration': 3600,
            },
            'params': {
                # rtmp download
                'skip_download': True,
            },
            'skip': 'Currently BBC iPlayer TV programmes are available to play in the UK only',
        }, {
            'url': 'http://www.bbc.co.uk/programmes/b04v20dw',
            'info_dict': {
                'id': 'b04v209v',
                'ext': 'flv',
                'title': 'Pete Tong, The Essential New Tune Special',
                'description': "Pete has a very special mix - all of 2014's Essential New Tunes!",
                'duration': 10800,
            },
            'params': {
                # rtmp download
                'skip_download': True,
            }
        }, {
            'url': 'http://www.bbc.co.uk/music/clips/p02frcc3',
            'note': 'Audio',
            'info_dict': {
                'id': 'p02frcch',
                'ext': 'flv',
                'title': 'Pete Tong, Past, Present and Future Special, Madeon - After Hours mix',
                'description': 'French house superstar Madeon takes us out of the club and onto the after party.',
                'duration': 3507,
            },
            'params': {
                # rtmp download
                'skip_download': True,
            }
        }, {
            'url': 'http://www.bbc.co.uk/music/clips/p025c0zz',
            'note': 'Video',
            'info_dict': {
                'id': 'p025c103',
                'ext': 'flv',
                'title': 'Reading and Leeds Festival, 2014, Rae Morris - Closer (Live on BBC Three)',
                'description': 'Rae Morris performs Closer for BBC Three at Reading 2014',
                'duration': 226,
            },
            'params': {
                # rtmp download
                'skip_download': True,
            }
        }, {
            'url': 'http://www.bbc.co.uk/iplayer/playlist/p01dvks4',
            'only_matching': True,
        }, {
            'url': 'http://www.bbc.co.uk/music/clips#p02frcc3',
            'only_matching': True,
        }, {
            'url': 'http://www.bbc.co.uk/iplayer/cbeebies/episode/b0480276/bing-14-atchoo',
            'only_matching': True,
        }
    ]

    def _extract_asx_playlist(self, connection, programme_id):
        asx = self._download_xml(connection.get('href'), programme_id, 'Downloading ASX playlist')
        return [ref.get('href') for ref in asx.findall('./Entry/ref')]

    def _extract_connection(self, connection, programme_id):
        formats = []
        protocol = connection.get('protocol')
        supplier = connection.get('supplier')
        if protocol == 'http':
            href = connection.get('href')
            # ASX playlist
            if supplier == 'asx':
                for i, ref in enumerate(self._extract_asx_playlist(connection, programme_id)):
                    formats.append({
                        'url': ref,
                        'format_id': 'ref%s_%s' % (i, supplier),
                    })
            # Direct link
            else:
                formats.append({
                    'url': href,
                    'format_id': supplier,
                })
        elif protocol == 'rtmp':
            application = connection.get('application', 'ondemand')
            auth_string = connection.get('authString')
            identifier = connection.get('identifier')
            server = connection.get('server')
            formats.append({
                'url': '%s://%s/%s?%s' % (protocol, server, application, auth_string),
                'play_path': identifier,
                'app': '%s?%s' % (application, auth_string),
                'page_url': 'http://www.bbc.co.uk',
                'player_url': 'http://www.bbc.co.uk/emp/releases/iplayer/revisions/617463_618125_4/617463_618125_4_emp.swf',
                'rtmp_live': False,
                'ext': 'flv',
                'format_id': supplier,
            })
        return formats

    def _extract_items(self, playlist):
        return playlist.findall('./{http://bbc.co.uk/2008/emp/playlist}item')

    def _extract_medias(self, media_selection):
        error = media_selection.find('./{http://bbc.co.uk/2008/mp/mediaselection}error')
        if error is not None:
            raise ExtractorError(
                '%s returned error: %s' % (self.IE_NAME, error.get('id')), expected=True)
        return media_selection.findall('./{http://bbc.co.uk/2008/mp/mediaselection}media')

    def _extract_connections(self, media):
        return media.findall('./{http://bbc.co.uk/2008/mp/mediaselection}connection')

    def _extract_video(self, media, programme_id):
        formats = []
        vbr = int(media.get('bitrate'))
        vcodec = media.get('encoding')
        service = media.get('service')
        width = int(media.get('width'))
        height = int(media.get('height'))
        file_size = int(media.get('media_file_size'))
        for connection in self._extract_connections(media):
            conn_formats = self._extract_connection(connection, programme_id)
            for format in conn_formats:
                format.update({
                    'format_id': '%s_%s' % (service, format['format_id']),
                    'width': width,
                    'height': height,
                    'vbr': vbr,
                    'vcodec': vcodec,
                    'filesize': file_size,
                })
            formats.extend(conn_formats)
        return formats

    def _extract_audio(self, media, programme_id):
        formats = []
        abr = int(media.get('bitrate'))
        acodec = media.get('encoding')
        service = media.get('service')
        for connection in self._extract_connections(media):
            conn_formats = self._extract_connection(connection, programme_id)
            for format in conn_formats:
                format.update({
                    'format_id': '%s_%s' % (service, format['format_id']),
                    'abr': abr,
                    'acodec': acodec,
                })
            formats.extend(conn_formats)
        return formats

    def _get_subtitles(self, media, programme_id):
        subtitles = {}
        for connection in self._extract_connections(media):
            captions = self._download_xml(connection.get('href'), programme_id, 'Downloading captions')
            lang = captions.get('{http://www.w3.org/XML/1998/namespace}lang', 'en')
            ps = captions.findall('./{0}body/{0}div/{0}p'.format('{http://www.w3.org/2006/10/ttaf1}'))
            srt = ''

            def _extract_text(p):
                if p.text is not None:
                    stripped_text = p.text.strip()
                    if stripped_text:
                        return stripped_text
                return ' '.join(span.text.strip() for span in p.findall('{http://www.w3.org/2006/10/ttaf1}span'))
            for pos, p in enumerate(ps):
                srt += '%s\r\n%s --> %s\r\n%s\r\n\r\n' % (str(pos), p.get('begin'), p.get('end'), _extract_text(p))
            subtitles[lang] = [
                {
                    'url': connection.get('href'),
                    'ext': 'ttml',
                },
                {
                    'data': srt,
                    'ext': 'srt',
                },
            ]
        return subtitles

    def _download_media_selector(self, programme_id):
        try:
            media_selection = self._download_xml(
                'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/pc/vpid/%s' % programme_id,
                programme_id, 'Downloading media selection XML')
        except ExtractorError as ee:
            if isinstance(ee.cause, compat_HTTPError) and ee.cause.code == 403:
                media_selection = xml.etree.ElementTree.fromstring(ee.cause.read().encode('utf-8'))
            else:
                raise

        formats = []
        subtitles = None

        for media in self._extract_medias(media_selection):
            kind = media.get('kind')
            if kind == 'audio':
                formats.extend(self._extract_audio(media, programme_id))
            elif kind == 'video':
                formats.extend(self._extract_video(media, programme_id))
            elif kind == 'captions':
                subtitles = self.extract_subtitles(media, programme_id)

        return formats, subtitles

    def _download_playlist(self, playlist_id):
        try:
            playlist = self._download_json(
                'http://www.bbc.co.uk/programmes/%s/playlist.json' % playlist_id,
                playlist_id, 'Downloading playlist JSON')

            version = playlist.get('defaultAvailableVersion')
            if version:
                smp_config = version['smpConfig']
                title = smp_config['title']
                description = smp_config['summary']
                for item in smp_config['items']:
                    kind = item['kind']
                    if kind != 'programme' and kind != 'radioProgramme':
                        continue
                    programme_id = item.get('vpid')
                    duration = int(item.get('duration'))
                    formats, subtitles = self._download_media_selector(programme_id)
                return programme_id, title, description, duration, formats, subtitles
        except ExtractorError as ee:
            if not (isinstance(ee.cause, compat_HTTPError) and ee.cause.code == 404):
                raise

        # fallback to legacy playlist
        playlist = self._download_xml(
            'http://www.bbc.co.uk/iplayer/playlist/%s' % playlist_id,
            playlist_id, 'Downloading legacy playlist XML')

        no_items = playlist.find('./{http://bbc.co.uk/2008/emp/playlist}noItems')
        if no_items is not None:
            reason = no_items.get('reason')
            if reason == 'preAvailability':
                msg = 'Episode %s is not yet available' % playlist_id
            elif reason == 'postAvailability':
                msg = 'Episode %s is no longer available' % playlist_id
            elif reason == 'noMedia':
                msg = 'Episode %s is not currently available' % playlist_id
            else:
                msg = 'Episode %s is not available: %s' % (playlist_id, reason)
            raise ExtractorError(msg, expected=True)

        for item in self._extract_items(playlist):
            kind = item.get('kind')
            if kind != 'programme' and kind != 'radioProgramme':
                continue
            title = playlist.find('./{http://bbc.co.uk/2008/emp/playlist}title').text
            description = playlist.find('./{http://bbc.co.uk/2008/emp/playlist}summary').text
            programme_id = item.get('identifier')
            duration = int(item.get('duration'))
            formats, subtitles = self._download_media_selector(programme_id)

        return programme_id, title, description, duration, formats, subtitles

    def _real_extract(self, url):
        group_id = self._match_id(url)

        webpage = self._download_webpage(url, group_id, 'Downloading video page')

        programme_id = self._search_regex(
            r'"vpid"\s*:\s*"([\da-z]{8})"', webpage, 'vpid', fatal=False, default=None)
        if programme_id:
            player = self._download_json(
                'http://www.bbc.co.uk/iplayer/episode/%s.json' % group_id,
                group_id)['jsConf']['player']
            title = player['title']
            description = player['subtitle']
            duration = player['duration']
            formats, subtitles = self._download_media_selector(programme_id)
        else:
            programme_id, title, description, duration, formats, subtitles = self._download_playlist(group_id)

        self._sort_formats(formats)

        return {
            'id': programme_id,
            'title': title,
            'description': description,
            'duration': duration,
            'formats': formats,
            'subtitles': subtitles,
        }
