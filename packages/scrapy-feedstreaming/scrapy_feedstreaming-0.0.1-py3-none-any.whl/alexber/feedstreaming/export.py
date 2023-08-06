from types import FunctionType
import logging
import warnings
from datetime import datetime
from collections import deque
from scrapy.extensions.feedexport import BlockingFeedStorage as _BlockingFeedStorage, FeedExporter as _FeedExporter, \
    feed_complete_default_values_from_settings as _feed_complete_default_values_from_settings, \
    signals #signals is used
from six.moves.urllib.parse import urlparse
from six.moves.urllib.parse import parse_qs
from scrapy.exceptions import NotConfigured, ScrapyDeprecationWarning
from scrapy.utils.misc import load_object
from twisted.internet import defer
from scrapy.utils.log import failure_to_exc_info

logger = logging.getLogger(__name__)

class BaseS3FeedStorage(_BlockingFeedStorage):

    @classmethod
    def is_optional_dependency_exists(cls):
        raise NotImplementedError

    def __init__(self, uri, settings):
        self.is_optional_dependency_exists()

        access_key = settings.get('AWS_ACCESS_KEY_ID', None)
        secret_key = settings.get('AWS_SECRET_ACCESS_KEY', None)
        region_name = settings.get('FEED_STORAGE_S3_REGION', None)
        ACL = settings.get('FEED_STORAGE_S3_ACL', None)

        u = urlparse(uri)
        d1 = parse_qs(u.query)
        locations = d1.get('location', None)
        location = next(iter(locations or []), None)

        acls = d1.get('acl', None)
        acl = next(iter(acls or []), None)

        self.bucketname = u.hostname
        self.access_key = u.username or access_key
        self.secret_key = u.password or secret_key
        self.region_name = region_name or location

        self.keyname = u.path[1:]  # remove first "/"
        self.acl = ACL or acl
        self._init_s3_related(uri, settings)


    def _init_s3_related(self, uri, settings):
        """This API is unstabel anc can change withou warning."""
        raise NotImplementedError

    @classmethod
    def from_crawler(cls, crawler, uri):
        return cls.from_settings(crawler.settings, uri)

    @classmethod
    #this method is called from FeedExporter constructor
    #(_storage_supported())
    def from_settings(cls, settings, uri):
        return cls(uri, settings)



    def _store_in_thread(self, file):
        raise NotImplementedError


class S3FeedStorage(BaseS3FeedStorage):

    @classmethod
    def is_optional_dependency_exists(cls):
        try:
            import botocore
            return True
        except ImportError:
            raise NotConfigured('missing botocore library')

    def _init_s3_related(self, uri, settings):
        import botocore.session
        self._botocore_session = botocore.session.get_session()
        self._botocore_session.set_config_variable('region', self.region_name)

        self._botocore_client = self.botocore_session.create_client('s3',
                                               aws_access_key_id=self.access_key,
                                               aws_secret_access_key=self.secret_key,
                                               #region_name=self.region_name
                                               )


    @property
    def botocore_session(self):
        """
        Public API
        """
        return self._botocore_session


    @property
    def botocore_client(self):
        """
        Public API
        """
        return self._botocore_client

    def _store_in_thread(self, file):
        file.seek(0)

        d = self.botocore_kwargs
        d= {**d, 'Body':file}
        self.botocore_client.put_object(**d)

    @property
    def botocore_kwargs(self):
        """
        Public API
        """
        d={'Bucket': self.bucketname, 'Key': self.keyname, 'ACL': self.acl}
        #filter out None values
        d=dict(filter(lambda x: x[1], d.items()))
        return d

    @property
    def botocore_base_kwargs(self):    #required
        """
        Public API
        """
        d={'Bucket': self.bucketname, 'Key': self.keyname}
        return d


class _FeedSlot(object):
    def __init__(self, file, exporter, storage, uri, format, store_empty, uri_template, buff_capacity, spider_name):
        self.file = file
        self.exporter = exporter
        self.storage = storage
        # feed params
        self.uri = uri
        self.format = format
        self.store_empty = store_empty
        # flags
        self.itemcount = 0
        self._exporting = False

        self.uri_template = uri_template
        self.buff_capacity = buff_capacity
        self.buff = deque(maxlen=buff_capacity)
        self.spider_name = spider_name

    def start_exporting(self):
        if not self._exporting:
            self.exporter.start_exporting()
            self._exporting = True

    def finish_exporting(self):
        if self._exporting:
            self.exporter.finish_exporting()
            self._exporting = False



