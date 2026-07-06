#!/usr/bin/env python3
"""Self-drawn institutional-grade diagrams for the Foundations Primer.
Semi dark theme, EN+ZH variants. Every figure carries an attribution footer:
  "Own illustration · Yicheng Yang" (+ "data: <source>" when a number is plotted).
Usage: python3 make_primer_figs.py [outdir]   -> writes figs_primer/pmXX_{en,zh}.png
"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib import font_manager as fm

for fp in ["/System/Library/Fonts/Hiragino Sans GB.ttc","/System/Library/Fonts/STHeiti Medium.ttc"]:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)
        try: matplotlib.rcParams["font.family"]=fm.FontProperties(fname=fp).get_name()
        except Exception: pass
        break

BG="#14101B"; POP="#F8A848"; POP2="#F79C2F"; INK="#EDEBF0"; SUB="#B5B4B7"
PANEL="#221E29"; PANEL2="#2B2832"; PANEL3="#34303A"; LINE="#56535B"
GREEN="#57C08A"; RED="#E8756A"; BLUE="#6FA8DC"

OUT = sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),"figs_primer")

def fig_ax(w=11,h=6):
    f,a=plt.subplots(figsize=(w,h)); f.patch.set_facecolor(BG); a.set_facecolor(BG)
    a.set_xlim(0,100); a.set_ylim(0,100); a.axis("off")
    return f,a

def box(a,x,y,w,h,label,sub="",fc=PANEL,ec=POP,fs=11,sfs=8.5,lc=None,tc=INK):
    a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.3,rounding_size=1.2",
                linewidth=1.1,edgecolor=ec,facecolor=fc))
    cy = y+h*(0.62 if sub else 0.5)
    a.text(x+w/2,cy,label,ha="center",va="center",color=lc or POP,fontsize=fs,fontweight="bold")
    if sub: a.text(x+w/2,y+h*0.3,sub,ha="center",va="center",color=tc,fontsize=sfs)

def arrow(a,x1,y1,x2,y2,color=POP2,lw=1.6,style="-|>"):
    a.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=15,color=color,linewidth=lw))

def footer(f,txt): f.text(0.012,0.015,txt,fontsize=8,color="#78767C")
def title(a,t,sub=""):
    a.text(2,96,t,fontsize=16,fontweight="bold",color=POP,va="top")
    if sub: a.text(2,90,sub,fontsize=10,color=SUB,va="top")

L=lambda en,zh,lang: en if lang=="en" else zh
OWN=lambda lang,data="": ("Own illustration · Yicheng Yang" if lang=="en" else "自绘示意 · Yicheng Yang")+((("  ·  data: " if lang=="en" else "  ·  数据来源: ")+data) if data else "")

# ---------- pm00: how the series fits together ----------
def pm00(lang):
    f,a=fig_ax(11,6.6)
    title(a,L("One machine, ten cross-sections","一台机器,十个横截面",lang),
          L("Primer modules (left) unlock the sector deep-dives (right)","基础篇模块(左)为对应板块深研(右)提供背景",lang))
    mods=[("01-02",L("Silicon & scaling","硅与缩放",lang)),("03-04",L("Compute & workloads","算力与负载",lang)),
          ("05-06",L("Memory & packaging","存储与封装",lang)),("07-08",L("Networks & power","网络与电力",lang)),
          ("09-10",L("Industry & metrics","行业与指标",lang))]
    secs=[L("Foundry · Equipment","代工 · 设备",lang),L("Accelerators · Models","加速器 · 模型",lang),
          L("Memory/HBM · Packaging","存储/HBM · 封装",lang),L("Networking · Datacenter","网络 · 数据中心",lang),
          L("Hyperscalers · China","超大规模 · 中国",lang)]
    for i,(mid,mm) in enumerate(mods):
        y=72-i*15
        box(a,4,y,34,11,f"§{mid}",mm,fs=11)
        box(a,62,y,34,11,secs[i],L("sector deep-dives","板块深研",lang),fc=PANEL2,ec=LINE,lc=INK)
        arrow(a,39,y+5.5,61,y+5.5)
    f.tight_layout(); footer(f,OWN(lang)); return f

# ---------- pm01: fab flow ----------
def pm01(lang):
    f,a=fig_ax(11,6.2)
    title(a,L("From sand to silicon: the manufacturing flow","从沙子到硅片:制造全流程",lang),
          L("The patterning loop repeats ~40-80x to build ~1,000 process steps","图形化循环重复约 40-80 次,累计约 1,000 道工序",lang))
    top=[(L("Quartz","石英砂",lang),L("refine","提纯",lang)),(L("Polysilicon","多晶硅",lang),"99.9999999%"),
         (L("Ingot","单晶锭",lang),L("Czochralski pull","直拉法",lang)),(L("Wafer","晶圆",lang),"300mm")]
    for i,(t,s) in enumerate(top):
        box(a,4+i*20,74,16,12,t,s);
        if i<3: arrow(a,20+i*20,80,24+i*20,80)
    arrow(a,72,74,60,64)
    loop=[L("Deposit","沉积",lang),L("Litho","光刻",lang),L("Etch","刻蚀",lang),L("Implant","掺杂",lang),L("CMP","抛光",lang)]
    a.add_patch(FancyBboxPatch((8,38),74,22,boxstyle="round,pad=0.4,rounding_size=1.5",lw=1.3,edgecolor=POP,facecolor="none",linestyle="--"))
    a.text(45,62,L("the patterning loop (x40-80)","图形化循环(×40-80 次)",lang),color=POP,fontsize=10,ha="center")
    for i,t in enumerate(loop):
        box(a,11+i*14,42,11,10,t,fc=PANEL2)
        if i<4: arrow(a,22+i*14,47,25+i*14,47)
    arrow(a,15,42,11,42, style="-")  # loop back visual
    bot=[(L("Test","测试",lang),L("defect density D0","缺陷密度 D0",lang)),(L("Dice","切割",lang),L("wafer → dies","晶圆→裸片",lang)),
         (L("Package","封装",lang),L("see Module 06","见模块 06",lang)),(L("Ship","出货",lang),L("yield decides cost","良率决定成本",lang))]
    for i,(t,s) in enumerate(bot):
        box(a,4+i*20,14,16,12,t,s,fc=PANEL3,ec=LINE,lc=INK)
        if i<3: arrow(a,20+i*20,20,24+i*20,20)
    arrow(a,45,38,45,27)
    f.tight_layout(); footer(f,OWN(lang)); return f

# ---------- pm02: scaling eras ----------
def pm02(lang):
    f,a=fig_ax(11,6)
    title(a,L("The end of cheap scaling","「便宜缩放」的终结",lang),
          L("Each era solved the last one's limit — until cost/transistor stopped falling","每个时代解决上个时代的极限——直到单位晶体管成本不再下降",lang))
    eras=[("1970-2006",L("Planar + Dennard","平面管 + Dennard",lang),L("smaller = faster = cheaper = cooler","更小=更快=更便宜=更省电",lang),GREEN),
          ("2006",L("Dennard dies","Dennard 失效",lang),L("power density stops falling; clocks stall ~4GHz","功率密度不再降;主频停在 ~4GHz",lang),RED),
          ("2011",L("FinFET","FinFET 鳍式",lang),L("gate wraps 3 sides — leakage tamed","栅极三面包裹沟道,压住漏电",lang),BLUE),
          ("2022+",L("GAA nanosheet","GAA 纳米片",lang),L("gate wraps all 4 sides","栅极四面全包",lang),BLUE),
          ("N3 era",L("Economics break","经济性断裂",lang),L("~15% cost/transistor gain - weakest in 50 yrs; SRAM ~0%","单位晶体管降本仅 ~15%=50 年最弱;SRAM 几乎 0",lang),RED)]
    for i,(yr,t,s,c) in enumerate(eras):
        y=70-i*13.5
        a.text(6,y+4,yr,color=POP,fontsize=11,fontweight="bold",ha="left")
        box(a,20,y,72,10,t,s,ec=c,fs=11,sfs=9)
        if i<4: arrow(a,16,y-1.2,16,y-11,color=LINE,lw=1.2)
    f.tight_layout(); footer(f,OWN(lang, "SemiAnalysis (verified: N3 ~15%, SRAM stall)")); return f

# ---------- pm03: GPU anatomy ----------
def pm03(lang):
    f,a=fig_ax(11,6.4)
    title(a,L("Anatomy of an AI accelerator","AI 加速器解剖",lang),
          L("Compute is easy to grow; feeding it (bandwidth) is the hard part","堆算力容易,喂饱算力(带宽)才是难点",lang))
    # HBM stacks left/right
    for i in range(3):
        box(a,4,18+i*20,10,14,"HBM",L("stack","堆叠",lang),fc=PANEL2,ec=BLUE,lc=BLUE)
        box(a,86,18+i*20,10,14,"HBM",L("stack","堆叠",lang),fc=PANEL2,ec=BLUE,lc=BLUE)
        arrow(a,14.5,25+i*20,19,25+i*20,color=BLUE); arrow(a,85.5,25+i*20,81,25+i*20,color=BLUE)
    # GPU die
    a.add_patch(FancyBboxPatch((20,12),60,68,boxstyle="round,pad=0.4,rounding_size=1.5",lw=1.4,edgecolor=POP,facecolor=PANEL))
    a.text(50,75,L("GPU die","GPU 裸片",lang),color=POP,fontsize=12,fontweight="bold",ha="center")
    for r in range(3):
        for c in range(6):
            x=24+c*9; y=52-r*13
            a.add_patch(Rectangle((x,y),8,10,facecolor=PANEL3,edgecolor=LINE,lw=0.7))
            a.text(x+4,y+6.6,"SM",color=INK,fontsize=7.5,ha="center")
            a.text(x+4,y+3,L("tensor","张量核",lang),color=POP2,fontsize=6,ha="center")
    box(a,24,15,52,7,L("L2 cache + NoC","L2 缓存 + 片上网络",lang),fc=PANEL2,ec=LINE,lc=INK,fs=9)
    box(a,30,2,40,7,"NVLink / PCIe",L("to other GPUs — Module 07","连向其他 GPU——见模块 07",lang),fc=PANEL2,ec=POP2,fs=9,sfs=7.5)
    arrow(a,50,12,50,9.4)
    f.tight_layout(); footer(f,OWN(lang)); return f

# ---------- pm04: training vs inference ----------
def pm04(lang):
    f,a=fig_ax(11,5.8)
    title(a,L("Two workloads, two bottlenecks","两种负载,两种瓶颈",lang))
    box(a,4,52,44,30,L("TRAINING","训练",lang),"",fc=PANEL,ec=GREEN,fs=13)
    a.text(26,70,L("compute-bound","算力受限",lang),color=GREEN,fontsize=10,ha="center")
    for i,t in enumerate([L("huge batches, weeks-long runs","超大 batch,数周连续运行",lang),
                          L("gradient sync every step -> needs fast scale-up","每步梯度同步 → 依赖高速纵向互连",lang),
                          L("metric: MFU (useful FLOPS / peak)","关键指标:MFU(有效算力占峰值比)",lang)]):
        a.text(6.5,64-i*5.5,"· "+t,color=INK,fontsize=9,ha="left")
    box(a,52,52,44,30,L("INFERENCE","推理",lang),"",fc=PANEL,ec=BLUE,fs=13)
    a.text(74,70,L("memory-bound (decode)","显存带宽受限(decode)",lang),color=BLUE,fontsize=10,ha="center")
    for i,t in enumerate([L("prefill: read prompt (compute-heavy)","prefill:读入提示词(吃算力)",lang),
                          L("decode: one token at a time, re-reads KV cache","decode:逐 token 生成,反复读 KV cache",lang),
                          L("metric: $/Mtok at target interactivity","关键指标:目标交互速度下的 $/百万token",lang)]):
        a.text(54.5,64-i*5.5,"· "+t,color=INK,fontsize=9,ha="left")
    box(a,14,14,72,24,L("Why it matters","为什么重要",lang),
        L("training rewards the biggest coherent machine; inference rewards $/token —\nthe two now pull chip and rack design in different directions",
          "训练奖励「最大的一台机器」;推理奖励「每 token 最便宜」——\n两者正把芯片与机柜设计拉向不同方向",lang),fc=PANEL2,ec=POP,fs=11,sfs=9)
    f.tight_layout(); footer(f,OWN(lang)); return f

# ---------- pm05: memory hierarchy + HBM stack ----------
def pm05(lang):
    f,a=fig_ax(11,6.2)
    title(a,L("The memory hierarchy — and why HBM exists","存储层级——以及 HBM 为什么存在",lang))
    tiers=[(L("Registers/SRAM (on-die)","寄存器/SRAM(片上)",lang),"~MB · <5ns",8),
           ("HBM","~100-1000GB · ~100ns",22),
           ("DDR/CXL","~TB · ~100-300ns",40),
           ("SSD",L("~10-100TB · ~100 us","~10-100TB · ~100微秒",lang),60)]
    for i,(t,s,w) in enumerate(tiers):
        y=66-i*14; x=50-w/2
        col=POP if i==1 else LINE
        box(a,x,y,w,11,t,s,ec=col,fc=PANEL if i==1 else PANEL2,fs=10.5,sfs=8.5,lc=POP if i==1 else INK)
    a.text(50,20,L("capacity grows downward · speed grows upward · HBM is the compromise AI lives on",
                   "越往下容量越大 · 越往上速度越快 · HBM 是 AI 赖以生存的折中层",lang),color=SUB,fontsize=9.5,ha="center")
    # HBM cross-section on the right
    a.text(84,78,L("inside an HBM stack","HBM 堆叠剖面",lang),color=POP,fontsize=10,ha="center")
    for i in range(8):
        a.add_patch(Rectangle((74,66-i*3.6),20,2.8,facecolor=PANEL3,edgecolor=BLUE,lw=0.8))
    a.text(84,70,L("8-16 DRAM dies","8-16 层 DRAM",lang),color=BLUE,fontsize=8,ha="center")
    for x in (78,84,90):
        a.plot([x,x],[38,66],color=POP2,lw=1.1)
    a.text(96,50,"TSV",color=POP2,fontsize=8,ha="left")
    a.add_patch(Rectangle((74,33),20,4,facecolor=PANEL,edgecolor=POP,lw=1))
    a.text(84,35,L("base die (logic)","基底 die(逻辑)",lang),color=POP,fontsize=8,ha="center")
    f.tight_layout(); footer(f,OWN(lang)); return f

# ---------- pm06: CoWoS cross-section ----------
def pm06(lang):
    f,a=fig_ax(11,5.6)
    title(a,L("2.5D packaging (CoWoS): how HBM meets the GPU","2.5D 封装(CoWoS):HBM 与 GPU 如何相遇",lang),
          L("Thousands of micro-wires through silicon — impossible on a normal circuit board","上万条硅内微互连——普通电路板做不到",lang))
    a.add_patch(Rectangle((10,18),80,8,facecolor=PANEL3,edgecolor=LINE))
    a.text(50,22,L("package substrate","封装基板",lang),color=INK,fontsize=9,ha="center")
    a.add_patch(Rectangle((16,28),68,8,facecolor=PANEL2,edgecolor=POP2))
    a.text(50,32,L("silicon interposer (the 'oS' wafer)","硅中介层(interposer)",lang),color=POP2,fontsize=9,ha="center")
    a.add_patch(Rectangle((22,38),26,16,facecolor=PANEL,edgecolor=POP,lw=1.3))
    a.text(35,46,"GPU",color=POP,fontsize=12,fontweight="bold",ha="center")
    for i in range(2):
        x=56+i*12
        for j in range(4):
            a.add_patch(Rectangle((x,38+j*3.4),9,2.6,facecolor=PANEL3,edgecolor=BLUE,lw=0.7))
        a.text(x+4.5,55,"HBM",color=BLUE,fontsize=9,ha="center")
    for x in range(24,84,4):
        a.plot([x,x],[36.4,38],color=LINE,lw=0.8)
    a.text(50,10,L("micro-bumps ~40-55um pitch · interposer routes GPU↔HBM at ~TB/s",
                   "微凸点间距 ~40-55um · 中介层以 ~TB/s 级带宽连接 GPU↔HBM",lang),color=SUB,fontsize=9,ha="center")
    a.text(50,60,L("3D (SoIC/hybrid bonding) stacks dies directly — bumpless, ~10x denser",
                   "3D(SoIC/混合键合)把 die 直接叠起——无凸点,密度再高一个量级",lang),color=SUB,fontsize=9,ha="center")
    f.tight_layout(); footer(f,OWN(lang)); return f

# ---------- pm07: scale-up vs scale-out ----------
def pm07(lang):
    f,a=fig_ax(11,6)
    title(a,L("Scale-up vs scale-out","纵向扩展 vs 横向扩展",lang),
          L("Copper for the rack, optics for the hall","机柜内用铜,机房间用光",lang))
    a.add_patch(FancyBboxPatch((6,26),38,52,boxstyle="round,pad=0.4,rounding_size=1.5",lw=1.3,edgecolor=POP,facecolor="none"))
    a.text(25,81,L("SCALE-UP: one giant GPU","纵向:拼成一颗大 GPU",lang),color=POP,fontsize=10.5,ha="center",fontweight="bold")
    for r in range(3):
        for c in range(3):
            box(a,10+c*11,60-r*13,9,9,"GPU","",fc=PANEL2,ec=LINE,lc=INK,fs=8)
    for r in range(3):
        a.plot([10,41],[64.5-r*13,64.5-r*13],color=POP2,lw=1)
    a.text(25,28.5,L("NVLink copper backplane · ~900GB/s/GPU","NVLink 铜背板 · ~900GB/s/GPU",lang),color=POP2,fontsize=8.5,ha="center")
    a.add_patch(FancyBboxPatch((56,26),38,52,boxstyle="round,pad=0.4,rounding_size=1.5",lw=1.3,edgecolor=BLUE,facecolor="none"))
    a.text(75,81,L("SCALE-OUT: many machines","横向:连接很多台机器",lang),color=BLUE,fontsize=10.5,ha="center",fontweight="bold")
    box(a,68,62,14,9,L("switch","交换机",lang),"",fc=PANEL2,ec=BLUE,lc=BLUE,fs=8.5)
    for i in range(3):
        box(a,60+i*11,38,9,9,L("rack","机柜",lang),"",fc=PANEL2,ec=LINE,lc=INK,fs=8)
        arrow(a,64.5+i*11,47,73+i*3,62,color=BLUE,lw=1.1)
    a.text(75,28.5,L("Ethernet/InfiniBand optics · ~100GB/s/GPU","以太网/IB 光互连 · ~100GB/s/GPU",lang),color=BLUE,fontsize=8.5,ha="center")
    a.text(50,14,L("9x bandwidth gap is why 'the rack is the new unit of compute' — and why CPO is coming",
                   "9 倍带宽差,就是「机柜成为新计算单元」的原因——也是 CPO 正在到来的原因",lang),color=SUB,fontsize=9.5,ha="center")
    f.tight_layout(); footer(f,OWN(lang,"SemiAnalysis (verified: 900 vs 100 GB/s)")); return f

# ---------- pm08: datacenter power chain ----------
def pm08(lang):
    f,a=fig_ax(11,5.8)
    title(a,L("The datacenter power chain","数据中心供电链",lang),
          L("Every stage is sold out — the cascade is circular: chips gate power, power gates chips","每一级都售罄——芯片卡电力,电力卡芯片",lang))
    chain=[(L("Grid","电网",lang),L("interconnection queue: years","并网排队:以年计",lang)),
           (L("Substation","变电站",lang),L("transformers: 3-4yr lead","变压器交期 3-4 年",lang)),
           (L("Switchgear/UPS","开关柜/UPS",lang),L("ride-through","穿越保护",lang)),
           (L("Busway","母线",lang),L("54V -> 800VDC era","54V → 800VDC 时代",lang)),
           (L("Rack","机柜",lang),L("120-600kW+","120-600kW+",lang)),
           ("GPU",L("~1-2kW each","单卡 ~1-2kW",lang))]
    for i,(t,s) in enumerate(chain):
        x=3+i*16.3
        box(a,x,52,14.5,16,t,s,fs=10,sfs=7.8)
        if i<5: arrow(a,x+14.6,60,x+16.2,60)
    box(a,10,20,36,18,L("COOLING","散热",lang),L("air -> liquid (cold plates + CDU)\n~30-40C coolant loops","风冷 → 液冷(冷板+CDU)\n冷却液回路 ~30-40°C",lang),ec=BLUE,fs=11,sfs=8.5)
    box(a,54,20,36,18,L("POWER REALITY","电力现实",lang),L("US grid peak ~745GW*\nAI queue ~1TW of requests*","美国电网峰值 ~745GW*\nAI 并网申请 ~1TW*",lang),ec=RED,fs=11,sfs=8.5)
    a.text(50,10,L("*reused from the verified sector data (Module 08 sources)","*数字复用已验证板块数据(见模块 08 来源)",lang),color=SUB,fontsize=8,ha="center")
    f.tight_layout(); footer(f,OWN(lang,"SemiAnalysis (verified figures)")); return f

# ---------- pm09: industry map ----------
def pm09(lang):
    f,a=fig_ax(11,6.6)
    title(a,L("The industry map: who does what","行业地图:谁在做什么",lang),
          L("Margin pools differ because moats differ","利润池不同,因为护城河不同",lang))
    rows=[(L("Design tools & IP","设计工具与 IP",lang),"Cadence · Synopsys · Arm",L("~90% GM — oligopoly toll","毛利 ~90%——寡头过路费",lang),GREEN),
          (L("Chip designers (fabless)","芯片设计(fabless)",lang),"Nvidia · AMD · Broadcom",L("~55-75% GM — product moats","毛利 ~55-75%——产品护城河",lang),GREEN),
          (L("Foundry","晶圆代工",lang),"TSMC · Samsung · Intel",L("~50%+ GM at scale — process moat","规模化毛利 ~50%+——工艺护城河",lang),GREEN),
          (L("Memory (IDM)","存储(IDM)",lang),"SK Hynix · Samsung · Micron",L("cyclical: -20%~+60% GM","强周期:毛利 -20%~+60%",lang),BLUE),
          (L("Packaging/OSAT","封装/OSAT",lang),"ASE · Amkor (+TSMC CoWoS)",L("~10-25% GM — capacity business","毛利 ~10-25%——产能生意",lang),RED),
          (L("Equipment","设备",lang),"ASML · AMAT · LAM · KLA · TEL",L("~45-50% GM — monopoly niches","毛利 ~45-50%——细分垄断",lang),GREEN),
          (L("Clouds & AI labs","云与 AI 实验室",lang),"AWS/Azure/GCP · OpenAI/Anthropic",L("where the end demand forms","终端需求在这里形成",lang),BLUE)]
    for i,(t,names,s,c) in enumerate(rows):
        y=76-i*10.5
        box(a,4,y,30,8.5,t,fs=10)
        box(a,36,y,34,8.5,names,"",fc=PANEL2,ec=LINE,lc=INK,fs=8.5)
        box(a,72,y,25,8.5,s,"",fc=PANEL2,ec=c,lc=c,fs=7.6)
    f.tight_layout(); footer(f,OWN(lang,L("typical ranges from company filings","典型区间,来自各公司财报",lang))); return f

# ---------- pm10: metrics toolkit ----------
def pm10(lang):
    f,a=fig_ax(11,5.6)
    title(a,L("The investor's dashboard","投研仪表盘",lang),
          L("Six numbers that explain most AI-hardware debates","六个数字,解释大多数 AI 硬件争论",lang))
    mets=[("perf/TCO",L("the real purchase criterion","真实采购准绳",lang)),
          ("$/Mtok",L("inference economics","推理经济学",lang)),
          ("MFU",L("useful fraction of peak FLOPS","峰值算力的有效占比",lang)),
          (L("HBM GB/GPU","HBM 含量/GPU",lang),L("memory content growth","存储含量增长",lang)),
          (L("CoWoS wafers","CoWoS 产能",lang),L("the packaging gate","封装闸门",lang)),
          (L("$ /GPU-hr","GPU 时租",lang),L("supply-demand thermometer","供需温度计",lang))]
    for i,(t,s) in enumerate(mets):
        x=4+(i%3)*32; y=48-(i//3)*26
        box(a,x,y,29,18,t,s,fs=12,sfs=9)
    f.tight_layout(); footer(f,OWN(lang)); return f

FIGS={"00":pm00,"01":pm01,"02":pm02,"03":pm03,"04":pm04,"05":pm05,"06":pm06,"07":pm07,"08":pm08,"09":pm09,"10":pm10}

if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True)
    for mid,fn in FIGS.items():
        for lang in ("en","zh"):
            f=fn(lang)
            p=f"{OUT}/pm{mid}_{lang}.png"
            f.savefig(p,dpi=150,bbox_inches="tight",facecolor=BG); plt.close(f)
            print("wrote",p)
