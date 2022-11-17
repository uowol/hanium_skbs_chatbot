import pandas as pd
import os
import csv
import pandas as pd
import pymongo

###########################################################불러오면되긴함
# database 연결
def connect_database(db):
    connect_to = pymongo.MongoClient("mongodb://localhost:27017")
    mdb = connect_to[db]
    return mdb

# collection 연결
def use(db, collection):
    return db[collection]

def insert(collection, data_list):
    collection.insert_many(data_list)

def find(collection, options = {}):
    searched = collection.find(options)
    return searched

def update(collection, options = {}):
    collection.update_many(options)

def delete(collection, options = {}):
    collection.delete_many(options)

db = connect_database('trip')
test   = use(db, 'test')
spot   = use(db, 'spot')

def db_to_list(collection):
    cur = find(collection)
    data_list = []
    key_names = []
    temp = []
    merged_data = []
    for doc in cur:
        data_list.append(doc)
    for i in range(len(data_list)):
        key_names.append(data_list[i].keys())
    for key in key_names:
        if key not in temp:
            temp.append(key)
    for j in range(len(temp)):
        tmp = []
        for data in data_list:
            if data.keys() == temp[j]:
                tmp.append(data)
        merged_data.append(tmp)
    return merged_data

#데이터프레임 리스트로 불러오는 함수
def to_dflist(data):
    df_list = []
    for i in range(len(data)):
        df_list.append(pd.DataFrame(data[i]))
    return df_list



def df_join(data):
    df = pd.concat(data, ignore_index=True)
    return df
#####################################################################불러올거

all = df_join(to_dflist(db_to_list(test))) # db region 모든 데이터 들고오괴


# 태깅을 위해 all에서 필요한 것만 뽑기
theme_df_1 = all[['관광지명', '지역', '주소', '합산 검색 수','분류']].dropna()
theme_df_1

# 관광지 가치가 없는 분류는 날림
del_list = ['모텔','기타쇼핑시설','면세점','쇼핑몰', '카페/찻집','호텔', '펜션/민박','전문매장/상가','펜션/민박','호스텔','콘도미니엄','교통시설','기타숙박']
for d in del_list:
    theme_df_1 = theme_df_1[theme_df_1['분류'] != d]

#하천/해양 테마
lab_1 =theme_df_1[theme_df_1['분류'] == '자연경관(하천/해양)']

theme_beach = lab_1['관광지명'].str.contains("해변|항$|해수욕장|부두|비치|방파제|포$|부두|포구$|선착장|해안|단괴|염전|항만|제방|경인항인천")
theme_lake = lab_1['관광지명'].str.contains("호$|저수지|지$|수원지|유수지|못$|호수|나루터|[^파]+제$|정$|포천화적연")
theme_swamp = lab_1['관광지명'].str.contains("늪")
theme_island = lab_1['관광지명'].str.contains("도$|섬$")
theme_sea_else = lab_1['관광지명'].str.contains("대합실|방축말방죽|수로|터미널")

df_beach = lab_1[theme_beach][['관광지명','주소', '지역','합산 검색 수']]
df_beach['태그'] = ['바다' for _ in range(len(df_beach['관광지명']))]
df_lake = lab_1[theme_lake][['관광지명','주소', '지역','합산 검색 수']]
df_lake['태그'] = ['호수' for _ in range(len(df_lake['관광지명']))]
df_swamp = lab_1[theme_swamp][['관광지명','주소', '지역','합산 검색 수']]
df_swamp['태그'] = ['늪' for _ in range(len(df_swamp['관광지명']))]
df_sea_else = lab_1[theme_sea_else][['관광지명','주소', '지역','합산 검색 수']]
df_sea_else['태그'] = ['기타_하천/해양' for _ in range(len(df_sea_else['관광지명']))]




#시장 테마
lab_2 =theme_df_1[theme_df_1['분류'] == '시장']

df_market = lab_2[['관광지명','주소', '지역','합산 검색 수']]
df_market['태그'] = ['시장' for _ in range(len(df_market['관광지명']))]

