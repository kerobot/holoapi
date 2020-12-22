import datetime

class Holodule:
    codes = {
        "ときのそら"  : "HL0001",
        "ロボ子さん" : "HL0002",
        "さくらみこ" : "HL0003",
        "星街すいせい" : "HL0004",
        "夜空メル" : "HL0101",
        "アキ・ローゼンタール" : "HL0102",
        "赤井はあと" : "HL0103",
        "白上フブキ" : "HL0104",
        "夏色まつり" : "HL0105",
        "湊あくあ" : "HL0201",
        "紫咲シオン" : "HL0202",
        "百鬼あやめ" : "HL0203",
        "癒月ちょこ" : "HL0204",
        "大空スバル" : "HL0205",
        "大神ミオ" : "HL0G02",
        "猫又おかゆ" : "HL0G03",
        "戌神ころね" : "HL0G04",
        "兎田ぺこら" : "HL0301",
        "潤羽るしあ" : "HL0302",
        "不知火フレア" : "HL0303",
        "白銀ノエル" : "HL0304",
        "宝鐘マリン" : "HL0305",
        "天音かなた" : "HL0401",
        "桐生ココ" : "HL0402",
        "角巻わため" : "HL0403",
        "常闇トワ" : "HL0404",
        "姫森ルーナ" : "HL0405",
        "獅白ぼたん" : "HL0501",
        "雪花ラミィ" : "HL0502",
        "尾丸ポルカ" : "HL0503",
        "桃鈴ねね" : "HL0504",
        "魔乃アロエ" : "HL0505"
    }

    def __init__(self, video_id="", datetime=None, name="", title="", url="", description=""):
        self.__video_id = video_id
        self.__datetime = datetime
        self.__name = name
        self.__title = title
        self.__url = url
        self.__description = description

    # キー
    @property
    def key(self):
        _code = Holodule.codes[self.name] if self.name in Holodule.codes else ""
        _dttm = self.datetime.strftime("%Y%m%d_%H%M%S") if self.datetime is not None else ""
        return _code + "_" + _dttm if ( len(_code) > 0 and len(_dttm) > 0 ) else ""

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
        holodule = Holodule(doc['video_id'], 
                            datetime.datetime.strptime(doc['datetime'], '%Y%m%d %H%M%S'), 
                            doc['name'], 
                            doc['title'], 
                            doc['url'], 
                            doc['description'])
        return holodule

    # ドキュメントへ変換
    def to_doc(self):
        doc = { 'key': str(self.key),
                'video_id': str(self.video_id),
                'datetime' : str(self.datetime.strftime("%Y%m%d %H%M%S")),
                'name' : str(self.name),
                'title' : str(self.title),
                'url' : str(self.url),
                'description' : str(self.description) }
        return doc