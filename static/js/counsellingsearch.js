var counsellingData = {};
var counsellingDataSelect2 = {};

// Form validation code
(() => {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = $(".needs-validation");
  const acckey = $("#api-acc");

  // Loop over them and prevent submission
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        event.preventDefault();
        event.stopPropagation();
        if (isFormValid(form, acckey)) {
          form.classList.remove("was-validated");
          formCallback(acckey);
        } else {
          form.classList.add("was-validated");
        }
      },
      false
    );
  });
})();

function isFormValid(form, accKey) {
  if (form.checkValidity()) {
    // check if access key valid
    var res = $.ajax({
      method: "POST",
      url: "/api/authorize",
      data: JSON.stringify({ acckey: accKey.val() }),
      contentType: "application/json",
      dataType: "json",
      async: false,
    }).responseJSON;

    if (res.isValid) {
      accKey.removeClass("is-invalid");
      return true;
    } else {
      accKey.addClass("is-invalid");
      return false;
    }
  } else {
    return false;
  }
}

function formCallback(acckey) {
  // get form data
  var instts = Array();
  var insts = Array();
  var apns = Array();
  var quotas = Array();
  var sts = Array();
  var gens = Array();

  $("#inst-type")
    .select2("data")
    .forEach((curval, index) => {
      instts.push(curval.text);
    });
  $("#inst-name")
    .select2("data")
    .forEach((curval, index) => {
      insts.push(curval.text);
    });
  $("#apname")
    .select2("data")
    .forEach((curval, index) => {
      apns.push(curval.text);
    });
  $("#quota")
    .select2("data")
    .forEach((curval, index) => {
      quotas.push(curval.text);
    });
  $("#seat-type")
    .select2("data")
    .forEach((curval, index) => {
      sts.push(curval.text);
    });
  $("#gender")
    .select2("data")
    .forEach((curval, index) => {
      gens.push(curval.text);
    });

  var fdata = {
    counsellingname: counsellingData.counselling,
    roundNo: parseInt($("#RoundNo").select2("data")[0].text),
    rank: parseInt($("#rank").val()),
    rankBuff: parseInt($("#rank-buff").val()),
    instts: instts,
    insts: insts,
    apns: apns,
    quotas: quotas,
    sts: sts,
    gens: gens,
    acckey: acckey.val(),
  };
  // update data on table
  $.ajax({
    method: "POST",
    url: "/api/counsellingdata",
    data: JSON.stringify(fdata),
    contentType: "application/json",
    dataType: "json",
  }).done((msg) => {
    var tabledata = Array();
    msg.data.forEach((curval, index) => {
      tabledata.push({
        instt: curval["Institute Type"],
        inst: curval["Institute"],
        apn: curval["Academic Program Name"],
        quota: curval["Quota"],
        st: curval["Seat Type"],
        gender: curval["Gender"],
        or: curval["Opening Rank"],
        cr: curval["Closing Rank"],
      });
    });
    $("#table").bootstrapTable("load", tabledata);
  });
}

function updateSelectData(element, data) {
  if (typeof element === "string" && Array.isArray(data)) {
    var e = $(element);
    if (e.length && e.hasClass("select2-hidden-accessible")) {
      var config = JSON.parse(JSON.stringify(e.data("select2").options.options));
      config.data = data;
      e.empty().select2("destroy").select2(config);
      e.val(null).trigger("change.select2");
    } else {
      console.error("Element does not exist or not an select2 element");
    }
  } else {
    console.error("Invalid argument types");
  }
}

$(".select2-select-single").select2({
  theme: "bootstrap-5",
  width: $(this).data("width")
    ? $(this).data("width")
    : $(this).hasClass("w-100")
    ? "100%"
    : "style",
  placeholder: $(this).data("placeholder"),
  closeOnSelect: true,
  allowClear: true,
});

$(".select2-select-multiple").select2({
  theme: "bootstrap-5",
  width: $(this).data("width")
    ? $(this).data("width")
    : $(this).hasClass("w-100")
    ? "100%"
    : "style",
  placeholder: $(this).data("placeholder"),
  closeOnSelect: false,
  multiple: true,
  allowClear: false,
});

$("#table").bootstrapTable({
  height: 750,
  pagination: true,
  paginationPreText: "Previous",
  paginationNextText: "Next",
  search: true,
  searchAccentNeutralise: true,
  trimOnSearch: false,
  showColumns: true,
  showColumnsToggleAll: true,
  showPaginationSwitch: true,
  advancedSearch: true,
  idTable: "advancedTable",
  showPrint: true,
  showExport: true,
  exportDataType: "all",
  exportTypes: ["pdf"],
  exportOptions: {
    fileName: 'SearchResults',
    jspdf: {
      autotable: {
        styles: {
          overflow: 'linebreak',
          lineWidth: 1,
          cellPadding: 5,
          fontSize: 10,
          halign: "center",
          cellWidth: "wrap",
          columnWidth: 'auto'
        },
        headerStyles: {
          halign: "center",
        },
        theme: 'grid',
      }
    }
  },
  data: [],
});

