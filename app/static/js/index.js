function search() {
    $(".add-form").remove();
    const word_query = $("input#word").val();
    const deck_name = $("input#decks").val();
    $(".search-spinner").removeClass("d-none");
    $.get("/search",
        {
            word_query: word_query,
            deck_name: deck_name
        },
        function (data) {
            $(".container").append(data);
            $(".search-spinner").addClass("d-none");
        }
    );
    searchImages(word_query);
}

function searchImages(query) {
    if (!query) {
        $(".image-search-spinner").removeClass("d-none");
        query = $("input#image_query").val();
    }
    $.get("/search-images",
        {word_query: query},
        function(data) {
            $(".image-search-spinner").addClass("d-none");
            $(".gallery").html("");
            data.forEach(function (link) {
               $("<img/>").attr("src", link).addClass("img-thumbnail").appendTo(".gallery");
            });
        }
    );
}

function playSound(el) {
    const filename = $(el).data("audio");
    const audio = new Audio(filename);
    audio.play();
}

function add() {
    $(".add-spinner").removeClass("d-none");
    var searchFormData = $(".search-form").serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    var addFormData = $(".add-form").serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    const formData = $.extend(searchFormData, addFormData);
    formData["image_paths"] = JSON.stringify(selectedImages);
    formData["audio_filename"] = $(".btn-audio").data("audio");
    delete formData["image_query"];

    $.post("/add", formData, function(data) {
        $(".add-spinner").addClass("d-none");
        $(".add-form").remove();
        $("input#word").val("");
        $(".alert-success").removeClass("d-none");
        setTimeout(function() {
            $(".alert-success").addClass("d-none");
        }, 1000);
    });
}

var selectedImages = [];

function imgWatch() {
    $("body").on("click", ".gallery img", function() {
        const isSelected = $(this).hasClass("img-selected");
        isSelected ? selectedImages.pop(this.src) : selectedImages.push(this.src);
        $(this).toggleClass("img-selected");
        console.log(selectedImages);
    });
}

$(document).ready(function() {
   imgWatch();
});