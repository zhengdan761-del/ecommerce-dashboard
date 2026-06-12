
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# =========================================================
# 原始報表資料
# =========================================================
RAW_DATA = """核心成效總覽

項目	數值
期間	2026/06/05－2026/06/12
幣別	NTD 新台幣
曝光量 IMP	18,734,650
點擊量	456,820
點擊率 CTR	2.44%
廣告花費	NT$5,780,000
平均點擊成本 CPC	NT$12.65
成交訂單數	16,384
成交轉換率 CVR	3.59%
商品交易總額 GMV	NT$33,620,000
廣告投資報酬率 ROAS	5.82x
單筆成交成本 CPA	NT$352.78
淨利	NT$6,845,304
扣除退款後營收	NT$33,233,370

報表圖表用資料

圖表資料	2026/06/05	2026/06/06	2026/06/07	2026/06/08	2026/06/09	2026/06/10	2026/06/11	2026/06/12	合計
曝光量 IMP	2,165,180	2,416,940	1,983,210	2,798,705	3,122,660	1,727,425	1,984,600	2,535,930	18,734,650
點擊量	53,820	60,435	48,790	70,860	78,620	42,175	51,240	50,880	456,820
成交訂單數	1,936	2,284	1,675	2,712	3,088	1,326	1,817	1,546	16,384
商品交易總額 GMV	NT$3,826,500	NT$4,313,200	NT$3,037,600	NT$4,938,100	NT$6,042,900	NT$2,484,800	NT$3,279,100	NT$5,697,800	NT$33,620,000
廣告花費	NT$786,400	NT$642,300	NT$934,800	NT$715,600	NT$824,900	NT$703,500	NT$612,800	NT$559,700	NT$5,780,000
淨利	NT$418,000	NT$1,234,000	NT$303,000	NT$1,496,000	NT$1,943,000	NT$186,000	NT$602,000	NT$663,304	NT$6,845,304
扣除退款後營收	NT$3,783,700	NT$4,263,050	NT$2,998,000	NT$4,885,500	NT$5,973,800	NT$2,451,400	NT$3,237,920	NT$5,640,000	NT$33,233,370

每日點擊趨勢

日期	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC
2026/06/05	2,165,180	53,820	2.49%	NT$786,400	NT$14.61
2026/06/06	2,416,940	60,435	2.50%	NT$642,300	NT$10.63
2026/06/07	1,983,210	48,790	2.46%	NT$934,800	NT$19.16
2026/06/08	2,798,705	70,860	2.53%	NT$715,600	NT$10.10
2026/06/09	3,122,660	78,620	2.52%	NT$824,900	NT$10.49
2026/06/10	1,727,425	42,175	2.44%	NT$703,500	NT$16.68
2026/06/11	1,984,600	51,240	2.58%	NT$612,800	NT$11.96
2026/06/12	2,535,930	50,880	2.01%	NT$559,700	NT$11.00
合計	18,734,650	456,820	2.44%	NT$5,780,000	NT$12.65

每日訂單趨勢

日期	點擊量	成交訂單數	成交轉換率 CVR	廣告花費	單筆成交成本 CPA
2026/06/05	53,820	1,936	3.60%	NT$786,400	NT$406.20
2026/06/06	60,435	2,284	3.78%	NT$642,300	NT$281.22
2026/06/07	48,790	1,675	3.43%	NT$934,800	NT$558.09
2026/06/08	70,860	2,712	3.83%	NT$715,600	NT$263.86
2026/06/09	78,620	3,088	3.93%	NT$824,900	NT$267.13
2026/06/10	42,175	1,326	3.14%	NT$703,500	NT$530.54
2026/06/11	51,240	1,817	3.55%	NT$612,800	NT$337.26
2026/06/12	50,880	1,546	3.04%	NT$559,700	NT$362.03
合計	456,820	16,384	3.59%	NT$5,780,000	NT$352.78

每日銷售額趨勢

日期	成交訂單數	商品交易總額 GMV	廣告花費	廣告投資報酬率 ROAS	淨利	扣除退款後營收	淨利率
2026/06/05	1,936	NT$3,826,500	NT$786,400	4.87x	NT$418,000	NT$3,783,700	11.05%
2026/06/06	2,284	NT$4,313,200	NT$642,300	6.71x	NT$1,234,000	NT$4,263,050	28.95%
2026/06/07	1,675	NT$3,037,600	NT$934,800	3.25x	NT$303,000	NT$2,998,000	10.11%
2026/06/08	2,712	NT$4,938,100	NT$715,600	6.90x	NT$1,496,000	NT$4,885,500	30.62%
2026/06/09	3,088	NT$6,042,900	NT$824,900	7.33x	NT$1,943,000	NT$5,973,800	32.53%
2026/06/10	1,326	NT$2,484,800	NT$703,500	3.53x	NT$186,000	NT$2,451,400	7.59%
2026/06/11	1,817	NT$3,279,100	NT$612,800	5.35x	NT$602,000	NT$3,237,920	18.59%
2026/06/12	1,546	NT$5,697,800	NT$559,700	10.18x	NT$663,304	NT$5,640,000	11.76%
合計	16,384	NT$33,620,000	NT$5,780,000	5.82x	NT$6,845,304	NT$33,233,370	20.60%

平台銷售額排名

排名	銷售平台／通路	成交訂單數	商品交易總額 GMV	銷售占比
1	自有品牌站／Shopify Plus	7,045	NT$14,120,400	42.00%
2	TikTok Shop	3,604	NT$7,732,600	23.00%
3	Amazon Marketplace	2,540	NT$5,379,200	16.00%
4	eBay	1,343	NT$2,689,600	8.00%
5	Shopee Cross-border	1,114	NT$2,185,300	6.50%
6	Walmart Marketplace	738	NT$1,512,900	4.50%
合計		16,384	NT$33,620,000	100.00%

每日完整投放數據

日期	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	淨利	扣除退款後營收	淨利率
2026/06/05	2,165,180	53,820	2.49%	NT$786,400	NT$14.61	1,936	3.60%	NT$3,826,500	4.87x	NT$406.20	NT$418,000	NT$3,783,700	11.05%
2026/06/06	2,416,940	60,435	2.50%	NT$642,300	NT$10.63	2,284	3.78%	NT$4,313,200	6.71x	NT$281.22	NT$1,234,000	NT$4,263,050	28.95%
2026/06/07	1,983,210	48,790	2.46%	NT$934,800	NT$19.16	1,675	3.43%	NT$3,037,600	3.25x	NT$558.09	NT$303,000	NT$2,998,000	10.11%
2026/06/08	2,798,705	70,860	2.53%	NT$715,600	NT$10.10	2,712	3.83%	NT$4,938,100	6.90x	NT$263.86	NT$1,496,000	NT$4,885,500	30.62%
2026/06/09	3,122,660	78,620	2.52%	NT$824,900	NT$10.49	3,088	3.93%	NT$6,042,900	7.33x	NT$267.13	NT$1,943,000	NT$5,973,800	32.53%
2026/06/10	1,727,425	42,175	2.44%	NT$703,500	NT$16.68	1,326	3.14%	NT$2,484,800	3.53x	NT$530.54	NT$186,000	NT$2,451,400	7.59%
2026/06/11	1,984,600	51,240	2.58%	NT$612,800	NT$11.96	1,817	3.55%	NT$3,279,100	5.35x	NT$337.26	NT$602,000	NT$3,237,920	18.59%
2026/06/12	2,535,930	50,880	2.01%	NT$559,700	NT$11.00	1,546	3.04%	NT$5,697,800	10.18x	NT$362.03	NT$663,304	NT$5,640,000	11.76%
合計	18,734,650	456,820	2.44%	NT$5,780,000	NT$12.65	16,384	3.59%	NT$33,620,000	5.82x	NT$352.78	NT$6,845,304	NT$33,233,370	20.60%

廣告平台成效

廣告平台	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
TikTok Ads	7,306,514	187,296	2.56%	NT$2,254,200	NT$12.04	6,226	3.32%	NT$12,103,200	5.37x	NT$362.05	NT$11,963,988	NT$1,095,249	9.16%
Meta Ads	5,433,049	127,910	2.35%	NT$1,473,900	NT$11.52	5,079	3.97%	NT$10,758,400	7.30x	NT$290.19	NT$10,634,682	NT$2,601,216	24.46%
Google Ads	3,372,237	73,091	2.17%	NT$1,184,900	NT$16.21	2,621	3.59%	NT$6,051,600	5.11x	NT$452.08	NT$5,982,044	NT$1,300,608	21.74%
Pinterest Ads	1,405,099	41,114	2.93%	NT$375,700	NT$9.14	1,557	3.79%	NT$2,857,700	7.61x	NT$241.30	NT$2,824,848	NT$1,369,061	48.46%
Snapchat Ads	1,217,751	27,409	2.25%	NT$491,300	NT$17.92	901	3.29%	NT$1,849,100	3.76x	NT$545.28	NT$1,827,808	NT$479,170	26.22%
合計	18,734,650	456,820	2.44%	NT$5,780,000	NT$12.65	16,384	3.59%	NT$33,620,000	5.82x	NT$352.78	NT$33,233,370	NT$6,845,304	20.60%

國家市場成效

國家市場	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
United States 美國	7,306,514	187,296	2.56%	NT$2,340,900	NT$12.50	6,390	3.41%	NT$12,775,600	5.46x	NT$366.34	NT$12,628,654	NT$1,369,061	10.84%
United Kingdom 英國	2,997,544	77,659	2.59%	NT$953,700	NT$12.28	2,785	3.59%	NT$6,051,600	6.34x	NT$342.44	NT$5,982,044	NT$2,395,856	40.05%
Canada 加拿大	2,622,851	61,671	2.35%	NT$809,200	NT$13.12	2,376	3.85%	NT$5,043,000	6.23x	NT$340.57	NT$4,985,036	NT$1,163,702	23.34%
Australia 澳洲	2,060,812	50,250	2.44%	NT$751,400	NT$14.95	1,720	3.42%	NT$3,866,300	5.15x	NT$436.86	NT$3,821,821	NT$479,171	12.54%
Japan 日本	1,873,465	38,830	2.07%	NT$520,200	NT$13.40	1,229	3.17%	NT$3,025,800	5.82x	NT$423.27	NT$2,991,008	NT$342,265	11.44%
Singapore 新加坡	1,030,406	27,409	2.66%	NT$260,100	NT$9.49	1,229	4.48%	NT$1,849,100	7.11x	NT$211.64	NT$1,827,808	NT$889,890	48.69%
Malaysia 馬來西亞	843,058	13,705	1.63%	NT$144,500	NT$10.54	655	4.78%	NT$1,008,600	6.98x	NT$220.61	NT$997,000	NT$205,359	20.60%
合計	18,734,650	456,820	2.44%	NT$5,780,000	NT$12.65	16,384	3.59%	NT$33,620,000	5.82x	NT$352.78	NT$33,233,370	NT$6,845,304	20.60%

商品銷售成效

商品名稱	商品類型	參考單價帶	平均客單價 AOV	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	淨利	扣除退款後營收	淨利率
智能香氛小夜燈	居家氛圍／生活小家電	NT$970－NT$1,870	NT$2,053.05	181,560	5,181	2.85%	NT$31,470	NT$6.07	181	3.49%	NT$371,602	11.81x	NT$173.87	NT$142,310	NT$368,152	38.65%
桌面空氣循環扇	辦公室／居家小家電	NT$1,040－NT$2,020	NT$2,739.81	190,266	5,352	2.81%	NT$70,790	NT$13.23	227	4.24%	NT$621,938	8.79x	NT$311.85	NT$196,090	NT$616,158	31.82%
智能空氣淨化器	居家健康／空氣清潔設備	NT$3,740－NT$7,240	NT$6,861.94	115,078	3,768	3.27%	NT$52,020	NT$13.81	31	0.82%	NT$212,720	4.09x	NT$1,678.06	NT$16,170	NT$210,580	7.68%
智能廚房秤	廚房用品／智能小工具	NT$520－NT$1,000	NT$1,305.17	117,668	3,599	3.06%	NT$37,480	NT$10.41	153	4.25%	NT$199,691	5.33x	NT$244.97	NT$64,520	NT$198,031	32.58%
便攜式保溫杯	生活用品／外出隨行	NT$590－NT$1,150	NT$1,716.36	178,374	5,056	2.83%	NT$64,280	NT$12.71	227	4.49%	NT$389,413	6.06x	NT$283.17	NT$123,960	NT$382,463	32.41%
多功能收納包	旅行／居家收納用品	NT$670－NT$1,290	NT$2,098.79	211,891	4,264	2.01%	NT$72,520	NT$17.01	181	4.24%	NT$379,881	5.24x	NT$400.66	NT$100,750	NT$377,421	26.69%
旅行壓縮袋組	旅行用品／行李收納	NT$820－NT$1,580	NT$2,462.84	599,910	13,964	2.33%	NT$186,760	NT$13.37	863	6.18%	NT$2,125,630	11.38x	NT$216.41	NT$1,050,220	NT$2,099,050	50.03%
磁吸式無線充電座	3C配件／桌面充電	NT$970－NT$1,870	NT$3,229.25	218,142	5,845	2.68%	NT$89,280	NT$15.27	136	2.33%	NT$439,178	4.92x	NT$656.47	NT$59,380	NT$434,698	13.66%
藍牙降噪耳機	3C配件／影音設備	NT$1,870－NT$3,610	NT$5,822.09	649,880	19,125	2.94%	NT$204,360	NT$10.69	227	1.19%	NT$1,321,614	6.47x	NT$900.26	NT$254,740	NT$1,303,754	19.54%
手機防水收納袋	戶外用品／手機配件	NT$290－NT$570	NT$905.74	609,037	16,686	2.74%	NT$144,970	NT$8.69	681	4.08%	NT$616,807	4.25x	NT$212.88	NT$195,630	NT$609,477	32.10%
摺疊式手機支架	3C配件／桌面用品	NT$340－NT$650	NT$1,043.59	358,288	7,727	2.16%	NT$41,600	NT$5.38	499	6.46%	NT$520,750	12.52x	NT$83.37	NT$206,610	NT$513,600	40.23%
LED補光化妝鏡	美妝工具／居家小物	NT$890－NT$1,730	NT$2,392.84	229,653	4,261	1.86%	NT$106,410	NT$24.97	182	4.27%	NT$435,497	4.09x	NT$584.67	NT$88,510	NT$430,557	20.56%
電動筋膜按摩器	健康放鬆／按摩設備	NT$2,240－NT$4,340	NT$6,219.92	749,579	19,223	2.56%	NT$290,550	NT$15.11	136	0.71%	NT$845,909	2.91x	NT$2,136.40	NT$73,550	NT$835,699	8.80%
頸掛式小風扇	夏季用品／個人小家電	NT$740－NT$1,440	NT$2,096.26	437,815	13,048	2.98%	NT$137,450	NT$10.53	409	3.13%	NT$857,370	6.24x	NT$336.06	NT$362,620	NT$850,440	42.64%
USB加熱暖手寶	冬季用品／生活小家電	NT$520－NT$1,000	NT$1,560.91	297,213	7,721	2.60%	NT$97,480	NT$12.62	318	4.12%	NT$496,370	5.09x	NT$306.54	NT$129,050	NT$491,710	26.25%
智能感應垃圾桶	居家用品／智能生活	NT$1,420－NT$2,740	NT$4,658.15	150,821	3,292	2.18%	NT$33,220	NT$10.09	136	4.13%	NT$633,509	19.07x	NT$244.26	NT$106,890	NT$628,649	17.00%
防滑浴室地墊	居家用品／浴室收納	NT$440－NT$860	NT$1,232.72	309,453	7,101	2.29%	NT$53,690	NT$7.56	272	3.83%	NT$335,300	6.24x	NT$197.39	NT$157,830	NT$330,890	47.69%
廚房瀝水置物架	廚房用品／收納整理	NT$890－NT$1,730	NT$2,681.30	421,982	13,011	3.08%	NT$104,720	NT$8.05	318	2.44%	NT$852,655	8.14x	NT$329.31	NT$384,910	NT$846,525	45.47%
矽膠保鮮袋組	廚房用品／環保收納	NT$370－NT$710	NT$1,178.64	115,276	2,901	2.52%	NT$21,060	NT$7.26	45	1.55%	NT$53,039	2.52x	NT$468.00	NT$10,090	NT$52,639	19.17%
不鏽鋼保鮮盒	廚房用品／食物收納	NT$670－NT$1,290	NT$2,086.79	391,404	10,522	2.69%	NT$61,670	NT$5.86	363	3.45%	NT$757,104	12.28x	NT$169.89	NT$335,170	NT$752,634	44.53%
可折疊購物袋	生活用品／外出收納	NT$290－NT$570	NT$945.67	559,598	18,182	3.25%	NT$118,920	NT$6.54	454	2.50%	NT$429,334	3.61x	NT$261.94	NT$200,430	NT$423,314	47.35%
旅行盥洗收納包	旅行用品／盥洗收納	NT$590－NT$1,150	NT$1,725.27	226,830	6,599	2.91%	NT$36,840	NT$5.58	159	2.41%	NT$274,318	7.45x	NT$231.70	NT$96,550	NT$272,538	35.43%
護照證件收納包	旅行用品／證件收納	NT$520－NT$1,000	NT$1,559.14	124,179	4,228	3.40%	NT$12,990	NT$3.07	68	1.61%	NT$106,021	8.16x	NT$191.03	NT$41,530	NT$104,891	39.59%
行李箱電子秤	旅行用品／行李配件	NT$440－NT$860	NT$1,250.81	207,391	4,613	2.22%	NT$63,060	NT$13.67	227	4.92%	NT$283,933	4.50x	NT$277.80	NT$96,520	NT$282,333	34.19%
車用手機支架	汽車用品／車內配件	NT$590－NT$1,150	NT$1,856.08	310,480	10,087	3.25%	NT$116,680	NT$11.57	159	1.58%	NT$295,117	2.53x	NT$733.84	NT$52,180	NT$292,757	17.82%
車用香氛擴香器	汽車用品／車內香氛	NT$740－NT$1,440	NT$2,123.89	370,927	13,358	3.60%	NT$167,500	NT$12.54	182	1.36%	NT$386,548	2.31x	NT$920.33	NT$34,450	NT$382,528	9.01%
車用吸塵器	汽車用品／清潔設備	NT$1,190－NT$2,310	NT$3,607.36	312,377	8,279	2.65%	NT$132,600	NT$16.02	318	3.84%	NT$1,147,141	8.65x	NT$416.98	NT$223,060	NT$1,133,581	19.68%
寵物飲水機	寵物用品／智能設備	NT$1,490－NT$2,890	NT$3,898.43	488,628	10,254	2.10%	NT$266,350	NT$25.98	340	3.32%	NT$1,325,466	4.98x	NT$783.38	NT$152,660	NT$1,318,676	11.58%
寵物除毛刷	寵物用品／清潔護理	NT$520－NT$1,000	NT$1,453.81	362,610	6,569	1.81%	NT$96,820	NT$14.74	477	7.26%	NT$693,466	7.16x	NT$202.98	NT$81,900	NT$683,076	11.99%
寵物外出水壺	寵物用品／外出用品	NT$490－NT$940	NT$1,303.17	373,644	10,463	2.80%	NT$180,260	NT$17.23	205	1.96%	NT$267,149	1.48x	NT$879.32	NT$48,010	NT$263,969	18.19%
瑜珈彈力帶組	運動用品／健身配件	NT$440－NT$860	NT$1,259.08	524,780	13,324	2.54%	NT$148,810	NT$11.17	454	3.41%	NT$571,624	3.84x	NT$327.78	NT$101,430	NT$564,104	17.98%
防滑瑜珈墊	運動用品／居家健身	NT$1,270－NT$2,450	NT$3,476.51	1,278,025	25,012	1.96%	NT$190,370	NT$7.61	908	3.63%	NT$3,156,676	16.58x	NT$209.66	NT$1,057,700	NT$3,115,436	33.95%
運動水壺	運動用品／外出補水	NT$520－NT$1,000	NT$1,416.53	125,387	4,336	3.46%	NT$27,330	NT$6.30	91	2.10%	NT$128,904	4.72x	NT$300.33	NT$29,430	NT$127,804	23.03%
快乾運動毛巾	運動用品／戶外用品	NT$370－NT$710	NT$1,031.20	255,753	5,493	2.15%	NT$57,560	NT$10.48	227	4.13%	NT$234,081	4.07x	NT$253.57	NT$57,180	NT$230,701	24.79%
露營LED掛燈	戶外用品／露營照明	NT$740－NT$1,440	NT$2,523.92	1,258,855	32,131	2.55%	NT$305,510	NT$9.51	545	1.70%	NT$1,375,538	4.50x	NT$560.57	NT$495,510	NT$1,357,568	36.50%
戶外折疊椅	戶外用品／露營家具	NT$1,790－NT$3,470	NT$5,412.77	380,372	8,063	2.12%	NT$114,160	NT$14.16	159	1.97%	NT$860,631	7.54x	NT$717.99	NT$377,580	NT$850,151	44.41%
便攜餐具組	戶外用品／旅行餐具	NT$370－NT$710	NT$1,170.45	167,832	4,832	2.88%	NT$28,420	NT$5.88	91	1.88%	NT$106,511	3.75x	NT$312.31	NT$18,960	NT$105,111	18.04%
防水收納乾濕袋	旅行用品／戶外收納	NT$440－NT$860	NT$1,231.60	125,425	2,706	2.16%	NT$47,260	NT$17.46	136	5.03%	NT$167,497	3.54x	NT$347.50	NT$46,040	NT$166,097	27.72%
兒童防漏水杯	親子用品／兒童餐具	NT$520－NT$1,000	NT$1,494.70	148,482	3,760	2.53%	NT$46,570	NT$12.39	91	2.42%	NT$136,018	2.92x	NT$511.76	NT$38,180	NT$134,718	28.34%
兒童矽膠圍兜	親子用品／用餐用品	NT$370－NT$710	NT$1,129.23	394,892	9,800	2.48%	NT$138,490	NT$14.13	636	6.49%	NT$718,190	5.19x	NT$217.75	NT$163,500	NT$706,820	23.13%
嬰兒推車收納袋	親子用品／外出收納	NT$670－NT$1,290	NT$1,804.43	179,983	4,983	2.77%	NT$46,980	NT$9.43	136	2.73%	NT$245,402	5.22x	NT$345.44	NT$83,520	NT$242,922	34.38%
居家防撞條組	親子用品／安全防護	NT$370－NT$710	NT$1,070.14	275,762	7,187	2.61%	NT$121,550	NT$16.91	272	3.78%	NT$291,077	2.39x	NT$446.88	NT$77,060	NT$287,277	26.82%
收納抽屜分隔板	居家收納／衣櫃整理	NT$520－NT$1,000	NT$1,411.90	412,647	9,626	2.33%	NT$131,380	NT$13.65	431	4.48%	NT$608,528	4.63x	NT$304.83	NT$192,140	NT$603,458	31.84%
真空壓縮收納袋	居家收納／換季整理	NT$590－NT$1,150	NT$1,774.90	487,497	11,788	2.42%	NT$131,690	NT$11.17	1,270	10.77%	NT$2,254,119	17.12x	NT$103.69	NT$1,030,960	NT$2,225,049	46.33%
衣物除毛球機	居家用品／衣物護理	NT$670－NT$1,290	NT$1,919.98	1,314,681	34,356	2.61%	NT$213,310	NT$6.21	1,089	3.17%	NT$2,090,858	9.80x	NT$195.88	NT$846,620	NT$2,066,538	40.97%
迷你熨燙機	居家用品／衣物整理	NT$1,190－NT$2,310	NT$3,266.04	370,330	11,066	2.99%	NT$132,740	NT$11.99	318	2.87%	NT$1,038,600	7.82x	NT$417.42	NT$278,560	NT$1,025,540	27.16%
防藍光眼鏡	健康用品／護眼配件	NT$590－NT$1,150	NT$1,936.37	382,570	12,060	3.15%	NT$151,860	NT$12.59	227	1.88%	NT$439,556	2.89x	NT$669.00	NT$69,700	NT$435,306	16.01%
睡眠遮光眼罩	生活用品／睡眠配件	NT$440－NT$860	NT$1,164.61	852,148	24,014	2.82%	NT$119,220	NT$4.96	727	3.03%	NT$846,872	7.10x	NT$163.99	NT$195,580	NT$834,022	23.45%
人體工學滑鼠墊	辦公用品／桌面配件	NT$520－NT$1,000	NT$1,591.20	221,623	7,207	3.25%	NT$72,280	NT$10.03	272	3.77%	NT$432,807	5.99x	NT$265.74	NT$172,830	NT$428,607	40.32%
桌面理線收納盒	辦公用品／桌面收納	NT$370－NT$710	NT$626.71	577,093	12,199	2.11%	NT$128,040	NT$10.50	363	2.98%	NT$227,494	1.78x	NT$352.73	NT$41,020	NT$224,464	18.27%
合計				18,734,650	456,820	2.44%	NT$5,780,000	NT$12.65	16,384	3.59%	NT$33,620,000	5.82x	NT$352.78	NT$6,845,304	NT$33,233,370	20.60%

廣告素材成效

廣告素材	素材類型	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
短影音A｜高單價家電開箱	15秒短影音	4,496,316	91,364	2.03%	NT$1,387,200	NT$15.18	2,785	3.05%	NT$7,396,400	5.33x	NT$498.10	NT$7,311,320	NT$684,530	9.36%
短影音B｜旅行收納前後對比	20秒短影音	3,559,584	105,069	2.95%	NT$867,000	NT$8.25	3,932	3.74%	NT$7,060,200	8.14x	NT$220.50	NT$6,979,207	NT$2,190,497	31.39%
短影音C｜辦公桌面改造	18秒短影音	2,716,024	63,955	2.35%	NT$809,200	NT$12.65	2,458	3.84%	NT$4,538,700	5.61x	NT$329.21	NT$4,486,489	NT$1,300,608	28.99%
短影音D｜寵物日常實測	25秒短影音	2,435,504	54,818	2.25%	NT$1,098,200	NT$20.03	2,130	3.89%	NT$4,370,600	3.98x	NT$515.59	NT$4,320,324	NT$821,436	19.01%
輪播圖E｜低單價爆品合集	圖文輪播	3,184,891	100,500	3.16%	NT$751,400	NT$7.48	3,768	3.75%	NT$5,379,200	7.16x	NT$199.42	NT$5,317,304	NT$1,437,514	27.04%
再行銷F｜購物車限時優惠	再行銷素材	2,342,331	41,114	1.76%	NT$867,000	NT$21.09	1,311	3.19%	NT$4,874,900	5.62x	NT$661.33	NT$4,818,727	NT$410,719	8.52%
合計	18,734,650	456,820	2.44%	NT$5,780,000	NT$12.65	16,384	3.59%	NT$33,620,000	5.82x	NT$352.78	NT$33,233,370	NT$6,845,304	20.60%	

裝置來源成效

裝置來源	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
Mobile App / 行動裝置	13,488,948	335,763	2.49%	NT$4,046,000	NT$12.05	11,796	3.51%	NT$23,870,200	5.90x	NT$343.00	NT$23,595,625	NT$3,970,276	16.83%
Desktop Web / 桌機網頁	3,184,891	73,091	2.29%	NT$1,040,400	NT$14.23	2,949	4.03%	NT$6,219,700	5.98x	NT$352.80	NT$6,148,158	NT$1,300,608	21.16%
Tablet / 平板	1,311,426	29,693	2.26%	NT$433,500	NT$14.60	1,065	3.59%	NT$2,353,400	5.43x	NT$407.04	NT$2,326,318	NT$1,026,796	44.14%
In-App Webview / 內嵌瀏覽器	749,386	18,273	2.44%	NT$260,100	NT$14.23	574	3.14%	NT$1,176,700	4.52x	NT$453.14	NT$1,163,269	NT$547,624	47.08%
合計	18,734,650	456,820	2.44%	NT$5,780,000	NT$12.65	16,384	3.59%	NT$33,620,000	5.82x	NT$352.78	NT$33,233,370	NT$6,845,304	20.60%

受眾年齡成效

年齡層	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
18-24	3,372,237	91,364	2.71%	NT$1,040,400	NT$11.39	2,785	3.05%	NT$5,379,200	5.17x	NT$373.57	NT$5,317,304	NT$889,890	16.74%
25-34	6,931,821	178,160	2.57%	NT$2,312,000	NT$12.98	6,881	3.86%	NT$14,120,400	6.11x	NT$335.99	NT$13,957,925	NT$2,874,028	20.59%
35-44	5,058,356	114,205	2.26%	NT$1,445,000	NT$12.65	4,096	3.59%	NT$8,741,200	6.05x	NT$352.78	NT$8,640,648	NT$1,506, -	
45-54	2,248,158	50,250	2.24%	NT$693,600	NT$13.80	1,802	3.59%	NT$3,698,200	5.33x	NT$384.91	NT$3,655,531	NT$547,624	14.98%
55+	1,124,079	22,841	2.03%	NT$289,000	NT$12.65	820	3.59%	NT$1,681,000	5.82x	NT$352.44	NT$1,661,963	NT$1,026,796	61.78%
合計	18,734,650	456,820	2.44%	NT$5,780,000	NT$12.65	16,384	3.59%	NT$33,620,000	5.82x	NT$352.78	NT$33,233,370	NT$6,845,304	20.60%

受眾性別成效

性別	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC	成交訂單數	成交轉換率 CVR	商品交易總額 GMV	廣告投資報酬率 ROAS	單筆成交成本 CPA	扣除退款後營收	淨利	淨利率
女性	11,615,483	292,365	2.52%	NT$3,468,000	NT$11.86	10,322	3.53%	NT$20,508,200	5.91x	NT$335.97	NT$20,272,299	NT$3,833,370	18.91%
男性	5,995,088	137,046	2.29%	NT$1,907,400	NT$13.92	5,243	3.83%	NT$11,430,800	5.99x	NT$363.80	NT$11,299,501	NT$2,190,497	19.39%
未揭露／其他	1,124,079	27,409	2.44%	NT$404,600	NT$14.76	819	2.99%	NT$1,681,000	4.15x	NT$494.02	NT$1,661,570	NT$821,437	49.44%
合計	18,734,650	456,820	2.44%	NT$5,780,000	NT$12.65	16,384	3.59%	NT$33,620,000	5.82x	NT$352.78	NT$33,233,370	NT$6,845,304	20.60%

顧客轉換路徑

轉換階段	數量	與上一階段轉換率
曝光量 IMP	18,734,650	-
點擊量	456,820	2.44%
成交訂單數	16,384	3.59%
商品交易總額 GMV	NT$33,620,000	-
扣除退款後營收	NT$33,233,370	98.85%
淨利	NT$6,845,304	20.60%

訂單與退款資料

日期	成交訂單數	商品交易總額 GMV	退款金額	扣除退款後營收	淨利
2026/06/05	1,936	NT$3,826,500	NT$42,800	NT$3,783,700	NT$418,000
2026/06/06	2,284	NT$4,313,200	NT$50,150	NT$4,263,050	NT$1,234,000
2026/06/07	1,675	NT$3,037,600	NT$39,600	NT$2,998,000	NT$303,000
2026/06/08	2,712	NT$4,938,100	NT$52,600	NT$4,885,500	NT$1,496,000
2026/06/09	3,088	NT$6,042,900	NT$69,100	NT$5,973,800	NT$1,943,000
2026/06/10	1,326	NT$2,484,800	NT$33,400	NT$2,451,400	NT$186,000
2026/06/11	1,817	NT$3,279,100	NT$41,180	NT$3,237,920	NT$602,000
2026/06/12	1,546	NT$5,697,800	NT$57,800	NT$5,640,000	NT$663,304
合計	16,384	NT$33,620,000	NT$386,630	NT$33,233,370	NT$6,845,304

營收與利潤

日期	商品交易總額 GMV	退款金額	扣除退款後營收	廣告花費	其他成本合計	淨利	淨利率
2026/06/05	NT$3,826,500	NT$42,800	NT$3,783,700	NT$786,400	NT$2,579,300	NT$418,000	11.05%
2026/06/06	NT$4,313,200	NT$50,150	NT$4,263,050	NT$642,300	NT$2,386,750	NT$1,234,000	28.95%
2026/06/07	NT$3,037,600	NT$39,600	NT$2,998,000	NT$934,800	NT$1,760,200	NT$303,000	10.11%
2026/06/08	NT$4,938,100	NT$52,600	NT$4,885,500	NT$715,600	NT$2,673,900	NT$1,496,000	30.62%
2026/06/09	NT$6,042,900	NT$69,100	NT$5,973,800	NT$824,900	NT$3,205,900	NT$1,943,000	32.53%
2026/06/10	NT$2,484,800	NT$33,400	NT$2,451,400	NT$703,500	NT$1,561,900	NT$186,000	7.59%
2026/06/11	NT$3,279,100	NT$41,180	NT$3,237,920	NT$612,800	NT$2,023,120	NT$602,000	18.59%
2026/06/12	NT$5,697,800	NT$57,800	NT$5,640,000	NT$559,700	NT$4,416,996	NT$663,304	11.76%
8天合計	NT$33,620,000	NT$386,630	NT$33,233,370	NT$5,780,000	NT$20,608,066	NT$6,845,304	20.60%"""

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
    font-size:28px;
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
.section-title{
    font-size:28px;
    font-weight:900;
    color:#0f172a;
    margin-top:28px;
    margin-bottom:12px;
}
.summary-box{
    border:1px solid #e5e7eb;
    border-radius:12px;
    padding:18px 20px;
    background:#ffffff;
    line-height:1.8;
    font-size:17px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 解析工具
# =========================================================
SECTION_TITLES = [
    "核心成效總覽",
    "報表圖表用資料",
    "每日點擊趨勢",
    "每日訂單趨勢",
    "每日銷售額趨勢",
    "平台銷售額排名",
    "每日完整投放數據",
    "廣告平台成效",
    "國家市場成效",
    "商品銷售成效",
    "廣告素材成效",
    "裝置來源成效",
    "受眾年齡成效",
    "受眾性別成效",
    "顧客轉換路徑",
    "訂單與退款資料",
    "營收與利潤",
]

def section_text(title):
    start = RAW_DATA.index(title) + len(title)
    next_positions = []
    for t in SECTION_TITLES:
        if t == title:
            continue
        pos = RAW_DATA.find(t, start)
        if pos != -1:
            next_positions.append(pos)
    end = min(next_positions) if next_positions else len(RAW_DATA)
    return RAW_DATA[start:end].strip()

def read_table(title):
    txt = section_text(title)
    lines = [line.strip() for line in txt.splitlines() if line.strip()]
    if not lines:
        return pd.DataFrame()
    return pd.read_csv(StringIO("\n".join(lines)), sep="\t", dtype=str).fillna("")

def to_int(v):
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).replace("NT$", "").replace(",", "").replace("%", "").replace("x", "").strip()
    if s in ["", "-", "nan", "None"]:
        return ""
    try:
        return int(round(float(s)))
    except Exception:
        return ""

