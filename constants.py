from database.models import periodDict

maxDay = 12
deptDict = {
    # 內科部
    '020': u'一般內科',
    '021': u'胸腔內科暨重症科',
    '022': u'胃腸肝膽科',
    '023': u'心臟血管科',
    '024': u'腎臟內科',
    '025': u'過敏免疫風濕科',
    '027': u'感染科',
    '028': u'血液腫瘤科',
    '029': u'代謝科',
    '029A': u'糖尿病特診',
    '120': u'神經內科',

    # 外科部
    '030': u'一般外科',
    '030A': u'減重外科',
    '030C': u'甲狀腺特診',
    '031': u'心臟血管外科',
    '031A': u'靜脈曲張特診',
    '032': u'整形外科',
    '034': u'胸腔外科',
    '035': u'大腸直腸外科',
    '037': u'乳房外科',
    '038': u'外傷科',
    '070': u'神經外科',
    '080': u'泌尿外科',

    # 兒童醫學部
    '040': u'兒童醫學部',
    '040A': u'健兒門診',
    '042': u'兒童胃腸科',
    '043': u'兒童心臟科',
    '044': u'兒童過敏免疫科',
    '045': u'兒童內分泌',
    '045A': u'兒童遺傳代謝科',
    '046': u'兒童腦神經科',
    '047': u'兒童感染科',
    '048': u'兒童腎臟科',
    '049': u'小兒血液腫瘤科',
    '033': u'小兒外科',

    # 骨科部
    '060': u'骨科',
    '062': u'骨科手外科',
    '063': u'踝及足外科',
    '065': u'脊椎外科',
    '066': u'運動醫學及肩肘外科',
    '067': u'關節重建科',
    '068': u'骨折外傷科',
    '069': u'小兒骨科',

    # 婦產部
    '050': u'婦產科',

    # 中醫部
    '620': u'中醫科',

    # 精神科
    '130': u'精神科',
    '133': u'兒童心理衛生門診',

    # 臨床心理中心
    '135A': u'身心壓力諮詢',
    '135B': u'兒青心智門診',

    # 獨立科
    '010': u'家庭醫學科',
    '010B': u'老人醫學科',
    '010C': u'緩和醫療門診',
    '0131': u'子宮頸抹片特別門診',
    '039': u'醫學美容(自費)',
    '090': u'耳鼻喉科',
    '100': u'眼科',
    '110': u'皮膚科',
    '140': u'復健科',
    '230': u'職業醫學科',
    '400': u'牙科',
    '401': u'口腔外科',
    '40A': u'特殊需求牙科',
    '811': u'疼痛科',
    '821': u'放射腫瘤科',
    '840': u'核醫科',
    'HSJ': u'戒菸門診',
}

scrapUrlPrefix = dict(
    status = 'http://59.125.231.55/trews/api/GetDptRoomInfo?DptID=',
    # status = 'http://www2.cs.ccu.edu.tw/~wth105u/cralwerData/server.php?id=',
    schedule = 'http://www2.cych.org.tw/WebToNewRegister/webSerchDrSch.aspx?No=',
)

schedulePeriodList = [
    dict(
        payload = 'lblMRest',
        period = periodDict['morning'],
    ),
    dict(
        payload = 'lblARest',
        period = periodDict['afternoon'],
    ),
    dict(
        payload = 'lblNRest',
        period = periodDict['night'],
    ),
]