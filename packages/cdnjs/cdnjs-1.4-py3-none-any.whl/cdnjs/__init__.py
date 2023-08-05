import os
import json
import logging
import requests

from fuzzywuzzy import fuzz
from urllib.parse import urlencode, urljoin

from cdnjs.settings import Settings


logger = logging.getLogger('cdnjs')


_cached_db = []
_default_subdir = 'lib'


class RepositoryNotFoundException(Exception):
    """
    If requested repository is not found at cdnjs.com
    """
    pass


class FileNotFoundException(Exception):
    """
    If requested file is not found at cdnjs.com repository
    """
    pass


class InvalidFileException(Exception):
    """
    Internal library exceptions type
    """
    pass


class FS:
    """
    CDNJS FileSystem shortcut
    """
    def __init__(self, subdir=_default_subdir):
        self._root = Settings.get('STATIC_ROOT', default_setting='STATIC_ROOT')
        self._url = Settings.get('STATIC_URL', default_setting='STATIC_URL')
        self._subdir = subdir

    @property
    def directory_root(self):
        return os.path.join(self._root, self._subdir)

    @property
    def directory_url(self):
        if self._subdir:
            return self._url + self._subdir + '/'
        return self._url

    def get_path(self, *parts):
        if self._subdir:
            return os.path.join(self._root, self._subdir, *parts)
        return os.path.join(self._root, *parts)

    def read(self, file_path):
        """
        Trying to read file if exists
        :param file_path:
        :return:
        """
        return open(self.get_path(file_path), 'r').read()

    def write(self, file_path, contents):
        """
        Trying to write file.
        :param file_path:
        :param contents:
        :return:
        """
        file_path = self.get_path(file_path)

        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        if isinstance(contents, list):
            if isinstance(contents[0], str):
                contents = ''.join(contents)
            elif isinstance(contents[0], bytes):
                contents = b''.join(contents)
            else:
                raise Exception('Invalid type of file contents: {}'.format(type(contents).__name__))

        if isinstance(contents, str):
            with open(file_path, 'w') as f:
                f.write(contents)
        elif isinstance(contents, bytes):
            with open(file_path, 'wb') as f:
                f.write(contents)
        else:
            raise Exception('Invalid type of file contents: {}'.format(type(contents).__name__))

    def exists(self, file_path):
        return os.path.exists(self.get_path(file_path))

    def delete(self, file_path):
        if self.exists(file_path):
            try:
                return os.unlink(self.get_path(file_path))
            except Exception as e:
                pass

    @staticmethod
    def urljoin(base_url=None, trailing_slash=False, *parts):
        """
        Join url and keep trailing slash.
        :param base_url:
        :param trailing_slash:
        :param parts:
        :return:
        """
        result = []
        for k in parts:
            if k.startswith('http') or k.startswith:
                result.append(k.strip('/'))

        uri = '/{}{}'.format('/'.join(result), '/' if trailing_slash else '')

        if base_url is None:
            return uri
        return urljoin(base_url, uri)


_fs = FS()


class CDNJsObject(object):
    """
    CDNJs object
    """
    def __init__(self, name, version, default=None, files=None, keywords=None):
        """
        Init object
        :param name:
        :param version:
        :param str default:
        :param dict files:
        :param list keywords:
        """
        self.name = name
        self.version = version
        self.default = default.split('/')[-1]
        self.files = files or {}
        self.keywords = keywords or []

    def __str__(self):
        """
        :return str:
        """
        return '<{}/{}>'.format(self.name, self.version)

    def __unicode__(self):
        """
        :return unicode:
        """
        return str(self)

    def __getitem__(self, item):
        """
        Returns file
        :param item:
        :return:
        """
        for name, obj in self.files.items():
            if name.endswith(item):
                return obj['uri' if Settings.get('USE_LOCAL') else 'cdn']

        raise FileNotFoundException('File {} was not found at {}'.format(item, self.name))

    def __setitem__(self, key, value):
        """
        Adds file
        :param key:
        :param value:
        :return:
        """
        if 'uri' not in value or 'cdn' not in value:
            raise InvalidFileException('Invalid File {} for storage'.format(key))

        self.files[key] = value

    def __contains__(self, item):
        """
        Contains file
        :param item:
        :return:
        """
        for f in self.files.keys():
            if item in f:
                return True

    @property
    def dict(self):
        return {
            'default': self.default,
            'files': self.files
        }

    @property
    def is_valid(self):
        """
        Is valid
        :return:
        """
        return len(self.files.keys()) > 0

    def matches(self, name, version=None):
        """
        Is matched to name with version
        :param name:
        :param version:
        :return:
        """
        if fuzz.ratio(name.lower(), self.name.lower()) < 90:
            return False

        if version is not None and self.version != version:
            return False

        return True

    def download(self):
        """
        Downloads cdn repository to local storage
        :return:
        """
        # Create storage path
        storage_path = _fs.get_path(self.name, self.version)

        # Load files
        for name, path_data in self.files.items():
            subdir = CDNJs.get_dir(path_data['cdn'], self.version)
            dir_path = os.path.join(storage_path, subdir)
            file_path = os.path.join(dir_path, name)
            file_uri = '{root}{name}/{version}/{subdir}{file}'.format(
                root=_fs.directory_url,
                name=self.name,
                version=self.version,
                subdir=subdir + '/' if subdir else '',
                file=name
            )

            if not _fs.exists(file_path):
                logger.info('> > Downloading {}...'.format(name))
                buffer = []
                for c in requests.get(path_data['cdn']):
                    buffer.append(c)

                _fs.write(file_path, buffer)
                logger.info('> > > Successfully wrote {}'.format(file_path))

            self[name] = {
                'cdn': path_data['cdn'],
                'uri': file_uri
            }