def to_float(v):
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace("NT$", "").replace(",", "").replace("%", "").replace("x", "").strip()
    if s in ["", "-", "nan", "None"]:
        return ""
    try:
        return float(s)
    except Exception:
        return ""

def clean_numeric_df(df):
    out = df.copy()
    int_cols = ["曝光量 IMP", "點擊量", "成交訂單數", "商品交易總額 GMV", "廣告花費", "淨利", "扣除退款後營收", "退款金額", "其他成本合計", "數量"]
    float_cols = ["點擊率 CTR", "平均點擊成本 CPC", "成交轉換率 CVR", "廣告投資報酬率 ROAS", "單筆成交成本 CPA", "銷售占比", "淨利率", "平均客單價 AOV"]
    for col in out.columns:
        if col in int_cols:
            out[col] = out[col].apply(to_int)
        elif col in float_cols:
            out[col] = out[col].apply(to_float)
        elif col == "排名":
            out[col] = out[col].apply(lambda x: to_int(x) if str(x).strip() not in ["合計", ""] else x)
    return out

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

def wan_label(v):
    return f"{v / 10000:,.1f} 萬"

# =========================================================
# 資料建立
# =========================================================
core_raw = read_table("核心成效總覽")
core_map = dict(zip(core_raw["項目"], core_raw["數值"]))
REPORT_TITLE = "跨境電商廣告投放報表"
PERIOD = core_map.get("期間", "")
CURRENCY = core_map.get("幣別", "")

