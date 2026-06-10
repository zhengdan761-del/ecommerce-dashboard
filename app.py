import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =========================================================
# 頁面設定
# =========================================================
st.set_page_config(
    page_title="跨境電商廣告投放報表",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    letter-spacing: .5px;
}
[data-testid="stMetricValue"] {
    font-size: 28px;
}
.metric-title{
    font-size:22px;
    font-weight:900;
    color:#0f172a;
    line-height:1.15;
    margin-bottom:8px;
}

.metric-value{
    font-size:42px;
    font-weight:900;
    color:#111827;
}

.gauge-title{
    text-align:center;
    font-size:36px;
    font-weight:900;
    color:#0f172a;
    margin-top:12px;
    margin-bottom:12px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 基本資料
# =========================================================
REPORT_TITLE = "跨境電商廣告投放報表"
PERIOD = "2026/06/03－2026/06/09"
CURRENCY = "NTD 新台幣"

# =========================================================
# 格式化工具
# =========================================================
def money(v):
    return f"NT${v:,.0f}"

def money2(v):
    return f"NT${v:,.2f}"

def number(v):
    return f"{v:,.0f}"

def percent(v):
    return f"{v:.2f}%"

def roas(v):
    return f"{v:.2f}x"

def rgba(hex_color, alpha=0.18):
    hex_color = hex_color.replace("#", "")
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:], 16)
    return f"rgba({r},{g},{b},{alpha})"

# =========================================================
# 核心成效總覽
# =========================================================
core = {
    "曝光量 IMP": 22_436_280,
    "點擊量": 573_482,
    "點擊率 CTR": 2.56,
    "廣告花費": 6_700_000,
    "平均點擊成本 CPC": 11.68,
    "成交訂單數": 18_742,
    "成交轉換率 CVR": 3.27,
    "商品交易總額 GMV": 46_850_000,
    "廣告投資報酬率 ROAS": 6.99,
    "單筆成交成本 CPA": 357.49,
    "淨利": 16_000_000,
    "扣除退款後營收": 46_381_500,
}

core_table = pd.DataFrame([
    ["期間", PERIOD],
    ["幣別", CURRENCY],
    ["曝光量 IMP", number(core["曝光量 IMP"])],
    ["點擊量", number(core["點擊量"])],
    ["點擊率 CTR", percent(core["點擊率 CTR"])],
    ["廣告花費", money(core["廣告花費"])],
    ["平均點擊成本 CPC", money2(core["平均點擊成本 CPC"])],
    ["成交訂單數", number(core["成交訂單數"])],
    ["成交轉換率 CVR", percent(core["成交轉換率 CVR"])],
    ["商品交易總額 GMV", money(core["商品交易總額 GMV"])],
    ["廣告投資報酬率 ROAS", roas(core["廣告投資報酬率 ROAS"])],
    ["單筆成交成本 CPA", money2(core["單筆成交成本 CPA"])],
    ["淨利", money(core["淨利"])],
    ["扣除退款後營收", money(core["扣除退款後營收"])],
], columns=["項目", "數值"])

# =========================================================
# 報表圖表用資料
# =========================================================
daily = pd.DataFrame({
    "日期": ["2026/06/03", "2026/06/04", "2026/06/05", "2026/06/06", "2026/06/07", "2026/06/08", "2026/06/09"],
    "曝光量 IMP": [3_284_910, 2_746_385, 3_615_772, 2_982_148, 3_405_629, 2_590_834, 3_810_602],
    "點擊量": [83_462, 69_918, 89_305, 80_744, 91_682, 61_509, 96_862],
    "成交訂單數": [2_741, 2_182, 3_104, 2_491, 3_218, 1_934, 3_072],
    "商品交易總額 GMV": [6_889_400, 5_302_800, 7_613_200, 6_091_700, 7_896_500, 4_656_300, 8_400_100],
    "廣告花費": [965_200, 824_600, 1_066_800, 917_400, 1_024_900, 761_500, 1_139_600],
    "淨利": [2_318_000, 1_728_000, 2_654_000, 1_996_000, 2_691_000, 1_422_000, 3_191_000],
    "扣除退款後營收": [6_823_200, 5_250_200, 7_537_300, 6_030_400, 7_818_100, 4_609_500, 8_312_800],
})

chart_table = pd.DataFrame({
    "圖表資料": ["曝光量 IMP", "點擊量", "成交訂單數", "商品交易總額 GMV", "廣告花費", "淨利", "扣除退款後營收"],
    "2026/06/03": ["3,284,910", "83,462", "2,741", "NT$6,889,400", "NT$965,200", "NT$2,318,000", "NT$6,823,200"],
    "2026/06/04": ["2,746,385", "69,918", "2,182", "NT$5,302,800", "NT$824,600", "NT$1,728,000", "NT$5,250,200"],
    "2026/06/05": ["3,615,772", "89,305", "3,104", "NT$7,613,200", "NT$1,066,800", "NT$2,654,000", "NT$7,537,300"],
    "2026/06/06": ["2,982,148", "80,744", "2,491", "NT$6,091,700", "NT$917,400", "NT$1,996,000", "NT$6,030,400"],
    "2026/06/07": ["3,405,629", "91,682", "3,218", "NT$7,896,500", "NT$1,024,900", "NT$2,691,000", "NT$7,818,100"],
    "2026/06/08": ["2,590,834", "61,509", "1,934", "NT$4,656,300", "NT$761,500", "NT$1,422,000", "NT$4,609,500"],
    "2026/06/09": ["3,810,602", "96,862", "3,072", "NT$8,400,100", "NT$1,139,600", "NT$3,191,000", "NT$8,312,800"],
    "合計": ["22,436,280", "573,482", "18,742", "NT$46,850,000", "NT$6,700,000", "NT$16,000,000", "NT$46,381,500"],
})

# =========================================================
# 每日趨勢資料
# =========================================================
click_trend = pd.DataFrame({
    "日期": daily["日期"],
    "曝光量 IMP": daily["曝光量 IMP"],
    "點擊量": daily["點擊量"],
    "點擊率 CTR": [2.54, 2.55, 2.47, 2.71, 2.69, 2.37, 2.54],
    "廣告花費": daily["廣告花費"],
    "平均點擊成本 CPC": [11.56, 11.79, 11.95, 11.36, 11.18, 12.38, 11.77],
})
click_total = pd.DataFrame([{
    "日期": "合計",
    "曝光量 IMP": 22_436_280,
    "點擊量": 573_482,
    "點擊率 CTR": 2.56,
    "廣告花費": 6_700_000,
    "平均點擊成本 CPC": 11.68,
}])
click_display = pd.concat([click_trend, click_total], ignore_index=True)

