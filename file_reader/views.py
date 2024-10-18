# import pandas as pd
# from django.shortcuts import render
# from .forms import UploadFileForm
# from .models import UploadedFile

# def upload_file(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
#         df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)

#         # Process data
#         total_rows = df.shape[0]
#         column_names = df.columns.tolist()
#         unique_states = df['Cust State'].unique().tolist()
#         unique_states = list(set(unique_states))

#         total_dpd = df['DPD'].sum()
#         average_dpd = df['DPD'].mean()
#         max_dpd = df['DPD'].max()
#         min_dpd = df['DPD'].min()

#         # Save file info to the database
#         uploaded_file = UploadedFile(file_name=file.name)
#         uploaded_file.save()

#         # Render summary
#         return render(request, 'upload/summary.html', {
#             'total_rows': total_rows,
#             'column_names': column_names,
#             'unique_states': unique_states,
#             'total_dpd': total_dpd,
#             'average_dpd': average_dpd,
#             'max_dpd': max_dpd,
#             'min_dpd': min_dpd,
#         })
#     else:
#         return render(request, 'upload/upload.html')  # Render the upload page


from django.shortcuts import render
import pandas as pd
from .models import UploadedFile

def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return render(request, 'upload/error.html')
        
        file = request.FILES['file']
        df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)

        df.columns = df.columns.str.replace(' ', '_')
        total_rows = df.shape[0]
        column_names = df.columns.tolist()
        unique_states = df['Cust_State'].unique().tolist()
        unique_states = list(set(unique_states))

        total_dpd = df['DPD'].sum()
        average_dpd = df['DPD'].mean()
        max_dpd = df['DPD'].max()
        min_dpd = df['DPD'].min()

        uploaded_file = UploadedFile(file_name=file.name)
        uploaded_file.save()

        return render(request, 'upload/summary.html', {
            'data': df.to_dict(orient='records'),
            'total_rows': total_rows,
            'column_names': column_names,
            'unique_states': unique_states,
            'total_dpd': total_dpd,
            'average_dpd': average_dpd,
            'max_dpd': max_dpd,
            'min_dpd': min_dpd,
        })
    else:
        return render(request, 'upload/upload.html')
