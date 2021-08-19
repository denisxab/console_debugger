__all__ = ["DataForSocket",
           "DataFlag",
           "InitTitleNameFlag", ]

from dataclasses import dataclass
from pickle import dumps, loads
from typing import List, Tuple

DataFlag: int = 0
InitTitleNameFlag: int = 1
MyKey = "TRUE_CONNECT"


@dataclass
class DataForSocket:

    # SERVER
    @staticmethod
    def true_connect_server() -> bytes:
        return MyKey.encode("ascii")

    @staticmethod
    def decode_obj_server(b_data: bytes) -> Tuple[int, int, List[str]]:
        """
        @param b_data:  DataForSocket.to_data_for_socket_bytes()
        @return: флаг(id, данные)
        """
        return loads(b_data)

    # CLIENT
    @staticmethod
    def is_connect_client(data_validate: bytes) -> bool:
        return True if data_validate.decode("ascii") == MyKey else False

    @staticmethod
    def to_init_title_name_bytes(init_title_name: List[str]) -> bytes:
        return dumps(
            (InitTitleNameFlag, -1, init_title_name),
            protocol=3)

    @staticmethod
    def to_data_for_socket_bytes(id_: int, text_send: List[str]) -> bytes:
        return dumps(
            (DataFlag, id_, text_send),
            protocol=3)
