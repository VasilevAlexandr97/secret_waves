# Определяем TypeVar, который будет представлять тип элементов в списке
from dataclasses import dataclass
from typing import TypeVar

ItemT = TypeVar("ItemT")

@dataclass
class PaginationDTO[ItemT]:
    """
    Датакласс для представления данных с пагинацией.

    Args:
        items: Список элементов текущей страницы. Тип элементов определяется Generic[T].
        count: Общее количество всех доступных элементов (не только на текущей странице).
        offset: Смещение (количество пропущенных элементов) для текущей страницы.
        limit: Максимальное количество элементов на текущей странице.
    """
    items: list[ItemT]
    count: int
    offset: int
    limit: int
