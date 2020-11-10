from notion.block import CollectionViewBlock, PageBlock, TodoBlock, TextBlock
from notion.client import NotionClient
from datetime import datetime

# notion github참고 : https://github.com/raphodn/know-your-planet/blob/master/api/admin.py

class notion:
    def __init__(self, title, date, summary_result):
        self.title = title
        self.date = date
        self.summary_result = summary_result

    def notion_temp(self):
        token_v2 = '' #notion 사용자 고유의 토큰 주소
        client = NotionClient(token_v2=token_v2)

        url = '' #자동으로 입력할 noiton 페이지
        page = client.get_block(url)

        # 표 새로 만들고 저장
        child = page.children.add_new(CollectionViewBlock)
        child.collection = client.get_collection(
            client.create_record(
                "collection", parent=child, schema={
            "title": {"name": "내용", "type": "title"},
            "date": {"name": "날짜", "type": "date"}
        })
            )
        child.title = '2020년도 회의록'
        child.views.add_new(view_type="table")

        row = child.collection.add_row()
        row.set_property('title', self.title)
        row.set_property('date', datetime.strptime(self.date, '%Y-%m-%d'))

        text = row.children.add_new(TextBlock)
        text.title = self.summary_result
        
        return url