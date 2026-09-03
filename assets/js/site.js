(function () {
  "use strict";

  var form = document.querySelector("[data-formspree-id]");
  if (!form) return;

  var formId = form.getAttribute("data-formspree-id") || "";
  var mailto = form.getAttribute("data-mailto") || "randy@lormand.com";

  if (formId && formId !== "YOUR_FORM_ID") return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var name = (form.querySelector('[name="name"]') || {}).value || "";
    var email = (form.querySelector('[name="email"]') || {}).value || "";
    var message = (form.querySelector('[name="message"]') || {}).value || "";
    var body =
      "From: " + name + " <" + email + ">\n\n" + message;
    var href =
      "mailto:" +
      encodeURIComponent(mailto) +
      "?subject=" +
      encodeURIComponent("lormand.com contact") +
      "&body=" +
      encodeURIComponent(body);
    window.location.href = href;
  });
})();
