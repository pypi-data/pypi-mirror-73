import typing as t
import typing_extensions as te
from collections import OrderedDict
import datetime as dt
from decimal import Decimal

from fixtrate.message import FixMessage
from .types import FixTag as FT, TYPE_MAP
from .validate import validate, convert, cast as _cast


class Quote(FixMessage):

    _msg_type = "S"

    _fields = OrderedDict({
        FT.QuoteReqID: False,
        FT.QuoteID: True,
        FT.QuoteResponseLevel: False,
        FT.TradingSessionID: False,
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
        FT.BidPx: False,
        FT.OfferPx: False,
        FT.BidSize: False,
        FT.OfferSize: False,
        FT.ValidUntilTime: False,
        FT.BidSpotRate: False,
        FT.OfferSpotRate: False,
        FT.BidForwardPoints: False,
        FT.OfferForwardPoints: False,
        FT.TransactTime: False,
        FT.FutSettDate: False,
        FT.OrdType: False,
        FT.FutSettDate2: False,
        FT.OrderQty2: False,
        FT.Currency: False,
    })

    def __init__(
        self,
        quote_id: str,
        symbol: str,
    ) -> None:
        super().__init__()
        self.append_pair(35, self._msg_type)
        self.append_pair(
            FT.QuoteID,
            convert("STRING", quote_id),
        )
        self.append_pair(
            FT.Symbol,
            convert("STRING", symbol),
        )

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.QuoteID]) -> str:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.Symbol]) -> str:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.QuoteReqID]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.QuoteResponseLevel]) -> t.Optional[int]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.TradingSessionID]) -> t.Optional[str]:
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

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.BidPx]) -> t.Optional[Decimal]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.OfferPx]) -> t.Optional[Decimal]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.BidSize]) -> t.Optional[Decimal]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.OfferSize]) -> t.Optional[Decimal]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.ValidUntilTime]) -> t.Optional[dt.datetime]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.BidSpotRate]) -> t.Optional[Decimal]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.OfferSpotRate]) -> t.Optional[Decimal]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.BidForwardPoints]) -> t.Optional[Decimal]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.OfferForwardPoints]) -> t.Optional[Decimal]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.TransactTime]) -> t.Optional[dt.datetime]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.FutSettDate]) -> t.Optional[dt.date]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.OrdType]) -> t.Optional[str]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.FutSettDate2]) -> t.Optional[dt.date]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.OrderQty2]) -> t.Optional[Decimal]:
        ...

    @t.overload  # NOQA
    def get(self, tag: te.Literal[FT.Currency]) -> t.Optional[str]:
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
        tag: te.Literal[FT.QuoteReqID],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.QuoteID],
        val: str,
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.QuoteResponseLevel],
        val: t.Optional[int],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.TradingSessionID],
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
        tag: te.Literal[FT.BidPx],
        val: t.Optional[Decimal],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.OfferPx],
        val: t.Optional[Decimal],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.BidSize],
        val: t.Optional[Decimal],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.OfferSize],
        val: t.Optional[Decimal],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.ValidUntilTime],
        val: t.Optional[dt.datetime],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.BidSpotRate],
        val: t.Optional[Decimal],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.OfferSpotRate],
        val: t.Optional[Decimal],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.BidForwardPoints],
        val: t.Optional[Decimal],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.OfferForwardPoints],
        val: t.Optional[Decimal],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.TransactTime],
        val: t.Optional[dt.datetime],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.FutSettDate],
        val: t.Optional[dt.date],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.OrdType],
        val: t.Optional[str],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.FutSettDate2],
        val: t.Optional[dt.date],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.OrderQty2],
        val: t.Optional[Decimal],
    ) -> None:
        ...

    @t.overload  # NOQA
    def append(
        self,
        tag: te.Literal[FT.Currency],
        val: t.Optional[str],
    ) -> None:
        ...

    def append(self, tag: FT, val: t.Any):  # NOQA
        if tag is FT.QuoteReqID:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.QuoteID:
            assert isinstance(val, str)
            converted = convert("STRING", val)
        elif tag is FT.QuoteResponseLevel:
            assert isinstance(val, int)
            converted = convert("INT", val)
        elif tag is FT.TradingSessionID:
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
        elif tag is FT.BidPx:
            assert isinstance(val, Decimal)
            converted = convert("PRICE", val)
        elif tag is FT.OfferPx:
            assert isinstance(val, Decimal)
            converted = convert("PRICE", val)
        elif tag is FT.BidSize:
            assert isinstance(val, Decimal)
            converted = convert("QTY", val)
        elif tag is FT.OfferSize:
            assert isinstance(val, Decimal)
            converted = convert("QTY", val)
        elif tag is FT.ValidUntilTime:
            assert isinstance(val, dt.datetime)
            converted = convert("UTCTIMESTAMP", val)
        elif tag is FT.BidSpotRate:
            assert isinstance(val, Decimal)
            converted = convert("PRICE", val)
        elif tag is FT.OfferSpotRate:
            assert isinstance(val, Decimal)
            converted = convert("PRICE", val)
        elif tag is FT.BidForwardPoints:
            assert isinstance(val, Decimal)
            converted = convert("PRICEOFFSET", val)
        elif tag is FT.OfferForwardPoints:
            assert isinstance(val, Decimal)
            converted = convert("PRICEOFFSET", val)
        elif tag is FT.TransactTime:
            assert isinstance(val, dt.datetime)
            converted = convert("UTCTIMESTAMP", val)
        elif tag is FT.FutSettDate:
            assert isinstance(val, dt.date)
            converted = convert("LOCALMKTDATE", val)
        elif tag is FT.OrdType:
            assert isinstance(val, str)
            converted = convert("CHAR", val)
        elif tag is FT.FutSettDate2:
            assert isinstance(val, dt.date)
            converted = convert("LOCALMKTDATE", val)
        elif tag is FT.OrderQty2:
            assert isinstance(val, Decimal)
            converted = convert("QTY", val)
        elif tag is FT.Currency:
            assert isinstance(val, str)
            converted = convert("CURRENCY", val)
        else:
            raise ValueError(f"{tag} is not a valid FIX tag")
        self.append_pair(tag, converted)

    @classmethod
    def cast(cls, msg: FixMessage) -> "Quote":
        return _cast(cls, msg)