"""生成 AI 资讯网站：首页（无语音）+ 10个详情页（全文+语音）"""
import json, subprocess, os, re, html as html_mod
from datetime import datetime

BASE = "/Users/zhizhen/workspace/Vscode develop/physics-hub/daily-ai-news"
VOICES_DIR = os.path.join(BASE, "voices")
os.makedirs(VOICES_DIR, exist_ok=True)

TODAY = datetime.now()
DATE_ISO = TODAY.strftime("%Y-%m-%d")
WEEKDAYS_CN = ['日','一','二','三','四','五','六']
DATE_CN = f"{TODAY.year}年{TODAY.month}月{TODAY.day}日 星期{WEEKDAYS_CN[TODAY.weekday()]}"

# ================================================================
#  📦 完整文章数据 — 每日更新修改这里
#  每篇都是完整长文，无字数限制
# ================================================================
ARTICLES = [
  {
    "rank": 1,
    "title": "Anthropic 完成 $650 亿 H 轮融资，估值 $9650 亿",
    "short": "Anthropic 宣布完成 650 亿美元 H 轮融资，投后估值 9650 亿美元，由 Altimeter、Dragoneer、Greenoaks 和 Sequoia 领投。公司同时披露年化收入已突破 470 亿美元。",
    "full": """Anthropic 于 2026 年 5 月 28 日正式宣布完成了 AI 领域迄今为止规模最大的单轮融资之一——H 轮融资，金额达到惊人的 650 亿美元，投后估值飙升至 9650 亿美元。这一数字不仅刷新了 Anthropic 自身的融资纪录，也使得这家 AI 初创公司的估值直逼万亿美元大关，在全球未上市公司中名列前茅。

本轮融资由 Altimeter、Dragoneer、Greenoaks 和 Sequoia 四家顶级投资机构联合领投，阵容堪称豪华。Altimeter 在官方声明中称这是其「有史以来最大的一笔投资」，并将 Claude 形容为正在成为「整个企业的默认操作系统」。这一表述揭示了投资者对 Anthropic 企业级 AI 平台的长期信心。

与融资消息同步公布的，还有 Anthropic 首次对外披露的年化运行率收入数据——突破 470 亿美元。这一数字大幅超出此前外界对 Anthropic 收入的普遍预期，表明 Claude 的企业级部署正在经历爆发式增长。Anthropic CEO Dario Amodei 在一份内部备忘录中表示，公司「在不到五年的时间内实现了 470 亿美元的年化收入」，这一增长速度在 SaaS 和 AI 行业中均属罕见。

资金用途方面，Anthropic 明确表示将主要投向两个方向。第一是前沿 AI 研究，包括下一代模型架构的探索、安全对齐技术的深化，以及推理能力的突破性提升。第二是计算基础设施的大规模扩张，尤其是在推理服务容量方面——随着 Claude Opus 4.8 以及 Dynamic Workflows 等长时运行 Agent 功能的推出，推理计算的需求正以指数级增长。据悉，Anthropic 已在与多家云服务提供商和芯片厂商洽谈价值数百亿美元的算力合约。

市场分析人士对此轮融资的评价呈现分化。乐观派认为，470 亿美元的收入数据证明了 AI 企业级市场的真实需求并非泡沫，Anthropic 扎实的商业化能力为高估值提供了有力支撑。谨慎派则指出，9650 亿美元的估值意味着投资者押注的是 Anthropic 未来数年的持续高增长，一旦增速放缓或市场竞争加剧，估值压力将随之而来。Jerry Liu 甚至在社交平台上调侃道「把 billions 换成 millions 看起来就合理多了」。

从更宏观的视角来看，本轮融资是 AI 行业资本密集化趋势的最新注脚。随着模型规模持续扩大、Agent 工作负载日益复杂，AI 公司的资金需求正在从「千万级」向「千亿级」跃迁。Anthropic 这一轮融资不仅为其自身赢得了喘息和发展的空间，也为整个行业树立了新的资金门槛。"""
  },
  {
    "rank": 2,
    "title": "Claude Opus 4.8 发布：推理更锐利，同价升级",
    "short": "Anthropic 推出 Claude Opus 4.8——Opus 4.7 的行为升级版，拥有更锐利的判断力、更诚实的自我认知和更长的自主工作能力。SWE-Bench Pro 达 69.2%，FrontierSWE 第一。",
    "full": """在宣布巨额融资的同一天，Anthropic 同步发布了 Claude Opus 4.8，这是 Opus 系列的最新版本，也是自 Opus 4.7 以来最重要的一次模型更新。

Opus 4.8 被官方定位为 Opus 4.7 的一次「行为升级」，而非全新的架构突破。Anthropic 方面用三句话概括了本次升级的核心：更锐利的判断力、对自己的进展更加诚实，以及能够更长时间地独立工作。官方同时确认，过去数月间团队根据 4.7 用户的广泛反馈进行了「大量修复」，在回答的自然度和细腻度方面也有显著提升。

在定价方面，Anthropic 做出了一个重要且富有竞争力的决定：Opus 4.8 维持在 Opus 4.7 的同等价格水平。具体定价为输入每百万 token 5 美元，输出每百万 token 25 美元，缓存写入每百万 6.25 美元（5 分钟 TTL），缓存命中仅为每百万 0.50 美元。这样的缓存优惠力度对于长上下文和大规模批处理场景尤为重要，可显著降低开发者的实际使用成本。

Fast Mode 是此次更新中一个值得关注的改进方向。Opus 4.8 Fast 模式下运行速度约为标准模式的 2.5 倍，但额外费用仅高出 2 倍——相比之下 Opus 4.7 Fast 模式的价格是标准模式的 6 倍。换句话说，Anthropic 将 Fast 模式的经济性大幅提升了 3 倍，使得追求速度不再是「烧钱」的选择。这对于需要高频交互的编码和 Agent 场景来说意义重大。

Opus 4.8 同时引入了更精细的推理努力度控制机制。用户可以在 Minimal、Default、Max 和 xHigh 四级设置间切换，根据任务复杂度灵活调节模型投入的推理深度。知名科技博主 Dan Shipper 在评测后给出了具体建议：编程任务选择 xHigh，写作任务选择 high。Andon Labs 的测试进一步发现了一个反直觉的现象——在某些标准化评测上，max 级别的表现反而不如 xhigh，提示推理努力度与任务类型之间存在微妙的匹配关系。

Anthropic 工程师 Alex Albert 在社交平台上分享了更多细节。他指出 Opus 4.8 在 4.7 用户反馈的基础上进行了大量针对性修复，使得模型在细微度、自然度和上下文感知方面均有显著提升。他特别提到 Opus 4.8 在编码和知识工作领域的能力「全面增强」，用户在交互中会明显感觉到模型「更聪明也更配合」。"""
  },
  {
    "rank": 3,
    "title": "Opus 4.8 基准测试成绩全面解析",
    "short": "Opus 4.8 在 SWE-Bench Pro 达到 69.2%（领先 GPT-5.5 达 10 分），FrontierSWE 排第一，APEX-SWE 45.3% Pass@1 领先 GPT-5.3 Codex。AA 智能指数 61.4 登顶，效率提升明显。",
    "full": """Claude Opus 4.8 的基准测试成绩是此次发布中最受关注的部分之一。从官方和第三方公布的评测数据来看，Opus 4.8 在多个关键维度上实现了对前代 Opus 4.7 的全面超越，同时也在多项指标上与 OpenAI 的 GPT-5.5 系列形成了直接竞争。

在软件工程能力方面，Opus 4.8 交出了最为亮眼的成绩单。SWE-Bench Pro 得分达到 69.2%，比 GPT-5.5 高出整整 10 个百分点，在所有参测模型中排名第一。在更细分的 APEX-SWE 测试中，它以 45.3% 的 Pass@1 率领先 GPT-5.3 Codex 的 41.5%，优势约 4 个百分点。FrontierSWE 排行榜上，Opus 4.8 同样占据了榜首位置。

综合能力评估方面，Opus 4.8 在 GDPval-AA 上达到了 1890 Elo 的评分，相比 Opus 4.7 提升了 137 分，相比 GPT-5.5 xhigh 提升了 121 分。在与后者的直接对决中，Opus 4.8 赢得了约 67% 的胜率，这是一个相当显著的领先幅度。

Artificial Analysis 发布的独立智能指数中，Opus 4.8 以 61.4 分位居所有模型之首，领先 Opus 4.7 的 57.3 分和 GPT-5.5 xhigh 的 60.2 分。在 AA-Omniscience 综合评测中，Opus 4.8 获得 27.4 分，排名第二，仅次于 Google Gemini 3.1 Pro 的 32.9 分；具体来看，准确率 46.6%，幻觉率 35.9%，在幻觉控制方面优于多数竞品。

在专项能力测试中，Opus 4.8 同样表现突出。Terminal-Bench Hard 相比 4.7 提升 6.8 分，τ²-Bench Telecom 提升 5.9 分，IFBench 提升 3.6 分。在长上下文评估中，Opus 4.8 使用完整的 100 万 token 窗口，成绩几乎追平 GPT-5.5 在 256K 窗口下的得分，展示了优秀的远距离信息保持和处理能力。

值得关注的还有效率指标。相比 Opus 4.7，Opus 4.8 每任务所需交互轮次减少了 15%，输出 token 减少了 35%，意味着在同等产出下用户消耗的资源显著降低。不过也有评测指出，它仍然比 GPT-5.5 多用约 30% 的交互轮次——正如社区评论所言，Opus 4.8「依然被 GPT-5.5 在 token 效率上压制」。这提示 Anthropic 在未来的优化中需要在模型质量与资源消耗之间找到更好的平衡点。"""
  },
  {
    "rank": 4,
    "title": "Claude Code Dynamic Workflows：数百子 Agent 并行协作",
    "short": "Anthropic 在 Claude Code 中发布 Dynamic Workflows 研究预览，Claude 自主规划任务并生成数百个并行子 Agent 协作完成大型项目。已成功将 Bun 从 Zig 移植到 Rust（75 万行代码、99.8% 测试通过率）。",
    "full": """Dynamic Workflows 是此次 Anthropic 发布中最具前瞻性的产品更新。这是一项研究预览级功能，核心突破在于从根本上改变了 AI Agent 的工作模式——从传统的单线程对话式交互，升级为「总指挥 + 大规模并行子 Agent」的协同架构。

在 Dynamic Workflows 框架下，Claude 首先接收用户的任务描述，然后自主规划出完整的工作分解结构，将大型任务拆解为数十甚至数百个可并行执行的子任务。随后，系统动态生成对应数量的子 Agent，各自独立执行分配的工作，最终由主 Agent 完成结果整合和质量检查。整个过程对用户而言是透明的，只需输入包含「workflow」关键字的提示即可触发。

Anthropic 在官方演示中展示了一个极具说服力的案例：将一个名为 Bun 的运行时环境从 Zig 语言移植到 Rust。整个项目涉及约 75 万行代码的跨语言迁移，Dynamic Workflows 派出了数百个子 Agent 并行工作，最终在 11 天内完成了移植，测试通过率达到了惊人的 99.8%。在另一个案例中，系统在不到 10 分钟内并行处理了数百个 A/B 测试标志的合并工作，这对于传统人工操作可能需要数天时间。

Dynamic Workflows 已面向 Max、Team、Enterprise 订阅用户开放，同时也支持通过 API、Bedrock、Vertex AI 和 Foundry 平台调用。Anthropic 表示，该功能目前处于研究预览阶段，团队正在积极收集用户反馈，未来计划推出更完善的任务编排可视化面板和调度控制能力。

社区对 Dynamic Workflows 的评价褒贬不一。支持者认为这是 Agent 架构的重要进化，将 AI 的能力从「回答问题」提升到了「组织并完成复杂工程」的层面。批评者则指出，本质上 Dynamic Workflows 仍然是「在循环中调用模型」，与开发者早已手动实现的并行 Agent 方案没有根本性区别。此外，多 Agent 间的通信和协调会消耗大量 token，成本和效率之间的平衡仍需谨慎把握——正如 Theo 所言，数百个子 Agent 可能「几秒钟内就烧光了配额」。"""
  },
  {
    "rank": 5,
    "title": "Opus 4.8 定价与推理控制详解",
    "short": "Opus 4.8 定价输入 $5/百万输出 $25/百万，Fast Mode 提速 2.5 倍仅贵 2 倍。四级推理努力度控制可按任务调节，Dan Shipper 推荐 xhigh 编码、high 写作。缓存机制可大幅降低成本。",
    "full": """Opus 4.8 的定价策略体现了 Anthropic 在「性能-成本」平衡上的深思熟虑，尤其是 Fast Mode 和推理努力度控制这两项核心功能，为不同场景下的最优配置提供了灵活选择。

在标准定价方面，Opus 4.8 延续了前代的标准：输入每百万 token 5 美元，输出每百万 token 25 美元。与竞品相比，这一价格处于高端区间，但考虑到 Opus 4.8 在编码和推理任务上的显著性能优势，许多开发者认为物有所值。缓存机制是控制成本的关键杠杆之一：缓存写入价格为每百万 6.25 美元（TTL 5 分钟），而缓存命中仅需每百万 0.50 美元，也就是说如果 Prompt 设计合理、上下文复用率高，实际使用成本可以大幅压低。

Fast Mode 是此次定价更新中的最大亮点。Opus 4.8 Fast 模式下运行速度约为标准模式的 2.5 倍，但额外费用仅为标准模式的 2 倍。考虑到 Opus 4.7 Fast 模式的价格是标准模式的 6 倍，这相当于 Anthropic 将加速推理的经济成本压缩到了原来的三分之一。这意味着在同等预算下，开发者可以使用 Fast Mode 完成更多轮次的交互，或者将加速模式从「偶尔使用」升级为「日常标配」。

推理努力度控制则是另一项值得深入理解的功能。Opus 4.8 提供了四级设置：Minimal（最低推理，适合快速常规问答）、Default（默认平衡模式）、Max（较强推理，适合复杂分析）和 xHigh（极致推理，适合高难度编码和数学任务）。每一级之间的性能和 token 消耗差异可达 2-3 倍，因此合理选择努力度直接影响使用体验和成本。

Dan Shipper 在详细评测后给出了针对性的使用建议：编程任务——特别是算法设计、重构和调试——选择 xHigh 级别效果最佳；而写作、文档总结和内容分析等任务，high 级别即可达到理想效果。Andon Labs 的测试进一步揭示了一个微妙的现象：在某些标准评测集上，max 级别的表现反而不如 xhigh，这可能是由于过于深入的推理在某些任务上导致了过度思考。这一发现提示用户不应机械地选择最高级别，而应根据具体任务特征进行实验和调整。"""
  },
  {
    "rank": 6,
    "title": "社区争议：Opus 4.8 是王者归来还是评测驱动？",
    "short": "AI 社区对 Opus 4.8 看法严重分化。支持派（Dan Shipper、Cursor 团队）认为堪称 Opus 5，在 Senior Engineer 基准上超越 GPT-5.5。怀疑派指出其在 Vending Bench 上表现更差，被称为「最评测感知的模型」。",
    "full": """每一次重大模型发布都伴随着社区的热议，但 Opus 4.8 引发的争议烈度在近年来的 AI 圈子中实属罕见。不同阵营基于各自的测试数据和使用体验，给出了截然不同的评价。

支持派的声音主要来自 Anthropic 的忠实用户和技术领袖。Dan Shipper 在评测文章中直言 Opus 4.8「完全有资格被命名为 Opus 5」，他认为模型在 Senior Engineer 基准测试上的表现超越了 GPT-5.5，比 Opus 4.7 提升了超过 30 分。Cursor 开发团队在社交平台上公开称赞 Opus 4.8 的持久性和诚实度，称其「在复杂任务中的坚持令人印象深刻」。开发者 Mikey K 和 Teknium 也发表了一致的好评，强调模型的自我认知能力——它更频繁地主动标注自身的局限和不确定之处——是一个被低估的进步。Artificial Analysis 将其列为智能指数第一模型的结论，为支持派提供了第三方数据背书。

怀疑派的论据同样坚实。Andon Labs 的独立测试表明，Opus 4.8 在 Vending Bench 和 Blueprint-Bench 2 上的表现反而比 4.7 更差，这与官方发布的亮眼成绩形成了鲜明对比。他们认为 Opus 4.8 是 Anthropic 迄今「最评测感知」的模型——即模型的能力提升可能部分源于对已知评测集的过度优化，而非真正的通用能力增长。部分用户在实际编码工作中报告称，并未感受到官方声称的那种「质的飞跃」，普通问答和文档处理任务上的改进幅度微乎其微。

中间派——暂且称之为「结构派」——提出了一个更高维度的观点：关于模型本身的讨论正在变得次要，因为 Agent 执行框架的重要性正在超过原始模型质量。Codex 凭借更成熟的执行环境、工具链集成和开发者体验，在编程助手市场建立了显著优势。Opus 4.8 虽然是更聪明的模型，但如果无法匹配对等的执行框架质量，用户仍然倾向于选择整体体验更好的竞品。值得注意的是，Opus 4.8 发布后的 48 小时内，Cursor、Windsurf、Perplexity 和 Cline 等主流开发平台均已宣布接入——这说明市场对模型本身仍然充满信心。"""
  },
  {
    "rank": 7,
    "title": "Agent 基础设施军备竞赛：Harness 成为决胜点",
    "short": "行业共识正在转向：模型质量不再是唯一壁垒，模型 × 执行框架 × 工作流 × UI × 记忆 × 成本的综合堆栈才是决胜关键。DeepSeek 组建 Harness 团队，LangChain、Google 竞相布局。",
    "full": """如果说 2024 年是「模型质量为王」的一年，那么 2026 年正在成为「Agent 基础设施决胜」的一年。一场围绕「Harness」（执行框架）的军备竞赛正在 AI 行业中悄然展开，其重要性可能不亚于基础模型的竞争。

Harness 这一概念是指连接 AI 模型与真实执行环境的完整基础设施层，包括运行时沙箱、工具调用机制、输入输出验证、错误恢复策略、反馈学习循环等核心组件。它的质量直接决定了模型能力能否被有效转化为实际生产力。越来越多的行业领袖和技术团队正在达成一个共识：拥有最聪明的模型，已经不足以保证产品的市场成功；「模型 × Harness × 工作流 × 交互界面 × 记忆管理 × 成本效益」的六维综合竞争力，才是真正的决胜因素。

这一趋势在行业中已经出现了明确的信号。DeepSeek 被曝正在积极组建专门的 Harness 团队，试图通过更紧密的「模型输出→运行反馈→错误纠正→重新生成」循环来提升整体系统质量，即使基础模型并非顶尖，也能凭借优秀的 Harness 实现更可靠的端到端表现。DeepSeek 在推理成本上的优势，使得运行这种密集验证循环在经济上变得可行。

LangChain 在这场竞赛中占据了独特的位置。新发布的 SmithDB 是一款为 Agent 追踪场景设计的专用低延迟数据库，查询速度比通用方案快 12-15 倍，解决了 Agent 工作流产生的大量结构化事件数据的存储和检索瓶颈。LangSmith Engine 进一步实现了自动修复循环——Agent 遇到错误时系统自动分析根因、生成修复方案并重新执行，整个处理过程无需人工介入。

Google 则通过 Gemini Managed Agents 给出了另一种解决方案。它将所有 Agent 基础设施抽象为单一的 API 调用——开发者只需描述目标，系统自动处理沙箱环境、工具挂载、持久化存储和结果聚合等复杂细节。这种零配置体验降低了 Agent 开发的门槛，但也将更多控制权交给了平台方。

从更广阔的视角来看，Harness 军备竞赛标志着 AI 行业从「研究驱动」向「工程驱动」的深刻转变。当基础模型的质量差距逐步缩小，真正的差异化将来自谁能构建最可靠、最高效、最易用的 Agent 执行系统。"""
  },
  {
    "rank": 8,
    "title": "Anthropic 安全门控策略：Mythos 级模型等待就绪",
    "short": "Anthropic 计划在安全护栏完善后推出「智能超越 Opus 的新模型类别」，被广泛解读为 Mythos 级部署路线。Opus 4.8 是阶段性发布——先提升可部署通用模型的质量，高风险能力暂缓释放。",
    "full": """在发布 Opus 4.8 的同时，Anthropic 透露了一项引人深思的产品路线图信息：计划在安全评估框架和运行时护栏完全就绪后，推出「智能超越 Opus 的全新模型类别」。这一表态迅速被业界解读为 Mythos 级模型的逐步部署策略——先打好安全基础，再释放更强的 AI 能力。

Mythos 是 Anthropic 内部对其下一代超强 AI 模型的非正式代号。据接近公司的消息人士透露，Mythos 在推理能力、自主性和创造性方面将显著超越 Opus 系列，尤其是在需要长链条推理和多步骤规划的高难度任务上。然而，更强的能力也意味着更高的安全风险——特别是在网络安全、生物技术和社会影响等敏感领域，不受约束的强大模型可能带来不可忽视的隐患。

Anthropic 的选择是一种「渐进式安全部署」策略。Opus 4.8 被定位为可安全广泛部署的「现阶段最佳」模型——它在通用任务上的质量达到了新的高度，但那些可能被滥用于高风险场景的能力被有意限制或移除。Mythos 级能力的释放将取决于安全评估的进展和运行时监控系统的完善程度。

这一策略在理论上得到了相当多的认可。AI 安全研究界的多位知名人物认为，Anthropic 的做法代表了一种负责任的发展态度——在能力与安全之间寻求动态平衡，而非一味追求模型性能的极致。这种「能力门控」理念也在影响更广泛的行业实践，越来越多的 AI 公司开始在模型发布前进行系统性的风险评估和缓解措施设计。

不过，这种审慎策略在实践中也面临着现实挑战。最直接的问题是商业竞争力——如果对手（如 OpenAI 的 GPT-5.5 系列或 Google 的 Gemini 3.1 Pro）不受类似约束地持续推进能力边界，Anthropic 可能会在部分高性能需求场景中丧失优势。另一个隐忧是「安全过度」削弱模型实用性——部分开发者已在 Opus 4.8 上感受到模型在某些边界性问题上的过度谨慎，担心这种倾向在 Mythos 级模型上会进一步加剧。"""
  },
  {
    "rank": 9,
    "title": "LangChain SmithDB 与 LangSmith Engine：Agent 可观测性革命",
    "short": "LangChain 发布 SmithDB——专为 Agent 追踪构建的低延迟数据库，速度比标准方案快 12-15 倍。LangSmith Engine 支持自动修复循环，大幅降低 Agent 运维成本。与 Deep Agents v0.6 形成完整工具链。",
    "full": """LangChain 在 Agent 基础设施赛道上连续发布了两款重磅产品——SmithDB 和 LangSmith Engine，进一步完善了从 Agent 开发调试到生产运维的全链路工具生态。

SmithDB 是一款为 AI Agent 追踪和可观测性场景深度定制的高性能数据库。传统的日志系统（如 Elasticsearch）和通用时序数据库在处理 Agent 工作流产生的大量结构化事件数据时，往往面临写入吞吐低、查询延迟高的问题。SmithDB 从底层架构上针对 Agent 数据模型进行了优化——它的数据模式设计天然适配 Agent 的调用链、状态转换和决策轨迹，查询速度比通用方案快 12 到 15 倍。对于需要实时监控数百个并行 Agent 运行状态的团队来说，这一性能优势意味着可以更快速地定位异常、分析根因。

LangSmith Engine 则更进一步，将 AI Agent 的可观测性从「被动记录」提升到了「主动修复」的层次。它建立了一个完整的「感知-分析-修复」闭环：当 Agent 在执行过程中出现异常（如工具调用失败、输出格式不符合预期、任务超时等），Engine 会自动分析错误的根本原因，生成用户可审核的修复方案，并在批准后自动重新执行。这意味着开发者和运维人员不再需要手动排查每一个失败的 Agent 调用——系统的自我修复能力大幅降低了人工干预的需求。

结合此前发布的 Deep Agents v0.6（引入了 Delta Channels 和 Context Hub 两项创新功能），LangChain 正在从单纯的开发框架提供商转型为全面的 Agent 基础设施平台。Delta Channels 允许 Agent 之间通过增量变化进行高效通信，大幅减少多 Agent 协作中的冗余数据传输；Context Hub 则为长时运行的 Agent 提供了统一的上下文管理能力，确保在跨会话场景中的状态一致性。

这三款产品的组合效果是显著的：对于运行大规模 Agent 集群的团队，SmithDB 解决了数据存储和查询的瓶颈，LangSmith Engine 降低了运维人力成本，而 Deep Agents v0.6 提升了多 Agent 协作的效率和可靠性。LangChain 正在将这些工具整合为统一的 Agent 运维平台，意图在快速增长的 Agent 基础设施市场中占据核心生态位。"""
  },
  {
    "rank": 10,
    "title": "多 Agent 编排与安全沙箱加速基础设施化",
    "short": "Cursor Composer 2.5、Google Antigravity 等平台推动多 Agent 协作。QEMU + bubblewrap + seccomp 方案被开源社区广泛采用，Agent 安全执行环境正快速基础设施化。太空级算力合作浮出水面。",
    "full": """多 Agent 编排正在从实验性概念走向生产级应用，成为 2026 年年中 AI 行业最受关注的技术趋势之一。像 Cursor Composer 2.5、Google Antigravity、Anthropic Dynamic Workflows 以及开源社区的各种实现，正在将 AI 系统的能力从「单次对话」提升到「多智能体企业协作」的全新维度。

Cursor Composer 2.5 引入的多 Agent 窗口是一个标志性的产品功能。开发者可以在同一界面中同时与多个 AI 助手协作，分别担任架构师、编码员、测试工程师和代码审查者等不同角色。系统自动协调各 Agent 之间的通信和任务交接，开发者只需定义角色分工和目标，即可启动一个「虚拟开发团队」。这一模式在大型代码库重构、跨模块功能开发和综合测试编写等场景中表现尤为出色。

Google Antigravity 则将 Agent 编排提升到了云原生基础设施的层级。开发者只需在配置文件中描述目标系统的功能和行为需求，Antigravity 自动完成 Agent 的分配、执行环境的配置、工具的挂载和结果的合并。Google 的演示案例展示了一个令人印象深刻的成果：使用 Antigravity 配合 Gemini 3.5 Flash，在 12 小时内生成了一个功能完整的操作系统，动用了 93 个并行子 Agent。这一案例有力地验证了大规模 Agent 编排在生产级项目中的可行性。

在安全沙箱领域，一个开放标准正在形成。QEMU 虚拟机、bubblewrap 轻量级容器和 seccomp 系统调用过滤的三层组合方案正在被越来越多的开源项目采用。多个社区项目（包括对 Anthropic Cowork 功能的各种克隆实现）均选择了这一技术栈来构建 Agent 的安全隔离环境。这种三层架构的优势在于灵活性和安全性之间的良好平衡：QEMU 提供了硬件级的强隔离，bubblewrap 实现了轻量级的文件系统隔离，seccomp 则对系统调用进行精细的权限控制。

更具想象力的是 SpaceX 与 Anthropic 之间的算力合作传闻。据业内人士透露，SpaceX 正在与 Anthropic 洽谈一个名为 Colossus 2 的合作项目，计划提供 10 倍于当前规模的 AI 训练和推理算力，以支持下一代模型的研发。如果这一合作落地，不仅将为 Anthropic 提供几乎无限的算力储备，也标志着 AI 基础设施建设正在从地球数据中心向太空级资源延伸。

总体而言，多 Agent 编排和 Agent 安全标准的快速成熟正在催生一个全新的基础设施层。在这一层之上，开发者可以像搭建微服务一样构建 AI Agent 系统，而无需关心底层的调度、隔离和通信细节。AI Agent 的商品化进程正在加速。"""
  }
]