#수상 레저 스포츠
lab_3 =theme_df_1[theme_df_1['분류'] == '수상레저스포츠']
theme_fishing = lab_3['관광지명'].str.contains("낚시|피싱|손맛|어장|좌대|당진|수로")
theme_surfing = lab_3['관광지명'].str.contains("서피|비치|서핑|웨이브|서프")
theme_water_leisure = lab_3['관광지명'].str.contains("수상|스키|레포츠|레저|합천|빠지|텐파크|물레길|골든몽키")
theme_ship = lab_3['관광지명'].str.contains("요트|보트|송도코마린|마리나|모나크")
theme_overall = lab_3['관광지명'].str.contains("워터플레이|랜드|데프콘|조이몰")
theme_w_lesiure_else = lab_3['관광지명'].str.contains("조정경기장|경륜|쎄시봉|쏠티캐빈")
theme_diving = lab_3['관광지명'].str.contains("스쿠버|잠수|다이버|다이빙")

df_fishing = lab_3[theme_fishing][['관광지명','주소', '지역','합산 검색 수']]
df_fishing['태그'] = ['낚시' for _ in range(len(df_fishing['관광지명']))]
df_surfing = lab_3[theme_surfing][['관광지명','주소', '지역','합산 검색 수']]
df_surfing['태그'] = ['서핑' for _ in range(len(df_surfing['관광지명']))]
df_water_leisure = lab_3[theme_water_leisure][['관광지명','주소', '지역','합산 검색 수']]
df_water_leisure['태그'] = ['수상레포츠' for _ in range(len(df_water_leisure['관광지명']))]
df_ship = lab_3[theme_ship][['관광지명','주소', '지역','합산 검색 수']]
df_ship['태그'] = ['요트/보트' for _ in range(len(df_ship['관광지명']))]
df_overall = lab_3[theme_overall][['관광지명','주소', '지역','합산 검색 수']]
df_overall['태그'] = ['워터파크' for _ in range(len(df_overall['관광지명']))]
df_w_leisure_else = lab_3[theme_w_lesiure_else][['관광지명','주소', '지역','합산 검색 수']]
df_w_leisure_else['태그'] = ['기타 수상레저' for _ in range(len(df_w_leisure_else['관광지명']))]
df_diving = lab_3[theme_diving][['관광지명','주소', '지역','합산 검색 수']]
df_diving['태그'] = ['스쿠버다이빙' for _ in range(len(df_diving['관광지명']))]





#전시시설
lab_4 =theme_df_1[theme_df_1['분류'] == '전시시설']
theme_museum = lab_4['관광지명'].str.contains("박물관|뮤지엄|양구")
theme_inv_else = lab_4['관광지명'].str.contains("기념관|체험|수호|이응노|청와대|문학|우포|홍보|전시|주택전시장|역사|인삼|보훈|생태|전봉준|노기남관|사료|와인갤러리|문화관|자연사|기록|민속|굴|모시")
theme_science = lab_4['관광지명'].str.contains("과학|천문|에너지|로봇|로보|테크")
theme_art = lab_4['관광지명'].str.contains("아트|Gallery|미술관|갤러리|디자인|빛|예술")
theme_center = lab_4['관광지명'].str.contains("문화관|체험|박물관|뮤지엄|이응노|청와대|도자|우포|로보|양구|아트|테크|Gallery|인삼|미술관|갤러리|주택전시장|디자인|빛|예술|기념관|수호|문학|자연사|기록|모시|민속|굴|홍보|전시|역사|보훈|생태|전봉준|노기남관|사료|와인갤러리|박물관|뮤지엄|양구|과학|천문|에너지|로봇")

df_museum = lab_4[theme_museum][['관광지명','주소', '지역','합산 검색 수']]
df_museum['태그'] = ['박물관' for _ in range(len(df_museum['관광지명']))]
df_inv_else = lab_4[theme_inv_else][['관광지명','주소', '지역','합산 검색 수']]
df_inv_else['태그'] = ['기타 전시시설' for _ in range(len(df_inv_else['관광지명']))]
df_science = lab_4[theme_science][['관광지명','주소', '지역','합산 검색 수']]
df_science['태그'] = ['과학관' for _ in range(len(df_science['관광지명']))]
df_art = lab_4[theme_art][['관광지명','주소', '지역','합산 검색 수']]
df_art['태그'] = ['미술관' for _ in range(len(df_art['관광지명']))]
df_center = lab_4[~theme_center][['관광지명','주소', '지역','합산 검색 수']]
df_center['태그'] = ['종합전시센터' for _ in range(len(df_center['관광지명']))]

