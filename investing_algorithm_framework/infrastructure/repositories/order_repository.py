from .repository import Repository
from investing_algorithm_framework.infrastructure.models import SQLOrder, \
    SQLPosition, SQLPortfolio
from investing_algorithm_framework.domain import OrderStatus, OrderType, \
    OrderSide


class SQLOrderRepository(Repository):
    base_class = SQLOrder

    def _apply_query_params(self, db, query, query_params):
        external_id_query_param = self.get_query_param(
            "external_id", query_params
        )
        portfolio_query_param = self.get_query_param(
            "portfolio_id", query_params
        )
        side_query_param = self.get_query_param("side", query_params)
        type_query_param = self.get_query_param("type", query_params)
        status_query_param = self.get_query_param("status", query_params)
        price_query_param = self.get_query_param("price", query_params)
        amount_target_symbol_query_param = \
            self.get_query_param("amount_target_symbol", query_params)
        amount_trading_symbol_query_param = \
            self.get_query_param("amount_trading_symbol", query_params)
        position_query_param = self.get_query_param(
            "position", query_params, many=True
        )
        target_symbol_query_param = self.get_query_param(
            "symbol", query_params
        )
        trading_symbol_query_param = self.get_query_param(
            "trading_symbol", query_params
        )

        if portfolio_query_param:
            portfolio = db.query(SQLPortfolio).filter_by(
                identifier=portfolio_query_param
            ).first()

            if portfolio is None:
                return query.filter_by(id=-1)

            positions = db.query(SQLPosition).filter_by(
                portfolio_id=portfolio.id
            ).all()
            position_ids = [p.id for p in positions]
            query = query.filter(SQLOrder.position_id.in_(position_ids))
        if external_id_query_param:
            query = query.filter_by(external_id=external_id_query_param)

        if side_query_param:
            side = OrderSide.from_value(side_query_param)
            query = query.filter_by(side=side.value)

        if type_query_param:
            order_type = OrderType.from_value(type_query_param)
            query = query.filter_by(type=order_type.value)

        if status_query_param:
            status = OrderStatus.from_value(status_query_param)
            query = query.filter_by(status=status.value)

        if price_query_param:
            query = query.filter(SQLOrder.price == price_query_param)

        if amount_target_symbol_query_param:
            query = query.filter_by(
                amount_target_symbol=amount_target_symbol_query_param
            )

        if amount_trading_symbol_query_param:
            query = query.filter_by(
                amount_trading_symbol=amount_trading_symbol_query_param
            )

        if position_query_param:
            query = query.filter(SQLOrder.position_id.in_(
                position_query_param)
            )

        if target_symbol_query_param:
            query = query.filter(
                SQLOrder.target_symbol == target_symbol_query_param
            )

        if trading_symbol_query_param:
            query = query.filter(
                SQLOrder.trading_symbol == trading_symbol_query_param
            )

        query = query.order_by(SQLOrder.created_at.desc())
        return query