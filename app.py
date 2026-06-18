
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
期間	2026/06/12－2026/06/18
幣別	NTD 新台幣
曝光量 IMP	32,948,617
點擊量	814,273
點擊率 CTR	2.47%
廣告花費	NT$8,936,417
平均點擊成本 CPC	NT$10.97
成交訂單數	27,894
成交轉換率 CVR	3.43%
商品交易總額 GMV	NT$67,826,941
廣告投資報酬率 ROAS	7.59x
單筆成交成本 CPA	NT$320.37
淨利	NT$16,752,150
扣除退款後營收	NT$67,047,678

報表圖表用資料

圖表資料	2026/06/12	2026/06/13	2026/06/14	2026/06/15	2026/06/16	2026/06/17	2026/06/18	合計
曝光量 IMP	4,365,812	5,021,479	4,738,206	4,102,667	5,894,305	4,287,531	4,538,617	32,948,617
點擊量	105,746	126,584	119,326	98,213	151,947	102,673	109,784	814,273
成交訂單數	3,481	4,216	3,982	3,125	5,304	3,458	4,328	27,894
商品交易總額 GMV	NT$8,356,724	NT$10,238,591	NT$9,764,318	NT$7,229,086	NT$13,998,472	NT$8,056,931	NT$10,182,819	NT$67,826,941
廣告花費	NT$1,196,583	NT$1,342,916	NT$1,269,485	NT$1,042,736	NT$1,528,219	NT$1,101,358	NT$1,455,120	NT$8,936,417
淨利	NT$1,956,300	NT$2,718,406	NT$2,144,820	NT$1,522,640	NT$4,186,275	NT$1,724,991	NT$2,498,718	NT$16,752,150
扣除退款後營收	NT$8,260,382	NT$10,121,307	NT$9,660,630	NT$7,141,049	NT$13,841,554	NT$7,965,727	NT$10,057,029	NT$67,047,678

每日點擊趨勢

日期	曝光量 IMP	點擊量	點擊率 CTR	廣告花費	平均點擊成本 CPC
2026/06/12	4,365,812	105,746	2.42%	NT$1,196,583	NT$11.32
2026/06/13	5,021,479	126,584	2.52%	NT$1,342,916	NT$10.61
2026/06/14	4,738,206	119,326	2.52%	NT$1,269,485	NT$10.64
2026/06/15	4,102,667	98,213	2.39%	NT$1,042,736	NT$10.62
2026/06/16	5,894,305	151,947	2.58%	NT$1,528,219	NT$10.06
2026/06/17	4,287,531	102,673	2.39%	NT$1,101,358	NT$10.73
2026/06/18	4,538,617	109,784	2.42%	NT$1,455,120	NT$13.25
合計	32,948,617	814,273	2.47%	NT$8,936,417	NT$10.97

每日訂單趨勢

日期	點擊量	成交訂單數	成交轉換率 CVR	廣告花費	單筆成交成本 CPA
2026/06/12	105,746	3,481	3.29%	NT$1,196,583	NT$343.75
2026/06/13	126,584	4,216	3.33%	NT$1,342,916	NT$318.53
2026/06/14	119,326	3,982	3.34%	NT$1,269,485	NT$318.81
2026/06/15	98,213	3,125	3.18%	NT$1,042,736	NT$333.68
2026/06/16	151,947	5,304	3.49%	NT$1,528,219	NT$288.13
2026/06/17	102,673	3,458	3.37%	NT$1,101,358	NT$318.50
2026/06/18	109,784	4,328	3.94%	NT$1,455,120	NT$336.21
合計	814,273	27,894	3.43%	NT$8,936,417	NT$320.37

每日銷售額趨勢

日期	成交訂單數	商品交易總額 GMV	廣告花費	ROAS	淨利	扣除退款後營收	淨利率
2026/06/12	3,481	NT$8,356,724	NT$1,196,583	6.98x	NT$1,956,300	NT$8,260,382	23.68%
2026/06/13	4,216	NT$10,238,591	NT$1,342,916	7.62x	NT$2,718,406	NT$10,121,307	26.86%
2026/06/14	3,982	NT$9,764,318	NT$1,269,485	7.69x	NT$2,144,820	NT$9,660,630	22.20%
2026/06/15	3,125	NT$7,229,086	NT$1,042,736	6.93x	NT$1,522,640	NT$7,141,049	21.32%
2026/06/16	5,304	NT$13,998,472	NT$1,528,219	9.16x	NT$4,186,275	NT$13,841,554	30.24%
2026/06/17	3,458	NT$8,056,931	NT$1,101,358	7.32x	NT$1,724,991	NT$7,965,727	21.66%
2026/06/18	4,328	NT$10,182,819	NT$1,455,120	7.00x	NT$2,498,718	NT$10,057,029	24.85%
合計	27,894	NT$67,826,941	NT$8,936,417	7.59x	NT$16,752,150	NT$67,047,678	24.99%

