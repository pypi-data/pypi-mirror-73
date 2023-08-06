#
#
#
import json

from gzip import GzipFile
from io import BytesIO
from typing import MutableSequence
from typing import Union


class CompressedJsonArray:
    """
    Compresses a `list` of json strings or dictionaries to an gziped compressed json array of json
    objects.

    Arguments:
        max_compressed_size [int]: This is the max compression size needed for one batch.
    """

    def __init__(self, max_compressed_size: int) -> None:
        self._max_compressed_size = max_compressed_size
        self._uncompressed_size: int = 0
        self._compressed_size: int = 0

    @property
    def max_compressed_size(self) -> int:
        return self._max_compressed_size

    @property
    def uncompressed_size(self) -> int:
        return self._uncompressed_size

    @property
    def compressed_size(self) -> int:
        return self._compressed_size

    @property
    def compression_ratio(self) -> float:
        ratio = 0.0
        if self.uncompressed_size != 0:
            ratio = self.compressed_size / self.uncompressed_size * 100.0
        return ratio

    def get_compressed_json_array(self, json_data: MutableSequence[Union[str, dict]]) -> bytes:
        """Get a compressed array of json objects

        Args:
            data (Union[List[str], List[dict]]): List of json string or python dictonaries to compress

        Returns:
            bytearray: The array of compressed bytes
        """
        compressed = None
        gzip_metadata_size = 20
        unzipped_chars = 1 + gzip_metadata_size

        byte_stream = BytesIO()
        gzip_stream = GzipFile(mode="wb", fileobj=byte_stream)

        gzip_stream.write(b"[")
        data_written = 0

        for org_data in json_data:
            if isinstance(org_data, dict):
                data = json.dumps(org_data)
            elif isinstance(org_data, str):
                data = org_data
            else:
                raise ValueError(f"We do not support type: {type(org_data)}")

            bytes = data.encode("utf-8")

            if (gzip_stream.size + len(bytes) + unzipped_chars) > self._max_compressed_size:  # type: ignore
                gzip_stream.flush()
                unzipped_chars = 0 + gzip_metadata_size

            if (gzip_stream.size + len(bytes)) >= self._max_compressed_size and data_written > 0:  # type: ignore
                break

            json_data.remove(org_data)
            if data_written > 0:
                gzip_stream.write(b",")
            gzip_stream.write(bytes)
            data_written += 1

            unzipped_chars += len(bytes)
            self._uncompressed_size += len(bytes)

        gzip_stream.write(b"]")
        gzip_stream.close()
        compressed = byte_stream.getvalue()
        self._compressed_size = len(byte_stream.getvalue())

        return compressed
