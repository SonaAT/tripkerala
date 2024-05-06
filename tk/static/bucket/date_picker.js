// static/js/date_picker.js

document.addEventListener('DOMContentLoaded', function() {
    var today = new Date().toISOString().split('T')[0];
    document.getElementsByName("start_date")[0].setAttribute('min', today);
    document.getElementsByName("end_date")[0].setAttribute('min', today);
});
