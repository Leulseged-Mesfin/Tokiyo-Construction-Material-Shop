from django.urls import path
from .views import (
    ProductListCreateAPIView, 
    ProductRetrieveUpdateDeleteAPIView,

    SupplierListCreateAPIView,
    SupplierRetrieveUpdateDeleteAPIView,

    OrderListCreateAPIView,
    OrderRetrieveUpdateDeleteAPIView,

    OrderItemListCreateAPIView,
    OrderItemRetrieveUpdateDeleteAPIView,

    CustomerListCreateAPIView,
    CustomerRetrieveUpdateDeleteAPIView,

    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDeleteAPIView,

    RetriveRevenueAPIView,
    RetriveProfitAPIView,
    ExcelReportAPIView,
    OrderLogAPIView,

    CompanyListCreateAPIView,
    CompanyRetrieveUpdateDeleteAPIView,

    ListOutOFStockProductAPIView,
    CountNearExpirationDateProductAPIView,

    ExpenseTypesListCreateAPIView,
    ExpenseTypesRetrieveUpdateDeleteAPIView,

    OtherExpensesListCreateAPIView,
    OtherExpensesRetrieveUpdateDeleteAPIView,

    RetriveTotalProductCostAPIView,
    ProductExcelReportAPIView,

    ProductsPerSupplierAPIView,

    PurchaseProductListCreate, 
    PurchaseExpenseListCreate
  
)

urlpatterns = [
    path('products', ProductListCreateAPIView.as_view(), name='products-list'),
    path('products/<pk>', ProductRetrieveUpdateDeleteAPIView.as_view(), name='products-retrieve'),

    path('suppliers', SupplierListCreateAPIView.as_view(), name='suppliers-list'),
    path('suppliers/<pk>', SupplierRetrieveUpdateDeleteAPIView.as_view(), name='suppliers-retrieve'),

    path('orders', OrderListCreateAPIView.as_view(), name='orders-list'),
    path('orders/<pk>', OrderRetrieveUpdateDeleteAPIView.as_view(), name='orders-retrieve'),

    path('orderitems', OrderItemListCreateAPIView.as_view(), name='orders-items-list'),
    path('orderitems/<pk>', OrderItemRetrieveUpdateDeleteAPIView.as_view(), name='orders-items-retrieve'),

    path('customers', CustomerListCreateAPIView.as_view(), name='customers-list'),
    path('customers/<pk>', CustomerRetrieveUpdateDeleteAPIView.as_view(), name='customers-retrieve'),
    
    path('company', CompanyListCreateAPIView.as_view(), name='company-list'),
    path('company/<pk>', CompanyRetrieveUpdateDeleteAPIView.as_view(), name='company-retrieve'),

    path('category', CategoryListCreateAPIView.as_view(), name='category-list'),
    path('category/<pk>', CategoryRetrieveUpdateDeleteAPIView.as_view(), name='category-retrieve'),

    path('revenue/', RetriveRevenueAPIView.as_view(), name='revenue-retrieve'),
    path('profit/', RetriveProfitAPIView.as_view(), name='profit-retrieve'),
    path('report/', ExcelReportAPIView.as_view(), name='report-retrieve'),
    path('order_log/', OrderLogAPIView.as_view(), name='order-log-retrieve'),
    path('stock/', ListOutOFStockProductAPIView.as_view(), name='stock-shortage-retrieve'),
    path('stock_count/', CountNearExpirationDateProductAPIView.as_view(), name='stock-shortage-count-retrieve'),

    path('expense_type', ExpenseTypesListCreateAPIView.as_view(), name='expense_type-list'),
    path('expense_type/<pk>', ExpenseTypesRetrieveUpdateDeleteAPIView.as_view(), name='expense_type-retrieve'),

    path('other_expenses', OtherExpensesListCreateAPIView.as_view(), name='other_expenses-list'),
    path('other_expenses/<pk>', OtherExpensesRetrieveUpdateDeleteAPIView.as_view(), name='other_expenses-retrieve'),
    path('product_report/', ProductExcelReportAPIView.as_view(), name='product-report-retrieve'),
    path('product_cost/', RetriveTotalProductCostAPIView.as_view(), name='total-product-cost-retrieve'),

    path('products_supplier/<pk>', ProductsPerSupplierAPIView.as_view(), name='products-per-supplier'),

    path('purchase-products/', PurchaseProductListCreate.as_view(), name='purchase-product-list-create'),
    path('purchase-products/<pk>', PurchaseProductListCreate.as_view(), name='purchase-product-list-create'),
    path('purchase-expenses/', PurchaseExpenseListCreate.as_view(), name='purchase-expense-list-create'),
    path('purchase-expenses/<pk>/', PurchaseExpenseListCreate.as_view(), name='purchase-expense-list-create'),
]