#캠핑
lab_5 =theme_df_1[theme_df_1['분류'] == '캠핑']
df_camping = lab_5[['관광지명','주소', '지역','합산 검색 수']]
df_camping['태그'] = ['캠핑' for _ in range(len(df_camping['관광지명']))]

#데이트코스
lab_6 =theme_df_1[theme_df_1['분류'] == '데이트코스']

df_date = lab_6[['관광지명','주소', '지역','합산 검색 수']]
df_date['태그'] = ['데이트' for _ in range(len(df_date['관광지명']))]


#종교성지
lab_7 =theme_df_1[theme_df_1['분류'] == '종교성지']
theme_shaman= lab_7['관광지명'].str.contains("군당|굿당|경수원")
theme_confu= lab_7['관광지명'].str.contains("월연정")
theme_buddhism= lab_7['관광지명'].str.contains("군당|굿당|경수원|월연정") #제거

df_shaman = lab_7[theme_shaman][['관광지명','주소', '지역','합산 검색 수']]
df_shaman['태그'] = ['무당' for _ in range(len(df_shaman['관광지명']))]
df_confu = lab_7[theme_confu][['관광지명','주소', '지역','합산 검색 수']]
df_confu['태그'] = ['유교' for _ in range(len(df_confu['관광지명']))]
df_buddhism = lab_7[~theme_buddhism][['관광지명','주소', '지역','합산 검색 수']]
df_buddhism['태그'] = ['불교' for _ in range(len(df_buddhism['관광지명']))]

#힐링
lab_8 =theme_df_1[theme_df_1['분류'] == '웰니스관광']

df_healing = lab_8[['관광지명','주소', '지역','합산 검색 수']]
df_healing['태그'] = ['힐링' for _ in range(len(df_healing['관광지명']))]

#교육시설(애기들 교육)
lab_9 =theme_df_1[theme_df_1['분류'] == '교육시설']

df_study = lab_9[['관광지명','주소', '지역','합산 검색 수']]
df_study['태그'] = ['교육시설' for _ in range(len(df_study['관광지명']))]

#자연경관(산) + 도시/지역문화관광
lab_10 =pd.concat([theme_df_1[theme_df_1['분류'] == '자연경관(산)'],theme_df_1[theme_df_1['분류'] == '도시/지역문화관광']], axis = 0)
theme_valley= lab_10['관광지명'].str.contains("계곡|골$|곰배골")
theme_waterfall= lab_10['관광지명'].str.contains("폭포")
theme_hiking= lab_10['관광지명'].str.contains("산$|오름|봉$|약수|고개|등산|재$|코스|령$|샘|코스|방면")
theme_mountain_heal =  lab_10['관광지명'].str.contains("리조트|온천")

df_valley = lab_10[theme_valley][['관광지명','주소', '지역','합산 검색 수']]
df_valley['태그'] = ['계곡' for _ in range(len(df_valley['관광지명']))]
df_waterfall = lab_10[theme_waterfall][['관광지명','주소', '지역','합산 검색 수']]
df_waterfall['태그'] = ['폭포' for _ in range(len(df_waterfall['관광지명']))]
df_hiking = lab_10[theme_hiking][['관광지명','주소', '지역','합산 검색 수']]
df_hiking['태그'] = ['등산' for _ in range(len(df_hiking['관광지명']))]
df_mountain_heal = lab_10[theme_mountain_heal][['관광지명','주소', '지역','합산 검색 수']]
df_mountain_heal['태그'] = ['리조트/온천' for _ in range(len(df_mountain_heal['관광지명']))]



#항공레저
lab_11 =theme_df_1[theme_df_1['분류'] == '항공레저스포츠']

df_sky_sports = lab_11[['관광지명','주소', '지역','합산 검색 수']]
df_sky_sports['태그'] = ['항공레저' for _ in range(len(df_sky_sports['관광지명']))]

#공원
lab_12 =theme_df_1[theme_df_1['분류'] == '도시공원']

df_park = lab_12[['관광지명','주소', '지역','합산 검색 수']]
df_park['태그'] = ['공원' for _ in range(len(df_park['관광지명']))]

#공방
lab_13 =theme_df_1[theme_df_1['분류'] == '공예체험']

