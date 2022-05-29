function dodajKordynaty() {
    var x = document.getElementById("formularzTworzeniaMisji");
    // create an input field to insert
    var new_field = document.createElement("input");
    // set input field data type to text
    new_field.setAttribute("type", "text");
    // set input field name
    new_field.setAttribute("name", "text_field[]");
    // select last position to insert element before it
    var pos = x.childElementCount;

    // insert element
    x.insertBefore(new_field, x.childNodes[pos]);
}