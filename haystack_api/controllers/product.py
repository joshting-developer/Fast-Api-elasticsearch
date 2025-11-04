from fastapi import APIRouter, HTTPException

from services.openai_service import expand_query, optimize_content, filter_results
from haystack.schema import Document

from repositories.mysql_repository import MysqlRepository
from repositories.haystack_repository import HaystackRepository

from schemas.sync_request import SyncRequest

router = APIRouter()

haystack_repository = HaystackRepository(index_name="product")
mysql_repository = MysqlRepository(table_name="product")

# 透過hatstack搜尋
@router.get("/search")
def search_products(query: str, top_k: int = 10):
    results = haystack_repository.search(query, top_k)

    # results = [{"id": d.meta["id"], "name": d.meta["name"], "price": d.meta["price"], "score": d.score} for d in results]

    return {"query": query, "results": [r.to_dict() for r in results]}

# 使用openAi進行關鍵字擴充後, 透過hatstack搜尋
@router.get('/search_with_openai')
def serach_with_openai(query: str, top_k: int = 10):
    expanded_query = expand_query(query)

    results = haystack_repository.search(expanded_query, top_k)

    return {"query": expanded_query, "results": [r.to_dict() for r in results]}

# 透過hatstack搜尋後, 使用openAi對搜尋結過再做一次篩選
@router.get('/search_and_filter_by_openai')
def search_and_filter_by_openai(query: str, top_k: int = 10):
    results = haystack_repository.search(query, top_k)

    return {"query": query, "results": filter_results(query, [r.to_dict() for r in results])}

# 寫入haystack商品指定資料
@router.post('/sync')
def sync(request: SyncRequest):
    id = request.id

    product = mysql_repository.get_by_id(id)

    haystack_repository.write(product)

    return {"id": id, "product": product}

# 刪除haystack商品指定資料
@router.delete('/sync/{id}')
def sync(id: int):
    haystack_repository.delete_by_ids([id])

    return {"id": id}

@router.delete('/destroy')
def destroy():
    haystack_repository.delete_all()

    return {"message": 'deleted'}