平台銷售額排名

排名	銷售平台／通路	成交訂單數	商品交易總額 GMV	銷售占比
1	自有品牌站／Shopify Plus	11,548	NT$29,572,546	43.60%
2	TikTok Shop	7,308	NT$16,753,254	24.70%
3	Amazon Marketplace	4,212	NT$9,834,906	14.50%
4	eBay	2,204	NT$5,019,194	7.40%
5	Shopee Cross-border	1,590	NT$3,798,309	5.60%
6	Walmart Marketplace	1,032	NT$2,848,732	4.20%
合計		27,894	NT$67,826,941	100.00%

每日完整投放數據

日期	曝光量 IMP	點擊量	CTR	廣告花費	CPC	訂單數	CVR	GMV	ROAS	CPA	淨利	扣除退款後營收	淨利率
2026/06/12	4,365,812	105,746	2.42%	NT$1,196,583	NT$11.32	3,481	3.29%	NT$8,356,724	6.98x	NT$343.75	NT$1,956,300	NT$8,260,382	23.68%
2026/06/13	5,021,479	126,584	2.52%	NT$1,342,916	NT$10.61	4,216	3.33%	NT$10,238,591	7.62x	NT$318.53	NT$2,718,406	NT$10,121,307	26.86%
2026/06/14	4,738,206	119,326	2.52%	NT$1,269,485	NT$10.64	3,982	3.34%	NT$9,764,318	7.69x	NT$318.81	NT$2,144,820	NT$9,660,630	22.20%
2026/06/15	4,102,667	98,213	2.39%	NT$1,042,736	NT$10.62	3,125	3.18%	NT$7,229,086	6.93x	NT$333.68	NT$1,522,640	NT$7,141,049	21.32%
2026/06/16	5,894,305	151,947	2.58%	NT$1,528,219	NT$10.06	5,304	3.49%	NT$13,998,472	9.16x	NT$288.13	NT$4,186,275	NT$13,841,554	30.24%
2026/06/17	4,287,531	102,673	2.39%	NT$1,101,358	NT$10.73	3,458	3.37%	NT$8,056,931	7.32x	NT$318.50	NT$1,724,991	NT$7,965,727	21.66%
2026/06/18	4,538,617	109,784	2.42%	NT$1,455,120	NT$13.25	4,328	3.94%	NT$10,182,819	7.00x	NT$336.21	NT$2,498,718	NT$10,057,029	24.85%
合計	32,948,617	814,273	2.47%	NT$8,936,417	NT$10.97	27,894	3.43%	NT$67,826,941	7.59x	NT$320.37	NT$16,752,150	NT$67,047,678	24.99%

廣告平台成效

廣告平台	曝光量 IMP	點擊量	CTR	廣告花費	CPC	訂單數	CVR	GMV	ROAS	CPA	扣除退款後營收	淨利	淨利率
TikTok Ads	13,179,447	333,852	2.53%	NT$3,485,203	NT$10.44	9,763	2.92%	NT$24,417,699	7.01x	NT$356.98	NT$24,137,164	NT$3,350,430	13.88%
Meta Ads	8,896,127	227,996	2.56%	NT$2,502,197	NT$10.97	8,647	3.79%	NT$21,026,352	8.40x	NT$289.37	NT$20,784,780	NT$6,030,774	29.02%
Google Ads	5,930,751	138,426	2.33%	NT$1,787,283	NT$12.91	5,300	3.83%	NT$12,887,119	7.21x	NT$337.22	NT$12,739,059	NT$3,685,473	28.93%
Pinterest Ads	2,965,375	73,285	2.47%	NT$625,549	NT$8.54	2,510	3.42%	NT$6,104,424	9.76x	NT$249.22	NT$6,034,291	NT$2,680,344	44.42%
Snapchat Ads	1,976,917	40,714	2.06%	NT$536,185	NT$13.17	1,674	4.11%	NT$3,391,347	6.32x	NT$320.30	NT$3,352,384	NT$1,005,129	29.98%
合計	32,948,617	814,273	2.47%	NT$8,936,417	NT$10.97	27,894	3.43%	NT$67,826,941	7.59x	NT$320.37	NT$67,047,678	NT$16,752,150	24.99%

