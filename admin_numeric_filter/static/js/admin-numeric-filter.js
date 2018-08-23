var sliders = document.getElementsByClassName('admin-numeric-filter-slider');

for (var i = 0; i < sliders.length; i++) {
    var slider = sliders[i];

    if (slider.classList.contains('noUi-target')) {
        continue;
    }

    if (slider) {
        var from = parseInt(slider.closest('.admin-numeric-filter-wrapper').querySelectorAll('.admin-numeric-filter-wrapper-group input')[0].value);
        var to = parseInt(slider.closest('.admin-numeric-filter-wrapper').querySelectorAll('.admin-numeric-filter-wrapper-group input')[1].value);

        var min = parseInt(slider.getAttribute('data-min'));
        var max = parseInt(slider.getAttribute('data-max'));

        noUiSlider.create(slider, {
            start: [from, to],
            step: 1,
            connect: true,
            format: wNumb({
                decimals: 0
            }),
            range: {
                'min': min,
                'max': max
            }
        });

        slider.noUiSlider.on('update', function(values, handle) {                        
            var parent = this.target.closest('.admin-numeric-filter-wrapper');
            var from = parent.querySelectorAll('.admin-numeric-filter-wrapper-group input')[0];
            var to = parent.querySelectorAll('.admin-numeric-filter-wrapper-group input')[1];
            
            parent.querySelectorAll('.admin-numeric-filter-slider-tooltip-from')[0].innerHTML = values[0];
            parent.querySelectorAll('.admin-numeric-filter-slider-tooltip-to')[0].innerHTML = values[1];

            from.value = values[0];
            to.value = values[1];
        });
    }
}