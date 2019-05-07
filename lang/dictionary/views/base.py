from lang.common.component import ComponentContext
from lang.dictionary.views.current_date import CurrentDateContext


class BaseContext(ComponentContext):
    context_classes = [CurrentDateContext]