國家市場成效

國家市場	曝光量 IMP	點擊量	CTR	廣告花費	CPC	訂單數	CVR	GMV	ROAS	CPA	扣除退款後營收	淨利	淨利率
United States 美國	13,838,419	333,852	2.41%	NT$3,842,659	NT$11.51	11,018	3.30%	NT$27,469,911	7.15x	NT$348.76	NT$27,154,310	NT$5,025,645	18.51%
United Kingdom 英國	5,601,265	146,569	2.62%	NT$1,429,827	NT$9.76	4,909	3.35%	NT$12,073,195	8.44x	NT$291.27	NT$11,934,487	NT$3,852,995	32.28%
Canada 加拿大	4,612,806	113,998	2.47%	NT$1,295,780	NT$11.37	4,045	3.55%	NT$9,631,426	7.43x	NT$320.34	NT$9,520,770	NT$2,680,344	28.15%
Australia 澳洲	3,624,348	85,499	2.36%	NT$983,006	NT$11.50	2,957	3.46%	NT$7,257,483	7.38x	NT$332.43	NT$7,174,101	NT$1,675,215	23.35%
Japan 日本	2,635,889	64,327	2.44%	NT$741,723	NT$11.53	2,259	3.51%	NT$5,426,155	7.32x	NT$328.34	NT$5,363,814	NT$1,340,172	24.99%
Singapore 新加坡	1,647,431	43,971	2.67%	NT$428,948	NT$9.76	1,618	3.68%	NT$3,662,655	8.54x	NT$265.11	NT$3,620,575	NT$1,507,693	41.64%
Malaysia 馬來西亞	988,459	26,057	2.64%	NT$214,474	NT$8.23	1,088	4.18%	NT$2,306,116	10.75x	NT$197.13	NT$2,279,621	NT$670,086	29.39%
合計	32,948,617	814,273	2.47%	NT$8,936,417	NT$10.97	27,894	3.43%	NT$67,826,941	7.59x	NT$320.37	NT$67,047,678	NT$16,752,150	24.99%

商品銷售成效

