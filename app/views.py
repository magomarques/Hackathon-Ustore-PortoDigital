from .models import Data
from django.shortcuts import render
import pandas as pd
from django.db.models import Sum
from django.http import JsonResponse

# Create your views here.    

# Função responsável por formatar a data:
def dateFormat(usageDate):

    newDate = usageDate[8:10] + '-' + usageDate[5:7] + '-' + usageDate[0:4] + usageDate[10:19]
    
    return newDate

# Função responsável por formatar casas decimais:
def numberFormat(result):
    
    for i in result:
        i['usageAmount'] = "%.10f" % float(i['usageAmount'])
        i['blendedRate'] = "%.10f" % float(i['blendedRate'])
        i['blendedCost'] = "%.10f" % float(i['blendedCost'])
    
    return result


# Função responsável por somar o valor da fatura:
def sumCost(result):
    
    totalCost = 0
    for i in result:
        totalCost += float(i['blendedCost'])
        # totalCost += float(i['usageAmount']) * float(i['blendedRate'])
    totalCost = "%.2f" % totalCost

    return totalCost

# Função responsável por armazenar os dados do arquivo no banco de dados:
def dataBase(dataList):
    
    data = Data()
    data.invoiceId = dataList[0]
    data.payerAccountId = dataList[1]
    data.billingPeriodStartDate = dataList[2]
    data.billingPeriodEndDate = dataList[3]
    data.usageAccountId = dataList[4]
    data.usageStartDate = dataList[5]
    data.usageEndDate = dataList[6]
    data.productCode = dataList[7]
    data.usageAmount = dataList[8]
    data.blendedRate = dataList[9]
    data.blendedCost = dataList[10]
    data.save()

# Função responsável por gerar uma lista de serviços:
def productsList():

    products = Data.objects.all().values()

    productsList = list()
    productsList = ["TODOS"]
    
    for i in products:
        if i['productCode'] not in productsList:
            productsList.append(i['productCode'])
    
    return productsList

# Função responsável por fazer consulta no banco de dados:
def products(request):

    if "GET" == request.method:
        products = productsList()
        return render(request, 'index.html', {"products": products})
    else:
        products = list()
        products = request.POST.getlist('products')
        print(products)

        for i in products:
            if i == "TODOS":
                result = Data.objects.all().values()
                break
            else:    
                result = Data.objects.filter(productCode=i).values()

        resultFormat = numberFormat(result)
        
        total = sumCost(result)

        products = productsList()
    
        return render(request, 'index.html', {"resultFormat": resultFormat, "total": total, "products": products})

# Função responsável por fazer o upload do arquivo e renderizar no template index:
def readFile(request):

    if "GET" == request.method:
        products = productsList()
        return render(request, 'index.html', {"products": products})
    else:
        csv_data = request.FILES.get('csv_file')
        
        # wb = pd.read_csv(csv_data)
        # wb = pd.read_csv(csv_data, usecols=[0, 1])
        wb = pd.read_csv(csv_data, usecols=[
            'bill/InvoiceId', #0
            'bill/PayerAccountId', #1
            'bill/BillingPeriodStartDate', #2
            'bill/BillingPeriodEndDate', #3
            'lineItem/UsageAccountId', #4
            'lineItem/UsageStartDate', #5
            'lineItem/UsageEndDate', #6
            'lineItem/ProductCode', #7
            'lineItem/UsageAmount', #8
            'lineItem/BlendedRate', #9
            'lineItem/BlendedCost']) #10
        wb.fillna(0, inplace=True)

        listInvoiceId = wb['bill/InvoiceId'].to_list()
        listPayerAccountId = wb['bill/PayerAccountId'].to_list()
        listBillingPeriodStartDate = wb['bill/BillingPeriodStartDate'].to_list()
        listBillingPeriodEndDate = wb['bill/BillingPeriodEndDate'].to_list()
        listUsageAccountId = wb['lineItem/UsageAccountId'].to_list()
        listUsageStartDate = wb['lineItem/UsageStartDate'].to_list()
        listUsageEndDate = wb['lineItem/UsageEndDate'].to_list()
        listProductCode = wb['lineItem/ProductCode'].to_list()
        listUsageAmount = wb['lineItem/UsageAmount'].to_list()
        listBlendedRate = wb['lineItem/BlendedRate'].to_list()
        listBlendedCost = wb['lineItem/BlendedCost'].to_list()

        for i in range(0, len(listInvoiceId)):
            listOfValues = []
            listOfValues.append(listInvoiceId[i])
            listOfValues.append(listPayerAccountId[i])
            listOfValues.append(listBillingPeriodStartDate[i])
            listOfValues.append(listBillingPeriodEndDate[i])
            listOfValues.append(listUsageAccountId[i])
            listOfValues.append(dateFormat(listUsageStartDate[i]))
            listOfValues.append(dateFormat(listUsageEndDate[i]))
            listOfValues.append(listProductCode[i])
            listOfValues.append(listUsageAmount[i])
            listOfValues.append(listBlendedRate[i])
            listOfValues.append(listBlendedCost[i])
            dataBase(listOfValues)
        
        result = Data.objects.all().values()

        resultFormat = numberFormat(result)

        total = sumCost(result)

        products = productsList()
        return render(request, 'index.html', {"resultFormat": resultFormat, "total": total, "products": products})

# Função responsável por renderizar os gráficos no template Pie Chart:
def pieChart(request):

    listProductCode = productsList()
    products = listProductCode
    listTotalBlendedCost = []

    result = Data.objects.all().values()
    
    for i in listProductCode:
        total = 0
        for j in result:
            if i == j['productCode']:
                total += float(j['blendedCost'])
        listTotalBlendedCost.append(total)

    return render(request, 'pieChart.html', {"listProductCode": listProductCode, "listTotalBlendedCost": listTotalBlendedCost, "products": products})

# Função responsável por renderizar os gráficos no template Bar Chart:
def barChart(request):

    listProductCode = productsList()
    products = listProductCode
    listTotalBlendedCost = []
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            11, 12, 13, 14, 15, 16, 17, 18, 19 , 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29 ,30, 31]

    result = Data.objects.all().values()
    
    for i in month:
        total = 0
        for j in result:
            if i == int(j['usageStartDate'][0:2]):
                total += float(j['blendedCost'])
        listTotalBlendedCost.append(total)

    return render(request, 'barChart.html', {"month": month, "listTotalBlendedCost": listTotalBlendedCost, "products": products})

    