// renderer.js
export function renderData(json) {
  const container = document.createElement('div');
  json.items.forEach(item => {
    const el = document.createElement('div');
    el.className = 'item';
    el.textContent = item.name;
    container.appendChild(el);
  });
  return container;
}