order_trend = pd.DataFrame({
    "日期": daily["日期"],
    "點擊量": daily["點擊量"],
    "成交訂單數": daily["成交訂單數"],
    "成交轉換率 CVR": [3.28, 3.12, 3.48, 3.09, 3.51, 3.14, 3.17],
    "廣告花費": daily["廣告花費"],
    "單筆成交成本 CPA": [352.13, 377.91, 343.69, 368.29, 318.49, 393.74, 370.96],
})
order_total = pd.DataFrame([{
    "日期": "合計",
    "點擊量": 573_482,
    "成交訂單數": 18_742,
    "成交轉換率 CVR": 3.27,
    "廣告花費": 6_700_000,
    "單筆成交成本 CPA": 357.49,
}])
order_display = pd.concat([order_trend, order_total], ignore_index=True)

sales_trend = pd.DataFrame({
    "日期": daily["日期"],
    "成交訂單數": daily["成交訂單數"],
    "商品交易總額 GMV": daily["商品交易總額 GMV"],
    "廣告花費": daily["廣告花費"],
    "廣告投資報酬率 ROAS": [7.14, 6.43, 7.14, 6.64, 7.70, 6.11, 7.37],
    "淨利": daily["淨利"],
    "扣除退款後營收": daily["扣除退款後營收"],
})
sales_total = pd.DataFrame([{
    "日期": "合計",
    "成交訂單數": 18_742,
    "商品交易總額 GMV": 46_850_000,
    "廣告花費": 6_700_000,
    "廣告投資報酬率 ROAS": 6.99,
    "淨利": 16_000_000,
    "扣除退款後營收": 46_381_500,
}])
sales_display = pd.concat([sales_trend, sales_total], ignore_index=True)

daily_full = pd.DataFrame({
    "日期": daily["日期"],
    "曝光量 IMP": daily["曝光量 IMP"],
    "點擊量": daily["點擊量"],
    "點擊率 CTR": click_trend["點擊率 CTR"],
    "廣告花費": daily["廣告花費"],
    "平均點擊成本 CPC": click_trend["平均點擊成本 CPC"],
    "成交訂單數": daily["成交訂單數"],
    "成交轉換率 CVR": order_trend["成交轉換率 CVR"],
    "商品交易總額 GMV": daily["商品交易總額 GMV"],
    "廣告投資報酬率 ROAS": sales_trend["廣告投資報酬率 ROAS"],
    "單筆成交成本 CPA": order_trend["單筆成交成本 CPA"],
    "淨利": daily["淨利"],
    "扣除退款後營收": daily["扣除退款後營收"],
})
daily_full_total = pd.DataFrame([{
    "日期": "合計",
    "曝光量 IMP": 22_436_280,
    "點擊量": 573_482,
    "點擊率 CTR": 2.56,
    "廣告花費": 6_700_000,
    "平均點擊成本 CPC": 11.68,
    "成交訂單數": 18_742,
    "成交轉換率 CVR": 3.27,
    "商品交易總額 GMV": 46_850_000,
    "廣告投資報酬率 ROAS": 6.99,
    "單筆成交成本 CPA": 357.49,
    "淨利": 16_000_000,
    "扣除退款後營收": 46_381_500,
}])
daily_full_display = pd.concat([daily_full, daily_full_total], ignore_index=True)

# =========================================================
# 平台銷售額排名
# =========================================================
platform_rank = pd.DataFrame({
    "排名": [1, 2, 3, 4, 5, 6],
    "銷售平台／通路": ["自有品牌站／Shopify Plus", "TikTok Shop", "Amazon Marketplace", "eBay", "Shopee Cross-border", "Walmart Marketplace"],
    "成交訂單數": [8_310, 4_261, 2_974, 1_508, 1_044, 645],
    "商品交易總額 GMV": [20_936_600, 10_704_900, 7_413_700, 3_768_400, 2_523_600, 1_502_800],
    "銷售占比": [44.69, 22.85, 15.82, 8.04, 5.39, 3.21],
    "報表顯示": ["2,093.7 萬", "1,070.5 萬", "741.4 萬", "376.8 萬", "252.4 萬", "150.3 萬"],
})
platform_rank_total = pd.DataFrame([{
    "排名": "合計",
    "銷售平台／通路": "",
    "成交訂單數": 18_742,
    "商品交易總額 GMV": 46_850_000,
    "銷售占比": 100.00,
    "報表顯示": "4,685.0 萬",
}])
platform_rank_display = pd.concat([platform_rank, platform_rank_total], ignore_index=True)

# =========================================================
# 廣告平台、國家市場
# =========================================================
ad_platform = pd.DataFrame({
    "廣告平台": ["TikTok Ads", "Meta Ads", "Google Ads", "Pinterest Ads", "Snapchat Ads"],
    "曝光量 IMP": [8_205_444, 6_389_105, 4_624_218, 1_741_906, 1_475_607],
    "點擊量": [221_915, 164_238, 108_642, 45_231, 33_456],
    "點擊率 CTR": [2.70, 2.57, 2.35, 2.60, 2.27],
    "廣告花費": [2_623_500, 1_835_400, 1_306_700, 537_600, 396_800],
    "平均點擊成本 CPC": [11.82, 11.18, 12.03, 11.89, 11.86],
    "成交訂單數": [7_182, 5_492, 3_724, 1_463, 881],
    "成交轉換率 CVR": [3.24, 3.34, 3.43, 3.23, 2.63],
    "商品交易總額 GMV": [17_942_600, 13_865_300, 9_342_800, 3_598_900, 2_100_400],
    "廣告投資報酬率 ROAS": [6.84, 7.55, 7.15, 6.69, 5.29],
    "單筆成交成本 CPA": [365.29, 334.20, 350.89, 367.46, 450.40],
})
ad_platform_total = pd.DataFrame([{
    "廣告平台": "合計",
    "曝光量 IMP": 22_436_280,
    "點擊量": 573_482,
    "點擊率 CTR": 2.56,
    "廣告花費": 6_700_000,
    "平均點擊成本 CPC": 11.68,
    "成交訂單數": 18_742,
    "成交轉換率 CVR": 3.27,
    "商品交易總額 GMV": 46_850_000,
    "廣告投資報酬率 ROAS": 6.99,
    "單筆成交成本 CPA": 357.49,
}])
ad_platform_display = pd.concat([ad_platform, ad_platform_total], ignore_index=True)

