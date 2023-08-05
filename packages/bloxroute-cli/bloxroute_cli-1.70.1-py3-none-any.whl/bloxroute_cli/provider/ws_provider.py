from typing import Optional, List, Union, Any, Dict, Tuple


from bxgateway.rpc.provider.abstract_ws_provider import AbstractWsProvider
from bxcommon.rpc.bx_json_rpc_request import BxJsonRpcRequest
from bxcommon.rpc.json_rpc_response import JsonRpcResponse
from bxcommon.rpc.rpc_errors import RpcError
from bxcommon.rpc.rpc_request_type import RpcRequestType


class WsProvider(AbstractWsProvider):
    """
    Provider that connects to bxgateway's websocket RPC endpoint.

    Usage:

    (with context manager, recommended)
    ```
    ws_uri = "ws://127.0.0.1:28333"
    async with WsProvider(ws_uri) as ws:
        subscription_id = await ws.subscribe("newTxs")
        while True:
            next_notification = await ws.get_next_subscription_notification_by_id(subscription_id)
            print(next_notification)  # or process it generally
    ```

    (without context manager)
    ```
    ws_uri = "ws://127.0.0.1:28333"
    try:
        ws = await WsProvider(ws_uri)
        subscription_id = await ws.subscribe("newTxs")
        while True:
            next_notification = await ws.get_next_subscription_notification_by_id(subscription_id)
            print(next_notification)  # or process it generally
    except:
        await ws.close()
    ```

    (callback interface)
    ```
    ws_uri = "ws://127.0.0.1:28333"
    ws = WsProvider(ws_uri)
    await ws.initialize()

    def process(subscription_message):
        print(subscription_message)

    ws.subscribe_with_callback(process, "newTxs")

    while True:
        await asyncio.sleep(0)  # otherwise program would exit
    ```
    """
    async def call_bx(
        self,
        method: RpcRequestType,
        params: Union[List[Any], Dict[Any, Any], None],
        request_id: Optional[str] = None
    ) -> JsonRpcResponse:
        if request_id is None:
            request_id = str(self.current_request_id)
            self.current_request_id += 1

        return await self.call(
            BxJsonRpcRequest(request_id, method, params)
        )

    async def subscribe(self, channel: str, fields: Optional[List[str]] = None) -> str:
        response = await self.call_bx(
            RpcRequestType.SUBSCRIBE, [channel, {"include": fields}]
        )
        subscription_id = response.result
        assert isinstance(subscription_id, str)
        self.subscription_manager.register_subscription(subscription_id)
        return subscription_id

    async def unsubscribe(self, subscription_id: str) -> Tuple[bool, Optional[RpcError]]:
        response = await self.call_bx(RpcRequestType.UNSUBSCRIBE, [subscription_id])
        if response.result is not None:
            self.subscription_manager.unregister_subscription(subscription_id)
            return True, None
        else:
            return False, response.error
