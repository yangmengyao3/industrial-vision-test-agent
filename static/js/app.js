function addFlowStep(containerId) {
  const container = document.getElementById(containerId);
  if (!container) {
    return;
  }
  const input = document.createElement("input");
  input.name = "flow_steps";
  container.appendChild(input);
}

document.addEventListener("DOMContentLoaded", () => {});
