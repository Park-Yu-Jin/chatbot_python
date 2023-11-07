from django.shortcuts import render
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
from .chatchat import cut,select_city,search_edu,record,search_job,search_ai
from django.http import JsonResponse
import random
# Create your views here.
def main(request):
    return render(request,'main.html')

output = dict()
response = dict()

@csrf_exempt
def chat_service(request):
    global output
    global response
    if request.method == 'POST':
        if "btn_sound" in request.POST:
            a=record()
            output = dict()
            output['response'] = a
            return JsonResponse(output)
        
        else:
            input1 = request.POST['input1']
            cutt = []
            cutt = cut(input1)

            if '교육'in cutt or '학원' in cutt :
                for i in range(len(cutt)):
                    end_city = select_city(cutt[i])
                    if len(end_city) != 0:  
                        break 
                edu = search_edu(end_city)
                response = edu
                output = dict()
                output['response'] = []
                output['urls'] = []
                output['index'] = "교육"
            
                for i in range(len(response)):
                    
                    output['response'].append(f"{i+1}번 교육과정은 {response[i]['SUBTITLE']}에서 진행하는 {response[i]['TITLE']}입니다.<br><br>")
                    output['urls'].append(f"<div class='box'><a href='{response[i]['URL']}'target='_blank'><button class='box1'>출발~</button></a></div>")
                return JsonResponse(output)
            elif '후기' in cutt:
                print(cutt)
                num = int(re.sub(r'[^0-9]','',str(cutt)))
                num = num - 1
                ko = search_ai(response[num]['SUBTITLE'])
                output['response']= []
                output['urls']=[]
                output['index'] = "후기"
                for i in range(3):
                    j = random.randint(0,9)
                    output['response'].append(f"{i+1}번 후기 블로그는 {ko[j]['blogname']}입니다.")
                    output['urls'].append(f"<div class='box'><a href='{ko[j]['url']}' target='_blank'><button class='box1'>출발~</button></a></div>")
                
                return JsonResponse(output)

            elif '취업' in cutt  or '일자리' in cutt or '구직' in cutt : 
                for i in range(len(cutt)):
                    end_city = select_city(cutt[i])
                    if len(end_city) != 0:  
                        break
                job = search_job(end_city)
                response = job
                output = dict()
                output['response'] = []
                output['urls'] = []
                output['index'] = "취업"

                for i in range(len(response)):
                   
                    output['response'].append(f"{i+1}번 취업공고는 {response[i]['company']}에서 {response[i]['position']}을 뽑습니다.<br><br>")
                    output['urls'].append(f"<div class='box'><a href='{response[i]['url']}'target='_blank'><button class='box1'>출발~</button></a></div>")
                    
                return JsonResponse(output)
            else:
                output['response'] = []
                output['index'] = "오류"
                output['response'].append("올바르게 입력해주세요 ex)○○시 ○○을 알려줘")
                print(output)
                return JsonResponse(output)
    else:
        return render(request, 'chat_test.html')