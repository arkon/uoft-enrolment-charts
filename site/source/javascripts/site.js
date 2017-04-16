'use strict';

(function () {
  var elChart = document.getElementById('chart');

  document.body.addEventListener('click', function (e) {
    if (e.target.nodeName === 'A' && e.target.classList.contains('courses__course')) {
      e.preventDefault();
      var elImg = document.createElement('IMG');
      elImg.src = e.target.href;

      elChart.innerHTML = '';
      elChart.appendChild(elImg);
      window.scrollTo(0, 0);
    }
  });
})();