商品名稱	AOV	單件成本	IMP	點擊	CTR	廣告花費	CPC	訂單	CVR	GMV	ROAS	CPA	商品成本	淨利	扣除退款後營收	淨利率
智能香氛小夜燈	NT$3,386.28	NT$1,211.89	297,953	9,999	3.36%	NT$185,674	NT$18.57	479	4.79%	NT$1,622,026	8.74x	NT$387.63	NT$580,494	NT$549,396	NT$1,610,824	34.11%
桌面空氣循環扇	NT$4,031.68	NT$1,434.89	832,628	17,525	2.10%	NT$181,811	NT$10.37	441	2.52%	NT$1,777,970	9.78x	NT$412.27	NT$632,785	NT$553,728	NT$1,759,315	31.47%
智能空氣淨化器	NT$10,606.60	NT$4,141.37	699,553	13,421	1.92%	NT$1,076,168	NT$80.18	359	2.67%	NT$3,807,770	3.54x	NT$2,997.68	NT$1,486,753	NT$593,310	NT$3,761,973	15.77%
智能廚房秤	NT$2,150.90	NT$673.43	191,754	5,700	2.97%	NT$56,367	NT$9.89	294	5.16%	NT$632,365	11.22x	NT$191.72	NT$197,989	NT$158,355	NT$625,649	25.31%
便攜式保溫杯	NT$1,617.07	NT$533.94	708,864	25,254	3.56%	NT$77,795	NT$3.08	696	2.76%	NT$1,125,480	14.47x	NT$111.77	NT$371,622	NT$201,089	NT$1,109,286	18.13%
多功能收納包	NT$2,989.31	NT$943.90	1,482,891	29,213	1.97%	NT$179,353	NT$6.14	875	3.00%	NT$2,615,645	14.58x	NT$204.97	NT$825,914	NT$556,604	NT$2,598,553	21.42%
旅行壓縮袋組	NT$3,240.61	NT$1,014.96	575,961	17,583	3.05%	NT$281,062	NT$15.98	863	4.91%	NT$2,796,648	9.95x	NT$325.68	NT$875,907	NT$1,002,276	NT$2,764,021	36.26%
磁吸式無線充電座	NT$3,820.75	NT$1,455.44	455,214	11,374	2.50%	NT$114,964	NT$10.11	287	2.52%	NT$1,096,554	9.54x	NT$400.57	NT$417,710	NT$206,253	NT$1,086,020	18.99%
藍牙降噪耳機	NT$6,046.60	NT$2,457.88	367,528	10,762	2.93%	NT$305,223	NT$28.36	406	3.77%	NT$2,454,918	8.04x	NT$751.78	NT$997,899	NT$270,377	NT$2,430,272	11.13%
手機防水收納袋	NT$1,290.34	NT$337.34	783,617	18,984	2.42%	NT$74,108	NT$3.90	837	4.41%	NT$1,080,018	14.57x	NT$88.54	NT$282,353	NT$199,218	NT$1,071,316	18.60%
摺疊式手機支架	NT$1,317.78	NT$416.57	972,481	29,498	3.03%	NT$149,687	NT$5.07	1,004	3.40%	NT$1,323,055	8.84x	NT$149.09	NT$418,233	NT$464,754	NT$1,311,610	35.43%
LED補光化妝鏡	NT$3,106.78	NT$961.51	432,876	11,071	2.56%	NT$129,459	NT$11.69	493	4.45%	NT$1,531,643	11.83x	NT$262.59	NT$474,025	NT$614,349	NT$1,511,152	40.65%
電動筋膜按摩器	NT$8,462.43	NT$3,397.43	205,484	5,074	2.47%	NT$216,735	NT$42.71	159	3.13%	NT$1,345,527	6.21x	NT$1,363.11	NT$540,192	NT$284,628	NT$1,322,244	21.53%
頸掛式小風扇	NT$2,414.22	NT$709.77	374,828	11,299	3.01%	NT$134,385	NT$11.89	600	5.31%	NT$1,448,535	10.78x	NT$223.98	NT$425,865	NT$324,267	NT$1,424,926	22.76%
USB加熱暖手寶	NT$1,659.91	NT$455.98	305,022	9,746	3.20%	NT$54,649	NT$5.61	334	3.43%	NT$554,410	10.14x	NT$163.62	NT$152,298	NT$143,778	NT$549,147	26.18%
智能感應垃圾桶	NT$4,831.06	NT$1,737.65	290,767	7,540	2.59%	NT$118,897	NT$15.77	399	5.29%	NT$1,927,594	16.21x	NT$297.99	NT$693,324	NT$799,822	NT$1,902,961	42.03%
防滑浴室地墊	NT$1,379.86	NT$397.12	648,568	20,439	3.15%	NT$239,543	NT$11.72	673	3.29%	NT$928,648	3.88x	NT$355.93	NT$267,262	NT$235,455	NT$914,572	25.74%
廚房瀝水置物架	NT$3,171.12	NT$1,132.34	1,165,180	20,338	1.75%	NT$184,278	NT$9.06	828	4.07%	NT$2,625,686	14.25x	NT$222.56	NT$937,581	NT$374,115	NT$2,580,770	14.50%
矽膠保鮮袋組	NT$1,130.64	NT$303.17	670,707	14,047	2.09%	NT$59,538	NT$4.24	347	2.47%	NT$392,331	6.59x	NT$171.58	NT$105,201	NT$100,298	NT$385,575	26.01%
不鏽鋼保鮮盒	NT$2,499.72	NT$839.13	1,297,758	32,082	2.47%	NT$426,735	NT$13.30	817	2.55%	NT$2,042,270	4.79x	NT$522.32	NT$685,572	NT$211,158	NT$2,014,412	10.48%
可折疊購物袋	NT$1,085.81	NT$255.24	881,084	16,053	1.82%	NT$55,834	NT$3.48	833	5.19%	NT$904,478	16.20x	NT$67.03	NT$212,611	NT$193,031	NT$898,802	21.48%
旅行盥洗收納包	NT$1,648.48	NT$534.99	827,690	24,462	2.96%	NT$129,240	NT$5.28	1,210	4.95%	NT$1,994,658	15.43x	NT$106.81	NT$647,341	NT$764,229	NT$1,970,439	38.78%
護照證件收納包	NT$1,511.87	NT$455.92	309,733	9,019	2.91%	NT$27,071	NT$3.00	277	3.07%	NT$418,787	15.47x	NT$97.73	NT$126,290	NT$147,717	NT$415,826	35.52%
行李箱電子秤	NT$1,332.67	NT$429.77	746,068	17,020	2.28%	NT$96,043	NT$5.64	745	4.38%	NT$992,837	10.34x	NT$128.92	NT$320,176	NT$240,452	NT$981,511	24.50%
車用手機支架	NT$1,949.54	NT$636.65	354,510	8,540	2.41%	NT$97,548	NT$11.42	445	5.21%	NT$867,544	8.89x	NT$219.21	NT$283,310	NT$353,871	NT$853,899	41.44%
車用香氛擴香器	NT$2,290.50	NT$779.56	479,383	15,332	3.20%	NT$74,218	NT$4.84	542	3.54%	NT$1,241,452	16.73x	NT$136.93	NT$422,522	NT$520,389	NT$1,221,299	42.61%
車用吸塵器	NT$3,730.40	NT$1,529.43	467,546	7,756	1.66%	NT$211,785	NT$27.31	389	5.02%	NT$1,451,126	6.85x	NT$544.43	NT$594,949	NT$348,780	NT$1,438,238	24.25%
寵物飲水機	NT$4,804.83	NT$1,912.46	1,219,949	22,200	1.82%	NT$432,828	NT$19.50	545	2.45%	NT$2,618,632	6.05x	NT$794.18	NT$1,042,293	NT$540,771	NT$2,584,292	20.93%
寵物除毛刷	NT$1,880.63	NT$582.82	492,295	15,418	3.13%	NT$107,799	NT$6.99	541	3.51%	NT$1,017,421	9.44x	NT$199.26	NT$315,303	NT$127,967	NT$1,010,852	12.66%
寵物外出水壺	NT$1,850.66	NT$504.76	445,400	10,712	2.41%	NT$109,577	NT$10.23	343	3.20%	NT$634,777	5.79x	NT$319.47	NT$173,132	NT$61,055	NT$625,646	9.76%
瑜珈彈力帶組	NT$1,378.68	NT$349.65	578,048	15,496	2.68%	NT$215,881	NT$13.93	755	4.87%	NT$1,040,905	4.82x	NT$285.94	NT$263,985	NT$252,565	NT$1,029,540	24.53%
防滑瑜珈墊	NT$4,806.35	NT$1,682.88	247,679	8,108	3.27%	NT$207,438	NT$25.58	419	5.17%	NT$2,013,862	9.71x	NT$495.08	NT$705,125	NT$200,937	NT$1,989,757	10.10%
運動水壺	NT$1,886.29	NT$578.85	489,213	10,984	2.25%	NT$61,545	NT$5.60	445	4.05%	NT$839,401	13.64x	NT$138.30	NT$257,589	NT$269,072	NT$831,066	32.38%
快乾運動毛巾	NT$1,174.47	NT$346.98	659,384	12,188	1.85%	NT$54,638	NT$4.48	398	3.27%	NT$467,440	8.56x	NT$137.28	NT$138,100	NT$64,130	NT$460,345	13.93%
露營LED掛燈	NT$2,630.89	NT$915.29	615,599	22,162	3.60%	NT$132,909	NT$6.00	499	2.25%	NT$1,312,813	9.88x	NT$266.35	NT$456,732	NT$317,050	NT$1,301,984	24.35%
戶外折疊椅	NT$6,413.66	NT$2,267.42	431,571	13,484	3.12%	NT$175,723	NT$13.03	364	2.70%	NT$2,334,572	13.29x	NT$482.76	NT$825,341	NT$638,785	NT$2,305,060	27.71%
便攜餐具組	NT$1,266.91	NT$375.14	470,031	12,029	2.56%	NT$67,669	NT$5.63	594	4.94%	NT$752,545	11.12x	NT$113.92	NT$222,831	NT$262,956	NT$741,769	35.45%
防水收納乾濕袋	NT$1,372.15	NT$396.58	291,466	6,836	2.35%	NT$83,873	NT$12.27	334	4.89%	NT$458,298	5.46x	NT$251.12	NT$132,457	NT$184,977	NT$453,672	40.77%
兒童防漏水杯	NT$1,916.88	NT$664.71	915,870	22,216	2.43%	NT$319,187	NT$14.37	492	2.21%	NT$943,104	2.95x	NT$648.75	NT$327,036	NT$218,378	NT$936,083	23.33%
兒童矽膠圍兜	NT$1,056.17	NT$292.76	552,214	10,917	1.98%	NT$134,488	NT$12.32	316	2.89%	NT$333,749	2.48x	NT$425.59	NT$92,511	NT$34,420	NT$330,450	10.42%
嬰兒推車收納袋	NT$2,389.23	NT$658.60	684,252	23,045	3.37%	NT$99,208	NT$4.30	622	2.70%	NT$1,486,101	14.98x	NT$159.50	NT$409,649	NT$161,023	NT$1,463,966	11.00%
居家防撞條組	NT$1,173.53	NT$316.10	441,480	8,264	1.87%	NT$29,029	NT$3.51	348	4.21%	NT$408,388	14.07x	NT$83.42	NT$110,003	NT$117,266	NT$405,174	28.94%
收納抽屜分隔板	NT$2,088.75	NT$646.83	506,170	14,617	2.89%	NT$250,874	NT$17.16	593	4.06%	NT$1,238,626	4.94x	NT$423.06	NT$383,568	NT$530,344	NT$1,221,792	43.41%
真空壓縮收納袋	NT$1,929.31	NT$613.69	360,475	10,469	2.90%	NT$174,930	NT$16.71	467	4.46%	NT$900,987	5.15x	NT$374.58	NT$286,595	NT$192,629	NT$889,396	21.66%
衣物除毛球機	NT$2,918.79	NT$1,098.77	669,532	22,874	3.42%	NT$380,683	NT$16.64	523	2.29%	NT$1,526,529	4.01x	NT$727.88	NT$574,658	NT$174,202	NT$1,504,597	11.58%
迷你熨燙機	NT$5,253.57	NT$1,846.60	326,267	10,522	3.22%	NT$264,648	NT$25.15	303	2.88%	NT$1,591,831	6.01x	NT$873.43	NT$559,520	NT$166,108	NT$1,581,429	10.50%
防藍光眼鏡	NT$2,317.80	NT$752.02	256,815	9,260	3.61%	NT$70,246	NT$7.59	491	5.30%	NT$1,138,041	16.20x	NT$143.07	NT$369,243	NT$408,786	NT$1,130,602	36.16%
睡眠遮光眼罩	NT$1,248.78	NT$295.55	4,351,485	80,801	1.86%	NT$158,091	NT$1.96	1,920	2.38%	NT$2,397,662	15.17x	NT$82.34	NT$567,448	NT$960,119	NT$2,378,634	40.36%
人體工學滑鼠墊	NT$1,587.96	NT$465.29	239,088	8,090	3.38%	NT$74,330	NT$9.19	303	3.75%	NT$481,152	6.47x	NT$245.31	NT$140,983	NT$67,227	NT$476,573	14.11%
桌面理線收納盒	NT$1,375.78	NT$388.65	878,686	24,450	2.78%	NT$149,663	NT$6.12	647	2.65%	NT$890,130	5.95x	NT$231.32	NT$251,456	NT$389,684	NT$880,387	44.26%
合計		NT$809.56	32,948,617	814,273	2.47%	NT$8,936,417	NT$10.97	27,894	3.43%	NT$67,826,941	7.59x	NT$320.37	NT$22,581,736	NT$16,752,150	NT$67,047,678	24.99%

