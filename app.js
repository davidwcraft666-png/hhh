const curriculumData = [
  {
    week: "第 1 周",
    phase: "foundation",
    title: "AI 基础概念与工具环境",
    summary: "了解 AI 发展脉络，搭建 Python 与数据科学环境，掌握基础数学知识。",
    tags: ["AI 概念", "Python", "线性代数"]
  },
  {
    week: "第 2 周",
    phase: "foundation",
    title: "机器学习入门",
    summary: "从监督与无监督学习开始，完成第一个房价预测小项目。",
    tags: ["监督学习", "Scikit-learn", "回归"]
  },
  {
    week: "第 3 周",
    phase: "foundation",
    title: "深度学习核心模块",
    summary: "理解神经网络、反向传播与优化算法，实现手写数字识别。",
    tags: ["神经网络", "优化", "MNIST"]
  },
  {
    week: "第 4 周",
    phase: "project",
    title: "自然语言处理基础",
    summary: "使用 RNN 与 Transformer 构建文本分类与序列标注任务。",
    tags: ["NLP", "Transformer", "文本分类"]
  },
  {
    week: "第 5 周",
    phase: "project",
    title: "计算机视觉项目",
    summary: "基于卷积神经网络完成图像分类与目标检测实践。",
    tags: ["CNN", "目标检测", "数据增强"]
  },
  {
    week: "第 6 周",
    phase: "project",
    title: "智能推荐系统",
    summary: "理解协同过滤、召回排序策略，构建个性化推荐项目。",
    tags: ["推荐系统", "召回", "排序"]
  },
  {
    week: "第 7 周",
    phase: "project",
    title: "对话机器人实战",
    summary: "结合检索增强与大语言模型 API，打造企业级客服助手。",
    tags: ["LLM", "RAG", "对话系统"]
  },
  {
    week: "第 8 周",
    phase: "project",
    title: "AIGC 创意工作坊",
    summary: "探索图像生成、提示工程与多模态创作流程。",
    tags: ["扩散模型", "Prompt", "多模态"]
  },
  {
    week: "第 9 周",
    phase: "research",
    title: "模型优化与部署",
    summary: "学习模型压缩、蒸馏与部署策略，让模型走出实验室。",
    tags: ["蒸馏", "部署", "MLOps"]
  },
  {
    week: "第 10 周",
    phase: "research",
    title: "强化学习导论",
    summary: "掌握强化学习的核心概念与经典算法，完成迷宫智能体训练。",
    tags: ["强化学习", "策略梯度", "Gym"]
  },
  {
    week: "第 11 周",
    phase: "research",
    title: "大模型微调技巧",
    summary: "实践 LoRA、指令微调等技术，优化模型在特定场景的表现。",
    tags: ["LoRA", "指令微调", "评估"]
  },
  {
    week: "第 12 周",
    phase: "research",
    title: "毕业答辩与职业发展",
    summary: "准备项目展示、求职材料与面试演练，规划下一步职业路径。",
    tags: ["作品集", "面试", "职业规划"]
  }
];

const faqData = [
  {
    question: "没有编程基础可以学习吗？",
    answer:
      "可以。课程前 3 周从 Python 与数学基础讲起，还配有预科内容和学习小组，帮助你建立底层知识。"
  },
  {
    question: "课程需要投入多少时间？",
    answer:
      "建议每周投入 6-8 小时完成视频、练习与项目。也提供加速计划，适合希望快速转职的学员。"
  },
  {
    question: "完成课程后有哪些成果？",
    answer:
      "你将完成至少 3 个可展示的项目作品，并获得导师的个性化反馈与求职指导。"
  },
  {
    question: "是否提供企业内训或高校合作？",
    answer:
      "我们提供定制化方案，可根据企业或高校需求组合课程模块，欢迎通过预约表单联系我们。"
  }
];

