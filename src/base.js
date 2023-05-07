var key = "";

(() => {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll(".needs-validation");

  // Loop over them and prevent submission
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (!form.checkValidity()) {
          form.classList.add("was-validated");
        } else {
          form.classList.remove("was-validated");
          setKeyGlobal();
        }
      },
      false
    );
  });
})();

function setKeyGlobal() {
  var res = $.ajax({
    method: "POST",
    url: "/api/authorize",
    async: false,
  }).responseJSON;
  key = res.key;
}

$("#cscontactus").on("submit", (e) => {
  if (e.target.checkValidity()) {
    contactusCallback(e.target);
  }
});

function contactusCallback(form) {
  var cdata = {
    name: form[0].value,
    email: form[1].value,
    subject: form[2].value,
    message: form[3].value,
    key: key,
    token: e3(key),
  };
  $.ajax({
    method: "POST",
    url: "/api/contactus",
    data: JSON.stringify(cdata),
    contentType: "application/json",
    dataType: "json",
  }).done((msg) => {
    form[0].value = '';
    form[1].value = '';
    form[2].value = '';
    form[3].value = '';
    $("#contactusinfo").text(msg["message"]);
    $("#contactusinfo").removeClass("d-none");
    setTimeout((e) => {
        $("#contactusinfo").text("");
        $("#contactusinfo").addClass("d-none");
    }, 5000);
  });
}
