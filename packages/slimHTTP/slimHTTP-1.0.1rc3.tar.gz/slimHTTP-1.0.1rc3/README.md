# <img src="docs/_static/slimHTTP.png" alt="drawing" width="200"/>
A simple, minimal and flexible HTTP server.<br>
Supports modules for parsing WebSocket¹ traffic as well as REST api routes.

 * slimHTTP [documentation](https://slimhttp.readthedocs.io/en/master)
 * slimHTTP [discord](https://discord.gg/CMjZbwR) server

## Supports

 * REST routes *(`@http.route('/some/endpoint')`)*
 * websockets if `@http.on_upgrade` is defined using [spiderWeb](https://github.com/Torxed/spiderWeb) ¹
 * Static file emulation with `@http.route('/example.html')`
 * vhosts
 * ssl/tls
 * No threading or threads used *(fully relies on `epoll()` (`select()` on Windows))*
 * flexible configuration for webroots etc via `@http.configuration`

## Minimal example

```py
import slimhttpd

http = slimhttpd.host(slimhttpd.HTTP)

while 1:
	for event, *event_data in http.poll():
		pass
```

The only important thing is that `.poll()` has to be called in order to process the events.

## Footnote

It's not pretty down here. But it'll do in a pinch.
