/* =========================================================
   Pets of Perfection | site behavior
   ========================================================= */
(function () {
  "use strict";
  var C = window.POP_CONFIG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* storage blocked */ } }
  };

  /* ---------- mobile nav ---------- */
  var toggle = $(".nav-toggle");
  var nav = $(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("open", !open);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("open");
        toggle.focus();
      }
    });
  }

  /* ---------- open / closed status ---------- */
  function nowInTz() {
    try {
      var parts = new Intl.DateTimeFormat("en-US", {
        timeZone: C.TIMEZONE || "America/New_York",
        weekday: "short", hour: "numeric", minute: "numeric", hour12: false
      }).formatToParts(new Date());
      var map = {};
      parts.forEach(function (p) { map[p.type] = p.value; });
      var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
      var h = parseInt(map.hour, 10) % 24;
      return { day: days[map.weekday], hour: h + parseInt(map.minute, 10) / 60 };
    } catch (e) {
      var d = new Date();
      return { day: d.getDay(), hour: d.getHours() + d.getMinutes() / 60 };
    }
  }
  function fmt(h) {
    var hr = Math.floor(h), min = Math.round((h - hr) * 60);
    var ampm = hr >= 12 ? "PM" : "AM";
    var h12 = hr % 12 === 0 ? 12 : hr % 12;
    return h12 + ":" + (min < 10 ? "0" : "") + min + " " + ampm;
  }
  var dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  function statusText() {
    var H = C.HOURS || {};
    var n = nowInTz();
    var today = H[n.day];
    if (today && n.hour >= today[0] && n.hour < today[1]) {
      return { open: true, text: "Open now · until " + fmt(today[1]) };
    }
    if (today && n.hour < today[0]) {
      return { open: false, text: "Opens today at " + fmt(today[0]) };
    }
    for (var i = 1; i <= 7; i++) {
      var d = (n.day + i) % 7;
      if (H[d]) {
        var label = i === 1 ? "tomorrow" : dayNames[d];
        return { open: false, text: "Closed · opens " + label + " at " + fmt(H[d][0]) };
      }
    }
    return { open: false, text: "Call for hours" };
  }
  $$("[data-open-status]").forEach(function (el) {
    var s = statusText();
    el.classList.toggle("is-open", s.open);
    var t = $(".status-text", el);
    if (t) t.textContent = s.text;
  });

  /* ---------- size picker + live prices ---------- */
  var sizeInputs = $$('input[name="dog-size"]');
  function applySize(size, animate) {
    $$("[data-prices]").forEach(function (el) {
      var val = el.getAttribute("data-" + size);
      if (!val) return;
      if (el.textContent !== "$" + val) {
        el.textContent = "$" + val;
        if (animate) {
          el.classList.remove("bump");
          void el.offsetWidth;
          el.classList.add("bump");
        }
      }
    });
    var label = $('label[for="size-' + size + '"] strong');
    $$("[data-size-label]").forEach(function (el) {
      el.textContent = label ? label.textContent.toLowerCase() + " pups" : "";
    });
  }
  if (sizeInputs.length) {
    var saved = store.get("pop-size");
    if (saved && $("#size-" + saved)) $("#size-" + saved).checked = true;
    var checked = sizeInputs.filter(function (i) { return i.checked; })[0] || sizeInputs[0];
    checked.checked = true;
    applySize(checked.value, false);
    sizeInputs.forEach(function (i) {
      i.addEventListener("change", function () {
        applySize(i.value, true);
        store.set("pop-size", i.value);
      });
    });
  }

  /* ---------- reveal on scroll ---------- */
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- before / after sliders ---------- */
  $$(".ba").forEach(function (ba) {
    var input = $("input[type=range]", ba);
    if (!input) return;
    var set = function () { ba.style.setProperty("--pos", input.value + "%"); };
    input.addEventListener("input", set);
    set();
  });

  /* ---------- gallery filter ---------- */
  var chips = $$(".chip[data-filter]");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.getAttribute("data-filter");
      chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
      var shown = 0;
      $$(".ba-card").forEach(function (card) {
        var match = f === "all" || card.getAttribute("data-cat").split(" ").indexOf(f) > -1;
        card.hidden = !match;
        if (match) shown++;
      });
      var live = $("#gallery-live");
      if (live) live.textContent = "Showing " + shown + (shown === 1 ? " groom" : " grooms");
    });
  });

  /* ---------- footer year ---------- */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- booking form ---------- */
  var form = $("#booking-form");
  if (!form) return;

  var params = new URLSearchParams(window.location.search);
  var petTypeInputs = $$('input[name="pet_type"]', form);
  var dogBlock = $("#dog-services");
  var catBlock = $("#cat-services");
  var sizeField = $("#field-size");

  function petType() {
    var c = petTypeInputs.filter(function (i) { return i.checked; })[0];
    return c ? c.value : "";
  }
  function syncPetType() {
    var t = petType();
    var isCat = t === "Cat";
    dogBlock.hidden = isCat;
    catBlock.hidden = !isCat;
    sizeField.hidden = isCat;
    $$("input", isCat ? dogBlock : catBlock).forEach(function (i) { i.checked = false; });
  }
  petTypeInputs.forEach(function (i) { i.addEventListener("change", function () { syncPetType(); clearErr("pet_type"); }); });

  // Prefill from ?service=
  var pre = params.get("service");
  if (pre) {
    var box = form.querySelector('input[name="services"][value="' + CSS.escape(pre) + '"]');
    if (box) {
      var cat = box.closest("#cat-services");
      var typeInput = form.querySelector('input[name="pet_type"][value="' + (cat ? "Cat" : "Dog") + '"]');
      if (typeInput) { typeInput.checked = true; syncPetType(); }
      box.checked = true;
    }
  } else {
    syncPetType();
  }

  // Date input: tomorrow onward
  var dateInput = $("#date", form);
  function isoDate(d) {
    var m = d.getMonth() + 1, day = d.getDate();
    return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + (day < 10 ? "0" : "") + day;
  }
  var tomorrow = new Date(); tomorrow.setDate(tomorrow.getDate() + 1);
  if (dateInput) dateInput.min = isoDate(tomorrow);

  function showErr(name, msg) {
    var box = $('[data-error-for="' + name + '"]', form);
    var fieldEls = $$('[name="' + name + '"]', form);
    if (box) { box.querySelector("span").textContent = msg; box.classList.add("show"); }
    fieldEls.forEach(function (el) {
      if (el.type === "checkbox" || el.type === "radio") {
        var grid = el.closest(".pick-grid");
        if (grid) grid.classList.add("invalid");
        if (el.type === "checkbox" && !grid) el.setAttribute("aria-invalid", "true");
      } else {
        el.setAttribute("aria-invalid", "true");
      }
    });
  }
  function clearErr(name) {
    var box = $('[data-error-for="' + name + '"]', form);
    if (box) box.classList.remove("show");
    $$('[name="' + name + '"]', form).forEach(function (el) {
      el.removeAttribute("aria-invalid");
      var grid = el.closest(".pick-grid");
      if (grid) grid.classList.remove("invalid");
    });
  }
  $$("input, select, textarea", form).forEach(function (el) {
    var ev = (el.type === "checkbox" || el.type === "radio" || el.tagName === "SELECT") ? "change" : "input";
    el.addEventListener(ev, function () { clearErr(el.name); });
  });

  function validate() {
    var errors = [];
    var v = function (n) { var el = form.elements[n]; return el ? String(el.value || "").trim() : ""; };

    if (!v("owner_name")) errors.push(["owner_name", "Who should we ask for? Add your name."]);
    var digits = v("phone").replace(/\D/g, "");
    if (digits.length === 11 && digits.charAt(0) === "1") digits = digits.slice(1);
    if (!digits) errors.push(["phone", "We need a number to text your confirmation to."]);
    else if (digits.length !== 10) errors.push(["phone", "That number looks short. Use 10 digits, like 561-555-0123."]);
    var email = v("email");
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) errors.push(["email", "That email doesn't look quite right."]);
    if (!v("pet_name")) errors.push(["pet_name", "We'd love to know the star's name."]);
    var t = petType();
    if (!t) errors.push(["pet_type", "Dog or cat? Pick one."]);
    if (t === "Dog" && !v("size")) errors.push(["size", "Pick a size so we can block enough time."]);
    var picked = $$('input[name="services"]:checked', form).length;
    if (!picked) errors.push(["services", "Pick at least one service."]);
    var date = v("date");
    if (!date) {
      errors.push(["date", "Pick a day that works for you."]);
    } else {
      var p = date.split("-");
      var d = new Date(+p[0], +p[1] - 1, +p[2]);
      var startOfTomorrow = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate());
      var bookable = C.BOOKABLE_DAYS || [2, 3, 4, 5, 6];
      if (d < startOfTomorrow) errors.push(["date", "Pick a day from tomorrow on."]);
      else if (bookable.indexOf(d.getDay()) === -1) errors.push(["date", "We're closed Sundays and Mondays. Try Tuesday to Saturday."]);
    }
    if (!form.elements.vaccines.checked) errors.push(["vaccines", "Please confirm vaccinations are current."]);
    return errors;
  }

  var alertBox = $(".form-alert", form);
  var submitBtn = $('button[type="submit"]', form);
  var success = $("#booking-success");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    $$(".error-msg.show", form).forEach(function (b) { clearErr(b.getAttribute("data-error-for")); });
    var errors = validate();
    if (errors.length) {
      errors.forEach(function (er) { showErr(er[0], er[1]); });
      alertBox.textContent = errors.length === 1
        ? "One thing to fix before we can fetch your appointment."
        : errors.length + " things to fix before we can fetch your appointment.";
      alertBox.classList.add("show");
      var first = form.querySelector('[name="' + errors[0][0] + '"]');
      if (first) {
        first.focus({ preventScroll: true });
        first.scrollIntoView({ behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "center" });
      }
      return;
    }
    alertBox.classList.remove("show");
    submitBtn.disabled = true;
    submitBtn.classList.add("is-loading");
    $(".btn-label", submitBtn).textContent = "Fetching...";

    var done = function () {
      var name = form.elements.pet_name.value.trim();
      var date = form.elements.date.value;
      var p = date.split("-");
      var nice = new Date(+p[0], +p[1] - 1, +p[2]).toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
      var services = $$('input[name="services"]:checked', form).map(function (i) { return i.getAttribute("data-label"); });
      $("[data-s-pet]", success).textContent = name;
      $("[data-s-date]", success).textContent = nice + " · " + form.elements.time.value;
      $("[data-s-services]", success).textContent = services.join(", ");
      form.hidden = true;
      success.classList.add("show");
      success.setAttribute("tabindex", "-1");
      success.focus();
      success.scrollIntoView({ block: "start" });
    };
    var fail = function () {
      submitBtn.disabled = false;
      submitBtn.classList.remove("is-loading");
      $(".btn-label", submitBtn).textContent = "Fetch my appointment";
      alertBox.innerHTML = "Ruh-roh, that didn't go through. Try again, or call us at <a href=\"tel:" + C.PHONE_TEL + "\">" + C.PHONE_DISPLAY + "</a>.";
      alertBox.classList.add("show");
    };

    if (C.FORM_ENDPOINT) {
      fetch(C.FORM_ENDPOINT, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (r) { if (r.ok) done(); else fail(); })
        .catch(fail);
    } else {
      window.setTimeout(done, 700); // demo mode
    }
  });

  var again = $("#book-another");
  if (again) {
    again.addEventListener("click", function () {
      form.reset();
      syncPetType();
      submitBtn.disabled = false;
      submitBtn.classList.remove("is-loading");
      $(".btn-label", submitBtn).textContent = "Fetch my appointment";
      success.classList.remove("show");
      form.hidden = false;
      form.elements.owner_name.focus();
    });
  }
})();
