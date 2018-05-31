    //Display selected table hide others
    
    function sort_by_author() {
        $("#sortAuthor").css("display", "inline-block");
        $("#sortDefault").css("display", "none");
        $("#sortName").css("display", "none");
        $("#sortUpvotes").css("display", "none");
        $("#sortDownvotes").css("display", "none");
        $("#sortCountry").css("display", "none");
    }

    function sort_by_name() {
        $("#sortName").css("display", "inline-block");
        $("#sortDefault").css("display", "none");
        $("#sortAuthor").css("display", "none");
        $("#sortUpvotes").css("display", "none");
        $("#sortDownvotes").css("display", "none");
        $("#sortCountry").css("display", "none");
    }

    function sort_by_country() {
        $("#sortCountry").css("display", "inline-block");
        $("#sortDefault").css("display", "none");
        $("#sortAuthor").css("display", "none");
        $("#sortUpvotes").css("display", "none");
        $("#sortDownvotes").css("display", "none");
        $("#sortName").css("display", "none");
    }

    function sort_by_upvotes() {
        $("#sortUpvotes").css("display", "inline-block");
        $("#sortDefault").css("display", "none");
        $("#sortAuthor").css("display", "none");
        $("#sortCountry").css("display", "none");
        $("#sortDownvotes").css("display", "none");
        $("#sortName").css("display", "none");
    }

    function sort_by_downvotes() {
        $("#sortDownvotes").css("display", "inline-block");
        $("#sortDefault").css("display", "none");
        $("#sortAuthor").css("display", "none");
        $("#sortCountry").css("display", "none");
        $("#sortUpvotes").css("display", "none");
        $("#sortName").css("display", "none");
    }
    