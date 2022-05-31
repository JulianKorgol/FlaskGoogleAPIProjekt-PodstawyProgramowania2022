let x = 2
$('#addCoordinates').click(function() {
    $('.Coordinates').append('<tr id="element' + x + '"><div id="CoordinatesInputs"><td><input type="text" class="form-control" name="kordynaty' + x + '" id="kordynaty' + x + '" required/></td></div></tr>');

    $("#allOfTheCoordinates").html('<input type="hidden" value="' + x + '" id= "allOfTheCoordinates" name="allOfTheCoordinates" />');
    x += 1
});