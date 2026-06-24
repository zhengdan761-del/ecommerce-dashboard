
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO
import re

# =========================================================
# 原始報表資料
# =========================================================
RAW_DATA = """核心成效總覽

項目	數值
期間	2026/06/18－2026/06/24
幣別	NTD 新台幣
曝光量 IMP	48,816,372
點擊量	1,382,947
點擊率 CTR	2.83%
廣告花費	NT$15,843,857
平均點擊成本 CPC	NT$11.46
成交訂單數	54,186
成交轉換率 CVR	3.92%
商品交易總額 GMV	NT$128,946,582
廣告投資報酬率 ROAS	8.14x
單筆成交成本 CPA	NT$292.40
淨利	NT$32,584,540
扣除退款後營收	NT$127,357,684

報表圖表用資料

圖表資料	2026/06/18	2026/06/19	2026/06/20	2026/06/21	2026/06/22	2026/06/23	2026/06/24	合計
曝光量 IMP	6,203,152	6,818,476	6,527,459	5,864,821	8,013,078	6,636,558	8,752,828	48,816,372
點擊量	174,628	199,382	184,917	160,438	236,982	182,641	243,959	1,382,947
成交訂單數	6,574	7,896	7,150	6,041	9,692	6,985	9,848	54,186
商品交易總額 GMV	NT$15,426,831	NT$19,073,854	NT$17,268,420	NT$13,985,936	NT$24,597,612	NT$16,245,879	NT$22,348,050	NT$128,946,582
廣告花費	NT$2,163,810	NT$2,364,958	NT$2,219,724	NT$1,873,036	NT$2,793,195	NT$2,035,316	NT$2,393,818	NT$15,843,857
淨利	NT$3,625,904	NT$4,932,807	NT$4,284,705	NT$3,201,846	NT$7,418,352	NT$3,867,608	NT$5,253,318	NT$32,584,540
扣除退款後營收	NT$15,242,516	NT$18,838,446	NT$17,059,748	NT$13,814,717	NT$24,290,130	NT$16,049,732	NT$22,062,395	NT$127,357,684

每日點擊趨勢

日期	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC
2026/06/18	6,203,152	174,628	2.82%	NT$2,163,810	NT$12.39
2026/06/19	6,818,476	199,382	2.92%	NT$2,364,958	NT$11.86
2026/06/20	6,527,459	184,917	2.83%	NT$2,219,724	NT$12.00
2026/06/21	5,864,821	160,438	2.74%	NT$1,873,036	NT$11.68
2026/06/22	8,013,078	236,982	2.96%	NT$2,793,195	NT$11.79
2026/06/23	6,636,558	182,641	2.75%	NT$2,035,316	NT$11.14
2026/06/24	8,752,828	243,959	2.79%	NT$2,393,818	NT$9.81
合計	48,816,372	1,382,947	2.83%	NT$15,843,857	NT$11.46

每日訂單趨勢

日期	點擊量	成交訂單數	成交轉換率 CVR	廣告花費	單筆成交成本 CPA
2026/06/18	174,628	6,574	3.77%	NT$2,163,810	NT$329.17
2026/06/19	199,382	7,896	3.96%	NT$2,364,958	NT$299.52
2026/06/20	184,917	7,150	3.87%	NT$2,219,724	NT$310.45
2026/06/21	160,438	6,041	3.77%	NT$1,873,036	NT$310.05
2026/06/22	236,982	9,692	4.09%	NT$2,793,195	NT$288.20
2026/06/23	182,641	6,985	3.82%	NT$2,035,316	NT$291.38
2026/06/24	243,959	9,848	4.04%	NT$2,393,818	NT$243.08
合計	1,382,947	54,186	3.92%	NT$15,843,857	NT$292.40

每日銷售額趨勢

日期	成交訂單數	商品交易總額 GMV	廣告花費	ROAS	淨利	扣除退款後營收	淨利率
2026/06/18	6,574	NT$15,426,831	NT$2,163,810	7.13x	NT$3,625,904	NT$15,242,516	23.79%
2026/06/19	7,896	NT$19,073,854	NT$2,364,958	8.06x	NT$4,932,807	NT$18,838,446	26.18%
2026/06/20	7,150	NT$17,268,420	NT$2,219,724	7.78x	NT$4,284,705	NT$17,059,748	25.12%
2026/06/21	6,041	NT$13,985,936	NT$1,873,036	7.47x	NT$3,201,846	NT$13,814,717	23.18%
2026/06/22	9,692	NT$24,597,612	NT$2,793,195	8.81x	NT$7,418,352	NT$24,290,130	30.54%
2026/06/23	6,985	NT$16,245,879	NT$2,035,316	7.98x	NT$3,867,608	NT$16,049,732	24.10%
2026/06/24	9,848	NT$22,348,050	NT$2,393,818	9.34x	NT$5,253,318	NT$22,062,395	23.81%
合計	54,186	NT$128,946,582	NT$15,843,857	8.14x	NT$32,584,540	NT$127,357,684	25.59%

平台銷售額排名

排名	銷售平台／通路	成交訂單數	商品交易總額 GMV	銷售占比
1	自有品牌站／Shopify Plus	23,625	NT$56,221,510	43.60%
2	TikTok Shop	13,384	NT$31,849,205	24.70%
3	Amazon Marketplace	7,857	NT$18,697,254	14.50%
4	eBay	4,010	NT$9,542,047	7.40%
5	Shopee Cross-border	3,034	NT$7,221,008	5.60%
6	Walmart Marketplace	2,276	NT$5,415,558	4.20%
合計	54,186	NT$128,946,582	100.00%

每日完整投放數據

日期	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Profit	Net Revenue	淨利率
2026/06/18	6,203,152	174,628	2.82%	NT$2,163,810	NT$12.39	6,574	3.77%	NT$15,426,831	7.13x	NT$329.17	NT$3,625,904	NT$15,242,516	23.79%
2026/06/19	6,818,476	199,382	2.92%	NT$2,364,958	NT$11.86	7,896	3.96%	NT$19,073,854	8.06x	NT$299.52	NT$4,932,807	NT$18,838,446	26.18%
2026/06/20	6,527,459	184,917	2.83%	NT$2,219,724	NT$12.00	7,150	3.87%	NT$17,268,420	7.78x	NT$310.45	NT$4,284,705	NT$17,059,748	25.12%
2026/06/21	5,864,821	160,438	2.74%	NT$1,873,036	NT$11.68	6,041	3.77%	NT$13,985,936	7.47x	NT$310.05	NT$3,201,846	NT$13,814,717	23.18%
2026/06/22	8,013,078	236,982	2.96%	NT$2,793,195	NT$11.79	9,692	4.09%	NT$24,597,612	8.81x	NT$288.20	NT$7,418,352	NT$24,290,130	30.54%
2026/06/23	6,636,558	182,641	2.75%	NT$2,035,316	NT$11.14	6,985	3.82%	NT$16,245,879	7.98x	NT$291.38	NT$3,867,608	NT$16,049,732	24.10%
2026/06/24	8,752,828	243,959	2.79%	NT$2,393,818	NT$9.81	9,848	4.04%	NT$22,348,050	9.34x	NT$243.08	NT$5,253,318	NT$22,062,395	23.81%
合計	48,816,372	1,382,947	2.83%	NT$15,843,857	NT$11.46	54,186	3.92%	NT$128,946,582	8.14x	NT$292.40	NT$32,584,540	NT$127,357,684	25.59%

廣告平台成效

廣告平台	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
TikTok Ads	19,038,385	567,008	2.98%	NT$6,020,666	NT$10.62	18,423	3.25%	NT$45,131,304	7.50x	NT$326.80	NT$44,575,190	NT$5,213,526	11.69%
Meta Ads	12,692,257	387,225	3.05%	NT$4,436,280	NT$11.46	16,256	4.20%	NT$39,973,440	9.01x	NT$272.90	NT$39,480,882	NT$11,078,744	28.06%
Google Ads	8,786,947	235,101	2.68%	NT$3,168,771	NT$13.48	10,837	4.61%	NT$24,499,851	7.73x	NT$292.40	NT$24,197,960	NT$7,168,599	29.62%
Pinterest Ads	4,881,637	124,465	2.55%	NT$950,632	NT$7.64	5,419	4.35%	NT$12,894,658	13.56x	NT$175.43	NT$12,735,768	NT$5,865,217	46.05%
Snapchat Ads	3,417,146	69,148	2.02%	NT$1,267,508	NT$18.33	3,251	4.70%	NT$6,447,329	5.09x	NT$389.88	NT$6,367,884	NT$3,258,454	51.18%
合計	48,816,372	1,382,947	2.83%	NT$15,843,857	NT$11.46	54,186	3.92%	NT$128,946,582	8.14x	NT$292.40	NT$127,357,684	NT$32,584,540	25.59%

國家市場成效

國家市場	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
United States 美國	20,502,876	567,008	2.77%	NT$6,812,858	NT$12.02	20,591	3.63%	NT$52,223,366	7.67x	NT$330.87	NT$51,579,862	NT$9,123,671	17.69%
United Kingdom 英國	8,298,783	248,931	3.00%	NT$2,535,017	NT$10.18	9,212	3.70%	NT$22,565,652	8.90x	NT$275.19	NT$22,287,595	NT$6,191,063	27.78%
Canada 加拿大	6,834,292	193,613	2.83%	NT$2,297,359	NT$11.87	8,128	4.20%	NT$18,697,254	8.14x	NT$282.65	NT$18,466,864	NT$5,213,526	28.23%
Australia 澳洲	5,369,801	152,124	2.83%	NT$1,663,605	NT$10.94	5,960	3.92%	NT$13,539,391	8.14x	NT$279.13	NT$13,372,557	NT$3,910,145	29.24%
Japan 日本	3,905,310	110,636	2.83%	NT$1,188,289	NT$10.74	4,335	3.92%	NT$10,315,727	8.68x	NT$274.12	NT$10,188,615	NT$3,258,454	31.98%
Singapore 新加坡	2,440,819	69,147	2.83%	NT$871,412	NT$12.60	3,793	5.49%	NT$7,092,062	8.14x	NT$229.74	NT$7,004,672	NT$3,258,454	46.52%
Malaysia 馬來西亞	1,464,491	41,488	2.83%	NT$475,316	NT$11.46	2,167	5.22%	NT$4,513,130	9.50x	NT$219.34	NT$4,457,519	NT$1,629,227	36.55%
合計	48,816,372	1,382,947	2.83%	NT$15,843,857	NT$11.46	54,186	3.92%	NT$128,946,582	8.14x	NT$292.40	NT$127,357,684	NT$32,584,540	25.59%

商品銷售成效
商品名稱	商品類型	參考單價帶	AOV	單件成本	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	商品成本	Net Profit	Net Revenue	淨利率
智能香氛小夜燈	居家氛圍／生活小家電	NT$970－NT$1,870	NT$1,892.48	NT$763.03	1,193,940	22,023	1.84%	NT$177,229	NT$8.05	865	3.93%	NT$1,636,997	9.24x	NT$204.89	NT$660,022	NT$264,938	NT$1,616,826	16.39%
桌面空氣循環扇	辦公室／居家小家電	NT$1,040－NT$2,020	NT$2,648.83	NT$953.58	611,007	13,588	2.22%	NT$128,602	NT$9.46	284	2.09%	NT$752,268	5.85x	NT$452.82	NT$270,816	NT$269,605	NT$742,998	36.29%
智能空氣淨化器	居家健康／空氣清潔設備	NT$3,740－NT$7,240	NT$8,237.26	NT$3,448.76	658,884	25,432	3.86%	NT$776,061	NT$30.52	1,321	5.19%	NT$10,881,419	14.02x	NT$587.48	NT$4,555,818	NT$2,649,503	NT$10,747,337	24.65%
智能廚房秤	廚房用品／智能小工具	NT$520－NT$1,000	NT$1,227.97	NT$412.66	934,646	25,507	2.73%	NT$275,662	NT$10.81	669	2.62%	NT$821,509	2.98x	NT$412.05	NT$276,069	NT$86,397	NT$811,386	10.65%
便攜式保溫杯	生活用品／外出隨行	NT$590－NT$1,150	NT$1,567.52	NT$614.91	959,281	25,806	2.69%	NT$243,340	NT$9.43	804	3.12%	NT$1,260,285	5.18x	NT$302.66	NT$494,389	NT$145,760	NT$1,244,756	11.71%
多功能收納包	旅行／居家收納用品	NT$670－NT$1,290	NT$2,398.49	NT$859.12	1,392,005	51,122	3.67%	NT$298,504	NT$5.84	2,738	5.36%	NT$6,567,068	22.00x	NT$109.02	NT$2,352,266	NT$2,662,474	NT$6,486,148	41.05%
旅行壓縮袋組	旅行用品／行李收納	NT$820－NT$1,580	NT$2,808.44	NT$841.27	1,666,834	42,775	2.57%	NT$343,211	NT$8.02	2,512	5.87%	NT$7,054,789	20.56x	NT$136.63	NT$2,113,275	NT$3,623,286	NT$6,967,859	52.00%
磁吸式無線充電座	3C配件／桌面充電	NT$970－NT$1,870	NT$3,635.84	NT$1,562.54	1,249,329	25,211	2.02%	NT$383,507	NT$15.21	1,195	4.74%	NT$4,344,829	11.33x	NT$320.93	NT$1,867,241	NT$1,499,090	NT$4,291,291	34.93%
藍牙降噪耳機	3C配件／影音設備	NT$1,870－NT$3,610	NT$7,169.57	NT$3,076.91	1,010,324	32,762	3.24%	NT$881,796	NT$26.92	1,430	4.36%	NT$10,252,490	11.63x	NT$616.64	NT$4,399,987	NT$934,714	NT$10,126,157	9.23%
手機防水收納袋	戶外用品／手機配件	NT$290－NT$570	NT$1,015.37	NT$276.27	599,132	18,649	3.11%	NT$346,085	NT$18.56	1,001	5.37%	NT$1,016,388	2.94x	NT$345.74	NT$276,546	NT$243,231	NT$1,003,864	24.23%
摺疊式手機支架	3C配件／桌面用品	NT$340－NT$650	NT$1,192.14	NT$368.34	938,377	20,554	2.19%	NT$405,226	NT$19.72	1,239	6.03%	NT$1,477,061	3.65x	NT$327.06	NT$456,368	NT$251,189	NT$1,458,860	17.22%
LED補光化妝鏡	美妝工具／居家小物	NT$890－NT$1,730	NT$2,615.66	NT$1,071.53	420,592	11,448	2.72%	NT$133,615	NT$11.67	376	3.28%	NT$983,487	7.36x	NT$355.36	NT$402,895	NT$134,499	NT$971,368	13.85%
電動筋膜按摩器	健康放鬆／按摩設備	NT$2,240－NT$4,340	NT$5,264.08	NT$2,162.35	153,905	5,908	3.84%	NT$173,609	NT$29.39	338	5.72%	NT$1,779,258	10.25x	NT$513.64	NT$730,874	NT$410,137	NT$1,757,334	23.34%
頸掛式小風扇	夏季用品／個人小家電	NT$740－NT$1,440	NT$2,591.47	NT$829.92	1,546,138	58,362	3.77%	NT$439,290	NT$7.53	1,238	2.12%	NT$3,208,240	7.30x	NT$354.84	NT$1,027,443	NT$738,191	NT$3,168,708	23.30%
USB加熱暖手寶	冬季用品／生活小家電	NT$520－NT$1,000	NT$1,805.79	NT$574.77	864,613	22,166	2.56%	NT$245,075	NT$11.06	1,107	4.99%	NT$1,999,007	8.16x	NT$221.39	NT$636,270	NT$692,270	NT$1,974,375	35.06%
智能感應垃圾桶	居家用品／智能生活	NT$1,420－NT$2,740	NT$4,525.38	NT$1,684.55	286,964	11,852	4.13%	NT$179,576	NT$15.15	873	7.37%	NT$3,950,657	22.00x	NT$205.70	NT$1,470,611	NT$1,055,543	NT$3,901,976	27.05%
防滑浴室地墊	居家用品／浴室收納	NT$440－NT$860	NT$1,106.21	NT$344.52	1,328,273	41,493	3.12%	NT$478,493	NT$11.53	1,166	2.81%	NT$1,289,846	2.70x	NT$410.37	NT$401,711	NT$250,757	NT$1,273,952	19.68%
廚房瀝水置物架	廚房用品／收納整理	NT$890－NT$1,730	NT$2,516.93	NT$803.77	753,174	29,601	3.93%	NT$160,969	NT$5.44	1,407	4.75%	NT$3,541,317	22.00x	NT$114.41	NT$1,130,903	NT$942,503	NT$3,497,680	26.95%
矽膠保鮮袋組	廚房用品／環保收納	NT$370－NT$710	NT$988.01	NT$265.59	784,438	32,475	4.14%	NT$253,171	NT$7.80	1,370	4.22%	NT$1,353,572	5.35x	NT$184.80	NT$363,861	NT$218,735	NT$1,336,893	16.36%
不鏽鋼保鮮盒	廚房用品／食物收納	NT$670－NT$1,290	NT$2,391.32	NT$851.34	2,956,717	121,946	4.12%	NT$881,393	NT$7.23	3,419	2.80%	NT$8,175,925	9.28x	NT$257.79	NT$2,910,729	NT$1,315,109	NT$8,075,180	16.29%
可折疊購物袋	生活用品／外出收納	NT$290－NT$570	NT$1,043.22	NT$285.10	1,063,244	20,256	1.91%	NT$132,920	NT$6.56	1,144	5.65%	NT$1,193,445	8.98x	NT$116.19	NT$326,159	NT$517,995	NT$1,178,739	43.94%
旅行盥洗收納包	旅行用品／盥洗收納	NT$590－NT$1,150	NT$1,945.09	NT$543.26	420,079	15,725	3.74%	NT$85,301	NT$5.42	848	5.39%	NT$1,649,435	19.34x	NT$100.59	NT$460,683	NT$788,025	NT$1,629,110	48.37%
護照證件收納包	旅行用品／證件收納	NT$520－NT$1,000	NT$1,297.12	NT$360.10	768,117	21,033	2.74%	NT$220,697	NT$10.49	699	3.32%	NT$906,690	4.11x	NT$315.73	NT$251,713	NT$154,090	NT$895,518	17.21%
行李箱電子秤	旅行用品／行李配件	NT$440－NT$860	NT$1,246.15	NT$381.19	1,292,783	28,992	2.24%	NT$356,631	NT$12.30	1,333	4.60%	NT$1,661,119	4.66x	NT$267.54	NT$508,123	NT$447,753	NT$1,640,651	27.29%
車用手機支架	汽車用品／車內配件	NT$590－NT$1,150	NT$2,033.64	NT$694.97	877,437	20,128	2.29%	NT$170,394	NT$8.47	640	3.18%	NT$1,301,530	7.64x	NT$266.24	NT$444,778	NT$169,219	NT$1,285,492	13.16%
車用香氛擴香器	汽車用品／車內香氛	NT$740－NT$1,440	NT$2,158.92	NT$732.97	705,020	19,317	2.74%	NT$106,302	NT$5.50	634	3.28%	NT$1,368,753	12.88x	NT$167.67	NT$464,702	NT$447,349	NT$1,351,887	33.09%
車用吸塵器	汽車用品／清潔設備	NT$1,190－NT$2,310	NT$3,583.64	NT$1,611.95	423,950	13,160	3.10%	NT$394,704	NT$29.99	624	4.74%	NT$2,236,193	5.67x	NT$632.54	NT$1,005,856	NT$225,969	NT$2,208,638	10.23%
寵物飲水機	寵物用品／智能設備	NT$1,490－NT$2,890	NT$5,880.52	NT$2,484.49	683,987	27,770	4.06%	NT$941,333	NT$33.90	947	3.41%	NT$5,568,857	5.92x	NT$994.02	NT$2,352,808	NT$1,295,636	NT$5,500,237	23.56%
寵物除毛刷	寵物用品／清潔護理	NT$520－NT$1,000	NT$1,869.89	NT$594.82	2,050,758	40,156	1.96%	NT$253,498	NT$6.31	849	2.11%	NT$1,587,538	6.26x	NT$298.58	NT$505,000	NT$347,411	NT$1,567,976	22.16%
寵物外出水壺	寵物用品／外出用品	NT$490－NT$940	NT$1,469.80	NT$460.22	217,804	4,428	2.03%	NT$78,105	NT$17.64	302	6.82%	NT$443,880	5.68x	NT$258.63	NT$138,987	NT$52,553	NT$438,411	11.99%
瑜珈彈力帶組	運動用品／健身配件	NT$440－NT$860	NT$1,028.78	NT$309.88	622,222	13,437	2.16%	NT$106,950	NT$7.96	682	5.08%	NT$701,630	6.56x	NT$156.82	NT$211,337	NT$279,520	NT$692,984	40.34%
防滑瑜珈墊	運動用品／居家健身	NT$1,270－NT$2,450	NT$3,768.80	NT$1,375.95	1,567,151	35,154	2.24%	NT$255,937	NT$7.28	1,494	4.25%	NT$5,630,593	22.00x	NT$171.31	NT$2,055,670	NT$1,407,130	NT$5,561,212	25.30%
運動水壺	運動用品／外出補水	NT$520－NT$1,000	NT$1,796.00	NT$663.39	512,991	19,569	3.81%	NT$205,185	NT$10.49	950	4.85%	NT$1,706,198	8.32x	NT$215.98	NT$630,223	NT$358,688	NT$1,685,174	21.28%
快乾運動毛巾	運動用品／戶外用品	NT$370－NT$710	NT$1,012.54	NT$326.76	983,176	31,809	3.24%	NT$552,060	NT$17.36	1,262	3.97%	NT$1,277,822	2.31x	NT$437.45	NT$412,369	NT$163,268	NT$1,262,077	12.94%
露營LED掛燈	戶外用品／露營照明	NT$740－NT$1,440	NT$2,921.26	NT$1,231.06	1,659,546	44,192	2.66%	NT$273,196	NT$6.18	1,116	2.53%	NT$3,260,122	11.93x	NT$244.80	NT$1,373,861	NT$530,450	NT$3,219,950	16.47%
戶外折疊椅	戶外用品／露營家具	NT$1,790－NT$3,470	NT$7,595.83	NT$3,141.64	634,395	20,641	3.25%	NT$584,892	NT$28.34	503	2.44%	NT$3,820,703	6.53x	NT$1,162.81	NT$1,580,246	NT$1,160,764	NT$3,773,624	30.76%
便攜餐具組	戶外用品／旅行餐具	NT$370－NT$710	NT$995.49	NT$297.65	486,950	15,673	3.22%	NT$98,480	NT$6.28	724	4.62%	NT$720,736	7.32x	NT$136.02	NT$215,495	NT$249,675	NT$711,855	35.07%
防水收納乾濕袋	旅行用品／戶外收納	NT$440－NT$860	NT$1,460.87	NT$382.00	250,197	9,260	3.70%	NT$134,017	NT$14.47	454	4.90%	NT$663,236	4.95x	NT$295.19	NT$173,426	NT$214,459	NT$655,064	32.74%
兒童防漏水杯	親子用品／兒童餐具	NT$520－NT$1,000	NT$1,760.11	NT$720.25	1,213,632	22,378	1.84%	NT$164,556	NT$7.35	1,149	5.13%	NT$2,022,369	12.29x	NT$143.22	NT$827,564	NT$454,216	NT$1,997,449	22.74%
兒童矽膠圍兜	親子用品／用餐用品	NT$370－NT$710	NT$1,255.62	NT$353.40	506,169	15,642	3.09%	NT$277,587	NT$17.75	568	3.63%	NT$713,191	2.57x	NT$488.71	NT$200,733	NT$127,781	NT$704,403	18.14%
嬰兒推車收納袋	親子用品／外出收納	NT$670－NT$1,290	NT$2,427.69	NT$871.07	460,537	16,236	3.53%	NT$271,349	NT$16.71	415	2.56%	NT$1,007,490	3.71x	NT$653.85	NT$361,493	NT$155,029	NT$995,076	15.58%
居家防撞條組	親子用品／安全防護	NT$370－NT$710	NT$851.60	NT$235.79	500,940	14,413	2.88%	NT$77,405	NT$5.37	509	3.53%	NT$433,463	5.60x	NT$152.07	NT$120,016	NT$140,850	NT$428,122	32.90%
收納抽屜分隔板	居家收納／衣櫃整理	NT$520－NT$1,000	NT$1,328.30	NT$413.63	1,057,949	38,064	3.60%	NT$431,362	NT$11.33	1,244	3.27%	NT$1,652,411	3.83x	NT$346.75	NT$514,561	NT$205,092	NT$1,632,050	12.57%
真空壓縮收納袋	居家收納／換季整理	NT$590－NT$1,150	NT$1,432.69	NT$488.33	4,928,558	89,936	1.82%	NT$1,117,799	NT$12.43	3,140	3.49%	NT$4,498,653	4.02x	NT$355.99	NT$1,533,355	NT$829,395	NT$4,443,220	18.67%
衣物除毛球機	居家用品／衣物護理	NT$670－NT$1,290	NT$2,185.01	NT$701.34	535,025	10,414	1.95%	NT$53,831	NT$5.17	542	5.20%	NT$1,184,277	22.00x	NT$99.32	NT$380,126	NT$561,631	NT$1,169,684	48.02%
迷你熨燙機	居家用品／衣物整理	NT$1,190－NT$2,310	NT$3,412.21	NT$1,557.38	357,149	12,492	3.50%	NT$105,314	NT$8.43	679	5.44%	NT$2,316,888	22.00x	NT$155.10	NT$1,057,461	NT$616,500	NT$2,288,339	26.94%
防藍光眼鏡	健康用品／護眼配件	NT$590－NT$1,150	NT$1,441.91	NT$445.66	795,264	22,489	2.83%	NT$293,941	NT$13.07	551	2.45%	NT$794,494	2.70x	NT$533.47	NT$245,558	NT$135,910	NT$784,704	17.32%
睡眠遮光眼罩	生活用品／睡眠配件	NT$440－NT$860	NT$1,360.79	NT$368.29	1,417,858	53,296	3.76%	NT$528,498	NT$9.92	1,715	3.22%	NT$2,333,762	4.42x	NT$308.16	NT$631,617	NT$402,492	NT$2,305,005	17.46%
人體工學滑鼠墊	辦公用品／桌面配件	NT$520－NT$1,000	NT$1,318.77	NT$350.86	861,900	32,140	3.73%	NT$289,274	NT$9.00	1,991	6.19%	NT$2,625,673	9.08x	NT$145.29	NT$698,554	NT$1,138,038	NT$2,593,319	43.88%
桌面理線收納盒	辦公用品／桌面收納	NT$370－NT$710	NT$1,171.42	NT$305.47	653,011	16,067	2.46%	NT$77,925	NT$4.85	1,126	7.01%	NT$1,319,019	16.93x	NT$69.21	NT$343,963	NT$619,721	NT$1,302,766	47.57%
合計	NT$864.14	48,816,372	1,382,947	2.83%	NT$15,843,857	NT$11.46	54,186	3.92%	NT$128,946,582	8.14x	NT$292.40	NT$46,824,531	NT$32,584,540	NT$127,357,684	25.59%

廣告素材成效

廣告素材	素材類型	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
短影音A｜高單價家電開箱	15秒短影音	11,960,011	276,589	2.31%	NT$3,802,526	NT$13.75	10,295	3.72%	NT$27,078,782	7.12x	NT$369.36	NT$26,745,114	NT$4,561,836	17.06%
短影音B｜旅行收納前後對比	20秒短影音	10,007,356	324,993	3.25%	NT$2,376,579	NT$7.31	13,547	4.17%	NT$31,591,913	13.29x	NT$175.43	NT$31,202,633	NT$9,449,517	30.28%
短影音C｜辦公桌面改造	18秒短影音	7,566,538	207,442	2.74%	NT$2,218,140	NT$10.69	8,670	4.18%	NT$20,631,453	9.30x	NT$255.84	NT$20,377,229	NT$5,213,526	25.59%
短影音D｜寵物日常實測	25秒短影音	6,590,210	179,783	2.73%	NT$3,168,771	NT$17.63	7,044	3.92%	NT$18,052,521	5.70x	NT$449.85	NT$17,830,076	NT$4,235,990	23.76%
輪播圖E｜低單價爆品合集	圖文輪播	8,054,702	304,248	3.78%	NT$2,218,140	NT$7.29	10,837	3.56%	NT$23,210,385	10.46x	NT$204.68	NT$22,924,383	NT$6,842,753	29.85%
再行銷F｜購物車限時優惠	再行銷素材	4,637,555	89,892	1.94%	NT$2,059,701	NT$22.91	3,793	4.22%	NT$8,381,528	4.07x	NT$543.03	NT$8,278,249	NT$2,280,918	27.55%
合計	48,816,372	1,382,947	2.83%	NT$15,843,857	NT$11.46	54,186	3.92%	NT$128,946,582	8.14x	NT$292.40	NT$127,357,684	NT$32,584,540	25.59%

裝置來源成效

裝置來源	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
Mobile App / 行動裝置	34,171,460	995,722	2.91%	NT$10,932,261	NT$10.98	37,930	3.81%	NT$90,262,607	8.26x	NT$288.22	NT$89,150,379	NT$19,550,724	21.93%
Desktop Web / 桌機網頁	8,786,947	235,101	2.68%	NT$3,010,333	NT$12.80	9,754	4.15%	NT$23,210,385	7.71x	NT$308.63	NT$22,924,383	NT$7,168,599	31.27%
Tablet / 平板	3,661,228	96,806	2.64%	NT$1,267,509	NT$13.09	4,064	4.20%	NT$9,670,994	7.63x	NT$311.89	NT$9,551,826	NT$3,258,454	34.11%
In-App Webview / 內嵌瀏覽器	2,196,737	55,318	2.52%	NT$633,754	NT$11.46	2,438	4.41%	NT$5,802,596	9.16x	NT$259.95	NT$5,731,096	NT$2,606,763	45.48%
合計	48,816,372	1,382,947	2.83%	NT$15,843,857	NT$11.46	54,186	3.92%	NT$128,946,582	8.14x	NT$292.40	NT$127,357,684	NT$32,584,540	25.59%

受眾年齡成效

年齡層	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
18-24	9,275,111	248,930	2.68%	NT$2,851,894	NT$11.46	9,212	3.70%	NT$21,920,919	7.69x	NT$309.58	NT$21,650,806	NT$5,213,526	24.08%
25-34	18,794,303	553,179	2.94%	NT$6,179,104	NT$11.17	21,674	3.92%	NT$51,578,633	8.35x	NT$285.09	NT$50,943,074	NT$12,707,971	24.95%
35-44	13,180,420	373,396	2.83%	NT$4,436,280	NT$11.88	15,443	4.14%	NT$36,105,043	8.14x	NT$287.27	NT$35,660,151	NT$8,797,826	24.67%
45-54	5,125,719	145,209	2.83%	NT$1,663,605	NT$11.46	5,419	3.73%	NT$13,539,391	8.14x	NT$306.99	NT$13,372,557	NT$3,910,145	29.24%
55+	2,440,819	62,233	2.55%	NT$712,974	NT$11.46	2,438	3.92%	NT$5,802,596	8.14x	NT$292.44	NT$5,731,096	NT$1,955,072	34.11%
合計	48,816,372	1,382,947	2.83%	NT$15,843,857	NT$11.46	54,186	3.92%	NT$128,946,582	8.14x	NT$292.40	NT$127,357,684	NT$32,584,540	25.59%

受眾性別成效

性別	IMP	Clicks	CTR	Ad Spend	CPC	Orders	CVR	GMV	ROAS	CPA	Net Revenue	Net Profit	淨利率
女性	30,266,151	871,257	2.88%	NT$9,506,314	NT$10.91	33,054	3.79%	NT$77,367,949	8.14x	NT$287.60	NT$76,414,610	NT$19,224,879	25.16%
男性	15,621,239	428,713	2.74%	NT$5,386,911	NT$12.57	17,881	4.17%	NT$43,841,838	8.14x	NT$301.26	NT$43,301,613	NT$11,404,589	26.34%
未揭露／其他	2,928,982	82,977	2.83%	NT$950,632	NT$11.46	3,251	3.92%	NT$7,736,795	8.14x	NT$292.41	NT$7,641,461	NT$1,955,072	25.59%
合計	48,816,372	1,382,947	2.83%	NT$15,843,857	NT$11.46	54,186	3.92%	NT$128,946,582	8.14x	NT$292.40	NT$127,357,684	NT$32,584,540	25.59%

顧客轉換路徑

轉換階段	數量	與上一階段轉換率
曝光量 IMP	48,816,372	-
點擊量	1,382,947	2.83%
成交訂單數	54,186	3.92%
商品交易總額 GMV	NT$128,946,582	-
扣除退款後營收	NT$127,357,684	98.77%
淨利	NT$32,584,540	25.59%

訂單與退款資料

日期	成交訂單數	GMV	退款金額	扣除退款後營收	淨利
2026/06/18	6,574	NT$15,426,831	NT$184,315	NT$15,242,516	NT$3,625,904
2026/06/19	7,896	NT$19,073,854	NT$235,408	NT$18,838,446	NT$4,932,807
2026/06/20	7,150	NT$17,268,420	NT$208,672	NT$17,059,748	NT$4,284,705
2026/06/21	6,041	NT$13,985,936	NT$171,219	NT$13,814,717	NT$3,201,846
2026/06/22	9,692	NT$24,597,612	NT$307,482	NT$24,290,130	NT$7,418,352
2026/06/23	6,985	NT$16,245,879	NT$196,147	NT$16,049,732	NT$3,867,608
2026/06/24	9,848	NT$22,348,050	NT$285,655	NT$22,062,395	NT$5,253,318
合計	54,186	NT$128,946,582	NT$1,588,898	NT$127,357,684	NT$32,584,540

營收與利潤

日期	GMV	退款金額	扣除退款後營收	商品成本	國際物流／履約成本	倉儲與包裝成本	平台／金流手續費	跨境關稅／稅務成本	退貨損耗	客服與營運成本	廣告花費	淨利	淨利率
2026/06/18	NT$15,426,831	NT$184,315	NT$15,242,516	NT$5,862,314	NT$793,368	NT$231,044	NT$409,202	NT$252,676	NT$214,982	NT$1,689,216	NT$2,163,810	NT$3,625,904	23.79%
2026/06/19	NT$19,073,854	NT$235,408	NT$18,838,446	NT$7,402,845	NT$904,191	NT$294,456	NT$485,065	NT$272,087	NT$225,190	NT$1,956,847	NT$2,364,958	NT$4,932,807	26.18%
2026/06/20	NT$17,268,420	NT$208,672	NT$17,059,748	NT$5,982,341	NT$1,035,338	NT$278,231	NT$481,980	NT$317,377	NT$270,453	NT$2,189,599	NT$2,219,724	NT$4,284,705	25.12%
2026/06/21	NT$13,985,936	NT$171,219	NT$13,814,717	NT$4,743,084	NT$872,959	NT$301,686	NT$431,765	NT$279,982	NT$220,106	NT$1,890,253	NT$1,873,036	NT$3,201,846	23.18%
2026/06/22	NT$24,597,612	NT$307,482	NT$24,290,130	NT$8,363,243	NT$1,457,539	NT$447,467	NT$595,371	NT$388,961	NT$375,792	NT$2,450,210	NT$2,793,195	NT$7,418,352	30.54%
2026/06/23	NT$16,245,879	NT$196,147	NT$16,049,732	NT$6,579,964	NT$840,988	NT$253,476	NT$426,073	NT$254,091	NT$200,958	NT$1,591,258	NT$2,035,316	NT$3,867,608	24.10%
2026/06/24	NT$22,348,050	NT$285,655	NT$22,062,395	NT$7,890,740	NT$1,583,700	NT$486,268	NT$638,084	NT$438,524	NT$345,896	NT$3,032,047	NT$2,393,818	NT$5,253,318	23.81%
7天合計	NT$128,946,582	NT$1,588,898	NT$127,357,684	NT$46,824,531	NT$7,488,083	NT$2,292,628	NT$3,467,540	NT$2,203,698	NT$1,853,377	NT$14,799,430	NT$15,843,857	NT$32,584,540	25.59%"""

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
    return normalize_columns(pd.read_csv(StringIO("\n".join(lines)), sep="\t", dtype=str).fillna(""))