df_gongbang = lab_13[['관광지명','주소', '지역','합산 검색 수']]
df_gongbang['태그'] = ['공방' for _ in range(len(df_gongbang['관광지명']))]

#스포츠시설
lab_14 =theme_df_1[theme_df_1['분류'] == '레저스포츠시설']
theme_football= lab_14['관광지명'].str.contains("축구|풋살|풋볼|하이탑필드|잔디|FC|센터$")
theme_baseball= lab_14['관광지명'].str.contains("야구|이닝|베이스볼|파워리그구장|[^풋볼|^풋살]+파크$|필드$")
theme_sports_all = lab_14['관광지명'].str.contains("종합|다목적")

df_football = lab_14[theme_football][['관광지명','주소', '지역','합산 검색 수']]
df_football['태그'] = ['축구' for _ in range(len(df_football['관광지명']))]
df_baseball = lab_14[theme_baseball][['관광지명','주소', '지역','합산 검색 수']]
df_baseball['태그'] = ['야구' for _ in range(len(df_baseball['관광지명']))]
df_sports_all = lab_14[theme_sports_all][['관광지명','주소', '지역','합산 검색 수']]
df_sports_all['태그'] = ['종합체육관' for _ in range(len(df_sports_all['관광지명']))]

#육상레저스포츠
lab_15 =theme_df_1[theme_df_1['분류'] == '육상레저스포츠']
theme_ice= lab_15['관광지명'].str.contains("스키|썰매|빙상|아이스|[^인라인]+스케이트|스노우|비발디")
theme_golf= lab_15['관광지명'].str.contains("CC|GC|골프|cc|gc|힐스|컨트리")
theme_field_leisure = lab_15['관광지명'].str.contains("CC|GC|골프|cc|gc|힐스|컨트리|스키|썰매|빙상|아이스|[^인라인]+스케이트|비발디") #제거

df_ice = lab_15[theme_ice][['관광지명','주소', '지역','합산 검색 수']]
df_ice['태그'] = ['동계스포츠' for _ in range(len(df_ice['관광지명']))]
df_golf = lab_15[theme_golf][['관광지명','주소', '지역','합산 검색 수']]
df_golf['태그'] = ['골프' for _ in range(len(df_golf['관광지명']))]
df_field_leisure = lab_15[~theme_field_leisure][['관광지명','주소', '지역','합산 검색 수']]
df_field_leisure['태그'] = ['기타육상스포츠' for _ in range(len(df_field_leisure['관광지명']))]

#역사
lab_16 = pd.concat([theme_df_1[theme_df_1['분류'] == '역사유물'],theme_df_1[theme_df_1['분류'] == '역사유적지']], axis = 0)

df_history = lab_16[['관광지명','주소', '지역','합산 검색 수']]
df_history['태그'] = ['역사유적지' for _ in range(len(df_history['관광지명']))]

#전망대
lab_17 =theme_df_1[theme_df_1['분류'] == '랜드마크관광']

df_tower = lab_17[['관광지명','주소', '지역','합산 검색 수']]
df_tower['태그'] = ['전망대' for _ in range(len(df_tower['관광지명']))]

# 수목원/휴양림
lab_18 =theme_df_1[theme_df_1['분류'] == '자연공원']

df_forest = lab_18[['관광지명','주소', '지역','합산 검색 수']]
df_forest['태그'] = ['수목원/휴양림' for _ in range(len(df_forest['관광지명']))]

# 동굴
lab_19 =theme_df_1[theme_df_1['분류'] == '자연생태']

df_cave = lab_19[['관광지명','주소', '지역','합산 검색 수']]
df_cave['태그'] = ['동굴' for _ in range(len(df_cave['관광지명']))]

# 테마파크
lab_20 =theme_df_1[theme_df_1['분류'] == '테마공원']

df_themepark = lab_20[['관광지명','주소', '지역','합산 검색 수']]
df_themepark['태그'] = ['테마파크' for _ in range(len(df_themepark['관광지명']))]

# 공연시설
lab_21 =theme_df_1[theme_df_1['분류'] == '공연시설']
theme_normal_cinema= lab_21['관광지명'].str.contains("롯데시네마|메가박스|CGV|시네마|영화")
theme_theater= lab_21['관광지명'].str.contains("[^자동차]+극장")
theme_car_theater= lab_21['관광지명'].str.contains("자동차극장")
theme_arthall = lab_21['관광지명'].str.contains("롯데시네마|메가박스|CGV|시네마|영화|[^자동차]+극장|자동차극장") #제거