class FeedExporter(object):

    def feed_complete_default_values_from_settings(self, feed, settings):
        out = _feed_complete_default_values_from_settings(feed, settings)
        out.setdefault("slot_key", None)
        out.setdefault("slot_key_param", None)
        out.setdefault("buff_capacity", 1)

        return out

    def __init__(self, crawler):
        settings = crawler.settings
        self.settings = settings
        self.feeds = {}
        self.slots = {}
        self.urids = {}
        self._slots_key_fun= {}

        if not self.settings['FEEDS'] and not self.settings['FEED_URI']:
            raise NotConfigured

        # Begin: Backward compatibility for FEED_URI and FEED_FORMAT settings
        if self.settings['FEED_URI']:
            warnings.warn(
                'The `FEED_URI` and `FEED_FORMAT` settings have been deprecated in favor of '
                'the `FEEDS` setting. Please see the `FEEDS` setting docs for more details',
                category=ScrapyDeprecationWarning, stacklevel=2,
            )
            uri = str(self.settings['FEED_URI'])  # handle pathlib.Path objects
            feed = {'format': self.settings.get('FEED_FORMAT', 'jsonlines')}
            self.feeds[uri] = self.feed_complete_default_values_from_settings(feed, self.settings)
        # End: Backward compatibility for FEED_URI and FEED_FORMAT settings

        # 'FEEDS' setting takes precedence over 'FEED_URI'
        for uri, feed in self.settings.getdict('FEEDS').items():
            uri = str(uri)  # handle pathlib.Path objects
            self.feeds[uri] = self.feed_complete_default_values_from_settings(feed, self.settings)

        self.storages = self._load_components('FEED_STORAGES')
        self.exporters = self._load_components('FEED_EXPORTERS')
        for uri, feed in self.feeds.items():
            self.urids[feed['slot_key']] = uri

            if not self._storage_supported(uri):
                raise NotConfigured
            if not self._exporter_supported(feed['format']):
                raise NotConfigured


    # convert bound method to regular function in order to pass cls as is
    from_crawler = FunctionType(_FeedExporter.from_crawler.__code__, globals())
    from_crawler = classmethod(from_crawler)


    def _create_slot(self, feed, spider):
        uri_template = self.urids[feed['slot_key']]
        uri = uri_template % self._get_uri_params(spider, feed['uri_params'])
        storage = self._get_storage(uri)
        file = storage.open(spider)
        exporter = self._get_exporter(
            file=file,
            format=feed['format'],
            fields_to_export=feed['fields'],
            encoding=feed['encoding'],
            indent=feed['indent'],
        )

        slot = _FeedSlot(file, exporter, storage, uri, feed['format'], feed['store_empty'],
                         uri_template, feed['buff_capacity'], spider.name)

        if slot.store_empty:
            slot.start_exporting()

        return slot


    def open_spider(self, spider):
        for _, feed in self.feeds.items():
            slot = self._create_slot(feed, spider)
            slot_key = feed['slot_key']
            self.slots.setdefault(slot_key, []).append(slot)

            slots_key_fun = feed['slot_key_param']
            slots_key_fun_key = spider.name
            self._slots_key_fun[slots_key_fun_key] = load_object(slots_key_fun) if slots_key_fun else lambda x, y: None


    def close_spider(self, spider):
        for uri, feed in self.feeds.items():
            slot_key = feed['slot_key']

            for slot in self.slots[slot_key]:
                slot.buff_capacity = len(slot.buff)
                slot.itemcount = 0
                buff = [*slot.buff]
                slot.buff.clear()
                for item in buff:
                    self.item_scraped(item, spider)


    def _replace(self, lst, old, new):
        for idx, item in enumerate(lst):
            if item==old:
                lst[idx] = new

    def get_slots(self, slot_key, spider, force_create=True):
        """
        Public API
        """
        spider_name = spider.name

        slots = self.slots.get(slot_key, [])
        ret = [slot for slot in slots if slot.spider_name == spider_name]

        if not ret and force_create:
            ret = []
            feed = None
            for l_feed in self.feeds.values():
                if l_feed['slot_key']==slot_key:
                    feed = l_feed
            if feed is not None:
                slot = self._create_slot(feed, spider)
                ret = [slot]

        return ret


    def item_scraped(self, item, spider):
        slots_key_fun_key = spider.name
        slots_key_fun = self._slots_key_fun[slots_key_fun_key]
        slot_key = slots_key_fun(item, spider)

        for slot in self.slots[slot_key]:

            slot.start_exporting()
            #slot.exporter.export_item(item)
            slot.buff.append(item)
            slot.itemcount += 1

            if len(slot.buff) < slot.buff_capacity:
                return

            deferred_list = []

            if not slot.itemcount and not slot.store_empty:
                # We need to call slot.storage.store nonetheless to get the file
                # properly closed.
                d = defer.maybeDeferred(slot.storage.store, slot.file)
                deferred_list.append(d)
                continue


            for export_item in slot.buff:
                 slot.exporter.export_item(export_item)


            slot.finish_exporting()
            slot.buff.clear()

            logfmt = "%s %%(format)s feed (%%(itemcount)d items) in: %%(uri)s"
            log_args = {'format': slot.format,
                        'itemcount': slot.itemcount,
                        'uri': slot.uri}
            d = defer.maybeDeferred(slot.storage.store, slot.file)
            # Use `largs=log_args` to copy log_args into function's scope
            # instead of using `log_args` from the outer scope
            d.addCallback(
                lambda _, largs=log_args: logger.info(
                    logfmt % "Stored", largs, extra={'spider': spider}
                )
            )
            d.addErrback(
                lambda f, largs=log_args: logger.error(
                    logfmt % "Error storing", largs,
                    exc_info=failure_to_exc_info(f), extra={'spider': spider}
                )
            )
            deferred_list.append(d)

            feed = self.feeds[slot.uri_template]
            new_slot= self._create_slot(feed, spider)

            lst = self.slots[slot_key]
            self._replace(lst, slot, new_slot)

            return defer.DeferredList(deferred_list) if deferred_list else None

    _load_components =_FeedExporter._load_components
    _exporter_supported = _FeedExporter._exporter_supported
    _storage_supported  = _FeedExporter._storage_supported
    _get_instance = _FeedExporter._get_instance
    _get_exporter = _FeedExporter._get_exporter
    _get_storage = _FeedExporter._get_storage
    #_get_uri_params = _FeedExporter._get_uri_params

    def _get_uri_params(self, spider, uri_params):
        params = {}
        for k in dir(spider):
            params[k] = getattr(spider, k)
        ts = datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '-')
        params['time'] = ts
        uripar_function = load_object(uri_params) if uri_params else lambda x, y: None
        uripar_function(params, spider)
        return params

