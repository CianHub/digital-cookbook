    //Get number of each field
    var i = $('.instructionClass').length
    var x = $('.allergenClass').length
    var y = $('.ingredientClass').length

    //If there is more than the relevent variable in each field show delete button
    if (i > 1) {
        $("#ins-remove").css("display", "inline-block");
    }
    if (x > 0) {
        $("#allerg-remove").css("display", "inline-block");
    }
    if (y > 1) {
        $("#ing-remove").css("display", "inline-block");
    }

    function add_more_instructions() {
        //When the add button is pressed add a field
        i++;
        $(".instructions").append("<br><div  id='ins" + i + "' class='col-md-6 mb-3'><label>Step " + i + ":</label><input name= 'instruction2' type='text' class='form-control instructionClass' placeholder='Please Enter The Instructions One At A Time' </div>");

        if (i > 1) {
            $("#ins-remove").css("display", "inline-block");
        }
    }

    function remove_instructions() {
        //When the delete button is pressed remove a field
        $("#ins" + i).remove();
        i--;
        if (i < 2) {
            $("#ins-remove").css("display", "none");
        }
    }

    function add_more_allergens() {
        //When the add button is pressed add a field
        x++;
        $(".allergens").append("<br><div id ='allerg" + x + "' class='col-md-6 mb-3'><input name='allergen2' type='text' class='form-control' placeholder='Please Enter Any Allergens One At A Time' </div>");
        if (x > 1) {
            $("#allerg-remove").css("display", "inline-block");
        }
    }

    function remove_allergens() {
        //When the remove button is pressed remove a field
        $("#allerg" + x).remove();
        x--;
        if (x === 0) {
            $("#allerg-remove").css("display", "none");
        }
    }

    function add_more_ingredients() {
        //When the add button is pressed add a field
        y++;
        $(".ingredients").append("<br><div  class='col-md-6 mb-3' id='ing" + y + "'><input name='ingredients2' type='text' class='form-control' placeholder='Please Enter Any Ingredients One At A Time' </div>");
        if (y > 1) {
            $("#ing-remove").css("display", "inline-block");
        }
    }

    function remove_ingredients() {
        //When the delete button is pressed delete a field
        $("#ing" + y).remove();
        y--;
        if (y < 2) {
            $("#ing-remove").css("display", "none");
        }
    }
    