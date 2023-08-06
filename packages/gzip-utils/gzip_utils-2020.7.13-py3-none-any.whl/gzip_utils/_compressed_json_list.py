#
#
#
import json

from gzip import GzipFile
from io import BytesIO
from typing import MutableSequence
from typing import Union

from ._exceptions import CompressionFull
from ._exceptions import SingleCompressionOnGoing


class CompressedJsonList:
    """
    Creates an json array of compressed json messages.

    [<compressed>, <compressed>, <compressed>]

    Arguments:
        max_compressed_size [int]: This is the max compression size needed for one batch.
    """

    def __init__(self, compression_limit: int) -> None:
        self._max_compressed_size: int = compression_limit
        self._uncompressed_size: int = 0
        self._compressed_size: int = 0

        self._single_compress_started = False

        self._byte_stream: BytesIO = None  # type: ignore
        self._gzip_stream: GzipFile = None  # type: ignore

        self._gzip_metadata_size = 20
        self._unzipped_chars = 1 + self._gzip_metadata_size
        self._data_written = 0

    def _get_max_compressed_size(self) -> int:
        """ Get the max compressed size """
        return self._max_compressed_size

    def _set_max_compressed_size(self, value: int) -> None:
        self._max_compressed_size = value

    compression_limit = property(_get_max_compressed_size, _set_max_compressed_size)

    @property
    def uncompressed_size(self) -> int:
        """ The size of the uncompressed data """
        return self._uncompressed_size

    @property
    def compressed_size(self) -> int:
        """ The size of the compression """
        return self._compressed_size

    @property
    def compression_ratio(self) -> float:
        """The compression ratio

        Returns:
            float: The ration of the compression
        """
        ratio = 0.0
        if self.uncompressed_size != 0:
            ratio = self.compressed_size / self.uncompressed_size * 100.0
        return ratio

    def get_data(self, before_maxed=False) -> bytes:
        """Get the compressed json array

        Args:
            before_maxed (bool, optional): Set to `True` if retriving data before reached max limit. Defaults to False.

        Returns:
            bytes: The compressed json array
        """
        if before_maxed:
            self._gzip_stream.write(b"]")

        compressed = self._byte_stream.getvalue()
        self._compressed_size = len(compressed)

        self._gzip_stream.close()
        self._single_compress_started = False
        return compressed

    def compress(self, data: Union[str, dict]) -> None:
        """
        Compress a single json object and adds it to the json array.

        Args:
            data (Union[str, dict]): The json string or python `dict`

        Raises:
            CompressionFull: When we have reached the max limit
        """
        if not self._single_compress_started:
            self._single_compress_started = True
            self._byte_stream = BytesIO()
            self._gzip_stream = GzipFile(mode="wb", fileobj=self._byte_stream)
            self._gzip_stream.write(b"[")

        if not self._compress(data):
            self._gzip_stream.write(b"]")
            raise CompressionFull()

    def get_compressed_json_list(self, json_data: MutableSequence[Union[str, dict]]) -> bytes:
        """Get a compressed list of json objects

        Args:
            data (MutableSequence[Union[str, dict]]): List of json string or python `dict` to compress

        Returns:
            bytearray: The array of compressed bytes
        """
        if self._single_compress_started:
            raise SingleCompressionOnGoing("Single compression started, cant compress a range now.")

        self._byte_stream = BytesIO()
        self._gzip_stream = GzipFile(mode="wb", fileobj=self._byte_stream)
        self._gzip_stream.write(b"[")

        for org_data in json_data:
            if self._compress(org_data):
                json_data.remove(org_data)

        self._gzip_stream.write(b"]")
        self._gzip_stream.close()
        compressed = self._byte_stream.getvalue()
        self._compressed_size = len(compressed)

        return compressed

    def _compress(self, org_data: Union[str, dict]) -> bool:
        if isinstance(org_data, dict):
            data = json.dumps(org_data)
        elif isinstance(org_data, str):
            data = org_data
        else:
            raise ValueError(f"We do not support type: {type(org_data)}")

        data_bytes = data.encode("utf-8")

        if not self._check_compression(data_bytes):
            return False

        if self._data_written > 0:
            self._gzip_stream.write(b",")  # This should be an array so add coma when mutiple messages
        self._gzip_stream.write(data_bytes)
        self._data_written += 1

        self._unzipped_chars += len(data_bytes)
        self._uncompressed_size += len(data_bytes)
        return True

    def _check_compression(self, data_bytes: bytes) -> bool:
        stream_size = self._gzip_stream.size  # type: ignore
        if (stream_size + len(data_bytes) + self._unzipped_chars) > self._max_compressed_size:
            self._gzip_stream.flush()
            self._unzipped_chars = 0 + self._gzip_metadata_size

        if (stream_size + len(data_bytes)) >= self._max_compressed_size and self._data_written > 0:
            return False

        return True