df_normal_cinema = lab_21[theme_normal_cinema][['관광지명','주소', '지역','합산 검색 수']]
df_normal_cinema['태그'] = ['영화관' for _ in range(len(df_normal_cinema['관광지명']))]
df_theater = lab_21[theme_theater][['관광지명','주소', '지역','합산 검색 수']]
df_theater['태그'] = ['극장' for _ in range(len(df_theater['관광지명']))]
df_car_theater = lab_21[theme_car_theater][['관광지명','주소', '지역','합산 검색 수']]
df_car_theater['태그'] = ['자동차극장' for _ in range(len(df_car_theater['관광지명']))]
df_arthall = lab_21[~theme_arthall][['관광지명','주소', '지역','합산 검색 수']]
df_arthall['태그'] = ['아트홀' for _ in range(len(df_arthall['관광지명']))]


# 기타 관광지
lab_22 =theme_df_1[theme_df_1['분류'] == '기타문화관광지']
theme_festival= lab_22['관광지명'].str.contains("축제|제$|잔치|행사|페스티벌|엑스포|박람회")
theme_culture_center= lab_22['관광지명'].str.contains("센터|파크")
theme_film_location= lab_22['관광지명'].str.contains("촬영|세트|스튜디오")
theme_landmark= lab_22['관광지명'].str.contains("축제|제$|잔치|행사|페스티벌|엑스포|박람회|촬영|세트|스튜디오|센터|파크") # 제거

df_festival = lab_22[theme_festival][['관광지명','주소', '지역','합산 검색 수']]
df_festival['태그'] = ['축제' for _ in range(len(df_festival['관광지명']))]
df_culture_center = lab_22[theme_culture_center][['관광지명','주소', '지역','합산 검색 수']]
df_culture_center['태그'] = ['문화센터' for _ in range(len(df_culture_center['관광지명']))]
df_film_location = lab_22[theme_film_location][['관광지명','주소', '지역','합산 검색 수']]
df_film_location['태그'] = ['촬영지' for _ in range(len(df_film_location['관광지명']))]
df_landmark = lab_22[~theme_landmark][['관광지명','주소', '지역','합산 검색 수']]
df_landmark['태그'] = ['랜드마크' for _ in range(len(df_landmark['관광지명']))]

# 농어촌체험
lab_23 =theme_df_1[theme_df_1['분류'] == '농/산/어촌체험']

df_country = lab_23[['관광지명','주소', '지역','합산 검색 수']]
df_country['태그'] = ['농어촌체험' for _ in range(len(df_country['관광지명']))]

# 기타레저스포츠
lab_24 =theme_df_1[theme_df_1['분류'] == '기타레저스포츠']

df_leisure_else = lab_24[['관광지명','주소', '지역','합산 검색 수']]
df_leisure_else['태그'] = ['기타레저스포츠' for _ in range(len(df_leisure_else['관광지명']))]

# 유원지
lab_25 =theme_df_1[theme_df_1['분류'] == '기타관광']

df_youwonji = lab_25[['관광지명','주소', '지역','합산 검색 수']]
df_youwonji['태그'] = ['유원지' for _ in range(len(df_youwonji['관광지명']))]

df_tag = pd.concat([df_beach, df_lake, df_swamp, df_sea_else, df_market, df_fishing, df_surfing, 
    df_water_leisure, df_ship, df_overall, df_w_leisure_else, df_diving, df_museum,
    df_inv_else, df_science, df_art, df_center, df_camping, df_date, df_shaman, df_confu, df_buddhism, df_healing,
    df_study, df_valley, df_waterfall, df_hiking, df_mountain_heal, df_sky_sports, df_park, df_gongbang,
    df_football, df_baseball, df_sports_all, df_ice, df_golf, df_field_leisure, df_history, df_tower, df_forest,
    df_cave, df_themepark, df_normal_cinema, df_theater, df_car_theater, df_arthall, df_festival,
    df_culture_center, df_film_location, df_landmark, df_country, df_leisure_else, df_youwonji], axis = 0)

df_tag

