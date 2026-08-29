/**
 * Simple toast notification. Call showToast("message") from any page.
 * Requires nothing special in the HTML - it creates its own element.
 */
function showToast(message) {
  let el = document.getElementById("wb-toast");
  if (!el) {
    el = document.createElement("div");
    el.id = "wb-toast";
    el.className = "wb-toast";
    document.body.appendChild(el);
  }
  el.textContent = message;
  el.style.display = "flex";

  clearTimeout(el._timer);
  el._timer = setTimeout(() => { el.style.display = "none"; }, 2600);
}
