import typing as t
import typing_extensions as te
from collections import OrderedDict
import datetime as dt
from decimal import Decimal

from fixtrate.message import FixMessage
from .types import FixTag as FT, TYPE_MAP
from .validate import validate, convert, cast as _cast


class OrderStatusRequest(FixMessage):

    _msg_type = "H"

    _fields = OrderedDict({
        FT.OrderID: False,
        FT.ClOrdID: True,
        FT.ClientID: False,
        FT.Account: False,
        FT.ExecBroker: False,
        FT.Symbol: True,
        FT.SymbolSfx: False,
        FT.SecurityID: False,
        FT.IDSource: False,
        FT.SecurityType: False,
        FT.MaturityMonthYear: False,
        FT.MaturityDay: False,
        FT.PutOrCall: False,
        FT.StrikePrice: False,
        FT.OptAttribute: False,
        FT.ContractMultiplier: False,
        FT.CouponRate: False,
        FT.SecurityExchange: False,
        FT.Issuer: False,
        FT.EncodedIssuerLen: False,
        FT.EncodedIssuer: False,
        FT.SecurityDesc: False,
        FT.EncodedSecurityDescLen: False,
        FT.EncodedSecurityDesc: False,
        FT.Side: True,
    })

    def __init__(
        self,
        cl_ord_id: str,
        symbol: str,
        side: str,
    ) -> None:
        super().__init__()
        self.append_pair(35, self._msg_type)
        self.append_pair(
            FT.ClOrdID,
            convert("STRING", cl_ord_id),
        )
        self.append_pair(
            FT.Symbol,
            convert("STRING", symbol),
        )
        self.append_pair(
            FT.Side,
            convert("CHAR", side),
        )

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.ClOrdID]) -> str:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.Symbol]) -> str:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.Side]) -> str:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.OrderID]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.ClientID]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.Account]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.ExecBroker]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.SymbolSfx]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.SecurityID]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.IDSource]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.SecurityType]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.MaturityMonthYear]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.MaturityDay]) -> t.Optional[int]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.PutOrCall]) -> t.Optional[int]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.StrikePrice]) -> t.Optional[Decimal]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.OptAttribute]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.ContractMultiplier]) -> t.Optional[float]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.CouponRate]) -> t.Optional[float]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.SecurityExchange]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.Issuer]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.EncodedIssuerLen]) -> t.Optional[int]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.EncodedIssuer]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.SecurityDesc]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.EncodedSecurityDescLen]) -> t.Optional[int]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.EncodedSecurityDesc]) -> t.Optional[str]:
        ...

    def get(self, tag: FT):  # NOQA
        is_required = self._fields[tag]
        val = self.get_raw(tag)
        if val is None:
            if is_required:
                raise ValueError
            return None
        return validate(TYPE_MAP[tag], val)

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.OrderID],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.ClOrdID],
        val: str,
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.ClientID],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.Account],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.ExecBroker],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.Symbol],
        val: str,
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.SymbolSfx],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.SecurityID],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.IDSource],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.SecurityType],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.MaturityMonthYear],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.MaturityDay],
        val: t.Optional[int],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.PutOrCall],
        val: t.Optional[int],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.StrikePrice],
        val: t.Optional[Decimal],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.OptAttribute],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.ContractMultiplier],
        val: t.Optional[float],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.CouponRate],
        val: t.Optional[float],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.SecurityExchange],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.Issuer],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.EncodedIssuerLen],
        val: t.Optional[int],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.EncodedIssuer],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.SecurityDesc],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.EncodedSecurityDescLen],
        val: t.Optional[int],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.EncodedSecurityDesc],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.Side],
        val: str,
    ) -> None:
        ...

    def append(self, tag: FT, val: t.Any):  # NOQA
        if tag is FT.OrderID:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.ClOrdID:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.ClientID:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.Account:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.ExecBroker:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.Symbol:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.SymbolSfx:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.SecurityID:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.IDSource:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.SecurityType:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.MaturityMonthYear:
            assert isinstance(val, str)
            converted = convert("MONTHYEAR", val)
        elif tag is FT.MaturityDay:
            assert isinstance(val, int)
            converted = convert("DAYOFMONTH", val)
        elif tag is FT.PutOrCall:
            assert isinstance(val, int)
            converted = convert("INT", val)
        elif tag is FT.StrikePrice:
            assert isinstance(val, Decimal)
            converted = convert("PRICE", val)
        elif tag is FT.OptAttribute:
            assert isinstance(val, str)
            converted = convert("CHAR", val)
        elif tag is FT.ContractMultiplier:
            assert isinstance(val, float)
            converted = convert("FLOAT", val)
        elif tag is FT.CouponRate:
            assert isinstance(val, float)
            converted = convert("FLOAT", val)
        elif tag is FT.SecurityExchange:
            assert isinstance(val, str)
            converted = convert("EXCHANGE", val)
        elif tag is FT.Issuer:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.EncodedIssuerLen:
            assert isinstance(val, int)
            converted = convert("LENGTH", val)
        elif tag is FT.EncodedIssuer:
            assert isinstance(val, str)
            converted = convert("DATA", val)
        elif tag is FT.SecurityDesc:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.EncodedSecurityDescLen:
            assert isinstance(val, int)
            converted = convert("LENGTH", val)
        elif tag is FT.EncodedSecurityDesc:
            assert isinstance(val, str)
            converted = convert("DATA", val)
        elif tag is FT.Side:
            assert isinstance(val, str)
            converted = convert("CHAR", val)
        else:
            raise ValueError(f"{tag} is not a valid FIX tag")
        self.append_pair(tag, converted)

    @classmethod
    def cast(cls, msg: FixMessage) -> "OrderStatusRequest":
        return _cast(cls, msg)