country = pd.DataFrame({
    "國家市場": ["United States 美國", "United Kingdom 英國", "Canada 加拿大", "Australia 澳洲", "Japan 日本", "Singapore 新加坡", "Malaysia 馬來西亞"],
    "曝光量 IMP": [8_727_842, 3_545_910, 2_994_681, 2_411_476, 2_506_384, 1_182_927, 1_067_060],
    "點擊量": [223_806, 91_734, 76_902, 62_310, 60_152, 31_672, 26_906],
    "點擊率 CTR": [2.56, 2.59, 2.57, 2.58, 2.40, 2.68, 2.52],
    "廣告花費": [2_574_900, 1_091_300, 922_800, 765_400, 842_600, 329_600, 173_400],
    "平均點擊成本 CPC": [11.51, 11.90, 12.00, 12.28, 14.01, 10.41, 6.44],
    "成交訂單數": [7_285, 3_136, 2_571, 2_102, 1_955, 1_062, 631],
    "成交轉換率 CVR": [3.26, 3.42, 3.34, 3.37, 3.25, 3.35, 2.35],
    "商品交易總額 GMV": [18_390_200, 7_869_600, 6_456_700, 5_266_500, 4_842_300, 2_651_700, 1_373_000],
    "廣告投資報酬率 ROAS": [7.14, 7.21, 7.00, 6.88, 5.75, 8.05, 7.92],
    "單筆成交成本 CPA": [353.45, 347.99, 358.93, 364.13, 431.00, 310.36, 274.80],
})
country_total = pd.DataFrame([{
    "國家市場": "合計",
    "曝光量 IMP": 22_436_280,
    "點擊量": 573_482,
    "點擊率 CTR": 2.56,
    "廣告花費": 6_700_000,
    "平均點擊成本 CPC": 11.68,
    "成交訂單數": 18_742,
    "成交轉換率 CVR": 3.27,
    "商品交易總額 GMV": 46_850_000,
    "廣告投資報酬率 ROAS": 6.99,
    "單筆成交成本 CPA": 357.49,
}])
country_display = pd.concat([country, country_total], ignore_index=True)

