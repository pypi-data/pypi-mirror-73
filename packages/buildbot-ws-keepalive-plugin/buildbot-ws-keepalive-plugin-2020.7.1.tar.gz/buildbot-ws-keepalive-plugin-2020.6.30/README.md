# README

Plugin sends keepalive messages on websocket to avoid a disconnect due to server timeouts.

## How to use plugin?

1. Install it
2. Configure plugin:
    ```python
        c['www'] = dict(
            ...
            plugins=dict(
                ...
                ws_keepalive_plugin={}
            )
        )
    ```
3. Reconfigure BuildBot

___

Supported BuildBot version: >= 2
