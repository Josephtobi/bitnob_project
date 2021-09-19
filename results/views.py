from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Lga,PollingUnit,AnnouncedLgaResults,AnnouncedPuResults,Party,Agentname

# Create your views here.

class Index(View):
    parties=Party.objects.all()
    agents=Agentname.objects.all()
    lga_list=[]
    lga_name_dict=Lga.objects.all().values('lga_name')
    for i in lga_name_dict:
        lga_list.append(i['lga_name'])
    pu_list=[]
    pu_name_dict=PollingUnit.objects.all().values('polling_unit_name')
    for i in pu_name_dict:
        pu_list.append(i['polling_unit_name'])
    context={
        'lga_list':lga_list,
        'pu_list':pu_list,
        'parties':parties,
        'agents':agents
        }


        
    
    def get(self, request):
        




        context=self.context
        return render(request, 'index.html', context=context)

    
    def post(self, request):
        ip=request.META.get("REMOTE_ADDR")
        
        target = request.POST['type']

        if target=='1':
            lga = request.POST['lga']
            lga_model=Lga.objects.filter(lga_name=lga)
            lga_name=lga_model[0].lga_name
            lga_id=lga_model[0].lga_id
            

        
            my_list=[]
            pu_lga=PollingUnit.objects.filter(lga_id=lga_id)
            for i in pu_lga:
                my_list.append(i.uniqueid)
            print(my_list)
            list_string = map(str, my_list)
            result_list=[]
            results=AnnouncedPuResults.objects.filter(polling_unit_uniqueid__in=list_string)
            

            

            
            
           





        elif target=='2':
            pu=request.POST['pu']
            pu_id=PollingUnit.objects.filter(polling_unit_name=pu)[0].uniqueid
            results=AnnouncedPuResults.objects.filter(polling_unit_uniqueid=pu_id)
            print(results)



        elif target=='3':
            party=request.POST['pa']
            result=request.POST['re']
            agent=request.POST['ag']
            date=request.POST['date']
            state='Delta'
            ip=ip
            results=''
            AnnouncedPuResults.objects.create(party_abbreviation=party,polling_unit_uniqueid=100,party_score=result,entered_by_user=agent,date_entered=date,user_ip_address=ip)



        else:
            return render(request, 'index.html', context=self.context)


        
        context={
        'lga_list':self.lga_list,
        'pu_list':self.pu_list,
        'results':results,
        'parties':self.parties,
        'agents':self.agents
        }
        return render(request, 'index.html', context=context)