# =========================================================
# 商品、素材、裝置、受眾
# =========================================================
product_rows = [['智能香氛小夜燈', '居家氛圍／生活小家電', 'NT$970－NT$1,870', 2750, 190624, 5407, 2.84, 47500, 8.78, 171, 3.16, 470250, 9.9, 277.78, 144000, 463650], ['桌面空氣循環扇', '辦公室／居家小家電', 'NT$1,040－NT$2,020', 3180, 259330, 9261, 3.57, 262500, 28.34, 412, 4.45, 1310160, 4.99, 637.14, 414000, 1289760], ['智能空氣淨化器', '居家健康／空氣清潔設備', 'NT$3,740－NT$7,240', 10640, 495616, 9042, 1.82, 386100, 42.7, 182, 2.01, 1936480, 5.02, 2121.43, 407000, 1918080], ['智能廚房秤', '廚房用品／智能小工具', 'NT$520－NT$1,000', 1480, 986900, 16571, 1.68, 89100, 5.38, 390, 2.35, 577200, 6.48, 228.46, 152000, 574000], ['便攜式保溫杯', '生活用品／外出隨行', 'NT$590－NT$1,150', 1760, 509996, 11355, 2.23, 117600, 10.36, 621, 5.47, 1092960, 9.29, 189.37, 435000, 1079360], ['多功能收納包', '旅行／居家收納用品', 'NT$670－NT$1,290', 2040, 315070, 9150, 2.9, 56400, 6.16, 420, 4.59, 856800, 15.19, 134.29, 333000, 849000], ['旅行壓縮袋組', '旅行用品／行李收納', 'NT$820－NT$1,580', 2470, 1617848, 41018, 2.54, 281500, 6.86, 1705, 4.16, 4211350, 14.96, 165.1, 1685000, 4161250], ['磁吸式無線充電座', '3C配件／桌面充電', 'NT$970－NT$1,870', 2900, 156723, 4425, 2.82, 54500, 12.32, 192, 4.34, 556800, 10.22, 283.85, 167000, 550100], ['藍牙降噪耳機', '3C配件／影音設備', 'NT$1,870－NT$3,610', 5550, 1750481, 50134, 2.86, 694700, 13.86, 522, 1.04, 2897100, 4.17, 1330.84, 787000, 2867100], ['手機防水收納袋', '戶外用品／手機配件', 'NT$290－NT$570', 970, 118645, 2714, 2.29, 22200, 8.18, 153, 5.64, 148410, 6.69, 145.1, 46000, 146810], ['摺疊式手機支架', '3C配件／桌面用品', 'NT$340－NT$650', 1120, 591611, 14225, 2.4, 112300, 7.9, 526, 3.7, 589120, 5.25, 213.5, 131000, 583420], ['LED補光化妝鏡', '美妝工具／居家小物', 'NT$890－NT$1,730', 2540, 1309096, 23234, 1.77, 314300, 13.53, 696, 3.0, 1767840, 5.63, 451.58, 425000, 1746440], ['電動筋膜按摩器', '健康放鬆／按摩設備', 'NT$2,240－NT$4,340', 6430, 240926, 7089, 2.94, 313200, 44.18, 206, 2.91, 1324580, 4.23, 1520.39, 323000, 1313380], ['頸掛式小風扇', '夏季用品／個人小家電', 'NT$740－NT$1,440', 2110, 811173, 19240, 2.37, 231200, 12.02, 1075, 5.59, 2268250, 9.81, 215.07, 694000, 2247750], ['USB加熱暖手寶', '冬季用品／生活小家電', 'NT$520－NT$1,000', 1630, 444852, 10615, 2.39, 102700, 9.67, 587, 5.53, 956810, 9.32, 174.96, 409000, 949010], ['智能感應垃圾桶', '居家用品／智能生活', 'NT$1,420－NT$2,740', 4040, 673051, 11934, 1.77, 250400, 20.98, 171, 1.43, 690840, 2.76, 1464.33, 159000, 685440], ['防滑浴室地墊', '居家用品／浴室收納', 'NT$440－NT$860', 1400, 315473, 7942, 2.52, 52300, 6.59, 359, 4.52, 502600, 9.61, 145.68, 170000, 497300], ['廚房瀝水置物架', '廚房用品／收納整理', 'NT$890－NT$1,730', 2840, 426925, 7362, 1.72, 55500, 7.54, 401, 5.45, 1138840, 20.52, 138.4, 373000, 1126040], ['矽膠保鮮袋組', '廚房用品／環保收納', 'NT$370－NT$710', 1200, 64753, 2210, 3.41, 11400, 5.16, 72, 3.26, 86400, 7.58, 158.33, 34000, 85700], ['不鏽鋼保鮮盒', '廚房用品／食物收納', 'NT$670－NT$1,290', 2110, 159543, 4721, 2.96, 28800, 6.1, 187, 3.96, 394570, 13.7, 154.01, 119000, 389070], ['可折疊購物袋', '生活用品／外出收納', 'NT$290－NT$570', 990, 495040, 12561, 2.54, 102900, 8.19, 743, 5.92, 735570, 7.15, 138.49, 271000, 727270], ['旅行盥洗收納包', '旅行用品／盥洗收納', 'NT$590－NT$1,150', 1910, 435874, 9378, 2.15, 72800, 7.76, 255, 2.72, 487050, 6.69, 285.49, 215000, 481750], ['護照證件收納包', '旅行用品／證件收納', 'NT$520－NT$1,000', 1590, 578793, 12552, 2.17, 57300, 4.56, 497, 3.96, 790230, 13.79, 115.29, 304000, 781530], ['行李箱電子秤', '旅行用品／行李配件', 'NT$440－NT$860', 1420, 625232, 12865, 2.06, 153600, 11.94, 601, 4.67, 853420, 5.56, 255.57, 288000, 845220], ['車用手機支架', '汽車用品／車內配件', 'NT$590－NT$1,150', 1830, 775962, 14827, 1.91, 131000, 8.83, 308, 2.08, 563640, 4.3, 425.32, 209000, 558540], ['車用香氛擴香器', '汽車用品／車內香氛', 'NT$740－NT$1,440', 2260, 501539, 9308, 1.86, 121100, 13.01, 558, 5.99, 1261080, 10.41, 217.03, 509000, 1249380], ['車用吸塵器', '汽車用品／清潔設備', 'NT$1,190－NT$2,310', 3610, 259700, 7713, 2.97, 421500, 54.66, 502, 6.51, 1812220, 4.3, 839.64, 654000, 1796720], ['寵物飲水機', '寵物用品／智能設備', 'NT$1,490－NT$2,890', 4260, 493332, 13033, 2.64, 359800, 27.61, 331, 2.54, 1410060, 3.92, 1087.01, 356000, 1397260], ['寵物除毛刷', '寵物用品／清潔護理', 'NT$520－NT$1,000', 1550, 71462, 2600, 3.64, 13900, 5.35, 149, 5.73, 230950, 16.62, 93.29, 94000, 229250], ['寵物外出水壺', '寵物用品／外出用品', 'NT$490－NT$940', 1480, 482399, 9611, 1.99, 78800, 8.2, 758, 7.89, 1121840, 14.24, 103.96, 381000, 1112940], ['瑜珈彈力帶組', '運動用品／健身配件', 'NT$440－NT$860', 1400, 141436, 4464, 3.16, 50200, 11.25, 50, 1.12, 70000, 1.39, 1004.0, 13000, 69500], ['防滑瑜珈墊', '運動用品／居家健身', 'NT$1,270－NT$2,450', 3610, 315467, 11111, 3.52, 88600, 7.97, 361, 3.25, 1303210, 14.71, 245.43, 541000, 1287310], ['運動水壺', '運動用品／外出補水', 'NT$520－NT$1,000', 1630, 521267, 14939, 2.87, 265000, 17.74, 707, 4.73, 1152410, 4.35, 374.82, 346000, 1137410], ['快乾運動毛巾', '運動用品／戶外用品', 'NT$370－NT$710', 1120, 156657, 2612, 1.67, 15100, 5.78, 166, 6.36, 185920, 12.31, 90.96, 69000, 183520], ['露營LED掛燈', '戶外用品／露營照明', 'NT$740－NT$1,440', 2470, 511793, 11947, 2.33, 202900, 16.98, 779, 6.52, 1924130, 9.48, 260.46, 598000, 1897830], ['戶外折疊椅', '戶外用品／露營家具', 'NT$1,790－NT$3,470', 5120, 1892398, 42457, 2.24, 435200, 10.25, 906, 2.13, 4638720, 10.66, 480.35, 1481000, 4578720], ['便攜餐具組', '戶外用品／旅行餐具', 'NT$370－NT$710', 1250, 275921, 8167, 2.96, 52300, 6.4, 164, 2.01, 205000, 3.92, 318.9, 80000, 202500], ['防水收納乾濕袋', '旅行用品／戶外收納', 'NT$440－NT$860', 1480, 250138, 5573, 2.23, 19000, 3.41, 438, 7.86, 648240, 34.12, 43.38, 261000, 639940], ['兒童防漏水杯', '親子用品／兒童餐具', 'NT$520－NT$1,000', 1680, 522470, 10572, 2.02, 97400, 9.21, 469, 4.44, 787920, 8.09, 207.68, 241000, 778420], ['兒童矽膠圍兜', '親子用品／用餐用品', 'NT$370－NT$710', 1200, 219304, 4396, 2.0, 24600, 5.6, 223, 5.07, 267600, 10.88, 110.31, 110000, 264500], ['嬰兒推車收納袋', '親子用品／外出收納', 'NT$670－NT$1,290', 2000, 297505, 9319, 3.13, 93200, 10.0, 326, 3.5, 652000, 7.0, 285.89, 272000, 644100], ['居家防撞條組', '親子用品／安全防護', 'NT$370－NT$710', 1270, 520220, 12592, 2.42, 90600, 7.2, 301, 2.39, 382270, 4.22, 300.0, 139000, 377470], ['收納抽屜分隔板', '居家收納／衣櫃整理', 'NT$520－NT$1,000', 1550, 136966, 4470, 3.26, 23500, 5.26, 64, 1.43, 99200, 4.22, 367.19, 22000, 98100], ['真空壓縮收納袋', '居家收納／換季整理', 'NT$590－NT$1,150', 1830, 1764705, 37125, 2.1, 525100, 14.14, 1018, 2.74, 1862940, 3.55, 515.82, 672000, 1838640], ['衣物除毛球機', '居家用品／衣物護理', 'NT$670－NT$1,290', 1980, 318646, 8060, 2.53, 60200, 7.47, 564, 7.0, 1116720, 18.55, 106.74, 347000, 1103720], ['迷你熨燙機', '居家用品／衣物整理', 'NT$1,190－NT$2,310', 3400, 292983, 8489, 2.9, 102600, 12.09, 134, 1.58, 455600, 4.44, 765.67, 206000, 449800], ['防藍光眼鏡', '健康用品／護眼配件', 'NT$590－NT$1,150', 1910, 212629, 5674, 2.67, 51700, 9.11, 137, 2.41, 261670, 5.06, 377.37, 116000, 260270], ['睡眠遮光眼罩', '生活用品／睡眠配件', 'NT$440－NT$860', 1400, 1768202, 31075, 1.76, 172100, 5.54, 954, 3.07, 1335600, 7.76, 180.4, 450000, 1315500], ['人體工學滑鼠墊', '辦公用品／桌面配件', 'NT$520－NT$1,000', 1630, 243026, 4095, 1.69, 17700, 4.32, 90, 2.2, 146700, 8.29, 196.67, 34000, 145200], ['桌面理線收納盒', '辦公用品／桌面收納', 'NT$370－NT$710', 740, 117787, 3953, 3.36, 6800, 1.72, 81, 2.05, 59970, 8.82, 83.95, 32000, 59170]]
product_columns = ['商品名稱', '商品類型', '參考單價帶', '平均客單價 AOV', '曝光量 IMP', '點擊量', '點擊率 CTR', '廣告花費', '平均點擊成本 CPC', '成交訂單數', '成交轉換率 CVR', '商品交易總額 GMV', '廣告投資報酬率 ROAS', '單筆成交成本 CPA', '淨利', '扣除退款後營收']
product = pd.DataFrame(product_rows, columns=product_columns)
product_total = pd.DataFrame([{
    "商品名稱": "合計",
    "商品類型": "",
    "參考單價帶": "",
    "平均客單價 AOV": "",
    "曝光量 IMP": 22_436_280,
    "點擊量": 573_482,
    "點擊率 CTR": 2.56,
    "廣告花費": 6_700_000,
    "平均點擊成本 CPC": 11.68,
    "成交訂單數": 18_742,
    "成交轉換率 CVR": 3.27,
    "商品交易總額 GMV": 46_850_000,
    "廣告投資報酬率 ROAS": 6.99,
    "單筆成交成本 CPA": 357.49,
    "淨利": 16_000_000,
    "扣除退款後營收": 46_381_500,
}])
product_display = pd.concat([product, product_total], ignore_index=True)