廣告素材成效

廣告素材	素材類型	IMP	點擊	CTR	廣告花費	CPC	訂單	CVR	GMV	ROAS	CPA	扣除退款後營收	淨利	淨利率
短影音A｜高單價家電開箱	15秒短影音	8,072,411	162,855	2.02%	NT$2,144,740	NT$13.17	5,300	3.25%	NT$14,243,658	6.64x	NT$404.67	NT$14,080,012	NT$2,345,301	16.66%
短影音B｜旅行收納前後對比	20秒短影音	6,754,466	191,354	2.83%	NT$1,340,463	NT$7.01	6,973	3.64%	NT$16,617,600	12.40x	NT$192.24	NT$16,426,681	NT$4,858,124	29.57%
短影音C｜辦公桌面改造	18秒短影音	5,107,036	122,141	2.39%	NT$1,251,098	NT$10.24	4,463	3.65%	NT$10,852,311	8.67x	NT$280.33	NT$10,727,629	NT$2,847,865	26.55%
短影音D｜寵物日常實測	25秒短影音	4,448,063	105,855	2.38%	NT$1,787,284	NT$16.88	3,626	3.43%	NT$9,495,772	5.31x	NT$492.91	NT$9,386,675	NT$2,010,258	21.42%
輪播圖E｜低單價爆品合集	圖文輪播	5,436,522	179,140	3.30%	NT$1,251,098	NT$6.98	5,579	3.11%	NT$12,208,849	9.76x	NT$224.25	NT$12,068,582	NT$3,685,473	30.54%
再行銷F｜購物車限時優惠	再行銷素材	3,130,119	52,928	1.69%	NT$1,161,734	NT$21.95	1,953	3.69%	NT$4,408,751	3.79x	NT$594.85	NT$4,358,099	NT$1,005,129	23.06%
合計		32,948,617	814,273	2.47%	NT$8,936,417	NT$10.97	27,894	3.43%	NT$67,826,941	7.59x	NT$320.37	NT$67,047,678	NT$16,752,150	24.99%

