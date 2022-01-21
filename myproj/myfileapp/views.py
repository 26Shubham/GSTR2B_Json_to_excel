import pandas as pd
from django.shortcuts import render,HttpResponse

from .forms import MyfileuploadForm

from .models import file_upload

import pandas as pd


# Create your views here.
def index(request):
    if request.method =='POST':
        c_form=MyfileuploadForm(request.POST, request.FILES)
        if c_form.is_valid():
             name=c_form.cleaned_data['file_name']
             the_files=c_form.cleaned_data['files_data']
             file_upload(file_name=name,my_file=the_files).save()

             df_output = pd.read_excel(the_files)
             print(df_output)
             df_output['New'] = "a"
             print(df_output)

             try:
                 from io import BytesIO as IO  # for modern python
             except ImportError:
                 from io import StringIO as IO  # for legacy python



             # my "Excel" file, which is an in-memory output file (buffer)
             # for the new workbook
             excel_file = IO()

             xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')

             df_output.to_excel(xlwriter, 'sheetname',encoding='latin-1')

             xlwriter.save()
             xlwriter.close()

             # important step, rewind the buffer or when it is read() you'll get nothing
             # but an error message when you try to open your zero length file in Excel
             excel_file.seek(0)

             # set the mime type so that the browser knows what to do with the file
             response = HttpResponse(excel_file.read(),
                                     content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

             # set the file name in the Content-Disposition header
             response['Content-Disposition'] = 'attachment; filename=myfile.xlsx'

             return response



        else:
            return  HttpResponse("Error")

    else:

        context={
            'form':MyfileuploadForm()
    }
        return render(request,'index.html',context)


