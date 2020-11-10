# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import datetime
from .models import *
from .utilities_notion import *
from .stt import *
from .forms import *
from .summarize import *
from .extract_date import *
from .calendar_true import *


def index(request):
    # return HttpResponse("Hello, world.")
    return render(request,'wow/index.html')


def input_info(request):
    return render(request,'wow/input_info.html')

def creating(request):
    if request.method == "POST":
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            title = form.cleaned_data['title']
            date = form.cleaned_data['date']
            members = form.cleaned_data['members']
            tag = form.cleaned_data['tag']
            wav = form.cleaned_data['wav'].name

            stt_try = STT()
            stt_result = stt_try.speech_recognize_continuous_from_file(filename='/home/lab05/A1B4/wow/static/wow/media/' + wav)

            context = {
                'title' : title,
                'date' : date,
                'members' : members,
                'tag' : tag,
                'stt_result' : stt_result,
            }

            return render(request, 'wow/summary_result.html', context)
        else:
            return HttpResponse("Form Failed")

def sum(request):
    if request.method == "POST":
        title = request.POST['title']
        date = request.POST['date']
        members = request.POST['members']
        tag = request.POST['tag']
        method = request.POST['method']
        stt_result = request.POST['stt_result']
        if method =='옵션1':
            num = request.POST['num1']
            num = int(num)
        else :
            num = request.POST['num2']
            num = int(num)/100
        summ = Summarize(stt_result, num)
        res_lexrankr = summ.summarize()
        res_lexrankr = '\n'.join(res_lexrankr)
        
        res_bertsum = summ.bertSum()
        
        context = {
            'title': title,
            'date': date,
            'members': members,
            'tag': tag,
            'method' : method,
            'stt_result' : stt_result,
            'res_lexrankr' : res_lexrankr,
            'res_bertsum' : res_bertsum,
        }
        return render(request, 'wow/summary_result.html', context)
    else:
        return HttpResponse("Form Failed")

def report(request):
    if request.method == "POST":
        title = request.POST['title']
        date = request.POST['date']
        members = request.POST['members']
        tag = request.POST['tag']
        var = request.POST['var']
        if var == 'Select':
            res = request.POST['res_lexrankr']
        else :
            res = request.POST['res_bertsum']
        stt_result = request.POST['stt_result']
        event = Date(date, stt_result)
        event_list = event.preprocessing()
        event_list = event_list[:3] # 3개까지만
        context = {
            'title': title,
            'date': date,
            'members': members,
            'tag': tag,
            'res' : res,
            'stt_result' : stt_result,
            'event_list':event_list,
        }
        print(title)
        return render(request, 'wow/report.html', context)
    else:
        return HttpResponse("Form Failed")


def summary_result(request):
    return render(request,'wow/summary_result.html')