// Form events - counselling name
$("#CounsellingName").on("select2:select", function (e) {
  $.ajax({
    method: "POST",
    url: "/api/counsellinginfo",
    data: JSON.stringify({ counsellingname: e.params.data.text }),
    contentType: "application/json",
    dataType: "json",
  }).done((msg) => {
    counsellingData = msg;
    var s2data_round = Array();
    var s2data_instt = Array();
    var s2data_inst = Array();
    var s2data_apn = Array();
    var s2data_quota = Array();
    var s2data_st = Array();
    var s2data_gen = Array();

    Array.from({ length: msg.Rounds }, (_, i) => i + 1).forEach((curval, index) => {
      s2data_round.push({
        id: index,
        text: curval,
      });
    });
    msg["Institute Types"].forEach((curval, index) => {
      s2data_instt.push({
        id: index,
        text: curval,
      });
    });
    msg["Institutes"].forEach((curval, index) => {
      s2data_inst.push({
        id: index,
        text: curval,
      });
    });
    msg["Academic Program Names"].forEach((curval, index) => {
      s2data_apn.push({
        id: index,
        text: curval,
      });
    });
    msg["Quotas"].forEach((curval, index) => {
      s2data_quota.push({
        id: index,
        text: curval,
      });
    });
    msg["Seat Types"].forEach((curval, index) => {
      s2data_st.push({
        id: index,
        text: curval,
      });
    });
    msg["Genders"].forEach((curval, index) => {
      s2data_gen.push({
        id: index,
        text: curval,
      });
    });

    counsellingDataSelect2 = {
      s2data_round: s2data_round,
      s2data_instt: s2data_instt,
      s2data_inst: s2data_inst,
      s2data_apn: s2data_apn,
      s2data_quota: s2data_quota,
      s2data_st: s2data_st,
      s2data_gen: s2data_gen,
    };

    updateSelectData("#RoundNo", s2data_round);
    updateSelectData("#inst-type", s2data_instt);
    updateSelectData("#inst-name", s2data_inst);
    updateSelectData("#apname", s2data_apn);
    updateSelectData("#quota", s2data_quota);
    updateSelectData("#seat-type", s2data_st);
    updateSelectData("#gender", s2data_gen);
    $(".stage1").prop("disabled", false);
    $("#cmessage").text("NOTE: " + msg["message"]);
    $("#cmessage").removeClass("d-none");
  });
});

$("#CounsellingName").on("select2:unselect", function (e) {
  updateSelectData("#RoundNo", []);
  updateSelectData("#inst-type", []);
  updateSelectData("#inst-name", []);
  updateSelectData("#apname", []);
  updateSelectData("#quota", []);
  updateSelectData("#seat-type", []);
  updateSelectData("#gender", []);
  $(".stage1").prop("disabled", true);
  $(".stage2").prop("disabled", true);
  $("#cmessage").text("");
  $("#cmessage").addClass("d-none");
});

// Form events - round no
$("#RoundNo").on("select2:select", function (e) {
  $(".stage2").prop("disabled", false);
});

$("#RoundNo").on("select2:unselect", function (e) {
  $(".stage2").prop("disabled", true);
});

// Form events - institute type
$("#inst-type").on("change", function (e) {
  var data_instts = Array();

  $("#inst-type")
    .select2("data")
    .forEach((curval, index) => {
      data_instts.push(curval.text);
    });
  if (data_instts.length != 0) {
    $.ajax({
      method: "POST",
      url: "/api/institutetypefilter",
      data: JSON.stringify({
        counsellingname: counsellingData.counselling,
        roundNo: parseInt($("#RoundNo").select2("data")[0].text),
        instts: data_instts,
      }),
      contentType: "application/json",
      dataType: "json",
    }).done((msg) => {
      var s2data_inst = Array();
      var s2data_apn = Array();

      msg["Institutes"].forEach((curval, index) => {
        s2data_inst.push({
          id: index,
          text: curval,
        });
      });
      msg["Academic Program Names"].forEach((curval, index) => {
        s2data_apn.push({
          id: index,
          text: curval,
        });
      });

      updateSelectData("#inst-name", s2data_inst);
      updateSelectData("#apname", s2data_apn);
    });
  } else {
    updateSelectData("#inst-name", counsellingDataSelect2.s2data_inst);
    updateSelectData("#apname", counsellingDataSelect2.s2data_apn);
  }
});

// Form events - institute type
$("#inst-name").on("change", function (e) {
  var data_instts = Array();
  var data_insts = Array();

  $("#inst-type")
    .select2("data")
    .forEach((curval, index) => {
      data_instts.push(curval.text);
    });

  $("#inst-name")
    .select2("data")
    .forEach((curval, index) => {
      data_insts.push(curval.text);
    });

  if (!(data_insts.length === 0 && data_instts.length === 0)) {
    $.ajax({
      method: "POST",
      url: "/api/institutefilter",
      data: JSON.stringify({
        counsellingname: counsellingData.counselling,
        roundNo: parseInt($("#RoundNo").select2("data")[0].text),
        instts: data_instts,
        insts: data_insts,
      }),
      contentType: "application/json",
      dataType: "json",
    }).done((msg) => {
      var s2data_apn = Array();

      msg["Academic Program Names"].forEach((curval, index) => {
        s2data_apn.push({
          id: index,
          text: curval,
        });
      });

      updateSelectData("#apname", s2data_apn);
    });
  } else {
    updateSelectData("#apname", counsellingDataSelect2.s2data_apn);
  }
});