creative = pd.DataFrame({
    "廣告素材": ['短影音A｜高單價家電開箱', '短影音B｜旅行收納前後對比', '短影音C｜辦公桌面改造', '短影音D｜寵物日常實測', '輪播圖E｜低單價爆品合集', '再行銷F｜購物車限時優惠'],
    "素材類型": ['15秒短影音', '20秒短影音', '18秒短影音', '25秒短影音', '圖文輪播', '再行銷素材'],
    "曝光量 IMP": [5412608, 4988320, 3106944, 2702885, 3648721, 2576802],
    "點擊量": [118394, 151862, 79526, 65228, 112783, 45689],
    "點擊率 CTR": [2.19, 3.04, 2.56, 2.41, 3.09, 1.77],
    "廣告花費": [1548700, 984500, 742400, 931800, 756600, 1736000],
    "平均點擊成本 CPC": [13.08, 6.48, 9.34, 14.29, 6.71, 38.0],
    "成交訂單數": [2492, 5408, 2186, 1719, 5122, 1815],
    "成交轉換率 CVR": [2.1, 3.56, 2.75, 2.64, 4.54, 3.97],
    "商品交易總額 GMV": [10236400, 9781600, 4963900, 5704800, 7946700, 8216600],
    "廣告投資報酬率 ROAS": [6.61, 9.94, 6.69, 6.12, 10.5, 4.73],
    "單筆成交成本 CPA": [621.47, 182.05, 339.62, 542.06, 147.72, 956.47],
})
creative_total = pd.DataFrame([{
    "廣告素材": "合計",
    "素材類型": "",
    "曝光量 IMP": 22_436_280,
    "點擊量": 573_482,
    "點擊率 CTR": 2.56,
    "廣告花費": 6_700_000,
    "平均點擊成本 CPC": 11.68,
    "成交訂單數": 18_742,
    "成交轉換率 CVR": 3.27,
    "商品交易總額 GMV": 46_850_000,
    "廣告投資報酬率 ROAS": 6.99,
    "單筆成交成本 CPA": 357.49,
}])
creative_display = pd.concat([creative, creative_total], ignore_index=True)

device = pd.DataFrame({
    "裝置來源": ["Mobile App / 行動裝置", "Desktop Web / 桌機網頁", "Tablet / 平板", "In-App Webview / 內嵌瀏覽器"],
    "曝光量 IMP": [16_482_705, 3_345_691, 1_506_482, 1_101_402],
    "點擊量": [424_316, 83_508, 38_992, 26_666],
    "點擊率 CTR": [2.57, 2.50, 2.59, 2.42],
    "廣告花費": [4_923_200, 1_037_900, 468_400, 270_500],
    "平均點擊成本 CPC": [11.60, 12.43, 12.01, 10.14],
    "成交訂單數": [13_844, 2_795, 1_274, 829],
    "成交轉換率 CVR": [3.26, 3.35, 3.27, 3.11],
    "商品交易總額 GMV": [34_679_500, 7_023_400, 3_198_700, 1_948_400],
    "廣告投資報酬率 ROAS": [7.04, 6.77, 6.83, 7.20],
    "單筆成交成本 CPA": [355.62, 371.34, 367.66, 326.30],
})
device_total = pd.DataFrame([{
    "裝置來源": "合計",
    "曝光量 IMP": 22_436_280,
    "點擊量": 573_482,
    "點擊率 CTR": 2.56,
    "廣告花費": 6_700_000,
    "平均點擊成本 CPC": 11.68,
    "成交訂單數": 18_742,
    "成交轉換率 CVR": 3.27,
    "商品交易總額 GMV": 46_850_000,
    "廣告投資報酬率 ROAS": 6.99,
    "單筆成交成本 CPA": 357.49,
}])
device_display = pd.concat([device, device_total], ignore_index=True)

