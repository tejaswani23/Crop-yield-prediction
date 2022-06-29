from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
model=joblib.load('MODELFORPREDICT1.pkl')

from .form import *
l=LabelEncoder()
# Create your views here.

def index(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html',{'section':'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form =UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

def predict(request):
    return render(request,'predict.html')

def prediction(request):
    if request.method == "POST":
        temp={}
        temp['Year']=request.POST['Year']
        average_rain_fall_mm_per_year=request.POST['average_rain_fall_mm_per_year']
        pesticides_tonnes=request.POST['pesticides_tonnes']
        avg_temp=request.POST['avg_temp']
        Area=request.POST['area']
        Item=request.POST['item']

        temp['average_rain_fall_mm_per_year']=float(average_rain_fall_mm_per_year)
        temp['pesticides_tonnes']=float(pesticides_tonnes)
        temp['avg_temp']=float(avg_temp)
    
    df=pd.read_csv('crop_yield_df.csv')
    area=l.fit_transform(df['Area'])
    res = {}
    for cl in l.classes_:
        res.update({cl:l.transform([cl])[0]})
        res
    
    area=res[Area]
    temp['area']=area

    print(area)
   
    item=l.fit_transform(df['Item'])
    ans={}
    for cl in l.classes_:
        ans.update({cl:l.transform([cl])[0]})
        ans
    
    item=ans[Item]
    temp['item']=item
   
    print(item)
    data=pd.DataFrame({'x':temp}).transpose()
    print(data)
    predictvalue=model.predict(data)[0]
    context={'predictvalue':predictvalue}
    return render(request,'value.html',context)