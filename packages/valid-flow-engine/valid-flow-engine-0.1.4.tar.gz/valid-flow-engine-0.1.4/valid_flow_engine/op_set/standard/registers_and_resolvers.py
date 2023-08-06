from dateutil.parser import parse

from ..resolver import ResolverRegistry, ParamResolver
from ..op_set import OpSetRegistry
from ..standard.comparison import ComparisonMixin
from ..standard.math import MathMixin


@OpSetRegistry.register
@ResolverRegistry.register
class Number(ParamResolver, ComparisonMixin, MathMixin):

    @classmethod
    def resolve(cls, data):
        num = data
        try:
            num = int(data)
        except ValueError:
            try:
                num = float(data)
            except ValueError:
                pass
        return num


@OpSetRegistry.register
@ResolverRegistry.register
class DateTime(ParamResolver, ComparisonMixin):
    @classmethod
    def resolve(cls, data):
        date = data
        try:
            date = parse(data)
        except Exception:
            pass
        return date
