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
        }
      },
      false
    );
  });
})();

function makeApiCall(url, data, auth, callback) {
  var data_copy = Object.assign({}, data);
  if (auth) {
    var res = $.ajax({
      method: "POST",
      url: "/api/authorize",
      async: false,
    }).responseJSON;
    data_copy["key"] = res.key;
    data_copy["token"] = e3(res.key);
  }
  $.ajax({
    method: "POST",
    url: url,
    data: JSON.stringify(data_copy),
    contentType: "application/json",
    dataType: "json",
  }).done((msg) => {callback(msg);});
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
  };
  makeApiCall("/api/contactus", cdata, true, 
    (msg) => {
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
    }
  );
}
