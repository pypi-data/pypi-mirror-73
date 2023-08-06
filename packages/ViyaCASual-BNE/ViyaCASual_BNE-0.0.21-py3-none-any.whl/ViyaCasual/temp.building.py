from ViyaCasual.Casual import Casual
from ViyaCasual.Database import MSSQLConnector
from ViyaCasual.CAS.CASTableBase import CASTableBase
import pandas as pd


class WarehouseConnector(MSSQLConnector):
    server = 'datawarehouse.boddienoell.com'
    username = 'python1'
    password = 'Cb7Ampdpnq'
    driver = '/opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.1.so.9.2'


def run():
    casual = Casual(server='reports.boddienoell.com', username='willhaley', password='wi1587ha',
                    db_conn=WarehouseConnector())

    input_sql = 'SELECT TOP (10)' \
                '	    t1.[Business_Date]' \
                '      ,datepart(hour, t1.CloseTime) as [TrxHour]' \
                '      ,t1.[StoreNum]' \
                '      ,t1.[OrderNum]' \
                '      ,t1.[State]' \
                '      ,t1.[Destination]' \
                '      ,t1.[LineDiscTotal]' \
                '      ,COALESCE(t1.[TransactionGUID], NEWID()) as [TransactionGUID]' \
                '	    ,t2.PayType' \
                '      ,\'None        \' AS MarketPlace' \
                '      ,\'None        \' AS DestinationCategory' \
                '      ,\'None        \' AS PayTypeCat' \
                '      ,\'None        \' AS DestinationName' \
                '      ,\'None        \' AS DiscountUsed' \
                '      ,\'None        \' AS MarketPlaceCategory' \
                '      ,\'None        \' AS TransactionStatus' \
                '      ,\'None        \' AS PayTypeName' \
                '      ,\'None        \' AS DayPart' \
                '  FROM [TransactionMart].[dbo].[tm_order] t1' \
                '  LEFT OUTER JOIN [TransactionMart].[dbo].[tm_orderCategories] t3 ON (' \
                '       t1.Business_Date = \'%s\'' \
                '       and t3.Business_Date = \'%s\'' \
                '       and t1.TransactionGUID = t3.TransactionGUID' \
                ')  ' \
                '   JOIN [TransactionMart].[dbo].[tm_orderPay] t2 ON (' \
                '         t1.Business_Date = \'%s\'' \
                '	  and t2.Business_Date = \'%s\'' \
                '    and t2.SerialNum = 1' \
                '    and t1.Business_Date = t2.Business_Date' \
                '	  and t1.StoreNum = t2.StoreNum' \
                '	  and t1.OrderNum = t2.OrderNum' \
                '  )' \
                '   WHERE t3.TransactionGUID is NULL' % ('2020-07-08', '2020-07-08', '2020-07-08', '2020-07-08')
    input_data = pd.read_sql(input_sql, casual.db_conn.conn)

    decision = casual.run_decision(
        name='Marketing Transaction Grouping',
        library="public",
        table_name="dm_table",
        input_data=input_data
    )


if __name__ == '__main__':
    run()