def show_report(request):
    title = '중간 발표 관련 회의'
    date = '2020년 11월 6일'
    members = '지니, 재니, 태니'
    tag = '주간회의'
    stt_result = '''
    1월 1일에 봐요. 목요일이요 그때가 언제냐면 저희가 일단 지금 보려고 하는 게 그니까 그래서 말씀 드릴 게 있잖아요? 네네. 일요일은요.
    '''
    # '''
    # 여러분 회의 시작할게요. 제 소리가 들리면 마이크를 모두 켜주세요. 네. 일단 진행 상황부터 1번 씩 얘기해 볼까요? 누가 먼저 얘기 하실래요? 얘기하고 싶으신 분 계신가요? 저는 일단 전에 하던 추상적 요약 계속하고 있어요. 버트 한국 버전 하시던 거 말씀하시는 건가요? 네. 그때 김태엽씨 두어서 하기로 했던 케이시 버트 구현하고 있어요. 일단 예제로 코드 올린 게 있어서 그대로 둘러보고요. 중간 중간에 gpu 관련 코드가 있어서 지워주고 돌렸는데 에포크 1번 보는데 시간이 너무 오래 걸리네요. 아, 그래요? 어느정도 걸리는지 말씀해 주실 수 있나요? 어, 지금도 콜백으로 계속 돌리고 있는데 1번 볼 때 30분 정도 소요되는 것 같아요. 아마 계속 돌리면 시간이 좀 걸릴 거예요. 그거 혹시 어디서 돌리고 있어요? 저희 멀티캠 에서 제공해준 aws 서버에서도 돌려 봤나요? 아니요. 저는 일단 콜에서 돌리고 있는데 아마 aws 랑 불리는 시간은 비슷할 것 같아요. 음, 그러면 돌릴 때 얼마나 걸릴 것 같으세요? 저희 이번주 금요일에 발표 해야 되는데 그때까지 가능할까요? Colab 서버가 근데 최대 12시간 까지 더럽게 못 써서 모델을 중간 중간 저장 해야 할 것 같아요. 일단 모델이 졸업하기 하니까 금요일까지 끝낼 수 있을 것 같아요. 좋아요. 그러면 중간에 하다가 또 어려운 거 있으면 말씀해주세요. 네. 그럼 재경부 만 하다는 거 계속 해주시면 될 것 같고 다음으로 얘기해 주실 분 계신가요? 저도 재경이랑 같이 코버트 관련 코드 계속 보고 있었어요. 어 예제의 감정 분석적으로 버트 모드를 구현한 게 있어서 보고 있는데요. 감정 분석 관련해서 참조 코드가 있어서 모델이 돌아가기는 하는데 저도 시간이 좀 많이 걸려요. 그리고 지금 결국엔 저희가 요양 모델이 랑 퍼트를 결합하려면 디코더를 만들어야 하는데 이 부분을 구현할 수 있을지 잘 모르겠어요. 응, 그럼 추가적으로 시간이 더 필요하신 건가요? 정확히 어떤 부분이 어려운지 말씀해 주실 수 있나요? 어, 이걸 처음부터 끝까지? 디코더를 코드로 짝인 힘들 것 같아서 지금 깃허브 를 몇 군데 찾아봤는데? 코드가 클래스와 되어 있어서 여러 파일에 디코더 관련 함수가 섞여 있더라구요. 그래서 어떤 코드를 가져와 할지 아직은 정확히 모르겠습니다. 또 코드가 모두 파이터즈 로 구성돼 서 더 보기가 힘든 것 같아요. 일단 그러면 태엽 님도 이번 주까지 최대한 해보시고 만약 우연히 힘들 것 같으면 다른 방안을 검토해 주시면 좋겠습니다. 네네, 알겠습니다. 그 다음에 감독님이 네 과장님 하고 계신 업무가 정확히 보였죠. 저는 계속해서 캘린더 연동 관련 업무를 진행 중입니다. 그때 구글 계정 키 관련해서 문제가 있었는데. 열한 님이 보내주신 코드 갖고 해결했습니다. 이제 연동하기 만 하면 되는데 위에 올려 봐야 정확히 되는지 알 수 있을 것 같습니다. 혹시 얘네 올려 봐야 한다는 말이 무슨 뜻인가요? 이게 지금 로컬 호스트 관련 url 을 제국을 포털에서 등록해 줘야 하는데, 제 로컬 환경에서 수행할 작업이 없어 리다이렉션 이 안 되더라고요. 제가 왜 관련해서 잘 몰라서 그러는데 장고 환경에서도 URL 이나 주소 같은 게 있나요? 아이디 주소 같은 게 있나요? 정확히 옳은 않은 코드에 대해서 혹시 화면 공유 해 주실 수 있나요? 아니면 있다. 회의 끝나고 제가 1번 같이 봐드릴게요. 내 감사합니다. 회의 끝나고 우리는 코드 드라이브에 올려드릴게요. 이렇게 서로 돕는 모습 너무 보기 좋습니다. 광덕 님 혹시 그 외 만들기로 했던 것은 진행이 됐을까요? 생각보다 캘린더 관련 오류가 해결이 잘 안 돼서 롤 모델은 아직 시작하지 못했어요. 그리고 저희 날짜 관련 텍스트 변환 해주는 기능은 캘린더 연동이 되고 나서 하는 게 맞는 것 같아요. 아, 그런가요? 저는 날짜 변환 기능 만들고 캘린더 운동하는 걸 생각했는데 서로 전달이 잘못 됐나 보네요. 우선 저희가 지금 11월 11일 까지시간이 얼마 안남아서 캘린더 연동이 끝나시면 날짜 표시해주는 기능 되는 데까지 봐주시고. 맨 마지막에 시간만 해도 괜찮을 것 같아요. 네, 알겠습니다. 우선 내일 캘린더 연동 관련해서 혜원 씨랑 같이 봐보고 이 작업이 끝나는 대로 날짜 관련 기능 시작할게요. 내 좋습니다. 담은 혜원 씨랑 저랑 봤던 부분인데 저희가 만든 거 화면 공유 일단 해드릴게요. 저희는 우선 잔고를 디자인을 계속하고 있어요. 회원 시가 조금 더 자세히 설명해 주실 수 있나요? 네. 일단 저희는 전체적인 디자인 구조를 짜는 것부터 했습니다. 우선 처음 페이지에는 회의 참가자 회의 날짜와 같은 정보가 적이고 밑에 이렇게 회의록 녹음 파일을 첨부할 수 있게 만들었습니다. 여기에 녹음 파일을 넣고 stt 를 돌리면 텍스트가 나오고 그 다음 페이지에서 저희는 추출 쩍 추상적 요약 내용을 보여주려고 합니다. 그리고 마지막 페이지에서 캘린더에 각 날짜에 해당하는 정보들을 적어주고 노선과 연동시키는 작업까지 해줄 예정입니다. 그러면 저기 보이는 게 아직 구현은 안되고 디자인만 된 건가요? 네 맞습니다. 저렇게 짜 놓고 저희가 잔고 서버 에다가 stt 라든지 요약 관련 기능 같은 걸 하나씩 추가해 주면 됩니다. 디자인 부분은 얼추 다 끝나고 나서 저랑 혜원 씨는 오늘 장고에 어떻게 기능들을 추가 하는지 알아보고 있겠습니다. 콧대가 완성된 게 있으면 저희가 테스트 해볼 테니까 바로 알려주세요. 롱 오늘 회의는 여기서 끝인가요? 아, 맞다. 저희 오프라인으로 이번 주에 1번 봐야 되지 않을까요? 다들 괜찮은 날짜에 있으신가요? 없으시면 투표 하겠습니다. 저는 이번 주 금요일 안 될 것 같고 나머지는 괜찮습니다. 도는 이번 주말에 코딩 테스트가 있어서 그 때만 안되고 나머지는 다 돼요. 저도 이번 주 월요일이랑 주말은 코딩 테스트가 있어서 안되고 다른 날짜는 괜찮을 것 같아요. 그러면 다들 평일이 괜찮으니까 수요일 어떠신가요? 네 좋습니다. 내 그러면 10월 28일로 하고 시간은 열시 괜찮으신가요? 에. 내 좋습니다. 혹시 까먹을 수도 있으니까 주셨네? 제가 일정이 랑 이번주 각자 맡아서 할 일을 적어 돌려놓을게요. 저흰 노션 꼭 이용해 주시고 이후에도 작업 끝난 거 있으면 꼭 기록으로 남겨 주세요. 네, 알겠습니다. 내. 그럼 오늘 회 여기서 마치도록 할게요. 중간에 혹시 도와야 할 있으면 소집할 시고 저희 오프라인 회의 10월 28 일 일이니까 꼭 까먹지마라 주세요. 다들 고생하셨습니다. 
    # '''
    res = '''
    감정 분석 관련해서 참조 코드가 있어서 모델이 돌아가기는 하는데 저도 시간이 좀 많이 걸려요
    그리고 저희 날짜 관련 텍스트 변환 해주는 기능은 캘린더 연동이 되고 나서 하는 게 맞는 것 같아요
    우선 저희가 지금 11월 11일 까지 시간이 얼마 안남아서 캘린더 연동이 끝나시면 날짜 표시해주는 기능 되는 데까지 봐주시고
    우선 내일 캘린더 연동 관련해서 혜원 씨랑 같이 봐보고 이 작업이 끝나는 대로 날짜 관련 기능 시작할게요
    디자인 부분은 얼추 다 끝나고 나서 저랑 혜원 씨는 오늘 장고에 어떻게 기능들을 추가 하는지 알아보고 있겠습니다
					
    '''
    event = Date(date, stt_result)
    event_list = event.preprocessing()
    event_list = event_list[:3]
    # dl = []
    # sl = []
    # for a, b in event_list:
    #     dl.append(a)
    #     sl.append(b)
    print(event_list)
    # print(sl)
    
    context = {
        'title': title,
        'date': date,
        'members': members,
        'tag': tag,
        'res' : res,
        'stt_result' : stt_result,
        'event_list':event_list,
        # 'dl':dl,
        # 'sl':sl,
    }
    return render(request, 'wow/report.html', context)

def notion_share(request):
    if request.method == "POST":
        summary_result = request.POST['summary_res']
        print(request.POST.keys())
        title = request.POST['title']
        date = '-'.join([ymd[:-1] for ymd in request.POST['date'].split()])

        notion_try = notion(title, date, summary_result)
        notion_result = notion_try.notion_temp()

        # return HttpResponse(notion_result)
        return redirect(notion_result)   
    else:
        return HttpResponse("Form Failed")
    
def calendar_share(request):
    if request.method == "POST":
        # e_l = request.POST['e_l']
        d = request.POST['d']
        e = request.POST['e']

        d = d.split()
        date_num = []
        for n in d:
            date_num.append(int(re.sub('[^0-9]','',n)))
        d = datetime.date(date_num[0], date_num[1], date_num[2])

        e_l = [d,e]
        # print(e_l)
        calendar_obj = calendar_google()
        due_list = calendar_obj.making_due_list(e_l)
        event = calendar_obj.insert_event(due_list)
        link = event.get('htmlLink')

        return redirect(link)   
    else:
        return HttpResponse("Form Failed")
# python manage.py makemigrations
# python manage.py migrate