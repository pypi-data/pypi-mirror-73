#
#
#


class GzipUtilsError(Exception):
    pass


class CompressionFull(GzipUtilsError):
    pass


class SingleCompressionOnGoing(GzipUtilsError):
    pass
