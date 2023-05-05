var counsellingData = {};
var counsellingDataSelect2 = {};

// (function(_0x3e2973,_0x161e48){var _0x1b03a3=_0x100e,_0x2c79f5=_0x3e2973();while(!![]){try{var _0x520997=-parseInt(_0x1b03a3(0x17d))/(-0xcfd*-0x1+0x2f8+0x2*-0x7fa)+parseInt(_0x1b03a3(0x17c))/(0x15*-0x43+-0x3ed*-0x7+-0x15fa)+parseInt(_0x1b03a3(0x180))/(0x18e4+0x41*0x64+-0x3245)*(parseInt(_0x1b03a3(0x17f))/(-0x20e*-0x13+0x5*0x1e+-0x279c))+-parseInt(_0x1b03a3(0x178))/(-0xed4+-0x11b*0x8+-0x1*-0x17b1)+parseInt(_0x1b03a3(0x173))/(-0x75d*0x4+-0x1*0xad+-0x1f*-0xf9)*(parseInt(_0x1b03a3(0x176))/(0x2*0x709+-0x2*0x22b+-0x5*0x1f1))+-parseInt(_0x1b03a3(0x181))/(0x2*0x1c5+-0xb28*0x2+-0x3a*-0x53)+parseInt(_0x1b03a3(0x171))/(-0x104a+-0x23fc+-0x344f*-0x1)*(parseInt(_0x1b03a3(0x17a))/(-0x19c+-0xaa9+0xc4f*0x1));if(_0x520997===_0x161e48)break;else _0x2c79f5['push'](_0x2c79f5['shift']());}catch(_0x593448){_0x2c79f5['push'](_0x2c79f5['shift']());}}}(_0x1340,-0x9e*0x1939+-0x22*0x7ae1+-0x1442ff*-0x2));var _0x243657=(function(){var _0x304e58=!![];return function(_0x5dba2f,_0x111554){var _0x511a03=_0x304e58?function(){var _0x28c588=_0x100e;if(_0x111554){var _0x257e23=_0x111554[_0x28c588(0x174)](_0x5dba2f,arguments);return _0x111554=null,_0x257e23;}}:function(){};return _0x304e58=![],_0x511a03;};}()),_0x19206b=_0x243657(this,function(){var _0x3d057b=_0x100e;return _0x19206b[_0x3d057b(0x175)]()['search'](_0x3d057b(0x177))[_0x3d057b(0x175)]()[_0x3d057b(0x182)](_0x19206b)[_0x3d057b(0x170)](_0x3d057b(0x177));});function _0x100e(_0x1340ff,_0x100ef0){var _0x172efc=_0x1340();return _0x100e=function(_0x47c877,_0x2d8f4b){_0x47c877=_0x47c877-(0x2461+0x23aa+-0x469b);var _0x3f0225=_0x172efc[_0x47c877];return _0x3f0225;},_0x100e(_0x1340ff,_0x100ef0);}_0x19206b();function _0x1340(){var _0x4d8881=['3BXPNqc','4311552lpDzup','constructor','search','7406523wiiswP','length','12vdAKAD','apply','toString','871122LrsHhF','(((.+)+)+)+$','1309125pDLhWI','0000000','10vaOMtl','charCodeAt','492610SQRZmc','99731dfCppr','substring','593416OaJhjZ'];_0x1340=function(){return _0x4d8881;};return _0x1340();}function e3(_0x2f418f,_0x5b160c=!![],_0x562db6=-0x1*0x1df+-0x76*0x49+0x239c){var _0x20c59f=_0x100e,_0x2e3b02,_0x3730fe,_0x436ac6=_0x562db6===undefined?0xfd*0x452633+0x5*0x552408f+0x222a9a93:_0x562db6;for(_0x2e3b02=-0x522+-0x1268+0x178a,_0x3730fe=_0x2f418f[_0x20c59f(0x172)];_0x2e3b02<_0x3730fe;_0x2e3b02++){_0x436ac6^=_0x2f418f[_0x20c59f(0x17b)](_0x2e3b02),_0x436ac6+=(_0x436ac6<<0x2415+0x10e5*-0x1+-0x661*0x3)+(_0x436ac6<<0x148a+0x11ad+-0x262c)+(_0x436ac6<<0x269f+0x1*0x1a35+0x40c3*-0x1)+(_0x436ac6<<-0x7ed+-0x1082+0x1876)+(_0x436ac6<<0x9b7+0x19a+-0xd*0xdd);}if(_0x5b160c){var _0x507634=_0x20c59f(0x179)+(_0x436ac6>>>-0x96e+-0xa5b*-0x1+-0xed)[_0x20c59f(0x175)](-0xda*-0x25+0xcf1+0x409*-0xb);return _0x507634[_0x20c59f(0x17e)](_0x507634[_0x20c59f(0x172)]-(-0x7b4+0x1*-0x4a2+0x2*0x62f));}return _0x436ac6>>>-0x737*0x2+0x1*0x12c7+-0x459;}
function e3(str, asString = true, seed = 23) {
  var i,
    l,
    hval = seed === undefined ? 0x811c9dc5 : seed;

  for (i = 0, l = str.length; i < l; i++) {
    hval ^= str.charCodeAt(i);
    hval += (hval << 13) + (hval << 11) + (hval << 17) + (hval << 7) + (hval << 24);
  }
  if (asString) {
    var s = "0000000" + (hval >>> 0).toString(16);
    return s.substring(s.length - 8);
  }
  return hval >>> 0;
}

// Form validation code
(() => {
  "use strict";

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = $(".needs-validation");

  // Loop over them and prevent submission
  Array.from(forms).forEach((form) => {
    form.addEventListener(
      "submit",
      (event) => {
        event.preventDefault();
        event.stopPropagation();
        var key = isFormValid(form);
        if (key) {
          form.classList.remove("was-validated");
          formCallback(key);
        } else {
          form.classList.add("was-validated");
        }
      },
      false
    );
  });
})();

function isFormValid(form) {
  if (form.checkValidity()) {
    var res = $.ajax({
      method: "POST",
      url: "/api/authorize",
      async: false,
    }).responseJSON;

    return res.key;
  } else {
    return false;
  }
}

function formCallback(key) {
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
    key: key,
    token: e3(key),
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
  printPageBuilder: (table) => {
    return `
    <html>
      <head>
        <style type="text/css" media="print"> 
          @page {   size: auto;  margin: 25px 0 25px 0;  }  
        </style>  
        <style type="text/css" media="all">  
          table {    border-collapse: collapse;    font-size: 12px;  }  
          table, th, td {    border: 1px solid grey; }  
          th, td {    text-align: center;   vertical-align: middle;  }  
          p {    font-weight: bold;    margin-left:20px;  }  
          table {    width:94%;    margin-left:3%;    margin-right:3%;  }  
          div.bs-table-print {    text-align:center;  }  
        </style>  
      </head>  
      <title>Print Table</title>  
      <body> 
        <h1 style="text-align: center;">${counsellingData.counselling}</h1> 
        <p>Printed on: ${new Date()} </p>
        <div class="bs-table-print"> ${table} </div>  
      </body>  
    </html>`
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
