'use strict';

(function () {
  var elChart = document.getElementById('chart');

  document.body.addEventListener('click', function (e) {
    if (e.target.nodeName === 'LI' && e.target.classList.contains('course')) {
      var elImg = document.createElement('IMG');
      elImg.src = e.target.dataset.chart;

      elChart.innerHTML = '';
      elChart.appendChild(elImg);
      window.scrollTo(0, 0);
    }
  });
})();
