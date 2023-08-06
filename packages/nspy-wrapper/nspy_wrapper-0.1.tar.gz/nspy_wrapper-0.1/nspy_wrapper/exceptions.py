class APIFailure(Warning):
    pass


class MalformedXML(APIFailure):
    pass


class MissingHeaders(APIFailure):
    pass


class FailedRequest(APIFailure):
    pass
