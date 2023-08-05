from tradex_common_python.models.Request import Request
from tradex_common_python.models.Base import Base
from typing import List, Dict


class AccountProfitLossReq(Request):
    __slots__ = 'accountNumber', 'subNumber', 'bankCode', 'lastStockCode', 'fetchCount', 'bankName'

    def __init__(self):
        super(AccountProfitLossReq, self).__init__()
        self.accountNumber: str = None
        self.subNumber: str = None
        self.bankCode: str = None
        self.lastStockCode: str = None
        self.fetchCount: int = None
        self.bankName: str = None


class AccountProfitLossItem(Base):
    __slots__ = 'stockCode', 'balanceQuantity', 'sellableQuantity', 'currentPrice', 'buyingQuantity', \
                'buyingPrice', 'buyingAmount', 'evaluationAmount', 'todayBuy', 'todaySell', 't1Buy', \
                't1Sell', 't2Buy', 't2Sell', 'profitLoss', 'profitLossRate'

    def __init__(self):
        super(AccountProfitLossItem, self).__init__()
        self.stockCode: str = None
        self.balanceQuantity: int = None
        self.sellableQuantity: int = None
        self.currentPrice: float = None
        self.buyingQuantity: int = None
        self.buyingPrice: float = None
        self.buyingAmount: float = None
        self.evaluationAmount: float = None
        self.todayBuy: int = None
        self.todaySell: int = None
        self.t1Buy: int = None
        self.t1Sell: int = None
        self.t2Buy: int = None
        self.t2Sell: int = None
        self.profitLoss: float = None
        self.profitLossRate: float = None


class AccountProfitLossRes(Base):
    __slots__ = 't1Deposit', 't2Deposit', 'depositAmount', 'totalBuyAmount', \
                'totalEvaluationAmount', 'totalProfitLoss', 'totalProfitLossRate', 'netAsset', \
                'profitLossItems', 'estimatedDeposit', 'tTradeValue'

    def __init__(self):
        super(AccountProfitLossRes, self).__init__()
        self.t1Deposit: float = None
        self.t2Deposit: float = None
        self.depositAmount: float = None
        self.totalBuyAmount: float = None
        self.totalEvaluationAmount: float = None
        self.totalProfitLoss: float = None
        self.totalProfitLossRate: float = None
        self.netAsset: float = None
        self.estimatedDeposit: float = None
        self.tTradeValue: float = None
        self.profitLossItems: List[AccountProfitLossItem] = []

    @classmethod
    def from_kis_response(cls, res: Dict):
        response = cls()
        if "f_n01" in res:
            response.t1Deposit = float(res["f_n01"][0] or 0)
            response.t2Deposit = float(res["f_n02"][0] or 0)
            response.depositAmount = float(res["f_n04"][0] or 0)
            response.totalBuyAmount = float(res["f_n05"][0] or 0)
            response.totalEvaluationAmount = float(res["f_n07"][0] or 0)
            response.totalProfitLoss = float(res["f_n08"][0] or 0)
            response.totalProfitLossRate = float(res["f_n09"][0] or 0)
            response.netAsset = float(res["f_n11"][0] or 0)
            response.estimatedDeposit = float(res["f_n06"][0] or 0)
            response.tTradeValue = float(res["f_n12"][0] or 0)
            response.profitLossItems = []

            if "f_n13" in res:
                for index in range(len(res["f_n13"])):
                    item: AccountProfitLossItem = AccountProfitLossItem()
                    item.stockCode = res["f_n13"][index]
                    item.todayBuy = int(res["f_n25"][index])
                    item.todaySell = int(res["f_n29"][index])
                    item.buyingQuantity = int(res["f_n14"][index])
                    item.buyingPrice = float(res["f_n20"][index])
                    item.currentPrice = float(res["f_n21"][index])
                    item.buyingAmount = float(res["f_n22"][index])
                    item.evaluationAmount = float(res["f_n23"][index])
                    item.profitLossRate = float(res["f_n24"][index])
                    item.profitLoss = item.evaluationAmount - item.buyingAmount
                    item.t2Buy = int(res["f_n27"][index])
                    item.balanceQuantity = int(res["f_n19"][index])
                    item.sellableQuantity = int(res["f_n16"][index])
                    item.t1Sell = int(res["f_n18"][index])
                    item.t1Buy = int(res["f_n17"][index])

                    # TODO check below fields
                    # item.t2Sell = int(res["f_n29"][index])
                    response.profitLossItems.append(item)
        return response

    @classmethod
    def from_vcsc_response(cls, res: Dict):
        response = cls()
        if "f_n01" in res:
            response.t1Deposit = float(res["f_n01"][0] or 0)
            response.t2Deposit = float(res["f_n02"][0] or 0)
            response.depositAmount = float(res["f_n04"][0] or 0)
            response.totalBuyAmount = float(res["f_n05"][0] or 0)
            response.totalEvaluationAmount = float(res["f_n07"][0] or 0)
            response.totalProfitLoss = float(res["f_n08"][0] or 0)
            response.totalProfitLossRate = float(res["f_n09"][0] or 0)
            response.netAsset = float(res["f_n06"][0] or 0)
            response.profitLossItems = []

            if "f_n13" in res:
                for index in range(len(res["f_n13"])):
                    profit_loss_item: AccountProfitLossItem = AccountProfitLossItem()
                    profit_loss_item.stockCode = res["f_n10"][index]
                    profit_loss_item.balanceQuantity = int(res["f_n11"][index])
                    profit_loss_item.sellableQuantity = int(res["f_n13"][index])
                    profit_loss_item.currentPrice = float(res["f_n18"][index])
                    profit_loss_item.buyingQuantity = int(res["f_n16"][index])
                    profit_loss_item.buyingPrice = float(res["f_n17"][index])
                    profit_loss_item.buyingAmount = float(res["f_n19"][index])
                    profit_loss_item.evaluationAmount = float(res["f_n20"][index])
                    profit_loss_item.todayBuy = int(res["f_n22"][index])
                    profit_loss_item.todaySell = int(res["f_n26"][index])
                    profit_loss_item.t1Buy = int(res["f_n23"][index])
                    profit_loss_item.t1Sell = int(res["f_n27"][index])
                    profit_loss_item.t2Buy = int(res["f_n24"][index])
                    profit_loss_item.t2Sell = int(res["f_n28"][index])
                    profit_loss_item.profitLoss = float(res["f_n20"][index]) - float(res["f_n19"][index])
                    profit_loss_item.profitLossRate = float(res["f_n21"][index])
                    response.profitLossItems.append(profit_loss_item)
        return response