裝置來源成效

裝置來源	IMP	點擊	CTR	廣告花費	CPC	訂單	CVR	GMV	ROAS	CPA	扣除退款後營收	淨利	淨利率
Mobile App / 行動裝置	23,064,032	586,277	2.54%	NT$6,166,128	NT$10.52	19,526	3.33%	NT$47,478,859	7.70x	NT$315.79	NT$46,933,375	NT$10,553,855	22.49%
Desktop Web / 桌機網頁	5,930,751	138,426	2.33%	NT$1,697,919	NT$12.27	5,021	3.63%	NT$12,208,849	7.19x	NT$338.16	NT$12,068,582	NT$3,685,473	30.54%
Tablet / 平板	2,471,146	56,999	2.31%	NT$714,913	NT$12.54	2,092	3.67%	NT$5,087,021	7.12x	NT$341.74	NT$5,028,576	NT$1,507,693	29.98%
In-App Webview / 內嵌瀏覽器	1,482,688	32,571	2.20%	NT$357,457	NT$10.97	1,255	3.85%	NT$3,052,212	8.54x	NT$284.83	NT$3,017,145	NT$1,005,129	33.31%
合計	32,948,617	814,273	2.47%	NT$8,936,417	NT$10.97	27,894	3.43%	NT$67,826,941	7.59x	NT$320.37	NT$67,047,678	NT$16,752,150	24.99%

