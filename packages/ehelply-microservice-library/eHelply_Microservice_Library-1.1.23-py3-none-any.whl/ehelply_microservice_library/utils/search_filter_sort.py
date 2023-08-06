from ehelply_bootstrapper.utils.state import State
from sqlalchemy import and_, or_
from sqlalchemy.orm.query import Query
from typing import List


class SQLSearch:
    def __init__(self, model, columns: List[str]):
        self.model = model
        self.columns: List[str] = columns

    def search(self, search: str, query: Query, use_or=True) -> Query:
        if len(search) < 3:
            raise Exception("Search criteria cannot be shorter than 3 characters")

        filters: list = []
        for column in self.columns:
            column = getattr(self.model, column, None)
            filters.append(
                column.like('%' + search + '%')
            )
        if use_or:
            return query.filter(or_(*filters))
        else:
            return query.filter(and_(*filters))


class SQLSort:
    def __init__(self, model, column: str):
        self.model = model
        self.column: str = column

    def sort(self, query: Query, desc=False):
        column = getattr(self.model, self.column, None)
        if desc:
            return query.order_by(column.desc())
        else:
            return query.order_by(column)
