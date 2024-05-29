class DnsRecord(object):
    """
    The base class for a DNS record
    Parse a record according to its type
    """

    def __init__(self, r, att):
        self._attributes = att
        self.type = r.rdtype.name
        for a in self._attributes:
            self.__setattr__(a, str(r.__getattribute__(a)))

    def json(self):
        out = dict(type=self.type)
        for a in self._attributes:
            out[a] = self.__getattribute__(a)

        return out


class DnsRecordA(DnsRecord):
    def __init__(self, r):
        super().__init__(r, ["address"])


class DnsRecordNS(DnsRecord):
    def __init__(self, r):
        super().__init__(r, ["target"])


class DnsRecordSOA(DnsRecord):
    def __init__(self, r):
        super().__init__(
            r, ["expire", "minimum", "mname", "refresh", "retry", "rname", "serial"]
        )


class DnsRecordMX(DnsRecord):
    def __init__(self, r):
        super().__init__(r, ["exchange", "preference"])


class DnsRecordTXT(DnsRecord):
    def __init__(self, r):
        super().__init__(r, ["strings"])


class DnsRecordAAAA(DnsRecord):
    def __init__(self, r):
        super().__init__(r, ["address"])


class DnsRecordOther(DnsRecord):
    def __init__(self, r):
        super().__init__(r, [])