受眾年齡成效

年齡層	IMP	點擊	CTR	廣告花費	CPC	訂單	CVR	GMV	ROAS	CPA	扣除退款後營收	淨利	淨利率
18-24	6,260,237	146,569	2.34%	NT$1,608,555	NT$10.97	4,742	3.24%	NT$11,530,580	7.17x	NT$339.21	NT$11,398,105	NT$2,680,344	23.52%
25-34	12,685,217	325,709	2.57%	NT$3,485,202	NT$10.70	11,297	3.47%	NT$27,130,776	7.78x	NT$308.51	NT$26,819,071	NT$6,868,382	25.61%
35-44	8,896,127	219,854	2.47%	NT$2,502,197	NT$11.38	7,671	3.49%	NT$18,991,544	7.59x	NT$326.19	NT$18,773,350	NT$4,523,080	24.09%
45-54	3,459,605	85,499	2.47%	NT$938,324	NT$10.97	2,929	3.43%	NT$7,121,829	7.59x	NT$320.36	NT$7,040,006	NT$1,675,215	23.80%
55+	1,647,431	36,642	2.22%	NT$402,139	NT$10.97	1,255	3.43%	NT$3,052,212	7.59x	NT$320.43	NT$3,017,146	NT$1,005,129	33.31%
合計	32,948,617	814,273	2.47%	NT$8,936,417	NT$10.97	27,894	3.43%	NT$67,826,941	7.59x	NT$320.37	NT$67,047,678	NT$16,752,150	24.99%

受眾性別成效

性別	IMP	點擊	CTR	廣告花費	CPC	訂單	CVR	GMV	ROAS	CPA	扣除退款後營收	淨利	淨利率
女性	20,428,143	512,992	2.51%	NT$5,361,850	NT$10.45	17,015	3.32%	NT$41,374,434	7.72x	NT$315.12	NT$40,899,083	NT$10,051,290	24.58%
男性	10,543,557	252,425	2.39%	NT$3,038,382	NT$12.04	9,205	3.65%	NT$22,382,891	7.37x	NT$330.08	NT$22,125,734	NT$5,695,731	25.74%
未揭露／其他	1,976,917	48,856	2.47%	NT$536,185	NT$10.97	1,674	3.43%	NT$4,069,616	7.59x	NT$320.30	NT$4,022,861	NT$1,005,129	24.99%
合計	32,948,617	814,273	2.47%	NT$8,936,417	NT$10.97	27,894	3.43%	NT$67,826,941	7.59x	NT$320.37	NT$67,047,678	NT$16,752,150	24.99%