age = pd.DataFrame({
    "年齡層": ["18-24", "25-34", "35-44", "45-54", "55+"],
    "曝光量 IMP": [3_704_820, 8_927_318, 5_694_276, 2_646_002, 1_463_864],
    "點擊量": [96_241, 232_805, 145_118, 66_492, 32_826],
    "點擊率 CTR": [2.60, 2.61, 2.55, 2.51, 2.24],
    "廣告花費": [1_104_700, 2_661_800, 1_765_600, 794_300, 373_600],
    "平均點擊成本 CPC": [11.48, 11.43, 12.17, 11.95, 11.38],
    "成交訂單數": [3_026, 7_540, 4_902, 2_176, 1_098],
    "成交轉換率 CVR": [3.14, 3.24, 3.38, 3.27, 3.34],
    "商品交易總額 GMV": [7_482_300, 18_958_600, 12_338_900, 5_488_500, 2_581_700],
    "廣告投資報酬率 ROAS": [6.77, 7.12, 6.99, 6.91, 6.91],
    "單筆成交成本 CPA": [365.07, 353.02, 360.18, 365.03, 340.26],
})
age_total = pd.DataFrame([{
    "年齡層": "合計",
    "曝光量 IMP": 22_436_280,
    "點擊量": 573_482,
    "點擊率 CTR": 2.56,
    "廣告花費": 6_700_000,
    "平均點擊成本 CPC": 11.68,
    "成交訂單數": 18_742,
    "成交轉換率 CVR": 3.27,
    "商品交易總額 GMV": 46_850_000,
    "廣告投資報酬率 ROAS": 6.99,
    "單筆成交成本 CPA": 357.49,
}])
age_display = pd.concat([age, age_total], ignore_index=True)

gender = pd.DataFrame({
    "性別": ["女性", "男性", "未揭露／其他"],
    "曝光量 IMP": [13_847_330, 7_362_915, 1_226_035],
    "點擊量": [356_204, 188_662, 28_616],
    "點擊率 CTR": [2.57, 2.56, 2.33],
    "廣告花費": [4_122_300, 2_252_900, 324_800],
    "平均點擊成本 CPC": [11.57, 11.94, 11.35],
    "成交訂單數": [11_832, 6_185, 725],
    "成交轉換率 CVR": [3.32, 3.28, 2.53],
    "商品交易總額 GMV": [29_624_800, 15_443_600, 1_781_600],
    "廣告投資報酬率 ROAS": [7.19, 6.85, 5.49],
    "單筆成交成本 CPA": [348.40, 364.25, 448.00],
})
gender_total = pd.DataFrame([{
    "性別": "合計",
    "曝光量 IMP": 22_436_280,
    "點擊量": 573_482,
    "點擊率 CTR": 2.56,
    "廣告花費": 6_700_000,
    "平均點擊成本 CPC": 11.68,
    "成交訂單數": 18_742,
    "成交轉換率 CVR": 3.27,
    "商品交易總額 GMV": 46_850_000,
    "廣告投資報酬率 ROAS": 6.99,
    "單筆成交成本 CPA": 357.49,
}])
gender_display = pd.concat([gender, gender_total], ignore_index=True)

# =========================================================
# 轉換與退款、利潤
# =========================================================
funnel = pd.DataFrame({
    "轉換階段": ["曝光量 IMP", "點擊量", "成交訂單數", "商品交易總額 GMV", "扣除退款後營收", "淨利"],
    "數量": [22_436_280, 573_482, 18_742, 46_850_000, 46_381_500, 16_000_000],
    "顯示數值": ["22,436,280", "573,482", "18,742", "NT$46,850,000", "NT$46,381,500", "NT$16,000,000"],
    "與上一階段轉換率": ["-", "2.56%", "3.27%", "-", "99.00%", "34.50%"],
})

refund = pd.DataFrame({
    "日期": daily["日期"].tolist() + ["合計"],
    "成交訂單數": [2_741, 2_182, 3_104, 2_491, 3_218, 1_934, 3_072, 18_742],
    "商品交易總額 GMV": [6_889_400, 5_302_800, 7_613_200, 6_091_700, 7_896_500, 4_656_300, 8_400_100, 46_850_000],
    "退款金額": [66_200, 52_600, 75_900, 61_300, 78_400, 46_800, 87_300, 468_500],
    "扣除退款後營收": [6_823_200, 5_250_200, 7_537_300, 6_030_400, 7_818_100, 4_609_500, 8_312_800, 46_381_500],
    "淨利": [2_318_000, 1_728_000, 2_654_000, 1_996_000, 2_691_000, 1_422_000, 3_191_000, 16_000_000],
})

profit = pd.DataFrame({
    "日期": daily["日期"].tolist() + ["7天合計"],
    "商品交易總額 GMV": [6_889_400, 5_302_800, 7_613_200, 6_091_700, 7_896_500, 4_656_300, 8_400_100, 46_850_000],
    "退款金額": [66_200, 52_600, 75_900, 61_300, 78_400, 46_800, 87_300, 468_500],
    "扣除退款後營收": [6_823_200, 5_250_200, 7_537_300, 6_030_400, 7_818_100, 4_609_500, 8_312_800, 46_381_500],
    "廣告花費": [965_200, 824_600, 1_066_800, 917_400, 1_024_900, 761_500, 1_139_600, 6_700_000],
    "其他成本合計": [3_540_000, 2_697_600, 3_816_500, 3_117_000, 4_102_200, 2_426_000, 3_982_200, 23_681_500],
    "淨利": [2_318_000, 1_728_000, 2_654_000, 1_996_000, 2_691_000, 1_422_000, 3_191_000, 16_000_000],
    "淨利率": [33.97, 32.91, 35.21, 33.10, 34.42, 30.85, 38.39, 34.50],
})

# =========================================================
# 顯示格式
# =========================================================
def display_df(df):
    out = df.copy()
    money_cols = [
        "商品交易總額 GMV", "廣告花費", "淨利", "扣除退款後營收", "退款金額",
        "其他成本合計", "平均客單價 AOV"
    ]
    number_cols = ["曝光量 IMP", "點擊量", "成交訂單數", "排名", "數量"]
    percent_cols = ["點擊率 CTR", "成交轉換率 CVR", "銷售占比", "淨利率"]
    money2_cols = ["平均點擊成本 CPC", "單筆成交成本 CPA"]
    roas_cols = ["廣告投資報酬率 ROAS"]

    for col in out.columns:
        if col in money_cols:
            out[col] = out[col].apply(lambda x: f"NT${x:,.0f}" if isinstance(x, (int, float)) else x)
        elif col in number_cols:
            out[col] = out[col].apply(lambda x: f"{x:,.0f}" if isinstance(x, (int, float)) else x)
        elif col in percent_cols:
            out[col] = out[col].apply(lambda x: f"{x:.2f}%" if isinstance(x, (int, float)) else x)
        elif col in money2_cols:
            out[col] = out[col].apply(lambda x: f"NT${x:,.2f}" if isinstance(x, (int, float)) else x)
        elif col in roas_cols:
            out[col] = out[col].apply(lambda x: f"{x:.2f}x" if isinstance(x, (int, float)) else x)
    return out

