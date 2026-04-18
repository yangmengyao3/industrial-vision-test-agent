function addFlowStep(containerId) {
  const container = document.getElementById(containerId);
  if (!container) {
    return;
  }
  const item = document.createElement("li");
  item.textContent = "新增流程步骤";
  container.appendChild(item);
}

function addParameterRow() {
  const table = document.querySelector(".parameter-table");
  if (!table) {
    return;
  }
  const row = document.createElement("div");
  row.className = "table-row";
  row.innerHTML = '<input name="parameter_names" placeholder="参数名" /><input name="parameter_ranges" placeholder="取值范围" /><input name="parameter_descriptions" placeholder="说明" />';
  table.appendChild(row);
}

async function submitWorkbenchForm(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const targetId = form.dataset.resultTarget;
  const target = document.getElementById(targetId);
  const formData = new FormData(form);
  const response = await fetch(form.action, {
    method: form.method,
    body: formData,
  });
  const html = await response.text();
  if (target) {
    target.innerHTML = html;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const dock = document.getElementById("result-dock");
  if (dock && dock.textContent.includes("结果预览区")) {
    dock.innerHTML = "<div class='panel-card'><h2>结果预览区</h2><p>提交生成或优化动作后，这里会显示测试点、用例和覆盖分析。</p></div>";
  }

  document.querySelectorAll("form[data-result-target]").forEach((form) => {
    form.addEventListener("submit", submitWorkbenchForm);
  });
});
