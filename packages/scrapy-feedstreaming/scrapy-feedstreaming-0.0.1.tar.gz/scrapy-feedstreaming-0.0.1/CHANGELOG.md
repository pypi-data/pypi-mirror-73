# Changelog

Scrapy live Streaming data. `scrapy.extensions.feedexport.FeedExporter` fork to export item during scraping. See 
[https://medium.com/@alex_ber/scrapy-streaming-data-cdf97434dc15]

All notable changes to this project will be documented in this file.

\#https://pypi.org/manage/project/scrapy-feedstreaming/releases/

## [Unrelased]


## [0.0.1] - 12/07/2020

### Added
* Buffering was added to `item_scraped()`.
* S3FeedStorage: you can specify `ACL` as query part of URI.
* S3FeedStorage: support of `region` is added. 
* FEEDS: `slot_key_param`: New (not available in Scrapy itself) specify (global) function which takes item and spider as parameter 
and `slot_key`. Given the item that is passed through the pipeline to what URI you want to send it.
Fall back to noop method — method that does nothing.
* FEEDS: `buff_capacity`: New (not available in Scrapy itself) — after what amount of item you want to export them. 
The fall back value is 1. 
* `_FeedSlot` instances are created from your settings. They are created per supplied URI. 
Some extra (compare to Scraping) information is stored, namely:
- `uri_template` — it is available through public API get_slots() method, see below.
- `spider_name` — is used in public API get_slots() method to restrict returned slots for requested spider.
- `buff_capacity` —buffer’s capacity, if the number of item exceed this number the buffer is flushed
- `buff` — buffer where all items pending export are stored.
* `FeedExported` there is 1 extra public method 
- `get_slots()` — this method is used to get feed slot’s information (see implementation note above). It is populated from the settings. For example, you can retrieve to either URI you will export the items.
Note:
1. `slot_key` is slot identifier as described above. If you have only 1 URI you can supply None for this value.
2. You can retrieve feed slot’s information only from your spider.
3. It has optional `force_create=True` parameter. 
If you’re calling this method early in the Scrapy life-cycle feed slot’s information may be not yet created. 
In this case, the default behavior is to create this information and return it for you. 
If `force_create=False` is supplied you will receive an empty collection of feed slot’s information.
* On `S3FeedStorage` there couple of public methods:

- `botocore_session`
- `botocore_client`
- `botocore_base_kwargs` — dict of minimal parameters for `botocore_client.put_object()` method as supplied in settings.
- `botocore_kwargs` — dict of all supplied parameters `for botocore_client.put_object()` method as supplied in settings. 
For example, if supplied, it will contain `ACL` parameter while `botocore_base_kwargs` will not contain it.


### Changed
* You can have multiple URI for exports.
* Logic of sending the item was moved from the `close_spider()` to `item_scraped()`.
* back-port Fix missing `storage.store()` calls in `FeedExporter.close_spider()` [https://github.com/scrapy/scrapy/pull/4626]
* back-port Fix duplicated feed logs [https://github.com/scrapy/scrapy/pull/4629]

 
### Removed
* removed deprecated: fallback to `boto` library if `botocore` is not found
* removed deprecated: implicit retrieval of settings from the project — settings is passed explicitly now


<!--
### Added 
### Changed
### Removed
-->