# =========================================================
# 圖表工具
# =========================================================
def metric_card(title, value, trend_data, note="", line_color="#7E57C2"):
    with st.container(border=True):
        left, right = st.columns([3, 1])
        with left:
            st.markdown(
    f"""
    <div class="metric-title">
        {title}
    </div>
    """,
    unsafe_allow_html=True
)
            st.markdown(f"<h2 style='margin:0;padding:0;'>{value}</h2>", unsafe_allow_html=True)
        with right:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=trend_data,
                mode="lines",
                line=dict(color=line_color, width=2.5),
                fill="tozeroy",
                fillcolor=rgba(line_color, 0.18)
            ))
            fig.update_layout(
                height=80,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def gauge_chart(title, value, max_value, color, suffix=""):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={
            "suffix": suffix,
            "font": {
                "size": 34,
                "color": "#0f172a",
                "family": "Arial Black"
            }
        },
        gauge={
            "axis": {"range": [0, max_value], "visible": False},
            "bar": {"color": color, "thickness": 0.35},
            "bgcolor": "#e5e7eb",
            "borderwidth": 0,
            "steps": [
                {"range": [0, max_value * .35], "color": "#fee2e2"},
                {"range": [max_value * .35, max_value * .7], "color": "#fef3c7"},
                {"range": [max_value * .7, max_value], "color": "#dcfce7"},
            ],
        },
        title={"text": ""},
    ))

    fig.update_layout(
        height=230,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
    )

    with st.container(border=True):
        st.markdown(
            f"""
            <div class="gauge-title">
                {title}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

def horizontal_bar(title, df, label_col, value_col, color="#2563eb", height=330, text_col=None):
    st.subheader(title)
    max_value = df[value_col].max()
    text_values = df[text_col] if text_col and text_col in df.columns else df[value_col].apply(lambda x: f"{x:,.0f}")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[value_col],
        y=df[label_col],
        orientation="h",
        text=text_values,
        textposition="outside",
        cliponaxis=False,
        marker=dict(color=color),
        textfont=dict(size=13),
    ))
    fig.update_layout(
        height=height,
        margin=dict(l=190, r=190, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, max_value * 1.30]),
        yaxis=dict(autorange="reversed", title="", tickfont=dict(size=14)),
        showlegend=False,
        font=dict(family="Microsoft JhengHei"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def line_chart(title, x, y, name, color="#2563eb", height=330):
    st.subheader(title)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode="lines+markers",
        name=name,
        line=dict(color=color, width=3),
        marker=dict(size=7),
    ))
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Microsoft JhengHei"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# =========================================================
# 頁面
# =========================================================
st.sidebar.header("篩選條件")
st.sidebar.write(f"期間：{PERIOD}")
st.sidebar.write(f"幣別：{CURRENCY}")
st.sidebar.divider()
st.sidebar.caption("資料類型：跨境電商廣告投放")
st.sidebar.caption("資料週期：7 天")

st.title(REPORT_TITLE)
st.caption(f"期間：{PERIOD}｜幣別：{CURRENCY}")

# KPI 卡片
r1 = st.columns(4)
with r1[0]:
    metric_card("曝光量 IMP", number(core["曝光量 IMP"]), daily["曝光量 IMP"], "", "#6D3FD1")
with r1[1]:
    metric_card("點擊量", number(core["點擊量"]), daily["點擊量"], "", "#1FA7A1")
with r1[2]:
    metric_card("點擊率 CTR", percent(core["點擊率 CTR"]), click_trend["點擊率 CTR"], "", "#F0A500")
with r1[3]:
    metric_card("廣告花費", money(core["廣告花費"]), daily["廣告花費"], "", "#EF5350")

r2 = st.columns(4)
with r2[0]:
    metric_card("平均點擊成本 CPC", money2(core["平均點擊成本 CPC"]), click_trend["平均點擊成本 CPC"], "", "#B14AE0")
with r2[1]:
    metric_card("成交訂單數", number(core["成交訂單數"]), daily["成交訂單數"], "", "#42A5F5")
with r2[2]:
    metric_card("成交轉換率 CVR", percent(core["成交轉換率 CVR"]), order_trend["成交轉換率 CVR"], "", "#66BB6A")
with r2[3]:
    metric_card("商品交易總額 GMV", money(core["商品交易總額 GMV"]), daily["商品交易總額 GMV"], "", "#F05A5A")

r3 = st.columns(4)
with r3[0]:
    metric_card("廣告投資報酬率 ROAS", roas(core["廣告投資報酬率 ROAS"]), sales_trend["廣告投資報酬率 ROAS"], "", "#22C55E")
with r3[1]:
    metric_card("單筆成交成本 CPA", money2(core["單筆成交成本 CPA"]), order_trend["單筆成交成本 CPA"], "", "#64748B")
with r3[2]:
    metric_card("淨利", money(core["淨利"]), daily["淨利"], "", "#0EA5E9")
with r3[3]:
    metric_card("扣除退款後營收", money(core["扣除退款後營收"]), daily["扣除退款後營收"], "", "#A855F7")

# 核心總覽
st.subheader("核心成效總覽")
g1, g2, g3 = st.columns([1, 1, 2])

with g1:
    gauge_chart("ROAS 廣告投報", core["廣告投資報酬率 ROAS"], 10, "#22c55e", "x")
with g2:
    gauge_chart("淨利率", 34.50, 50, "#3b82f6", "%")
with g3:
    with st.container(border=True):
        st.markdown("**核心成效總覽表**")
        st.dataframe(core_table, use_container_width=True, hide_index=True, height=330)

horizontal_bar(
    "平台銷售額排名",
    platform_rank,
    "銷售平台／通路",
    "商品交易總額 GMV",
    "#2563eb",
    350,
    text_col="報表顯示",
)

# 報表圖表用資料
st.subheader("報表圖表用資料")
c1, c2 = st.columns(2)

with c1:
    line_chart("每日曝光趨勢", daily["日期"], daily["曝光量 IMP"], "曝光量 IMP", "#2563eb")
    line_chart("每日點擊趨勢", daily["日期"], daily["點擊量"], "點擊量", "#f97316")

with c2:
    line_chart("每日訂單趨勢", daily["日期"], daily["成交訂單數"], "成交訂單數", "#22c55e")
    line_chart("每日銷售額趨勢", daily["日期"], daily["商品交易總額 GMV"], "商品交易總額 GMV", "#a855f7")

st.dataframe(chart_table, use_container_width=True, hide_index=True)

# 分頁
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "每日數據", "平台／市場", "商品／素材", "裝置／受眾", "轉換與退款", "營收與利潤"
])

with tab1:
    st.subheader("每日點擊趨勢")
    st.dataframe(display_df(click_display), use_container_width=True, hide_index=True)

    st.subheader("每日訂單趨勢")
    st.dataframe(display_df(order_display), use_container_width=True, hide_index=True)

    st.subheader("每日銷售額趨勢")
    st.dataframe(display_df(sales_display), use_container_width=True, hide_index=True)

    st.subheader("每日完整投放數據")
    st.dataframe(display_df(daily_full_display), use_container_width=True, hide_index=True)

with tab2:
    st.subheader("平台銷售額排名")
    st.dataframe(display_df(platform_rank_display), use_container_width=True, hide_index=True)

    st.subheader("廣告平台成效")
    st.dataframe(display_df(ad_platform_display), use_container_width=True, hide_index=True)

    st.subheader("國家市場成效")
    st.dataframe(display_df(country_display), use_container_width=True, hide_index=True)

    cc1, cc2 = st.columns(2)
    with cc1:
        horizontal_bar("廣告平台 GMV", ad_platform.sort_values("商品交易總額 GMV", ascending=False), "廣告平台", "商品交易總額 GMV", "#2563eb", 360)
    with cc2:
        horizontal_bar("國家市場 GMV", country.sort_values("商品交易總額 GMV", ascending=False), "國家市場", "商品交易總額 GMV", "#0ea5e9", 360)

with tab3:
    st.subheader("商品銷售成效")
    st.dataframe(display_df(product_display), use_container_width=True, hide_index=True)

    st.subheader("廣告素材成效")
    st.dataframe(display_df(creative_display), use_container_width=True, hide_index=True)

    horizontal_bar("商品 GMV", product.sort_values("商品交易總額 GMV", ascending=False), "商品名稱", "商品交易總額 GMV", "#22c55e", 1150)
    horizontal_bar("廣告素材 GMV", creative.sort_values("商品交易總額 GMV", ascending=False), "廣告素材", "商品交易總額 GMV", "#f97316", 420)

with tab4:
    st.subheader("裝置來源成效")
    st.dataframe(display_df(device_display), use_container_width=True, hide_index=True)

    st.subheader("受眾年齡成效")
    st.dataframe(display_df(age_display), use_container_width=True, hide_index=True)

    st.subheader("受眾性別成效")
    st.dataframe(display_df(gender_display), use_container_width=True, hide_index=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        horizontal_bar("裝置來源 GMV", device.sort_values("商品交易總額 GMV", ascending=False), "裝置來源", "商品交易總額 GMV", "#2563eb", 340)
    with d2:
        horizontal_bar("受眾年齡 GMV", age.sort_values("商品交易總額 GMV", ascending=False), "年齡層", "商品交易總額 GMV", "#a855f7", 340)
    with d3:
        horizontal_bar("受眾性別 GMV", gender.sort_values("商品交易總額 GMV", ascending=False), "性別", "商品交易總額 GMV", "#ec4899", 340)

with tab5:
    st.subheader("顧客轉換路徑")

    fig_funnel = go.Figure()
    fig_funnel.add_trace(go.Bar(
        x=funnel["數量"],
        y=funnel["轉換階段"],
        orientation="h",
        text=funnel["顯示數值"],
        textposition="outside",
        cliponaxis=False,
        marker=dict(color=["#2563eb", "#7c3aed", "#10b981", "#f59e0b", "#0ea5e9", "#22c55e"]),
    ))
    fig_funnel.update_layout(
        height=430,
        margin=dict(l=170, r=190, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[0, funnel["數量"].max() * 1.25]),
        yaxis=dict(autorange="reversed", title=""),
        showlegend=False,
        font=dict(family="Microsoft JhengHei"),
    )
    st.plotly_chart(fig_funnel, use_container_width=True, config={"displayModeBar": False})

    st.dataframe(funnel[["轉換階段", "顯示數值", "與上一階段轉換率"]], use_container_width=True, hide_index=True)

    st.subheader("訂單與退款資料")
    st.dataframe(display_df(refund), use_container_width=True, hide_index=True)

with tab6:
    st.subheader("營收與利潤")
    st.dataframe(display_df(profit), use_container_width=True, hide_index=True)

    profit_chart = pd.DataFrame({
        "項目": ["扣除退款後營收", "廣告花費", "其他成本合計", "淨利"],
        "金額": [46_381_500, 6_700_000, 23_681_500, 16_000_000],
        "顯示": ["4,638.2 萬", "670.0 萬", "2,368.2 萬", "1,600.0 萬"],
    })
    horizontal_bar("營收與利潤結構", profit_chart, "項目", "金額", "#22c55e", 390, text_col="顯示")

st.markdown("<div class='section-title'>關鍵摘要</div>", unsafe_allow_html=True)
st.markdown(f"""
<div class="summary-box">
本期 <b>{REPORT_TITLE}</b> 期間為 <b>{PERIOD}</b>。<br>
曝光量 IMP <b>{number(core['曝光量 IMP'])}</b>、點擊量 <b>{number(core['點擊量'])}</b>、點擊率 CTR <b>{percent(core['點擊率 CTR'])}</b>。<br>
廣告花費 <b>{money(core['廣告花費'])}</b>，成交訂單數 <b>{number(core['成交訂單數'])}</b>，商品交易總額 GMV <b>{money(core['商品交易總額 GMV'])}</b>。<br>
廣告投資報酬率 ROAS <b>{roas(core['廣告投資報酬率 ROAS'])}</b>，單筆成交成本 CPA <b>{money2(core['單筆成交成本 CPA'])}</b>。<br>
淨利 <b>{money(core['淨利'])}</b>，扣除退款後營收 <b>{money(core['扣除退款後營收'])}</b>。
</div>
""", unsafe_allow_html=True)