@router.post('/write-fake')
def destroy():
    docs = [
        Document(content="蘋果 iPhone 15 Pro Max，搭載 A17 晶片", meta={"id": 1, "name": "iPhone 15 Pro Max", "price": 49900}),
        Document(content="三星 Galaxy S24 Ultra，搭載高效相機", meta={"id": 2, "name": "Galaxy S24 Ultra", "price": 38900}),
        Document(content="Sony WH-1000XM5 主動降噪耳機", meta={"id": 3, "name": "Sony WH-1000XM5", "price": 11900}),
        Document(content="蘋果 MacBook Pro 16 吋，配備 M3 晶片", meta={"id": 4, "name": "MacBook Pro 16", "price": 79900}),
        Document(content="Dell XPS 15 高效能筆電", meta={"id": 5, "name": "Dell XPS 15", "price": 59900}),
        Document(content="華碩 ROG Zephyrus G14 電競筆電", meta={"id": 6, "name": "ROG Zephyrus G14", "price": 48900}),
        Document(content="蘋果 iPad Pro 12.9 吋，搭載 M2 晶片", meta={"id": 7, "name": "iPad Pro 12.9", "price": 35900}),
        Document(content="三星 Galaxy Tab S9 Ultra 平板電腦", meta={"id": 8, "name": "Galaxy Tab S9 Ultra", "price": 29900}),
        Document(content="羅技 MX Master 3S 無線滑鼠", meta={"id": 9, "name": "MX Master 3S", "price": 3500}),
        Document(content="Razer DeathAdder V3 Pro 電競滑鼠", meta={"id": 10, "name": "DeathAdder V3 Pro", "price": 4500}),
        Document(content="蘋果 AirPods Pro 第二代", meta={"id": 11, "name": "AirPods Pro 2", "price": 6990}),
        Document(content="Bose QuietComfort Ultra 耳罩式耳機", meta={"id": 12, "name": "Bose QC Ultra", "price": 12900}),
        Document(content="Sony Alpha 7 IV 全片幅無反相機", meta={"id": 13, "name": "Sony A7 IV", "price": 79900}),
        Document(content="Canon EOS R8 無反相機", meta={"id": 14, "name": "Canon EOS R8", "price": 49900}),
        Document(content="Nikon Z6 II 無反相機", meta={"id": 15, "name": "Nikon Z6 II", "price": 59900}),
        Document(content="DJI Air 3 空拍機，內建 4K 鏡頭", meta={"id": 16, "name": "DJI Air 3", "price": 45900}),
        Document(content="GoPro HERO12 Black 運動攝影機", meta={"id": 17, "name": "GoPro HERO12", "price": 13900}),
        Document(content="三星 55 吋 Neo QLED 4K 電視", meta={"id": 18, "name": "Samsung Neo QLED 55", "price": 35900}),
        Document(content="LG OLED C3 65 吋 4K 電視", meta={"id": 19, "name": "LG OLED C3 65", "price": 54900}),
        Document(content="Sony Bravia XR A80L 55 吋 OLED 電視", meta={"id": 20, "name": "Sony Bravia XR A80L", "price": 49900}),
        Document(content="微軟 Surface Pro 9 二合一筆電", meta={"id": 21, "name": "Surface Pro 9", "price": 45900}),
        Document(content="蘋果 Apple Watch Series 9 45mm 智慧手錶", meta={"id": 22, "name": "Apple Watch Series 9", "price": 14900}),
        Document(content="Garmin Fenix 7X Pro 多運動 GPS 手錶", meta={"id": 23, "name": "Garmin Fenix 7X", "price": 25900}),
        Document(content="Fitbit Sense 2 健康智慧手錶", meta={"id": 24, "name": "Fitbit Sense 2", "price": 8990}),
        Document(content="Anker 737 行動電源（PowerCore 24K）", meta={"id": 25, "name": "Anker 737 Power Bank", "price": 4990}),
        Document(content="Belkin 3 合 1 無線充電座", meta={"id": 26, "name": "Belkin 3-in-1 Charger", "price": 6990}),
        Document(content="Philips Hue 白色與彩色氛圍燈入門組", meta={"id": 27, "name": "Philips Hue Starter Kit", "price": 8990}),
        Document(content="Dyson V15 Detect 無線吸塵器", meta={"id": 28, "name": "Dyson V15 Detect", "price": 23900}),
        Document(content="小米空氣清淨機 4 Pro", meta={"id": 29, "name": "Xiaomi Air Purifier 4 Pro", "price": 7990}),
        Document(content="Panasonic NN-CD87KS 四合一微波爐", meta={"id": 30, "name": "Panasonic Microwave Oven", "price": 14900}),
        Document(content="The North Face Summit Series 登山背包 65L", meta={"id": 31, "name": "TNF Summit Backpack 65L", "price": 8900}),
        Document(content="Black Diamond Trail Pro 登山杖", meta={"id": 32, "name": "BD Trail Pro Poles", "price": 3990}),
        Document(content="Garmin inReach Mini 2 衛星通訊器", meta={"id": 33, "name": "inReach Mini 2", "price": 11900}),
        Document(content="MSR Hubba Hubba 2人帳篷，輕量設計", meta={"id": 34, "name": "MSR Hubba Hubba 2P", "price": 16900}),
        Document(content="Jetboil Flash 戶外快煮爐", meta={"id": 35, "name": "Jetboil Flash", "price": 4890}),
        Document(content="Sawyer Squeeze 戶外濾水器", meta={"id": 36, "name": "Sawyer Squeeze Filter", "price": 1490}),
        Document(content="Therm-a-Rest NeoAir Xlite 充氣睡墊", meta={"id": 37, "name": "NeoAir Xlite", "price": 6590}),
        Document(content="Petzl Actik Core 充電式頭燈", meta={"id": 38, "name": "Petzl Actik Core", "price": 2490}),
        Document(content="Columbia Newton Ridge Plus 防水登山鞋", meta={"id": 39, "name": "Newton Ridge Plus Boots", "price": 3290}),
        Document(content="Osprey Hydraulics 2L 水袋", meta={"id": 40, "name": "Osprey Hydraulics 2L", "price": 1150}),
        Document(content="Outdoor Research Helium II 超輕雨衣", meta={"id": 41, "name": "OR Helium II Jacket", "price": 4990}),
        Document(content="ALPS King Kong 重型露營椅", meta={"id": 42, "name": "King Kong Camp Chair", "price": 2790}),
        Document(content="BioLite CampStove 2+ USB 發電爐", meta={"id": 43, "name": "BioLite CampStove 2+", "price": 4690}),
        Document(content="Sea to Summit Ultra-Sil 13L 防水袋", meta={"id": 44, "name": "Ultra-Sil Dry Sack 13L", "price": 890}),
        Document(content="Goal Zero Nomad 10 太陽能板", meta={"id": 45, "name": "Goal Zero Nomad 10", "price": 3690}),
        Document(content="Platypus GravityWorks 4L 重力濾水系統", meta={"id": 46, "name": "Platypus GravityWorks 4L", "price": 4990}),
        Document(content="Montbell Down Hugger 800 #3 羽絨睡袋", meta={"id": 47, "name": "Montbell Down Hugger 800 #3", "price": 8690}),
        Document(content="LEKI Makalu Lite 登山杖", meta={"id": 48, "name": "LEKI Makalu Lite", "price": 4290}),
        Document(content="Snow Peak 鈦合金炊具組", meta={"id": 49, "name": "Snow Peak Titanium Cook Set", "price": 3590}),
        Document(content="Helinox Chair Zero 超輕露營椅", meta={"id": 50, "name": "Helinox Chair Zero", "price": 4590}),
        Document(content="特斯拉 Model 3 長續航版，搭載全自動駕駛輔助功能", meta={"id": 51, "name": "Tesla Model 3 Long Range", "price": 1899000}),
        Document(content="Toyota Corolla Cross 油電混合 SUV，經濟實用", meta={"id": 52, "name": "Toyota Corolla Cross Hybrid", "price": 950000}),
        Document(content="BMW X5 豪華運動休旅，內建全景天窗與抬頭顯示器", meta={"id": 53, "name": "BMW X5 xDrive40i", "price": 3290000}),
        Document(content="Honda CR-V 五代 AWD，搭載 Honda Sensing 智慧駕駛系統", meta={"id": 54, "name": "Honda CR-V AWD", "price": 1180000}),
        Document(content="Ford Focus 1.5L EcoBoost 五門掀背車，操控靈活", meta={"id": 55, "name": "Ford Focus Hatchback", "price": 799000}),
        Document(content="Lexus NX 350h 油電混合 SUV，豪華與省油兼具", meta={"id": 56, "name": "Lexus NX 350h", "price": 2090000}),
        Document(content="Mazda CX-5 Skyactiv-G，日系操控好手感 SUV", meta={"id": 57, "name": "Mazda CX-5", "price": 1030000}),
        Document(content="Hyundai Ioniq 5 純電 SUV，支援 800V 超充技術", meta={"id": 58, "name": "Hyundai Ioniq 5", "price": 1550000}),
        Document(content="Porsche Taycan 4S 純電跑車，結合性能與未來科技", meta={"id": 59, "name": "Porsche Taycan 4S", "price": 4390000}),
        Document(content="Volvo XC60 B5 Mild Hybrid，安全科技滿載的北歐休旅", meta={"id": 60, "name": "Volvo XC60 B5", "price": 2390000}),
        Document(content="Herman Miller Aeron 人體工學椅，經典網布設計，支援長時間坐姿", meta={"id": 61, "name": "Herman Miller Aeron", "price": 48900}),
        Document(content="Steelcase Leap V2 人體工學椅，自動調整腰靠與座椅深度", meta={"id": 62, "name": "Steelcase Leap V2", "price": 42900}),
        Document(content="Ergotune Supreme 人體工學椅，11 向可調節與人體曲線對應", meta={"id": 63, "name": "Ergotune Supreme", "price": 18900}),
        Document(content="Sihoo M18 人體工學椅，適合辦公室與居家長時間使用", meta={"id": 64, "name": "Sihoo M18", "price": 6990}),
        Document(content="Secretlab TITAN Evo 2022 人體工學電競椅，附磁吸頭枕", meta={"id": 65, "name": "Secretlab TITAN Evo 2022", "price": 16900}),
        Document(content="Hbada E3 人體工學椅，雙背支撐與彈力網布設計", meta={"id": 66, "name": "Hbada E3", "price": 7590}),
        Document(content="SIDIZ T50 人體工學椅，韓國品牌，高彈力坐墊與可調節頭枕", meta={"id": 67, "name": "SIDIZ T50", "price": 13800}),
        Document(content="Humanscale Freedom 人體工學椅，自動傾仰機構與高級皮革選項", meta={"id": 68, "name": "Humanscale Freedom", "price": 39800}),
        Document(content="Komene 人體工學椅，帶腿托與頭枕，適合午休與躺坐", meta={"id": 69, "name": "Komene Chair", "price": 7990}),
        Document(content="NOUHAUS Ergo3D 人體工學椅，雙層網布與動態腰部支撐", meta={"id": 70, "name": "NOUHAUS Ergo3D", "price": 12800}),
        Document(content="Duramont 人體工學椅，具備調整扶手與椅背彈性", meta={"id": 71, "name": "Duramont Ergonomic Chair", "price": 10500}),
        Document(content="ErgoTune Classic 人體工學椅，針對小空間設計，經濟實惠", meta={"id": 72, "name": "ErgoTune Classic", "price": 8990}),
        Document(content="X-Chair X2 人體工學辦公椅，動態頭枕與背部支撐", meta={"id": 73, "name": "X-Chair X2", "price": 28900}),
        Document(content="Uplift Vert 人體工學網椅，通風舒適，適合站坐交替工作", meta={"id": 74, "name": "Uplift Vert", "price": 11800}),
        Document(content="Kulik System Diamond 人體工學醫療級辦公椅", meta={"id": 75, "name": "Kulik Diamond", "price": 29800}),
        Document(content="FlexiSpot BS8 人體工學電腦椅，彈力腰靠與舒壓坐墊", meta={"id": 76, "name": "FlexiSpot BS8", "price": 8990}),
        Document(content="Autonomous ErgoChair Pro 人體工學椅，全功能支撐", meta={"id": 77, "name": "ErgoChair Pro", "price": 13900}),
        Document(content="RECARO Office Chair，賽車椅風格結合人體工學", meta={"id": 78, "name": "RECARO Office Chair", "price": 25900}),
        Document(content="WorkPro Quantum 9000 網布人體工學椅，高性價比", meta={"id": 79, "name": "WorkPro Quantum 9000", "price": 11900}),
        Document(content="Hbada Butterfly 人體工學電競椅，蝴蝶造型背靠", meta={"id": 80, "name": "Hbada Butterfly", "price": 5890}),
        Document(content="Yamaha MT-07 街車，搭載 689cc 雙缸引擎，輕巧靈活", meta={"id": 81, "name": "Yamaha MT-07", "price": 328000}),
        Document(content="Kawasaki Ninja 400，跑車外型，適合新手入門的運動車款", meta={"id": 82, "name": "Kawasaki Ninja 400", "price": 278000}),
        Document(content="SYM DRG BT 158，配備 TCS 與 LED 全車燈組，運動速克達", meta={"id": 83, "name": "SYM DRG BT", "price": 108000}),
        Document(content="Kymco KRV 180，白牌頂規速克達，獨立搖臂與 ABS", meta={"id": 84, "name": "Kymco KRV 180", "price": 115000}),
        Document(content="Gogoro VIVA MIX Belt 電動機車，採用皮帶傳動與可換電系統", meta={"id": 85, "name": "Gogoro VIVA MIX", "price": 79500}),
        Document(content="Yamaha TMAX 560，黃牌頂級大型速克達，配備電動風鏡", meta={"id": 86, "name": "Yamaha TMAX 560", "price": 488000}),
        Document(content="Honda CB500X 探險車款，搭載 471cc 並列雙缸引擎", meta={"id": 87, "name": "Honda CB500X", "price": 298000}),
        Document(content="Suzuki Burgman 400 大型速克達，舒適長途座艙", meta={"id": 88, "name": "Suzuki Burgman 400", "price": 318000}),
        Document(content="Vespa Primavera 150 經典復古速克達，義大利設計", meta={"id": 89, "name": "Vespa Primavera 150", "price": 155000}),
        Document(content="Yamaha Cygnus Gryphus 勁戰六代，125cc 都會速克達", meta={"id": 90, "name": "Yamaha 勁戰六代", "price": 89500}),
        Document(content="Kymco Many 110 EV 電動機車，復古車型結合現代電能", meta={"id": 91, "name": "Kymco Many EV", "price": 72500}),
        Document(content="Honda PCX 160，125 級距頂規白牌速克達", meta={"id": 92, "name": "Honda PCX 160", "price": 108000}),
        Document(content="Gogoro SuperSport，高性能電動速克達，支援多段模式", meta={"id": 93, "name": "Gogoro SuperSport", "price": 109800}),
        Document(content="Kawasaki Z900，948cc 街車王者，直列四缸引擎", meta={"id": 94, "name": "Kawasaki Z900", "price": 468000}),
        Document(content="Suzuki GSX-S150 輕檔車，新手友善、造型銳利", meta={"id": 95, "name": "Suzuki GSX-S150", "price": 112000}),
        Document(content="SYM MMBCU 158，外觀科技未來感，支援 TCS", meta={"id": 96, "name": "SYM MMBCU", "price": 115000}),
        Document(content="Aprilia SR GT 200 義式速克達，擁有越野懸吊與 ABS", meta={"id": 97, "name": "Aprilia SR GT 200", "price": 136000}),
        Document(content="Honda Forza 350 白牌大羊，配備電動風鏡與 HSTC", meta={"id": 98, "name": "Honda Forza 350", "price": 218000}),
        Document(content="Yamaha XMAX 300 大羊，運動外型與舒適兼備", meta={"id": 99, "name": "Yamaha XMAX 300", "price": 225000}),
        Document(content="KTM Duke 390，輕量化鋼管車架與強勁單缸引擎", meta={"id": 100, "name": "KTM Duke 390", "price": 248000}),
    ]

    haystack_repository.write(docs)

    return {"message": 'created'}