顧客轉換路徑

轉換階段	數量	與上一階段轉換率
曝光量 IMP	32,948,617	-
點擊量	814,273	2.47%
成交訂單數	27,894	3.43%
商品交易總額 GMV	NT$67,826,941	-
扣除退款後營收	NT$67,047,678	98.85%
淨利	NT$16,752,150	24.99%

訂單與退款資料

日期	成交訂單數	商品交易總額 GMV	退款金額	扣除退款後營收	淨利
2026/06/12	3,481	NT$8,356,724	NT$96,342	NT$8,260,382	NT$1,956,300
2026/06/13	4,216	NT$10,238,591	NT$117,284	NT$10,121,307	NT$2,718,406
2026/06/14	3,982	NT$9,764,318	NT$103,688	NT$9,660,630	NT$2,144,820
2026/06/15	3,125	NT$7,229,086	NT$88,037	NT$7,141,049	NT$1,522,640
2026/06/16	5,304	NT$13,998,472	NT$156,918	NT$13,841,554	NT$4,186,275
2026/06/17	3,458	NT$8,056,931	NT$91,204	NT$7,965,727	NT$1,724,991
2026/06/18	4,328	NT$10,182,819	NT$125,790	NT$10,057,029	NT$2,498,718
合計	27,894	NT$67,826,941	NT$779,263	NT$67,047,678	NT$16,752,150

營收與利潤

日期	GMV	退款金額	扣除退款後營收	商品成本	國際物流／履約成本	倉儲與包裝成本	平台／金流手續費	跨境關稅／稅務成本	退貨損耗	客服與營運成本	廣告花費	淨利	淨利率
2026/06/12	NT$8,356,724	NT$96,342	NT$8,260,382	NT$2,838,999	NT$730,685	NT$214,067	NT$245,749	NT$202,072	NT$133,057	NT$742,870	NT$1,196,583	NT$1,956,300	23.68%
2026/06/13	NT$10,238,591	NT$117,284	NT$10,121,307	NT$3,306,371	NT$937,210	NT$233,497	NT$396,057	NT$218,666	NT$130,509	NT$837,675	NT$1,342,916	NT$2,718,406	26.86%
2026/06/14	NT$9,764,318	NT$103,688	NT$9,660,630	NT$3,353,122	NT$1,025,518	NT$278,373	NT$322,892	NT$243,957	NT$154,334	NT$868,129	NT$1,269,485	NT$2,144,820	22.20%
2026/06/15	NT$7,229,086	NT$88,037	NT$7,141,049	NT$2,502,897	NT$604,001	NT$192,379	NT$260,552	NT$164,937	NT$117,185	NT$733,722	NT$1,042,736	NT$1,522,640	21.32%
2026/06/16	NT$13,998,472	NT$156,918	NT$13,841,554	NT$4,333,277	NT$1,050,143	NT$414,378	NT$490,482	NT$271,062	NT$237,344	NT$1,330,374	NT$1,528,219	NT$4,186,275	30.24%
2026/06/17	NT$8,056,931	NT$91,204	NT$7,965,727	NT$2,927,474	NT$722,433	NT$187,214	NT$306,558	NT$158,800	NT$106,520	NT$730,379	NT$1,101,358	NT$1,724,991	21.66%
2026/06/18	NT$10,182,819	NT$125,790	NT$10,057,029	NT$3,319,596	NT$911,061	NT$300,982	NT$357,685	NT$192,168	NT$164,004	NT$857,695	NT$1,455,120	NT$2,498,718	24.85%
7天合計	NT$67,826,941	NT$779,263	NT$67,047,678	NT$22,581,736	NT$5,981,051	NT$1,820,890	NT$2,379,975	NT$1,451,662	NT$1,042,953	NT$6,100,844	NT$8,936,417	NT$16,752,150	24.99%"""

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
        "CTR": "點擊率 CTR",
        "CPC": "平均點擊成本 CPC",
        "訂單數": "成交訂單數",
        "訂單": "成交訂單數",
        "CVR": "成交轉換率 CVR",
        "GMV": "商品交易總額 GMV",
        "ROAS": "廣告投資報酬率 ROAS",
        "CPA": "單筆成交成本 CPA",
        "IMP": "曝光量 IMP",
        "點擊": "點擊量",
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
