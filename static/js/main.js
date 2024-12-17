'use strict';

function addMultipleListeners(el, types, listener, options, useCapture) {
	types.forEach(type => el.addEventListener(type, listener, options, useCapture));
}

document.addEventListener("DOMContentLoaded", (e) => {
	document.body.addEventListener("showMessage", e => window.alert(e.detail.value));
	document.body.addEventListener("htmx:beforeSend", e => document.body.style.cursor = "wait");
	addMultipleListeners(document, ["htmx:afterSwap", "htmx:responseError", "htmx:abort", "htmx:timeout"], e => document.body.style.cursor = "auto");
});