class CDNJs(object):
    """
    CDNJs.com parser
    """
    API_URL = 'https://api.cdnjs.com/libraries{query}'
    FILE_CDN = 'https://cdnjs.cloudflare.com/ajax/libs/{name}/{version}/{file}'

    @staticmethod
    def get_dir(cdn, version):
        """
        Returns subdirectory
        :param cdn:
        :return:
        """
        filename = cdn.split('/')[-1]
        return cdn.split(version)[-1].replace(filename, '').strip('/')

    def find(self, name, version=None):
        """
        Lads CDNJSObject
        :param name:
        :param version:
        :return CDNJsObject:
        """
        # Load base info
        realname = self._find_hit(name)

        # Check hits
        if realname is None:
            raise RepositoryNotFoundException('Repository {} was not found'.format(name))

        # Load version files
        return self._load_version(realname, version)

    def _find_hit(self, name):
        """
        Tries to find hits for selected repository
        :param str name:
        :return dict:
        """
        query = {
            'search': name
        }

        # Match library
        hits = requests.get(
            self.API_URL.format(query='?' + urlencode(query))
        ).json()['results']

        # Try to find exact matching
        matches = [(fuzz.ratio(x['name'].lower(), name.lower()), x) for x in hits]

        return sorted(matches, key=lambda x: x[0], reverse=True)[0][1]['name']

    def _load_version(self, name, version=None):
        """
        Loads files for selected version
        :param name:
        :param version:
        :return CDNJsObject:
        """
        # Load info about version
        response = requests.get(
            self.API_URL.format(query='/{}'.format(name))
        ).json()

        # Version to be saved
        version = version or response['version']

        # Create initial cdnjs object
        obj = CDNJsObject(
            name=response['name'],
            version=version,
            default=response['filename'],
            keywords=response['keywords']
        )

        # Get version assets
        for assets in response['assets']:
            if assets['version'] == version:
                obj.files = self._parse_assets(response['name'], assets)
                break
        if not obj.files and response['assets']:
            logger.error('{} - Invalid assets, loading fallback...'.format(name))
        if not obj.is_valid:
            return None

        return obj

    def _parse_assets(self, repository, assets):
        """
        Returns files
        :param repository:
        :param assets:
        :return:
        """
        result = {}

        for filename in assets['files']:
            result[self._file_name(filename)] = {
                'cdn': self._file_cdn(repository, assets['version'], filename),
                'uri': None
            }

        return result

    def _file_cdn(self, repository, version, fname):
        """
        Returns file cdn
        :param repository:
        :param version:
        :param fname:
        :return:
        """
        return self.FILE_CDN.format(
            name=repository,
            version=version,
            file=fname
        )

    def _file_name(self, fname):
        """
        Returns clean filename
        :param fname:
        :return:
        """
        return fname.split('/')[-1]


class CDNStorage(object):
    """
    CDN Storage
    """
    cache_file = Settings.get('CACHE_FILE', 'cache.json')

    def __init__(self):
        self.storage = CDNJs()

    @property
    def database(self):
        return self._load_db()

    def get(self, repository, filename):
        """
        Returns CDN or URI
        :param repository:
        :param filename:
        :return:
        """
        global _cached_db

        name, ver = self.parse_name(repository)

        logger.info('Searching for repository {} version {}'.format(name, ver))

        # Find repo
        repo = None
        for r in self.database:
            if r.matches(name, ver):
                repo = r
                break

        # If not local copy exists load it
        if repo is None:
            logger.info('> Repository not found. Trying to ask API CDNJS...')
            repo = self.storage.find(name, ver)
        if repo is None:
            logger.info('> CDNJS Do not know requested repository.')
            raise RepositoryNotFoundException('Repository {} was not found'.format(repository))
        else:
            logger.info('> CDNJS Responsed with the requested repository.')
            _cached_db.append(repo)

        # If we need local URI
        if Settings.get('USE_LOCAL'):
            repo.download()

        # Update database
        self._save_db()

        # Find file
        return repo[filename or repo.default]

    def _load_db(self):
        """
        Loads cdns from db
        :return CDNJsObject:
        """
        global _cached_db

        if _cached_db:
            return _cached_db

        cache_file = _fs.get_path(self.cache_file)

        if not _fs.exists(cache_file):
            return _cached_db

        f = _fs.read(cache_file)
        # Read db
        result = []
        try:
            content = json.loads(f)
            # Parse objects
            for name, info in content.items():
                for ver, data in info['releases'].items():
                    result.append(CDNJsObject(
                        name=name,
                        version=ver,
                        default=data['default'],
                        files=data['files'],
                        keywords=info['keywords']
                    ))
        except Exception as e:
            print(e)

        _cached_db = result
        return _cached_db

    def _save_db(self):
        """
        Saving cdns to db
        :return:
        """
        data = {}
        cache_file = _fs.get_path(self.cache_file)

        for cdn in self.database:
            if cdn.name not in data:
                data[cdn.name] = {
                    'releases': {},
                    'keywords': cdn.keywords
                }

            if cdn.version not in data[cdn.name]['releases']:
                data[cdn.name]['releases'][cdn.version] = cdn.dict

        if _fs.exists(cache_file):
            _fs.delete(cache_file)
        _fs.write(cache_file, json.dumps(data, indent=2))

    @staticmethod
    def parse_name(repository_name):
        """
        Parses repository name and version
        :param repository_name:
        :return tuple(str, str):
        """
        pair = repository_name.split('/')
        return pair[0], pair[1] if len(pair) > 1 else None
