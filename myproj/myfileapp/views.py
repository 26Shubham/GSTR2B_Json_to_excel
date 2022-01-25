import pandas as pd
from django.shortcuts import render,HttpResponse

from .forms import MyfileuploadForm

from .models import file_upload

import pandas as pd

import json
import warnings
from openpyxl import load_workbook
import os

import glob


def flatten_dict(dic):



    warnings.filterwarnings('ignore')

    df2 = pd.DataFrame()

    key_list = list(dic.keys())
    flat_dict = dict()

    for i in key_list:
        dict_whole = {i: dic[i]}
        dict_value = dic[i]

        if isinstance(dict_value, dict):
            flat_dict.update(dict_value)

        elif isinstance(dict_value, list):

            if len(dict_value) == 1:
                a = dict_value[0]
                b = flatten_dict(a)
                flat_dict.update(b)
            elif len(dict_value) == 0:
                pass

            else:
                dicdf = expand_list(dict_value)
                flat_dict.update(dicdf)

        else:
            flat_dict.update(dict_whole)

    data_list = list(flat_dict.items())

    df = pd.DataFrame(data_list)
    df1 = df.T
    df1.columns = df1.loc[0]
    df1 = df1.drop(0)
    df1 = df1.reset_index(drop=True)
    return (flat_dict)


def expand_list(list_dic):


    warnings.filterwarnings('ignore')

    df2 = pd.DataFrame()

    if len(list_dic) == 1:
        a = list_dic[0]
        b = flatten_dict(a)
        conv_dict = b
    else:

        for i in list_dic:
            if isinstance(i, dict):

                flat_dictl = flatten_dict(i)

                try:
                    df1 = pd.DataFrame(flat_dictl)
                except:
                    df = pd.DataFrame(list(flat_dictl.items()))
                    df1 = df.T
                    df1.columns = df1.loc[0]
                    df1 = df1.drop(0)
                    df1 = df1.reset_index(drop=True)

                df2 = df2.append(df1)

            elif isinstance(i, list):
                a = expand_list(i)
                df2 = a

            else:
                dict_whole = {i: list_dic[i]}
                df = pd.DataFrame(list(dict_whole.items()))
                df1 = df.T
                df1.columns = df1.loc[0]
                df1 = df1.drop(0)
                df1 = df1.reset_index(drop=True)

                df2 = df2.append(df1)

        conv_dict = df2.to_dict(orient="list")

    return (conv_dict)

def rename_2b_columns(dataframe):


    dataframe.rename(columns={"dt": "Final_Invoice_CNDN_Date",
                              "val": "Invoice_CNDN_Value",
                              "rev": "Supply_Attract_Reverse_Charge",
                              "itcavl": "ITC_Available",
                              "diffprcnt": "Applicable_Percent_TaxRate",
                              "pos": "Place_Of_Supply",
                              "typ": "Final_Inv_CNDN_Type",
                              "inum": "Final_Invoice_CNDN_No",
                              "rsn": "Reason",
                              "sgst": "SGST_Amount",
                              "rt": "Tax_Rate",
                              "num": "Check_num",
                              "txval": "Taxable_Value",
                              "cgst": "CGST_Amount",
                              "cess": "Cess_Amount",
                              "trdnm": "Trade_Name_of_Supplier",
                              "supfildt": "Supplier_Filing_Date",
                              "supprd": "Supplier_Filing_Period",
                              "ctin": "GSTIN_of_Supplier",
                              "igst": "IGST_Amount",
                              "irn": "IRN",
                              "irngendate": "IRN_Generate_Date",
                              "srctyp": "Source_Type",
                              "GSTR2B-Table": "GSTR2B-Table",
                              "rtnprd": "GSTR2B_Period",
                              "gstin": "Recipient_GSTIN",
                              "Json File Name": "JSON_Source_File",
                              "File_Name": "Source_Excel_File",
                              "oinum": "Initial_Inv_CNDN_No",
                              "oidt": "Initial_Inv_CNDN_Date",
                              "ntnum": "Final_Invoice_CNDN_No",
                              "suptyp": "Note_Supply_Type",
                              "ontdt": "Initial_Inv_CNDN_Date",
                              "onttyp": "Initial_Inv_CNDN_Type",
                              "ontnum": "Initial_Inv_CNDN_No",
                              "docnum": "Final_Invoice_CNDN_No",
                              "itcelg": "ITC_Available",
                              "doctyp": "Final_Inv_CNDN_Type",
                              "docdt": "Final_Invoice_CNDN_Date",
                              "oinvnum": "Initial_Inv_CNDN_No",
                              "oinvdt": "Initial_Inv_CNDN_Date",
                              "boedt": "Bill_Of_Entry_Date",
                              "isamd": "Amended_Y_N",
                              "recdt": "Record_Date",
                              "refdt": "IceGate_Ref_Date",
                              "boenum": "Bill_Of_Entry_No",
                              "portcode": "Port_Code"}, inplace=True)



