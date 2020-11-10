from django.urls import path

from . import views

app_name = 'wow'

urlpatterns = [
    path('', views.index, name='index'),
    path('input_info/', views.input_info, name='input_info'),
    path('input_info/creating', views.creating, name='creating'), # stt 해주는 부분
    path('input_info/sum', views.sum, name='sum'), # lexrank 결과
    path('summary_result/', views.summary_result, name='summary_result'), # 요약 나오는 부분(지금은 안 쓰지만 일단 냅둠)
    path('report_result/', views.show_report, name='report_result'), # report page
    path('report/', views.report, name='report'), # 최종 보고서 부분
    path("notion_share/", views.notion_share, name="notion_share"), # notion
    path('report_result/calendar_goo/', views.calendar_share, name="calendar_share")
]