def normalize_columns(df):
    alias = {
        "IMP": "曝光量 IMP",
        "Clicks": "點擊量",
        "點擊": "點擊量",
        "CTR": "點擊率 CTR",
        "Ad Spend": "廣告花費",
        "CPC": "平均點擊成本 CPC",
        "Orders": "成交訂單數",
        "訂單": "成交訂單數",
        "訂單數": "成交訂單數",
        "CVR": "成交轉換率 CVR",
        "GMV": "商品交易總額 GMV",
        "ROAS": "廣告投資報酬率 ROAS",
        "CPA": "單筆成交成本 CPA",
        "Net Profit": "淨利",
        "Net Revenue": "扣除退款後營收",
        "AOV": "平均客單價 AOV",
    }
    return df.rename(columns={k: v for k, v in alias.items() if k in df.columns})

def to_int(v):
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).replace("NT$", "").replace(",", "").replace("%", "").replace("x", "").strip()
    if s in ["", "-", "nan", "None"]:
        return ""
    try:
        return int(round(float(s)))
    except Exception:
        m = re.search(r"-?\d+(?:\.\d+)?", s)
        if m:
            return int(round(float(m.group(0))))
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
        m = re.search(r"-?\d+(?:\.\d+)?", s)
        if m:
            return float(m.group(0))
        return ""