# Create your views here.
def index(request):
    if request.method =='POST':
        c_form=MyfileuploadForm(request.POST, request.FILES)
        if c_form.is_valid():

             the_files=c_form.cleaned_data['files_data']
             file_upload(file_name="file",my_file=the_files).save()
             a= "C:\\Users\\SHUBHAM\\PycharmProjects\\GSTR2B Json to excel\\myproj\\media\\"
             b=str(the_files)
             c=a+b



             warnings.filterwarnings('ignore')
             try:
                 from io import BytesIO as IO
             except ImportError:
                 from io import StringIO as IO


             excel_file = IO()

             writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')

             df_impg = pd.DataFrame()
             df_isd = pd.DataFrame()
             df_cdnr = pd.DataFrame()
             df_cdnra = pd.DataFrame()
             df_b2b = pd.DataFrame()
             df_b2ba = pd.DataFrame()


             with open(c) as json_file:
                 data = json.load(json_file)

                 main_data = data["data"]['docdata']

                 return_period = data["data"]["rtnprd"]
                 rec_gstin = data["data"]["gstin"]


                 for i in main_data.keys():


                     if i == "b2b":

                         print(f"Fetching the {i} data, Please wait for some time...!!")
                         b2b_data = main_data[i]
                         dic_b2b = expand_list(b2b_data)

                         try:

                             df_b2b = pd.DataFrame(dic_b2b)
                         except ValueError:
                             df_b2b = pd.DataFrame(dic_b2b, index=[0])

                         df_b2b["GSTR2B_Table"] = i
                         df_b2b["rtnprd"] = return_period
                         df_b2b["gstin"] = rec_gstin
                         df_b2b["Json File Name"] = c

                         df_b2b.to_excel(writer, sheet_name=str(i + '_data'), index=False)

                         rename_2b_columns(df_b2b)



                     elif i == "b2ba":


                         b2ba_data = main_data[i]
                         dic_b2ba = expand_list(b2ba_data)

                         try:
                             df_b2ba = pd.DataFrame(dic_b2ba)
                         except ValueError:
                             df_b2ba = pd.DataFrame(dic_b2ba, index=[0])

                         df_b2ba["GSTR2B_Table"] = i
                         df_b2ba["rtnprd"] = return_period
                         df_b2ba["gstin"] = rec_gstin
                         df_b2ba["Json File Name"] = c

                         df_b2ba.to_excel(writer, sheet_name=str(i + '_data'), index=False)

                         rename_2b_columns(df_b2ba)





                     elif i == "cdnr":

                         cdnr_data = main_data[i]
                         dic_cdnr = expand_list(cdnr_data)

                         try:
                             df_cdnr = pd.DataFrame(dic_cdnr)
                         except ValueError:
                             df_cdnr = pd.DataFrame(dic_cdnr, index=[0])

                         df_cdnr["GSTR2B_Table"] = i
                         df_cdnr["rtnprd"] = return_period
                         df_cdnr["gstin"] = rec_gstin
                         df_cdnr["Json File Name"] = c

                         df_cdnr.to_excel(writer, sheet_name=str(i + '_data'), index=False)

                         rename_2b_columns(df_cdnr)





                     elif i == "cdnra":

                         cdnra_data = main_data[i]
                         dic_cdnra = expand_list(cdnra_data)

                         try:
                             df_cdnra = pd.DataFrame(dic_cdnra)
                         except ValueError:
                             df_cdnra = pd.DataFrame(dic_cdnra, index=[0])

                         df_cdnra["GSTR2B_Table"] = i
                         df_cdnra["rtnprd"] = return_period
                         df_cdnra["gstin"] = rec_gstin
                         df_cdnra["Json File Name"] = c

                         df_cdnra.to_excel(writer, sheet_name=str(i + '_data'), index=False)

                         rename_2b_columns(df_cdnra)



                     elif i == "isd":

                         isd_data = main_data[i]
                         dic_isd = expand_list(isd_data)

                         try:
                             df_isd = pd.DataFrame(dic_isd)
                         except ValueError:
                             df_isd = pd.DataFrame(dic_isd, index=[0])

                         df_isd["GSTR2B_Table"] = i
                         df_isd["rtnprd"] = return_period
                         df_isd["gstin"] = rec_gstin
                         df_isd["Json File Name"] = c

                         df_isd.to_excel(writer, sheet_name=str(i + '_data'), index=False)

                         rename_2b_columns(df_isd)



                     elif i == "impg":

                         impg_data = main_data[i]
                         dic_impg = expand_list(impg_data)

                         try:
                             df_impg = pd.DataFrame(dic_impg)
                         except ValueError:
                             df_impg = pd.DataFrame(dic_impg, index=[0])

                         df_impg["GSTR2B_Table"] = i
                         df_impg["rtnprd"] = return_period
                         df_impg["gstin"] = rec_gstin
                         df_impg["Json File Name"] = c

                         df_impg.to_excel(writer, sheet_name=str(i + '_data'), index=False)

                         rename_2b_columns(df_impg)


                     else:

                         pass



             combined_2b = pd.concat([df_b2b, df_b2ba, df_cdnr, df_cdnra, df_isd, df_impg])



             combined_2b.to_excel(writer, sheet_name="effcorp_all_combined", index=False)



             writer.save()
             writer.close()


             excel_file.seek(0)


             response = HttpResponse(excel_file.read(),
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


             response['Content-Disposition'] = 'attachment; filename=GSTR2B_Excel.xlsx'

             return response




        else:
            return HttpResponse("Error")

    else:

        context = {
            'form': MyfileuploadForm()
        }
    return render(request, 'index.html', context)


