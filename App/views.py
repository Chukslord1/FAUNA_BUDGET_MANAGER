from django.shortcuts import render,redirect
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import hashlib
import datetime
from django.contrib import messages
# Create your views here.

client = FaunaClient(secret="fnAEI01JP1ACAXhfMTMg4iB2TDHHTuLgLYCVxs-i")

def index(request):
    if request.method=="POST":
        income=int(request.POST.get("income"))
        rent=int(request.POST.get("rent"))
        food=int(request.POST.get("food"))
        utilities=int(request.POST.get("utilities"))
        insurance=int(request.POST.get("insurance"))
        date=request.POST.get("date")
        extra=income-(rent+food+utilities+insurance)
        save=20*income/100
        if extra>0:
            if extra>save:
                advice= "Your expenditure rate is very good keep it up 😉. At this rate you going to be rich 💸💸. You have an extra $"+str(extra)
            else:
                advice= "Your expenditure rate is just fine 😀. You have $"+str(extra)+" . You should try to save atleast "+" $"+str(save)+" "
        else:
            advice= "Your expenditure rate is very poor 😣 . At this rate you might go broke. You have $"+str(extra)+" . You should try to save atleast "+" $"+str(save)+" "
        try:
            report_date = client.query(q.get(q.match(q.index("report_index"), date)))
            messages.add_message(request, messages.INFO, 'Report Already Exists')
            return redirect("App:index")
        except:
            book = client.query(q.create(q.collection("Budget_Report"), {
                "data": {
                    "monthly_income":income,
                    "rent": rent,
                    "food": food,
                    "utilities":utilities,
                    "insurance":insurance,
                    "date":date,
                    "extra":extra,
                    "advice":advice,
                    "report":"True"
                }
            }))
            messages.add_message(request, messages.INFO, 'Report Created Successfully')
            return redirect("App:index")

    try:
        check_report= client.query(q.paginate(q.match(q.index("report_index"), datetime.datetime.today().strftime("%Y-%m"))))
        previous_report= client.query(q.paginate(q.match(q.index("report_previous_index"), "True")))
        all_reports=[]
        previous_reports=[]
        for i in check_report["data"]:
            all_reports.append(q.get(q.ref(q.collection("Budget_Report"),i.id())))
        for j in previous_report["data"]:
            if q.get(q.ref(q.collection("Budget_Report"),j.id())) in all_reports:
                pass
            else:
                previous_reports.append(q.get(q.ref(q.collection("Budget_Report"),j.id())))
        reports=client.query(all_reports)
        previous_reports=client.query(previous_reports)
        context={"reports":reports,"previous_reports":previous_reports}
        return render(request,"index.html",context)
    except:
        return render(request,"index.html")
