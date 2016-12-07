# http://qthttp.apple.com.edgesuite.net/1010qwoeiuryfg/sl.m3u8
# http://devimages.apple.com/iphone/samples/bipbop/bipbopall.m3u8
# http://devimages.apple.com/iphone/samples/bipbop/gear1/prog_index.m3u8
# http://playertest.longtailvideo.com/adaptive/oceans_aes/oceans_aes.m3u8 (AES encrypted)
# http://playertest.longtailvideo.com/adaptive/captions/playlist.m3u8 (HLS stream with CEA-608 captions)
# http://playertest.longtailvideo.com/adaptive/wowzaid3/playlist.m3u8 (with metadata)
# http://content.jwplatform.com/manifests/vM7nH0Kl.m3u8
# http://cdn-fms.rbs.com.br/hls-vod/sample1_1500kbps.f4v.m3u8
# http://cdn-fms.rbs.com.br/vod/hls_sample1_manifest.m3u8
# http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch1/appleman.m3u8 (LIVE TV)
# http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch2/appleman.m3u8 (LIVE TV)
# http://vevoplaylist-live.hls.adaptive.level3.net/vevo/ch3/appleman.m3u8 (LIVE TV)
# http://www.nacentapps.com/m3u8/index.m3u8 (VOD)
# http://srv6.zoeweb.tv:1935/z330-live/stream/playlist.m3u8 (LIVE TV)
# http://content.jwplatform.com/manifests/vM7nH0Kl.m3u8 ( link protection, video not encrypted )
# http://sample.vodobox.net/skate_phantom_flex_4k/skate_phantom_flex_4k.m3u8 (4K HLS Video stream)%

# uwsgi log:
# pid -> the pid of the worker managing the request
# app -> the id (it is a integer, starting from 0) of the app, it makes
# sense when multiple apps are hosted in the same instance. It is -1 when no
# app managed the request (like when serving static files) or when the 'app'
# concept does not apply (like with php or cgi's)
# req: N/M -> N is the number of managed requests by the current worker for
# the specific app, M is the grand total (sum of all requests of all
# workers)

# then you have REMOTE_ADDR followd by the (optional) REMOTE_USER (very
# similar to apache)

# vars are the number of CGI vars in the request, and their size (from the
# uwsgi protocol point of view). The size is never higher than the
# --buffer-size (higher requests are discarded)

# The time of the request follows

# Then you have REQUEST_METHOD + REQUEST_URI

# Then the response size and the time required for generating it

# "via" is the techology used to send the response, currently can be
# sendfile, routing or offloading.

# The response status follows, as well as the number of response headers.

# "core" is the low-level concept for uWSGI concurrency context in a process
# (can be a thread or a greenlet or a fiber or a goroutine and so on...)
# while switches count is incremented whenever an app "yield" its status
# (this has various meanings based on the lower concurrency model used)