def clean_numeric_df(df):
    out = df.copy()
    int_cols = ["曝光量 IMP", "點擊量", "成交訂單數", "商品交易總額 GMV", "廣告花費", "淨利", "扣除退款後營收", "退款金額", "其他成本合計", "商品成本", "單件成本", "國際物流／履約成本", "倉儲與包裝成本", "平台／金流手續費", "跨境關稅／稅務成本", "退貨損耗", "客服與營運成本", "數量"]
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
cost_cols_for_total = ["商品成本", "國際物流／履約成本", "倉儲與包裝成本", "平台／金流手續費", "跨境關稅／稅務成本", "退貨損耗", "客服與營運成本"]
if "其他成本合計" not in profit.columns:
    present_cost_cols = [c for c in cost_cols_for_total if c in profit.columns]
    if present_cost_cols:
        profit["其他成本合計"] = profit[present_cost_cols].apply(
            lambda row: sum([x for x in row if isinstance(x, (int, float))]),
            axis=1
        )
    else:
        profit["其他成本合計"] = 0

total_profit_rate = to_float(profit.iloc[-1]["淨利率"])

total_profit_rate = to_float(profit.iloc[-1]["淨利率"])

# =========================================================
# 顯示格式
# =========================================================
def display_df(df):
    out = df.copy()
    money_cols = [
        "商品交易總額 GMV", "廣告花費", "淨利", "扣除退款後營收", "退款金額",
        "其他成本合計", "商品成本", "單件成本", "國際物流／履約成本", "倉儲與包裝成本", "平台／金流手續費", "跨境關稅／稅務成本", "退貨損耗", "客服與營運成本", "平均客單價 AOV"
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
        horizontal_bar("廣告平台 GMV", ad_platform.assign(**{"商品交易總額 GMV": pd.to_numeric(ad_platform["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "廣告平台", "商品交易總額 GMV", "#2563eb", 360)
    with cc2:
        horizontal_bar("國家市場 GMV", country.assign(**{"商品交易總額 GMV": pd.to_numeric(country["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "國家市場", "商品交易總額 GMV", "#0ea5e9", 360)

with tab3:
    st.subheader("商品銷售成效")
    st.dataframe(display_df(product_display), use_container_width=True, hide_index=True)

    st.subheader("廣告素材成效")
    st.dataframe(display_df(creative_display), use_container_width=True, hide_index=True)

    horizontal_bar("商品 GMV", product.assign(**{"商品交易總額 GMV": pd.to_numeric(product["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "商品名稱", "商品交易總額 GMV", "#22c55e", 1150)
    horizontal_bar("廣告素材 GMV", creative.assign(**{"商品交易總額 GMV": pd.to_numeric(creative["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "廣告素材", "商品交易總額 GMV", "#f97316", 420)

with tab4:
    st.subheader("裝置來源成效")
    st.dataframe(display_df(device_display), use_container_width=True, hide_index=True)

    st.subheader("受眾年齡成效")
    st.dataframe(display_df(age_display), use_container_width=True, hide_index=True)

    st.subheader("受眾性別成效")
    st.dataframe(display_df(gender_display), use_container_width=True, hide_index=True)

    d1, d2, d3 = st.columns(3)
    with d1:
        horizontal_bar("裝置來源 GMV", device.assign(**{"商品交易總額 GMV": pd.to_numeric(device["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "裝置來源", "商品交易總額 GMV", "#2563eb", 340)
    with d2:
        horizontal_bar("受眾年齡 GMV", age.assign(**{"商品交易總額 GMV": pd.to_numeric(age["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "年齡層", "商品交易總額 GMV", "#a855f7", 340)
    with d3:
        horizontal_bar("受眾性別 GMV", gender.assign(**{"商品交易總額 GMV": pd.to_numeric(gender["商品交易總額 GMV"], errors="coerce").fillna(0)}).sort_values("商品交易總額 GMV", ascending=False), "性別", "商品交易總額 GMV", "#ec4899", 340)

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
