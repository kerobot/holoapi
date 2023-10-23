import datetime

class Holodule:
    def __init__(self, code="", video_id="", datetime=None, name="", title="", url="", description=""):
        self.__code = code
        self.__video_id = video_id
        self.__datetime = datetime
        self.__name = name
        self.__title = title
        self.__url = url
        self.__description = description

    # キー
    @property
    def key(self):
        _code = self.code;
        _dttm = self.datetime.strftime("%Y%m%d_%H%M%S") if self.datetime is not None else ""
        return _code + "_" + _dttm if ( len(_code) > 0 and len(_dttm) > 0 ) else ""

    # コード
    @property
    def code(self):
        return self.__code

    # video_id
    @property
    def video_id(self):
        return self.__video_id

    @video_id.setter
    def video_id(self, video_id):
        self.__video_id = video_id

    # 日時
    @property
    def datetime(self):
        return self.__datetime

    @datetime.setter
    def datetime(self, datetime):
        self.__datetime = datetime

    # 名前
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    # タイトル（Youtubeから取得）
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    # URL
    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    # 説明（Youtubeから取得）
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    # ドキュメントから変換
    @classmethod
    def from_doc(cls, doc):
        if doc is None:
            return None
        holodule = Holodule(doc['code'],
                            doc['video_id'], 
                            datetime.datetime.strptime(doc['datetime'], '%Y%m%d %H%M%S'), 
                            doc['name'], 
                            doc['title'], 
                            doc['url'], 
                            doc['description'])
        return holodule

    # ドキュメントへ変換
    def to_doc(self):
        doc = { 'key': str(self.key),
                'code': str(self.code),
                'video_id': str(self.video_id),
                'datetime' : str(self.datetime.strftime("%Y%m%d %H%M%S")),
                'name' : str(self.name),
                'title' : str(self.title),
                'url' : str(self.url),
                'description' : str(self.description) }
        return doc