core = {
    "曝光量 IMP": to_int(core_map["曝光量 IMP"]),
    "點擊量": to_int(core_map["點擊量"]),
    "點擊率 CTR": to_float(core_map["點擊率 CTR"]),
    "廣告花費": to_int(core_map["廣告花費"]),
    "平均點擊成本 CPC": to_float(core_map["平均點擊成本 CPC"]),
    "成交訂單數": to_int(core_map["成交訂單數"]),
    "成交轉換率 CVR": to_float(core_map["成交轉換率 CVR"]),
    "商品交易總額 GMV": to_int(core_map["商品交易總額 GMV"]),
    "廣告投資報酬率 ROAS": to_float(core_map["廣告投資報酬率 ROAS"]),
    "單筆成交成本 CPA": to_float(core_map["單筆成交成本 CPA"]),
    "淨利": to_int(core_map["淨利"]),
    "扣除退款後營收": to_int(core_map["扣除退款後營收"]),
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

chart_table = read_table("報表圖表用資料")

daily_full_display = clean_numeric_df(read_table("每日完整投放數據"))
daily_full = daily_full_display[daily_full_display["日期"] != "合計"].copy()

daily = daily_full[[
    "日期", "曝光量 IMP", "點擊量", "成交訂單數",
    "商品交易總額 GMV", "廣告花費", "淨利", "扣除退款後營收"
]].copy()

click_display = clean_numeric_df(read_table("每日點擊趨勢"))
click_trend = click_display[click_display["日期"] != "合計"].copy()

order_display = clean_numeric_df(read_table("每日訂單趨勢"))
order_trend = order_display[order_display["日期"] != "合計"].copy()

sales_display = clean_numeric_df(read_table("每日銷售額趨勢"))
sales_trend = sales_display[sales_display["日期"] != "合計"].copy()

platform_rank_display = clean_numeric_df(read_table("平台銷售額排名"))
platform_rank = platform_rank_display[platform_rank_display["排名"] != "合計"].copy()
platform_rank["報表顯示"] = platform_rank["商品交易總額 GMV"].apply(wan_label)
platform_rank_display["報表顯示"] = platform_rank_display["商品交易總額 GMV"].apply(lambda x: wan_label(x) if isinstance(x, (int, float)) else "")

ad_platform_display = clean_numeric_df(read_table("廣告平台成效"))
ad_platform = ad_platform_display[ad_platform_display["廣告平台"] != "合計"].copy()

country_display = clean_numeric_df(read_table("國家市場成效"))
country = country_display[country_display["國家市場"] != "合計"].copy()

product_display = clean_numeric_df(read_table("商品銷售成效"))
product = product_display[product_display["商品名稱"] != "合計"].copy()

creative_display = clean_numeric_df(read_table("廣告素材成效"))
creative = creative_display[creative_display["廣告素材"] != "合計"].copy()

device_display = clean_numeric_df(read_table("裝置來源成效"))
device = device_display[device_display["裝置來源"] != "合計"].copy()

age_display = clean_numeric_df(read_table("受眾年齡成效"))
age = age_display[age_display["年齡層"] != "合計"].copy()

gender_display = clean_numeric_df(read_table("受眾性別成效"))
gender = gender_display[gender_display["性別"] != "合計"].copy()

funnel_raw = read_table("顧客轉換路徑")
funnel = funnel_raw.copy()
funnel["顯示數值"] = funnel["數量"]
funnel["數量"] = funnel["數量"].apply(to_int)

refund = clean_numeric_df(read_table("訂單與退款資料"))
profit = clean_numeric_df(read_table("營收與利潤"))

total_profit_rate = to_float(profit.iloc[-1]["淨利率"])

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
            out[col] = out[col].apply(lambda x: f"NT${x:,.2f}" if col == "平均客單價 AOV" and isinstance(x, (int, float)) else (f"NT${x:,.0f}" if isinstance(x, (int, float)) else x))
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
            st.markdown(
    f"""
    <div class="metric-value">
        {value}
    </div>
    """,
    unsafe_allow_html=True
)
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
    dfx = df.copy()
    dfx[value_col] = pd.to_numeric(dfx[value_col], errors="coerce").fillna(0)
    max_value = dfx[value_col].max()
    if max_value == 0:
        max_value = 1
    text_values = dfx[text_col] if text_col and text_col in dfx.columns else dfx[value_col].apply(lambda x: f"{x:,.0f}")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dfx[value_col],
        y=dfx[label_col],
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

st.subheader("核心成效總覽")
g1, g2, g3 = st.columns([1, 1, 2])

with g1:
    gauge_chart(
        "ROAS 廣告投報",
        core["廣告投資報酬率 ROAS"],
        10,
        "#22c55e",
        "x"
    )

with g2:
    gauge_chart(
        "淨利率",
        total_profit_rate,
        100,
        "#3b82f6",
        "%"
    )
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

st.subheader("報表圖表用資料")
c1, c2 = st.columns(2)

with c1:
    line_chart("每日曝光趨勢", daily["日期"], daily["曝光量 IMP"], "曝光量 IMP", "#2563eb")
    line_chart("每日點擊趨勢", daily["日期"], daily["點擊量"], "點擊量", "#f97316")

with c2:
    line_chart("每日訂單趨勢", daily["日期"], daily["成交訂單數"], "成交訂單數", "#22c55e")
    line_chart("每日銷售額趨勢", daily["日期"], daily["商品交易總額 GMV"], "商品交易總額 GMV", "#a855f7")

st.dataframe(chart_table, use_container_width=True, hide_index=True)

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

    total_profit = profit.iloc[-1]
    profit_chart = pd.DataFrame({
        "項目": ["扣除退款後營收", "廣告花費", "其他成本合計", "淨利"],
        "金額": [
            to_int(total_profit["扣除退款後營收"]),
            to_int(total_profit["廣告花費"]),
            to_int(total_profit["其他成本合計"]),
            to_int(total_profit["淨利"]),
        ],
    })
    profit_chart["顯示"] = profit_chart["金額"].apply(wan_label)
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
