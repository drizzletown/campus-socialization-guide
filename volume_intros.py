"""Reader-facing bridges across the five chapters of each volume (not a new part of the SSCM model)."""
ZH=[
'大学生活中的社会化问题从来不是“我够不够合群”这么简单。第一辑先把对人的整体判断转化为对具体事务的分析：谁与谁发生联系、规则怎样运作、行动选择受到什么限制。五章依次回答社会化的含义、支持网络、状态与变化机制，以及面对实际事情时如何作出可修正的决定。',
'学业成长既需要独立建构知识，也需要课程规则、教师反馈和同伴合作。第二辑从培养方案走到日常学习，再讨论教学关系、小组任务和AI辅助；贯穿的核心问题是：学生究竟在什么条件下，能够把“完成一项课程要求”发展成可解释、可验证、可迁移的能力。',
'日常生活为专业学习提供真实的时间、空间和身体条件。宿舍约定、任务承诺、经济责任、身心支持与家庭协商彼此牵连；一种安排带来的便利，也可能占用另一种必要资源。第三辑关注合理生活的条件和边界，让学生认识到独立生活包含求助、预算、协商与承担适当责任。',
'在友谊和亲密关系中，人既需要联结，也需要保留独立判断和拒绝的权利。第四辑从结识朋友谈到差异、冲突、亲密承诺及同意与隐私。关系的质量无法通过认识多少人或相处多久来衡量，关键是期待能否说明、分歧能否处理、双方能否在安全条件下作出选择。',
'社团与班级公共事务让学生第一次直观地面对“有人负责”与“有人有权决定”之间的差别。第五辑围绕加入、组织、服务、公共表达和退出展开，强调成员自愿、规则透明、资源分配和连续交接。承担责任有价值，但责任必须与授权、支持和可解释的程序相配套。',
'科研、竞赛与实习把课堂知识带入有真实后果的专业活动。第六辑从寻找受监督的入门机会开始，逐步讨论指导关系、实验和数据伦理、竞赛合作及企业责任。培养专业能力不意味着自行承担所有风险，真正可靠的实践需要训练、复核、授权和对不确定性的及时报告。',
'数字平台改变信息传递方式，也改变个人的可见度和隐私风险。第七辑从群聊协作、数字身份与信息判断进入AI工具使用和网络保护。技术本身不能自动决定哪些关系值得建立、哪些消息可信或哪些行动合规；学生需要把核验、同意和责任重新带入数字环境。',
'大学后期的分岔路口有时看起来像一张单一排名表：专业、升学、职业、关系资源和创业都被比较高低。第八辑把这些路径还原成不同的目标、能力条件和生活成本。职业准备不等于迎合热门标准，而是通过信息、实践和反复选择，使未来路线逐渐具有现实依据。',
'面对权益争议与风险，普通协商、正式复核和紧急保护有完全不同的行动逻辑。第九辑讨论评价公平、骚扰与控制、经济纠纷、申诉程序和突发危机，强调事实记录、适当权限和安全优先。学生应学会寻找有实际处理权的支持，而无需通过个人交际弥补正式制度的缺位。',
'最后一辑将视线从一次成功的行动转向持续变化的生活。挫折、角色冲突、个人立场、跨环境迁移和毕业后的新关系，都要求我们反复核实条件、重新安排责任。成长不会在毕业当天完成，也不需要维持一条从不回头的轨迹；重要的是保留判断、学习和修正的能力。'
]
EN=[
'The first five chapters turn the vague question “Am I social enough?” into identifiable situations. They introduce relationships, accessible support, roles, actual contributions and informed choices, then explain how networks change. The goal is to understand a particular event before evaluating what a person should do.',
'Academic development combines independent understanding with institutional rules, feedback and cooperation. This part moves from the degree plan to learning strategies, communication with instructors, group work and AI assistance. Its connecting question is how completing university tasks can build knowledge and ability that students can explain and verify.',
'Everyday life supplies the time, space, money and health needed for study. Housing agreements, commitments, expenses, wellbeing and family relationships affect one another. This part examines how students can negotiate realistic arrangements while recognizing that independence includes legitimate support and responsible boundaries.',
'Friendship and intimacy involve both connection and the right to choose. These chapters trace how relationships begin, how difference and conflict are handled, and how consent, privacy and future commitments shape personal autonomy. The measure is not the size of a social circle but the ability to act respectfully and safely.',
'Student organizations expose the difference between being responsible and having authority. This part follows joining, organizing, volunteering, public deliberation and leaving a group. It asks whether participation is voluntary, procedures are transparent and responsibilities are matched by actual support and decision-making powers.',
'Research, competitions and internships place classroom knowledge in settings with real consequences. From supervised entry tasks to mentoring, research integrity, team competition and professional work, this part emphasizes training, authorization, evidence and knowing when a qualified person must review a decision.',
'Digital life changes how information travels and how people experience visibility, comparison and risk. This part connects group communication, digital identity, source evaluation, AI and online protection. Tools are useful, but they do not replace verification, permission or responsibility to others.',
'Choices about majors, graduate study, employment, professional contacts and entrepreneurship cannot be reduced to a prestige ranking. This part connects them through goals, preparation, resources, financial realities and revisable decisions. It invites students to build evidence before committing to a future path.',
'Ordinary disagreement, formal appeal and immediate danger require different kinds of action. These chapters address fairness, coercion, financial disputes, support channels and crisis response. Students need facts, appropriate institutional authority and safety protections, not pressure to resolve every problem privately.',
'The final part looks beyond individual successes to an evolving life. Failure, competing roles, independent judgment, moving between communities and graduation all require fresh information and revised commitments. Development has no universal finishing date; the durable skill is to learn and act when conditions change.'
]
assert len(ZH)==len(EN)==10
