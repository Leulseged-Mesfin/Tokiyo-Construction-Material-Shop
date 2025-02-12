from rest_framework.views import APIView
from django.db.models import Sum, Count
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.models import F, Sum, ExpressionWrapper, DecimalField
from .models import Product, Supplier, Order, OrderItem, Category, CustomerInfo, CompanyInfo, OrderLog, Report, ExpenseTypes, OtherExpenses, PurchaseExpense, PurchaseProduct
from .serializers import (
    ProductPostSerializer, 
    ProductGetSerializer, 
    ProductGetReportSerializer, 
    SupplierSerializer, 
    OrderGetSerializer, 
    OrderSerializer, 
    OrderItemSerializer, 
    # OrderItemReportSerializer,
    CategorySerializer, 
    CustomerInfoSerializer,
    CompanyInfoSerializer,
    OrderLogSerializer,
    OrderReportSerializer,
    ExpenseTypesSerializer,
    OtherExpensesSerializer,
    OtherExpensesGetSerializer,
    PurchaseProductSerializer,
    PurchaseExpenseSerializer

)
import logging

logger = logging.getLogger(__name__)
from django.core.exceptions import ValidationError
from .utils import create_order_log

class ProductListCreateAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Product."},
                    status=status.HTTP_403_FORBIDDEN
                )
            product = Product.objects.all()
            # products = Product.objects.all().order_by('id')
            serializer = ProductGetSerializer(product, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to create the Product."},
                    status=status.HTTP_403_FORBIDDEN
                 )   
            serializer = ProductPostSerializer(data=request.data)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            serializer.create(validated_data, user=request.user)
            return Response({"message": f"Product Created successfully."}, status=status.HTTP_201_CREATED)

        except KeyError as e:
            print(e)
            return Response(
                {"error": f"An error occurred while Creating the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductRetrieveUpdateDeleteAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to retrive the Product."},
                    status=status.HTTP_403_FORBIDDEN
                )               
            if not Product.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            product = Product.objects.get(id=pk)
            serializer = ProductGetSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def put(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to update the Product."},
                    status=status.HTTP_403_FORBIDDEN
                ) 
            if not Product.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            product = Product.objects.get(id=pk)
            serializer = ProductPostSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            validated_data['user'] = user
            serializer.update(product, validated_data)
            return Response({"message": f"Product Updated successfully."}, status=status.HTTP_200_OK)        
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to update the Product."},
                    status=status.HTTP_403_FORBIDDEN
                )          
            if not Product.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            product = Product.objects.get(id=pk)    
            serializer = ProductPostSerializer(product, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": f"Product Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def delete(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to delete the Product."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not Product.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Product Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            Product.objects.get(id=pk).delete()
            if not Product.objects.filter(id=pk).exists():
                return Response({"message": f"Product Deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"error": "Failed to delete an Product."},
                    status=status.HTTP_400_BAD_REQUEST
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Deleting the Product.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SupplierListCreateAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Supplier."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # print(user.role)
            supplier = Supplier.objects.all()
            serializer = SupplierSerializer(supplier, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)                            
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to create the Supplier."},
                    status=status.HTTP_403_FORBIDDEN
                ) 
            print(user.role)
            serializer = SupplierSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            # validated_data['user'] = user
            serializer.create(validated_data, user=request.user)
            return Response({"message": "Supplier created successfully."}, status=status.HTTP_201_CREATED) 
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while creating the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class SupplierRetrieveUpdateDeleteAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Supplier."},
                    status=status.HTTP_403_FORBIDDEN
                )            
            if not Supplier.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Supplier Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            supplier = Supplier.objects.get(id=pk)
            serializer = SupplierSerializer(supplier)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to update the Supplier."},
                    status=status.HTTP_403_FORBIDDEN
                )              
            if not Supplier.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Supplier Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            supplier = Supplier.objects.get(id=pk)
            serializer = SupplierSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(supplier, validated_data)
            return Response({"message": f"Supplier Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to update the Supplier."},
                    status=status.HTTP_403_FORBIDDEN
                )  
            if not Supplier.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Supplier Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            supplier = Supplier.objects.get(id=pk)    
            serializer = SupplierSerializer(supplier, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": f"Supplier Updated successfully."}, status=status.HTTP_200_OK)                    
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to delete the Supplier."},
                    status=status.HTTP_403_FORBIDDEN
                )  

            if not Supplier.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Supplier Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            Supplier.objects.get(id=pk).delete()
            if not Supplier.objects.filter(id=pk).exists():
                return Response({"message": f"Supplier Deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"error": "Failed to delete an Supplier."},
                    status=status.HTTP_400_BAD_REQUEST
                )
                    
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Deleting the Supplier.{str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CustomerListCreateAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Customers."},
                    status=status.HTTP_403_FORBIDDEN
                ) 
            customer = CustomerInfo.objects.all()
            serializer = CustomerInfoSerializer(customer, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Customers.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to create the Customer."},
                    status=status.HTTP_403_FORBIDDEN
                )               
            serializer = CustomerInfoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.create(validated_data, user=request.user)
            return Response({"message": f"Customer Created successfully."}, status=status.HTTP_201_CREATED)     
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while creating the Customer.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class CustomerRetrieveUpdateDeleteAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Customer."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not CustomerInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Customer Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            customer = CustomerInfo.objects.get(id=pk)
            serializer = CustomerInfoSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Customer.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to update the Customer."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not CustomerInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Customer Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            customer = CustomerInfo.objects.get(id=pk)
            serializer = CustomerInfoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(customer, validated_data)
            return Response({"message": f"Customer Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Customer.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
       
    def patch(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to update the Customer."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not CustomerInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Customer Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            customer = CustomerInfo.objects.get(id=pk) 
            serializer = CustomerInfoSerializer (customer, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": f"Category Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Customer.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to delete the Customer."},
                    status=status.HTTP_403_FORBIDDEN
                )               
            if not CustomerInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Customer Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            CustomerInfo.objects.get(id=pk).delete()
            if not CustomerInfo.objects.filter(id=pk).exists():
                return Response({"message": f"Customer Deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"error": "Failed to delete an Customer."},
                    status=status.HTTP_400_BAD_REQUEST
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Deleting the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CompanyListCreateAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Company."},
                    status=status.HTTP_403_FORBIDDEN
                )
            company = CompanyInfo.objects.all()
            serializer = CompanyInfoSerializer(company, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Company.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to create the Company."},
                    status=status.HTTP_403_FORBIDDEN
                 )   
            serializer = CompanyInfoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            validated_data['user'] = user
            serializer.create(validated_data, user=request.user)
            return Response({"message": f"Company Created successfully."}, status=status.HTTP_201_CREATED)

        except KeyError as e:
            print(e)
            return Response(
                {"error": f"An error occurred while Creating the Company.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CompanyRetrieveUpdateDeleteAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to retrive the Product."},
                    status=status.HTTP_403_FORBIDDEN
                )               
            if not CompanyInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Company Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            company = CompanyInfo.objects.get(id=pk)
            serializer = CompanyInfoSerializer(company)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Company.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def put(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to update the Product."},
                    status=status.HTTP_403_FORBIDDEN
                ) 
            if not CompanyInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Company Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            company = CompanyInfo.objects.get(id=pk)
            serializer = CompanyInfoSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(company, validated_data)
            return Response({"message": f"Company Updated successfully."}, status=status.HTTP_200_OK)        
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Company.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to update the Company."},
                    status=status.HTTP_403_FORBIDDEN
                )          
            if not CompanyInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Company Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            company = CompanyInfo.objects.get(id=pk)    
            serializer = CompanyInfoSerializer(company, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": f"Company Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Company.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to delete the Company."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not CompanyInfo.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Company Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            CompanyInfo.objects.get(id=pk).delete()
            if not CompanyInfo.objects.filter(id=pk).exists():
                return Response({"message": f"Company Deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {"error": "Failed to delete an Company."},
                    status=status.HTTP_400_BAD_REQUEST
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Deleting the Company.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderListCreateAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrieve the Order."},
                    status=status.HTTP_403_FORBIDDEN
                )               
            order = Order.objects.all()
            serializer = OrderGetSerializer(order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)     
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Orders.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to create the Order."},
                    status=status.HTTP_403_FORBIDDEN
                ) 
            serializer = OrderSerializer(data=request.data, context={"request": request})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(user=request.user) # calls the create method in OrderSerializer
            return Response({"message": f"Order Created successfully."}, status=status.HTTP_201_CREATED)      
        except KeyError as e:
            print(e)
            return Response(
                {"error": f"An error occurred while creating the Order.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderRetrieveUpdateDeleteAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrieve the Order."},
                    status=status.HTTP_403_FORBIDDEN
                ) 
            
            if not Order.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Customer Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            order = Order.objects.get(id=pk)
            serializer = OrderGetSerializer(order)
            # print(order)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Order.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to update the Order."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Check if the order exists
            order = Order.objects.filter(id=pk).first()
            if not order:
                return Response(
                    {"error": "Order Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Initialize the serializer with the existing instance and new data
            serializer = OrderSerializer(order, data=request.data, partial=False)

            # Validate the data
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Save the validated data and update the instance
            # serializer.save()
            validated_data = serializer.validated_data
            serializer.update(order, validated_data)

            # Return the updated data as a response
            return Response({"message": f"Order Updated successfully."}, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Order. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 
    def patch(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to update the Order."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not Order.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Order Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            order = Order.objects.get(id=pk)    
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(order, validated_data)
            # serializer.save()
            return Response({"message": f"Order Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Order.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def delete(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to delete the Order."},
                    status=status.HTTP_403_FORBIDDEN
                )  
            # Retrieve the order
            order = Order.objects.filter(id=pk).first()
            
            # Check if the order exists
            if not order:
                logger.debug(f"Order with id {pk} does not exist.")
                return Response(
                    {"error": "Order does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Delete the order, which should cascade to related items
            logger.debug(f"Deleting Order with id {pk}.")
            order.delete()

            # Confirm deletion by querying again
            if not Order.objects.filter(id=pk).exists():
                logger.debug(f"Order with id {pk} successfully deleted.")
                return Response(
                    {"message": "Order and related items were successfully deleted."},
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                logger.error(f"Order with id {pk} was not deleted for some reason.")
                return Response(
                    {"error": "Failed to delete the order."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            # logger.error(f"An exception occurred while deleting the order: {str(e)}")
            return Response(
                {"error": f"An error occurred while deleting the order: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderItemListCreateAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request):
        try:   
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Order."},
                    status=status.HTTP_403_FORBIDDEN
                )           
            order_item = OrderItem.objects.all()
            serializer = OrderItemSerializer(order_item, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)     
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Order_Item.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderItemRetrieveUpdateDeleteAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Order."},
                    status=status.HTTP_403_FORBIDDEN
                )
            order_item = OrderItem.objects.filter(id=pk).first()
            if not order_item:
                return Response(
                    {"error": "OrderItem Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = OrderItemSerializer(order_item)
            # print(order)
            return Response(serializer.data, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the OrderItem.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to update the Order."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Check if the order_item exists
            order_item = OrderItem.objects.filter(id=pk).first()
            if not order_item:
                return Response(
                    {"error": "OrderItem Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Initialize the serializer with the existing instance and new data
            serializer = OrderItemSerializer(order_item, data=request.data, partial=False)

            # Validate the data
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Save the validated data and update the instance
            # serializer.save()
            validated_data = serializer.validated_data
            items = serializer.update(order_item, validated_data)
            # Adding it into the log with every itration
            user_name = user.name
            create_order_log(
                user = user_name,
                action="Update",
                model_name="OrderItem",
                object_id=items.order.id,
                customer_info = items.order.customer,
                product_name = items.product.name,
                quantity = items.quantity,
                price = items.price,
                changes_on_update = f"Updated Order :  quantity to {items.quantity}.",
            )

            # Return the updated data as a response
            return Response({"message": f"Order Item Updated successfully."}, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the OrderItem. {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def patch(self, request, pk):
        try:     
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to update the Order."},
                    status=status.HTTP_403_FORBIDDEN
                )         
            if not OrderItem.objects.filter(id=pk).exists():
                return Response(
                    {"error": "OrderItem Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            order_item = OrderItem.objects.get(id=pk)    
            serializer = OrderItemSerializer(order_item, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            items = serializer.update(order_item, validated_data)
            # Adding it into the log with every itration
            user_name = user.name
            create_order_log(
                user = user_name,
                action="Update",
                model_name="OrderItem",
                object_id=items.order.id,
                customer_info = items.order.customer,
                product_name = items.product.name,
                quantity = items.quantity,
                price = items.price,
                changes_on_update = f"Updated Order :  quantity to {items.quantity}.",
            )
            return Response({"message": f"Order Item Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the OrderItem.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):  
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to delete the Order."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # Retrieve the orderItem
            order_item = OrderItem.objects.filter(id=pk).first()
            # Check if the order_item exists
            if not order_item:
                logger.debug(f"OrderItem with id {pk} does not exist.")
                return Response(
                    {"error": "OrderItem does not exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Delete the order, which should cascade to related items
            logger.debug(f"Deleting OrderItem with id {pk}.")
            order_item.delete()

            # Confirm deletion by querying again
            if not OrderItem.objects.filter(id=pk).exists():
                logger.debug(f"OrderItem with id {pk} successfully deleted.")
                # Adding it into the log with every itration
                if order_item.product is None:
                    create_order_log(
                        user = user.name,
                        action="Delete",
                        model_name="OrderItem",
                        object_id=order_item.id,
                        customer_info = order_item.order.customer,
                        product_name = "Product",
                        quantity = order_item.quantity,
                        price = order_item.price,
                        changes_on_update = f"Deleted Order Item.",
                    )
                else:
                    create_order_log(
                        user = user.name,
                        action="Delete",
                        model_name="OrderItem",
                        object_id=order_item.id,
                        customer_info = order_item.order.customer,
                        product_name = order_item.product.name,
                        quantity = order_item.quantity,
                        price = order_item.price,
                        changes_on_update = f"Deleted Order Item.",
                    )

                return Response(
                    {"message": "OrderItem successfully deleted."},
                    status=status.HTTP_204_NO_CONTENT
                )
                
            else:
                logger.error(f"OrderItem with id {pk} was not deleted for some reason.")
                return Response(
                    {"error": "Failed to delete the order."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"An exception occurred while deleting the orderItem: {str(e)}")
            return Response(
                {"error": f"An error occurred while deleting the orderItem: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CategoryListCreateAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Category."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # category = Category.objects.all()
            category = Category.objects.all().order_by('id')
            serializer = CategorySerializer(category, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)              
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Category.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to create the Category."},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = CategorySerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            validated_data['user'] = user
            serializer.create(validated_data, user=request.user)
            return Response({"message": f"Category created successfully."}, status=status.HTTP_201_CREATED)
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while creating the Category.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
   

class CategoryRetrieveUpdateDeleteAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Category."},
                    status=status.HTTP_403_FORBIDDEN
                )
            if not Category.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Category Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)     
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Category.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to update the Category."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not Category.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Category Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(category, validated_data)
            return Response({"message": f"Category Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Category.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def patch(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to update the Category."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not Category.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Category Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            category = Category.objects.get(id=pk)    
            serializer = CategorySerializer(category, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": f"Category Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Category.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True):
                return Response(
                    {"error": "You are not authorized to delete the Category."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not Category.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Customer Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            Category.objects.get(id=pk).delete()
            if not Category.objects.filter(id=pk).exists():
                return Response({"message": f"Category Deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT   
                )
            else:
                return Response(
                    {"error": "Failed to delete an Customer."},
                    status=status.HTTP_400_BAD_REQUEST
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Delete the Supplier.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RetriveRevenueAPIView(APIView):
    def get(self, request): 
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Revenue."},
                    status=status.HTTP_403_FORBIDDEN
                ) 

            # revenue = Order.objects.aggregate(total_revenue=Sum('total_amount'))        
            revenue = OrderItem.objects.aggregate(total_revenue=Sum('price'))        
            return Response(revenue, status=status.HTTP_200_OK)         
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Revenue.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RetriveProfitAPIView(APIView):
    def get(self, request): 
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Profit."},
                    status=status.HTTP_403_FORBIDDEN
                )
            # buying_price = Product.objects.aggregate(total_cost=Sum('buying_price'))

            revenue = OrderItem.objects.aggregate(total_revenue=Sum('price')) 
            cost = OrderItem.objects.aggregate(total_cost=Sum('cost')) 
            # profit = OrderItem.objects.aggregate(total_profit=Diff('price' - 'cost'))
            profit = OrderItem.objects.aggregate(
                    total_profit=Sum(
                        ExpressionWrapper(
                            F('price') - F('cost'),
                            output_field=DecimalField()
                        )
                    )
                )
            return Response(profit, status=status.HTTP_200_OK)         
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Profit.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OrderLogAPIView(APIView):
    def get(self, request):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Receipt."},
                    status=status.HTTP_403_FORBIDDEN
                )
            logs = OrderLog.objects.all()
            serializer = OrderLogSerializer(logs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Log.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExcelReportAPIView(APIView):
    def get(self, request):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Receipt."},
                    status=status.HTTP_403_FORBIDDEN
                )
            report = Report.objects.all()
            serializer = OrderReportSerializer(report, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Report.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListOutOFStockProductAPIView(APIView):
    def get(self, request):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the near Stock."},
                    status=status.HTTP_403_FORBIDDEN
                )
            out_of_stock_products = Product.objects.filter(stock__lte=3)
            serializer = ProductGetSerializer(out_of_stock_products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Stock Shortage.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CountNearExpirationDateProductAPIView(APIView):
    def get(self, request):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Stock Shortage."},
                    status=status.HTTP_403_FORBIDDEN
                )
            out_of_stock_products = Product.objects.filter(stock__lte=3).aggregate(out_of_stock=Count('name'))
            return Response(out_of_stock_products, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Stock Shortage.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExpenseTypesListCreateAPIView(APIView):

    # permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Expense Types."},
                    status=status.HTTP_403_FORBIDDEN
                )
            expense_type = ExpenseTypes.objects.all().order_by('id')
            serializer = ExpenseTypesSerializer(expense_type, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)              
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Expense Types.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to create the Expense Types."},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = ExpenseTypesSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            serializer.create(validated_data, user=request.user)
            return Response({"message": f"Expense Types created successfully."}, status=status.HTTP_201_CREATED)
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while creating the Expense Types.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExpenseTypesRetrieveUpdateDeleteAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Expense Types."},
                    status=status.HTTP_403_FORBIDDEN
                )
            if not ExpenseTypes.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Expense Types Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            expense_type = ExpenseTypes.objects.get(id=pk)
            serializer = ExpenseTypesSerializer(expense_type)
            return Response(serializer.data, status=status.HTTP_200_OK)     
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Expense Types.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to update the Expense Types."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not ExpenseTypes.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Expense Types Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            expense_type = ExpenseTypes.objects.get(id=pk)
            serializer = ExpenseTypesSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(expense_type, validated_data)
            return Response({"message": f"Expense Types Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Expense Types.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def patch(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to update the Expense Types."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not ExpenseTypes.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Expense Types Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            expense_type = ExpenseTypes.objects.get(id=pk)    
            serializer = ExpenseTypesSerializer(expense_type, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": f"Expense Types Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating the Expense Types.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to delete the Expense Types."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not ExpenseTypes.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Expense Types Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            ExpenseTypes.objects.get(id=pk).delete()
            if not ExpenseTypes.objects.filter(id=pk).exists():
                return Response({"message": f"Expense Types Deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT   
                )
            else:
                return Response(
                    {"error": "Failed to delete an Expense Types."},
                    status=status.HTTP_400_BAD_REQUEST
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Delete the Expense Types.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OtherExpensesListCreateAPIView(APIView):

    # permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive Other Expenses."},
                    status=status.HTTP_403_FORBIDDEN
                )
            other_expenses = OtherExpenses.objects.all().order_by('id')
            serializer = OtherExpensesGetSerializer(other_expenses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)              
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving Other Expenses.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, format=None):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to create Other Expenses."},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = OtherExpensesSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            serializer.create(validated_data, user=request.user)
            return Response({"message": f"Other Expenses created successfully."}, status=status.HTTP_201_CREATED)
                      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while creating Other Expenses.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OtherExpensesRetrieveUpdateDeleteAPIView(APIView):
    # permission_classes = (permissions.AllowAny,)
    def get(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive Other Expenses."},
                    status=status.HTTP_403_FORBIDDEN
                )
            if not OtherExpenses.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Expense Types Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            other_expenses = OtherExpenses.objects.get(id=pk)
            serializer = OtherExpensesGetSerializer(other_expenses)
            return Response(serializer.data, status=status.HTTP_200_OK)     
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving Other Expenses.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to update Other Expenses."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not OtherExpenses.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Other Expenses Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            other_expenses = OtherExpenses.objects.get(id=pk)
            serializer = OtherExpensesSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            validated_data = serializer.validated_data
            serializer.update(other_expenses, validated_data)
            return Response({"message": f"Other Expenses Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating Other Expenses  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def patch(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to update Other Expenses."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not OtherExpenses.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Other Expenses Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            other_expenses = OtherExpenses.objects.get(id=pk)    
            serializer = OtherExpensesSerializer(other_expenses, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"message": f"Other Expenses Updated successfully."}, status=status.HTTP_200_OK)      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while updating Other Expenses.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to delete Other Expenses."},
                    status=status.HTTP_403_FORBIDDEN
                )                
            if not OtherExpenses.objects.filter(id=pk).exists():
                return Response(
                    {"error": "Other Expenses Does not Exist."},
                    status=status.HTTP_404_NOT_FOUND
                )
            OtherExpenses.objects.get(id=pk).delete()
            if not OtherExpenses.objects.filter(id=pk).exists():
                return Response({"message": f"Other Expenses Deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT   
                )
            else:
                return Response(
                    {"error": "Failed to delete Other Expenses."},
                    status=status.HTTP_400_BAD_REQUEST
                )      
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Delete Other Expenses.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RetriveTotalProductCostAPIView(APIView):
    def get(self, request): 
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Total Product Cost."},
                    status=status.HTTP_403_FORBIDDEN
                ) 
     
            total_product_cost = Product.objects.aggregate(total_product_cost=Sum('buying_price'))        
            return Response(total_product_cost, status=status.HTTP_200_OK)         
        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Total Product Cost.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductExcelReportAPIView(APIView):
    def get(self, request):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to retrive the Product Report."},
                    status=status.HTTP_403_FORBIDDEN
                )
            report = Product.objects.all()
            serializer = ProductGetReportSerializer(report, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response(
                {"error": f"An error occurred while Retriving the Product Report.  {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductsPerSupplierAPIView(APIView):
    def get(self, request, pk):
        try:
            user = request.user
            if not (user.role == 'Manager' or user.is_superuser == True or user.role == 'Salesman'):
                return Response(
                    {"error": "You are not authorized to Retrive products for this supplier."},
                    status=status.HTTP_403_FORBIDDEN
                ) 
            """Retrieve all products belonging to a specific supplier."""
            products = Product.objects.filter(supplier_id=pk)
            if not products.exists():
                return Response({"message": "No products found for this supplier"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProductGetSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred while retrieving products for this supplier: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

 

class PurchaseProductListCreate(APIView):
    def get(self, request):
        products = PurchaseProduct.objects.all()
        serializer = PurchaseProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseExpenseListCreate(APIView):
    def get(self, request):
        expenses = PurchaseExpense.objects.all()
        serializer = PurchaseExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

