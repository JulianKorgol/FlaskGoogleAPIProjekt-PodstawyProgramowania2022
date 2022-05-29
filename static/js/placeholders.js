let x = 3
let y = 4
let z = 1
$('#addCoordinates').click(function() {
    $('.Coordinates').append('<tr id="element' + z + '"><div id="CoordinatesInputs"><td><input type="text" class="form-control" name="kordynaty' + x + '" id="kordynaty' + x + '" required/></td><td><input type="text" class="form-control" name="kordynaty' + y + '" id="kordynaty' + y + '" required/></td></div></tr>');

    $("#allOfTheCoordinates").html('<input type="hidden" value="' + y + '" id= "allOfTheCoordinates" name="allOfTheCoordinates" />');
    x += 2
    y += 2
    z += 1
});