const timelineContainer = document.getElementById("curriculumTimeline");
const filterButtons = document.querySelectorAll("[data-filter]");
const faqList = document.getElementById("faqList");
const currentYear = document.getElementById("currentYear");
const trialForm = document.getElementById("trialForm");
const formNote = document.getElementById("formNote");

function renderTimeline(data) {
  timelineContainer.innerHTML = "";

  data.forEach((item) => {
    const article = document.createElement("article");
    article.className = "timeline__item";
    article.dataset.phase = item.phase;

    article.innerHTML = `
      <div class="timeline__week">${item.week}</div>
      <div>
        <h3 class="timeline__title">${item.title}</h3>
        <p class="timeline__summary">${item.summary}</p>
        <div class="timeline__chips">
          ${item.tags.map((tag) => `<span class="chip">${tag}</span>`).join("")}
        </div>
      </div>
    `;

    timelineContainer.appendChild(article);
  });
}

function renderFaq() {
  faqData.forEach((item, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "faq__item";

    const questionButton = document.createElement("button");
    questionButton.className = "faq__question";
    questionButton.setAttribute("aria-expanded", "false");
    questionButton.setAttribute("aria-controls", `faq-panel-${index}`);
    questionButton.innerHTML = `
      <span>${item.question}</span>
      <span class="faq__icon">＋</span>
    `;

    const answer = document.createElement("div");
    answer.className = "faq__answer";
    answer.id = `faq-panel-${index}`;
    answer.setAttribute("role", "region");
    answer.setAttribute("aria-hidden", "true");
    answer.textContent = item.answer;

    questionButton.addEventListener("click", () => {
      const isOpen = questionButton.getAttribute("aria-expanded") === "true";
      questionButton.setAttribute("aria-expanded", String(!isOpen));
      answer.setAttribute("aria-hidden", String(isOpen));
      answer.classList.toggle("is-open", !isOpen);
      answer.style.maxHeight = !isOpen ? `${answer.scrollHeight}px` : "0";
      questionButton.querySelector(".faq__icon").textContent = !isOpen ? "－" : "＋";
    });

    wrapper.appendChild(questionButton);
    wrapper.appendChild(answer);
    faqList.appendChild(wrapper);
  });
}

function setupFilters() {
  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      filterButtons.forEach((btn) => btn.classList.remove("is-active"));
      button.classList.add("is-active");

      const filter = button.dataset.filter;
      if (filter === "all") {
        renderTimeline(curriculumData);
      } else {
        const filtered = curriculumData.filter((item) => item.phase === filter);
        renderTimeline(filtered);
      }
    });
  });
}

function validateForm() {
  let isValid = true;

  const fields = ["name", "email", "goal"];
  fields.forEach((fieldName) => {
    const field = trialForm.elements[fieldName];
    const errorEl = document.querySelector(`.form__error[data-for="${fieldName}"]`);

    if (!field.value.trim()) {
      errorEl.textContent = "请填写此字段";
      isValid = false;
      return;
    }

    if (fieldName === "email") {
      const emailPattern = /[^@\s]+@[^@\s]+\.[^@\s]+/;
      if (!emailPattern.test(field.value)) {
        errorEl.textContent = "请输入有效的邮箱地址";
        isValid = false;
        return;
      }
    }

    errorEl.textContent = "";
  });

  return isValid;
}

function handleFormSubmit(event) {
  event.preventDefault();
  formNote.textContent = "";

  if (!validateForm()) {
    formNote.textContent = "请先完善表单信息，我们才能为你安排体验课。";
    return;
  }

  const formData = Object.fromEntries(new FormData(trialForm));
  formNote.textContent = `${formData.name}，收到你的需求啦！我们会在 24 小时内发送邮件至 ${formData.email}。`;
  trialForm.reset();
}

function init() {
  renderTimeline(curriculumData);
  renderFaq();
  setupFilters();
  currentYear.textContent = new Date().getFullYear();
  trialForm.addEventListener("submit", handleFormSubmit);
}

init();
