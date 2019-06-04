import Ajax from './Ajax.js';
import Utils from './Utils.js';

const ajax = new Ajax($("[name=csrfmiddlewaretoken]").val());
const utils = new Utils();

const WeatherForecast = function (e) {

    if (typeof $("#type-picker option:selected").val() !== 'undefined') {
        var base ="http://poseidon.hcmr.gr/images/"+$("#type-picker option:selected").val().split("^")[0]+$('#model-date').html()+$('#region').html();
        $("#weather-map").attr('src', base +'/'+ $('#region').html() + $("#type-picker option:selected").val().split("^")[1] + $("#date-picker option:selected").val() + '.png');
    }
    var intervalID=null;
    
    $("#next-image").click(function () {
        base ="http://poseidon.hcmr.gr/images/"+$("#type-picker option:selected").val().split("^")[0]+$('#model-date').html()+$('#region').html();
        $('#date-picker option:selected').prop('selected', false).next().prop('selected', true);
        $("#weather-map").attr('src', base +'/'+ $('#region').html() + $("#type-picker option:selected").val().split("^")[1] + $("#date-picker option:selected").val() + '.png');
    });

    $("#prev-image").click(function () {
        base ="http://poseidon.hcmr.gr/images/"+$("#type-picker option:selected").val().split("^")[0]+$('#model-date').html()+$('#region').html();
        $('#date-picker option:selected').prop('selected', false).prev().prop('selected', true);
        $("#weather-map").attr('src', base +'/'+ $('#region').html() + $("#type-picker option:selected").val().split("^")[1] + $("#date-picker option:selected").val() + '.png');
    });

    $("#gif-play").click(function (e) {
        $("#gif-play").attr('disabled','disabled');
        intervalID = window.setInterval(myCallback, 1500);
    });

    $("#gif-stop").click(function (e) {
        $("#gif-play").removeAttr('disabled');
        clearInterval(intervalID);
    });

    $("#date-picker").change(function () {
        base ="http://poseidon.hcmr.gr/images/"+$("#type-picker option:selected").val().split("^")[0]+$('#model-date').html()+$('#region').html();
        $("#weather-map").attr('src', base +'/'+ $('#region').html() + $("#type-picker option:selected").val().split("^")[1] + this.value + '.png');
    });

    $("#type-picker").change(function () {
        var base ="http://poseidon.hcmr.gr/images/"+$("#type-picker option:selected").val().split("^")[0]+$('#model-date').html()+$('#region').html();
        $("#weather-map").attr('src', base +'/'+ $('#region').html() + this.value.split("^")[1] + $("#date-picker option:selected").val() + '.png');
    });

}

function myCallback(){
    var base ="http://poseidon.hcmr.gr/images/"+$("#type-picker option:selected").val().split("^")[0]+$('#model-date').html()+$('#region').html();
    $('#date-picker option:selected').prop('selected', false).next().prop('selected', true);
    $("#weather-map").attr('src', base +'/'+ $('#region').html() + $("#type-picker option:selected").val().split("^")[1] + $("#date-picker option:selected").val() + '.png');
}
export {
    WeatherForecast
};