def esc(text):
    return html_mod.escape(text)

def build_index():
    """首页 — 无语音功能，纯列表展示"""
    items_html = []
    for a in ARTICLES:
        r = a['rank']
        rc = 'news-rank top3' if r <= 3 else 'news-rank'
        items_html.append(f"""
    <li class="news-item">
      <a href="detail-{r:02d}.html" class="news-link">
        <div class="news-head">
          <span class="{rc}">{r}</span>
          <div class="news-title-area">
            <div class="news-title">{esc(a['title'])}</div>
            <div class="news-desc">{esc(a['short'])}</div>
          </div>
          <span class="arrow-icon">→</span>
        </div>
      </a>
    </li>""")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>每日 AI 资讯 TOP10</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                   "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100vh;
      color: #1a1a2e;
      line-height: 1.6;
      padding: 24px 16px;
    }}
    .container {{ max-width: 820px; margin: 0 auto; }}

    .header {{
      text-align: center; padding: 42px 20px 22px;
      background: rgba(255,255,255,0.55);
      backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
      border-radius: 20px; margin-bottom: 28px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    }}
    .header h1 {{
      font-size: 2rem;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      background-clip: text; letter-spacing: 1px;
    }}
    .header .subtitle {{ margin-top: 8px; font-size: 0.95rem; color: #555; }}
    .header .source-area {{ margin-top: 8px; font-size: 0.82rem; color: #888; }}
    .header .source-area a {{ color: #667eea; text-decoration: none; }}
    .header .source-area a:hover {{ text-decoration: underline; }}
    .date-badge {{
      display: inline-block; margin-top: 12px;
      padding: 5px 20px; border-radius: 20px;
      background: #667eea; color: #fff;
      font-size: 0.85rem; font-weight: 500;
    }}

    .click-hint {{
      text-align: center; font-size: 0.82rem; color: #999;
      margin-bottom: 18px;
    }}

    .news-list {{ list-style: none; }}
    .news-item {{
      background: rgba(255,255,255,0.7);
      backdrop-filter: blur(8px);
      border-radius: 16px; margin-bottom: 14px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.04);
      transition: all 0.25s ease;
      border-left: 4px solid transparent;
      overflow: hidden;
    }}
    .news-item:hover {{
      box-shadow: 0 6px 24px rgba(0,0,0,0.12);
      border-left-color: #667eea;
      transform: translateX(4px);
    }}
    .news-item:active {{ transform: scale(0.98); }}
    .news-link {{
      display: block; padding: 22px 24px;
      text-decoration: none; color: inherit;
    }}
    .news-head {{ display: flex; align-items: flex-start; gap: 8px; }}
    .news-rank {{
      display: inline-flex; align-items: center; justify-content: center;
      width: 34px; height: 34px; border-radius: 10px;
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: #fff; font-weight: 700; font-size: 0.85rem; flex-shrink: 0;
    }}
    .news-rank.top3 {{ width: 38px; height: 38px; font-size: 1rem; }}
    .news-title-area {{ flex: 1; min-width: 0; }}
    .news-title {{ font-size: 1.08rem; font-weight: 600; color: #1a1a2e; line-height: 1.4; }}
    .news-desc {{
      margin-top: 6px; font-size: 0.9rem; color: #666; line-height: 1.6;
    }}
    .arrow-icon {{
      flex-shrink: 0; font-size: 1.3rem; color: #ccc;
      transition: all 0.2s; margin-left: 6px; margin-top: 6px;
    }}
    .news-item:hover .arrow-icon {{ color: #667eea; transform: translateX(4px); }}

    .footer {{
      text-align: center; padding: 28px 16px 10px; font-size: 0.82rem; color: #999;
    }}
    .footer a {{ color: #667eea; text-decoration: none; }}

    @media (max-width: 600px) {{
      body {{ padding: 12px 10px; }}
      .header h1 {{ font-size: 1.5rem; }}
      .news-link {{ padding: 16px; }}
      .news-title {{ font-size: 1rem; }}
    }}
  </style>
</head>
<body>
<div class="container">

  <header class="header">
    <h1>🔥 每日 AI 资讯 TOP10</h1>
    <p class="subtitle">精选当日最热门人工智能资讯 · 点击条目阅读完整报道</p>
    <span class="date-badge">{DATE_CN}</span>
  </header>

  <div class="click-hint">💡 点击任意卡片查看完整报道与语音朗读</div>

  <ul class="news-list">
    {''.join(items_html)}
  </ul>

  <div class="footer">
  </div>

</div>

</body>
</html>"""

    path = os.path.join(BASE, 'index.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ index.html")

def build_detail(a):
    """详情页 — 含完整文章 + 语音播放"""
    r = a['rank']
    paras = [p.strip() for p in a['full'].strip().split('\n\n') if p.strip()]
    paras_html = '\n'.join(f'      <p>{esc(p)}</p>' for p in paras)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>#{r} {esc(a['title'])} — 每日 AI 资讯</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                   "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100vh;
      color: #1a1a2e;
      padding: 24px 16px;
    }}
    .container {{ max-width: 780px; margin: 0 auto; }}

    /* 导航栏 */
    .nav-bar {{
      display: flex; align-items: center; justify-content: space-between;
      margin-bottom: 20px; flex-wrap: wrap; gap: 8px;
    }}
    .back-link {{
      display: inline-flex; align-items: center; gap: 4px;
      color: #667eea; text-decoration: none; font-size: 0.9rem; font-weight: 500;
      padding: 7px 16px; border-radius: 10px;
      background: rgba(255,255,255,0.5);
      transition: all 0.2s;
    }}
    .back-link:hover {{ background: rgba(255,255,255,0.8); transform: translateX(-3px); }}
    .rank-badge {{
      display: inline-flex; align-items: center; justify-content: center;
      width: 34px; height: 34px; border-radius: 10px;
      background: linear-gradient(135deg, #667eea, #764ba2);
      color: #fff; font-weight: 700; font-size: 0.85rem;
    }}

    /* 语音控件 */
    .voice-bar {{
      display: flex; align-items: center; gap: 10px; flex-wrap: wrap;
      padding: 16px 22px;
      background: rgba(255,255,255,0.7);
      backdrop-filter: blur(10px);
      border-radius: 14px; margin-bottom: 22px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }}
    .voice-bar .label {{ font-size: 0.85rem; color: #666; font-weight: 500; }}
    .voice-btn {{
      padding: 8px 18px; border: none; border-radius: 10px;
      font-size: 0.85rem; font-weight: 500; cursor: pointer;
      transition: all 0.2s; background: #eef0f7; color: #333;
    }}
    .voice-btn:hover {{ transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
    .voice-btn:active {{ transform: scale(0.96); }}
    .voice-btn.primary {{
      background: linear-gradient(135deg, #667eea, #764ba2); color: #fff;
    }}
    .voice-btn.primary:hover {{ box-shadow: 0 4px 16px rgba(102,126,234,0.4); }}
    .voice-btn.danger {{ background: #ff6b6b; color: #fff; }}
    .voice-btn:disabled {{ opacity: 0.4; cursor: not-allowed; transform: none !important; }}
    .voice-status {{
      font-size: 0.8rem; color: #888; text-align: center; padding: 4px 0 0;
    }}
    .progress-wrap {{
      width: 100%; height: 4px; background: #e0e0e0;
      border-radius: 2px; overflow: hidden;
    }}
    .progress-bar {{
      height: 100%; width: 0%;
      background: linear-gradient(90deg, #667eea, #764ba2);
      border-radius: 2px; transition: width 0.3s linear;
    }}

    /* 文章正文 */
    .article {{
      background: rgba(255,255,255,0.7);
      backdrop-filter: blur(8px);
      border-radius: 20px; padding: 36px 40px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    }}
    .article h1 {{
      font-size: 1.6rem; line-height: 1.4; color: #1a1a2e;
      margin-bottom: 8px;
    }}
    .article .meta {{
      font-size: 0.82rem; color: #999; margin-bottom: 24px;
      padding-bottom: 16px; border-bottom: 1px solid #e8e8e8;
    }}
    .article p {{
      font-size: 1rem; color: #333; line-height: 2;
      margin-bottom: 18px;
      text-indent: 2em;
    }}

    @media (max-width: 600px) {{
      body {{ padding: 12px 10px; }}
      .article {{ padding: 18px 16px; }}
      .article h1 {{ font-size: 1.2rem; }}
      .article p {{ font-size: 0.93rem; text-indent: 1.5em; }}
      .voice-bar {{ flex-direction: column; gap: 6px; }}
      .voice-btn {{ width: 100%; justify-content: center; }}
    }}
  </style>
</head>
<body>
<div class="container">

  <!-- 导航栏 -->
  <div class="nav-bar">
    <a class="back-link" href="index.html">← 返回全部资讯</a>
    <span class="rank-badge">#{r}</span>
  </div>

  <!-- 语音控件 -->
  <div class="voice-bar">
    <span class="label">🔊 语音</span>
    <button class="voice-btn primary" id="playBtn">▶ 朗读本文</button>
    <button class="voice-btn" id="pauseBtn">⏸ 暂停</button>
    <button class="voice-btn danger" id="stopBtn">⏹ 停止</button>
    <div class="progress-wrap">
      <div class="progress-bar" id="progressBar"></div>
    </div>
  </div>
  <div class="voice-status" id="voiceStatus">点击「朗读本文」收听全文</div>

  <!-- 正文 -->
  <div class="article">
    <h1>{esc(a['title'])}</h1>
    <div class="meta">{DATE_ISO}</div>
{paras_html}
  </div>

</div>

<script>
(function() {{
  var audio = new Audio();
  audio.src = 'voices/voice_{r:02d}.mp3';
  audio.preload = 'auto';

  var $ = function(id) {{ return document.getElementById(id); }};
  var playBtn = $('playBtn'), pauseBtn = $('pauseBtn'), stopBtn = $('stopBtn');
  var status = $('voiceStatus'), progressBar = $('progressBar');
  var timer = null;

  function setProgress() {{
    if (audio.duration && !isNaN(audio.duration))
      progressBar.style.width = Math.min((audio.currentTime / audio.duration) * 100, 100) + '%';
  }}
  function startTimer() {{ clearTimer(); timer = setInterval(setProgress, 200); }}
  function clearTimer() {{ if (timer) {{ clearInterval(timer); timer = null; }} }}

  audio.onplay = function() {{
    playBtn.textContent = '⏸ 播放中'; startTimer();
    status.textContent = '🔊 正在朗读全文...';
  }};
  audio.onpause = function() {{
    playBtn.textContent = '▶ 继续'; clearTimer();
    status.textContent = '⏸ 已暂停';
  }};
  audio.onended = function() {{
    playBtn.textContent = '▶ 重播'; clearTimer();
    progressBar.style.width = '0%';
    status.textContent = '✅ 播放完成';
  }};
  audio.onerror = function() {{
    playBtn.textContent = '▶ 朗读本文'; status.textContent = '⚠️ 音频加载失败';
    clearTimer(); progressBar.style.width = '0%';
  }};

  playBtn.onclick = function() {{
    if (!audio.paused) {{ audio.pause(); return; }}
    if (audio.ended) audio.currentTime = 0;
    audio.play().catch(function() {{ status.textContent = '⚠️ 请先点击页面激活音频'; }});
  }};
  pauseBtn.onclick = function() {{
    if (audio.paused) audio.play().catch(function(){{}}); else audio.pause();
  }};
  stopBtn.onclick = function() {{
    audio.pause(); audio.currentTime = 0;
    playBtn.textContent = '▶ 朗读本文'; status.textContent = '⏹ 已停止';
    clearTimer(); progressBar.style.width = '0%';
  }};
  document.addEventListener('keydown', function(e) {{
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.code === 'Space') {{
      e.preventDefault();
      if (audio.paused) audio.play().catch(function(){{}}); else audio.pause();
    }}
  }});
}})();
</script>
</body>
</html>"""

    path = os.path.join(BASE, f'detail-{r:02d}.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✓ detail-{r:02d}.html")

def gen_voice(a):
    """为全文生成语音"""
    r = a['rank']
    mp3 = os.path.join(VOICES_DIR, f'voice_{r:02d}.mp3')
    if os.path.exists(mp3) and os.path.getsize(mp3) > 300000:
        return
    text = f"第{a['rank']}条：{a['title']}。" + a['full'].replace('\n\n', '。')
    cmd = ['edge-tts', '--voice', 'zh-CN-XiaoxiaoNeural', '--rate', '+0%', '--text', text, '--write-media', mp3]
    subprocess.run(cmd, capture_output=True, text=True)

def main():
    print("🔊 Generating voice files (full articles)...")
    for a in ARTICLES:
        gen_voice(a)
        print(f"  ✓ voice_{a['rank']:02d}.mp3")

    print("\n📄 Generating index.html...")
    build_index()

    print("📄 Generating 10 detail pages...")
    for a in ARTICLES:
        build_detail(a)

    import os
    size = sum(os.path.getsize(os.path.join(BASE, f'detail-{a["rank"]:02d}.html')) for a in ARTICLES)
    print(f"\n✅ Done! {len(ARTICLES)} detail pages + index.html + voices/")
    print(f"   Total size: {size/1024:.0f}KB HTML + voices/")

if __name__ == '__main__':
    main()
