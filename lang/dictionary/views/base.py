from lang.common.component import ComponentContext, ComponentView
from lang.dictionary.views.current_date import CurrentDateContext


class BaseContext(ComponentContext):
    context_classes = [CurrentDateContext]


class PageView(ComponentView):
    context_classes = [BaseContext]
