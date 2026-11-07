// Estimate form -> WhatsApp.
//
// There is no server and no mailbox: the form composes the enquiry and opens
// the Plinth WhatsApp chat with it already typed. Nothing is stored, nothing
// is emailed, and the lead arrives where the phone already is.
(function () {
  var form = document.getElementById("estimate-form");
  if (!form) return;

  var WHATSAPP = "27661505770";

  function val(id) {
    var el = document.getElementById(id);
    return el ? String(el.value || "").trim() : "";
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    var lines = ["Hi Plinth, I would like a quote.", "Name: " + val("name")];
    if (val("phone")) lines.push("Phone: " + val("phone"));
    if (val("email")) lines.push("Email: " + val("email"));
    if (val("suburb")) lines.push("Suburb: " + val("suburb"));
    if (val("service")) lines.push("Service: " + val("service"));
    if (val("details")) lines.push("Details: " + val("details"));

    var url = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(lines.join("\n"));

    // the confirmation replaces the button, so a second tap cannot double-send
    var button = form.querySelector("button[type=submit]");
    if (button) {
      button.disabled = true;
      button.textContent = "Opening WhatsApp...";
    }

    var note = form.querySelector(".wa-note");
    if (note) {
      note.innerHTML =
        'Your enquiry is ready in WhatsApp. If it did not open, ' +
        '<a href="' + url + '" target="_blank" rel="noopener">tap here to send it</a>.';
      note.className = "wa-note wa-note--ready";
    }

    window.open(url, "_blank");
  });
})();
