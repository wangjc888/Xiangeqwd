// JavaScript Document
(function (doc, win) {
  var docEl = doc.documentElement,
	resizeEvt = 'orientationchange' in window ? 'orientationchange' : 'resize',
	recalc = function () {
	  var clientWidth = docEl.clientWidth;
	  if (!clientWidth) return;
	  docEl.style.fontSize = 100 * (clientWidth / 400) + 'px';
	};

  if (!doc.addEventListener) return;
  win.addEventListener(resizeEvt, recalc, false);
  recalc();
})(document, window);